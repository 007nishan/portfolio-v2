"""
make_book_pdf.py — build a book's print PDF with WeasyPrint (BCS v1.1 §8/§B).

Consumes the SAME server-side-rendered HTML as the screen page (math already
baked to KaTeX, code highlighted) so screen == PDF, with zero JS at render time.
Applies style.css + book_math.css + print.css. Embeds fonts. Runs a no-JS grep
gate and the readability lint gate before writing the PDF.

Usage:
    python make_book_pdf.py --book linear-algebra [--out static/books/linear-algebra.pdf]
    python make_book_pdf.py --book python
"""
import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import _weasy_env  # noqa: wire GTK/Pango on Windows (no-op on Linux)
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

from book_generator import render_book_body_for_pdf
from book_content import load_book

STATIC = os.path.join(HERE, "static")
_JS_LEAK = re.compile(r"katex\.js|auto-render|MathJax|arithmatex")


def _static_url_fetcher(url):
    """Resolve root-relative /static/... URLs (as written by the figure fence and
    templates) to the repo's static dir, so WeasyPrint finds images/fonts in the
    PDF. Everything else falls through to WeasyPrint's default fetcher."""
    from weasyprint.urls import default_url_fetcher

    marker = "/static/"
    if marker in url and not url.startswith("http"):
        # strip any file:/// prefix WeasyPrint may have prepended
        idx = url.find(marker)
        rel = url[idx + len(marker):]
        local = os.path.join(STATIC, rel.replace("/", os.sep))
        if os.path.isfile(local):
            return default_url_fetcher("file:///" + local.replace(os.sep, "/"))
    return default_url_fetcher(url)

# Cover HTML fragment: title/subtitle/institution on the cover page.
_COVER = """<section class="book-cover" style="height:100vh;display:flex;flex-direction:column;
  justify-content:center;padding:0 32.4mm 0 20mm;">
  <div style="font-family:'Libre Franklin',sans-serif;text-transform:uppercase;letter-spacing:.12em;
    font-weight:700;color:{lead};font-size:11pt;">{kicker}</div>
  <h1 style="font-family:'Crimson Text',Georgia,serif;font-weight:700;font-size:46pt;line-height:1.05;
    color:#000;margin:.4em 0 0;">{title}</h1>
  <div style="width:60.2mm;height:4px;background:#a70e13;margin:16pt 0;"></div>
  <p style="font-family:'Crimson Text',Georgia,serif;font-style:italic;font-size:15pt;color:#212529;margin:0;">{subtitle}</p>
  <p style="font-family:'Libre Franklin',sans-serif;font-size:10pt;color:#666;margin-top:auto;
    text-transform:uppercase;letter-spacing:.06em;">{institution}</p>
</section>"""


def build_html(book):
    body = render_book_body_for_pdf(book)
    if _JS_LEAK.search(body):
        raise SystemExit("NO-JS GATE FAILED: runtime math/JS reference left in %s HTML" % book["slug"])
    _LEADS = {"linear-algebra": "#005863", "aws-ml": "#d58000"}
    lead = _LEADS.get(book["slug"], "#00719a")
    cover = _COVER.format(
        kicker=book.get("kicker", "A Portfolio Book"),
        title=book["title"],
        subtitle=book.get("subtitle", ""),
        institution=book.get("institution", ""),
        lead=lead,
    )
    head = (
        '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
        '<title>{title}</title>'
        '<meta name="author" content="{author}">'
        '<meta name="description" content="{desc}">'
        '<meta name="generator" content="portfolio-v2 make_book_pdf">'
        '</head><body>'
        '<span class="book-title-src" hidden>{title}</span>'
    ).format(title=book["title"], author=book.get("institution", ""), desc=book.get("subtitle", ""))
    doc = (
        head
        + cover
        + '<article class="reader book-content markdown-content book-body">'
        + body
        + "</article></body></html>"
    )
    return doc


def _stamp_pdf_metadata(path, book):
    """Post-stamp PDF Info dict (version-independent of WeasyPrint metadata)."""
    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError:
        return
    reader = PdfReader(path)
    writer = PdfWriter()
    for pg in reader.pages:
        writer.add_page(pg)
    writer.add_metadata({
        "/Title": book["title"],
        "/Author": book.get("institution", ""),
        "/Subject": book.get("subtitle", ""),
        "/Creator": "portfolio-v2 make_book_pdf",
        "/Producer": "WeasyPrint + portfolio-v2",
    })
    tmp = path + ".meta.tmp"
    with open(tmp, "wb") as f:
        writer.write(f)
    os.replace(tmp, path)


def make_book_pdf(slug, out=None):
    book = load_book(slug)
    html = build_html(book)

    # Readability ship gate (imported lazily so PDF build fails if a book has errors).
    try:
        import book_lint

        rc = book_lint.check(slug, strict=True)
        if rc != 0:
            raise SystemExit("QA GATE FAILED for %s (rc=%d) — see static/books/qa/%s.qa.json" % (slug, rc, slug))
    except ImportError:
        print("[warn] book_lint not present; skipping QA gate (dev only)")

    out = out or os.path.join(STATIC, "books", slug + ".pdf")
    os.makedirs(os.path.dirname(out), exist_ok=True)

    fc = FontConfiguration()
    stylesheets = [
        CSS(os.path.join(STATIC, "css", "style.css"), font_config=fc),
        CSS(os.path.join(STATIC, "vendor", "katex", "katex.min.css"), font_config=fc),
        CSS(os.path.join(STATIC, "css", "book_math.css"), font_config=fc),
        CSS(os.path.join(STATIC, "css", "print.css"), font_config=fc),
    ]
    # base_url = dir containing static/; custom fetcher maps /static/... to disk.
    doc = HTML(string=html, base_url=HERE + os.sep, url_fetcher=_static_url_fetcher).render(
        stylesheets=stylesheets, font_config=fc)
    doc.metadata.title = book["title"]
    doc.metadata.authors = [book.get("institution", "")]
    doc.metadata.generator = "portfolio-v2 make_book_pdf"
    doc.metadata.description = book.get("subtitle", "")
    tmp = out + ".tmp"
    doc.write_pdf(tmp)
    os.replace(tmp, out)
    _stamp_pdf_metadata(out, book)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", required=True, help="slug: python | linear-algebra")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    path = make_book_pdf(args.book, args.out)
    print("wrote", path, "(%d bytes)" % os.path.getsize(path))
