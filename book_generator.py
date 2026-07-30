"""
book_generator.py — compile a book's Markdown source into a static reader page
(BCS v1.1 §A.5/§A.6/§C.2). Repo-relative paths; no hardcoded Windows dir.

Pipeline per book:
    source units (Markdown)
      -> render_book_md            (models.py — frozen extension set)
      -> wrap_code_blocks          (set data-lang on .book-code, selectolax)
      -> katex_prerender.render    (bake math to KaTeX, single Node process)
      -> validate_anchors          (fail build on numbering/anchor errors)
      -> assemble reader shell     (TOC + book-bar + opener/unit sections)
      -> write templates/books/<slug>.html   (extends base.html)

Content lives under the "Python Book/" and "Linear Algebra/" folders as Python
modules exposing a BOOK dict (see book_content.py). This module only compiles.
"""
import os
import re

from selectolax.parser import HTMLParser

from models import render_book_md
import katex_prerender

HERE = os.path.dirname(os.path.abspath(__file__))
BOOKS_DIR = os.path.join(HERE, "templates", "books")

# Fixed anchor sets (BCS v1.0 numbering)
_LA_MODULES = ["0"] + list("ABCDEFGHIJKLMNO")   # 16 openers
_PY_CHAPTERS = [str(n) for n in range(9)]        # ch 0-8
_AWS_CHAPTERS = [str(n) for n in range(8)]       # aws-ml ch 0-7 (MLA-C01 roadmap)

# slug -> fixed module/chapter id set the anchor validator accepts.
_CHAPTER_SETS = {
    "linear-algebra": set(_LA_MODULES),
    "python": set(_PY_CHAPTERS),
    "aws-ml": set(_AWS_CHAPTERS),
}


# ---------------------------------------------------------------------------
# Stage: code-block language tab
# ---------------------------------------------------------------------------
def wrap_code_blocks(html):
    """Set data-lang on every .book-code div so the CSS ::before language tab
    shows the language. Direct attribute set — robust across selectolax
    versions (raw-string insert_before HTML-escapes in some builds)."""
    if "book-code" not in html:
        return html
    tree = HTMLParser(html)
    for div in tree.css("div.book-code"):
        lang = "CODE"
        # pygments_lang_class puts "language-<lang>" on the wrapper div; fall back
        # to a language-* class on the inner <code> for robustness.
        classes = (div.attributes.get("class") or "").split()
        code = div.css_first("code")
        if code:
            classes += (code.attributes.get("class") or "").split()
        for c in classes:
            if c.startswith("language-"):
                lang = c[len("language-"):].upper()
                break
        div.attrs["data-lang"] = lang
    body = tree.css_first("body")
    if body is None:
        return html
    out = body.html
    return out[len("<body>"):-len("</body>")] if out.startswith("<body>") else out


# ---------------------------------------------------------------------------
# Stage: anchor / numbering validator (fail build on any error)
# ---------------------------------------------------------------------------
def validate_anchors(html, book):
    errs = []
    qs = sorted(int(m) for m in re.findall(r'id="q-(\d+)"', html))
    if qs and qs != list(range(1, qs[-1] + 1)):
        missing = sorted(set(range(1, qs[-1] + 1)) - set(qs))
        errs.append(f"question numbers not contiguous 1..{qs[-1]}; missing: {missing}")
    if len(qs) != len(set(qs)):
        errs.append("duplicate question ids")
    sols = set(re.findall(r'id="q-(\d+)-solution"', html))
    for s in sols:
        if f'id="q-{s}"' not in html:
            errs.append(f"orphan #q-{s}-solution with no #q-{s}")
    allowed = _CHAPTER_SETS.get(book, set(_PY_CHAPTERS))
    mods = re.findall(r'id="(?:mod|ch)-([0-9A-O]+)"', html)
    for mid in mods:
        if mid not in allowed:
            errs.append(f"module/chapter id '{mid}' not in fixed set for {book}")
    if len(mods) != len(set(mods)):
        errs.append("duplicate module/chapter ids")
    return errs


# ---------------------------------------------------------------------------
# Stage: flag wide display equations for print
# ---------------------------------------------------------------------------
_TEXTBLOCK_PX = 157.6 / 25.4 * 96.0   # 157.6mm text block -> CSS px (~595.6)


def mark_wide_equations(html):
    """Flag .katex-display blocks wider than the print text block as .is-wide
    (print CSS then applies transform:scale(0.618)). A reliable per-block pixel
    width from WeasyPrint's box tree is version-sensitive, so by default we do
    NOT fabricate a measurement: screen overflow-x remains the deterministic
    fallback and the ship gate + visual proof cover the rare wide case. Kept as
    a single hook so a future exact measurer drops in here."""
    return html, []


# ---------------------------------------------------------------------------
# Assembly
# ---------------------------------------------------------------------------
def _prefix_for(section):
    """Per-section id namespace for auto-generated heading ids (from the source
    filename, e.g. 'ch-1.md' -> 'ch-1', 'mod-A.md' -> 'mod-A')."""
    fname = section.get("file", "")
    return os.path.splitext(fname)[0] if fname else ""


def compile_unit_html(md_text, id_prefix=""):
    html = render_book_md(md_text, id_prefix=id_prefix)
    html = wrap_code_blocks(html)
    html = katex_prerender.render(html)
    return html


def _toc_html(book):
    groups = []
    for g in book["toc"]:
        links = "\n".join(
            f'      <a href="#{a["id"]}" data-crumbs="{a.get("crumb", a["label"])}">{a["label"]}</a>'
            for a in g["items"]
        )
        groups.append(
            f'    <div class="book-toc__group">\n'
            f'      <p class="book-toc__group-title">{g["title"]}</p>\n{links}\n    </div>'
        )
    return "\n".join(groups)


_PAGE_TEMPLATE = """{{% extends "base.html" %}}
{{% block title %}}{title}{{% endblock %}}
{{% block extra_css %}}
  <link rel="stylesheet" href="{{{{ url_for('static', filename='vendor/katex/katex.min.css') }}}}">
  <link rel="stylesheet" href="{{{{ url_for('static', filename='css/book_math.css') }}}}">
{{% endblock %}}
{{% block content %}}
<div class="book-bar">
  <nav class="book-bar__crumbs" aria-label="Breadcrumb">
    <span>BOOKS</span><span class="sep">/</span><span class="current">{title}</span>
  </nav>
  <button class="book-toc-toggle" aria-controls="book-toc" aria-expanded="false">Contents</button>
  <div class="book-bar__nav">
    <a class="book-prev" href="#" aria-disabled="true">&lsaquo; Prev</a>
    <a class="book-next" href="#">Next &rsaquo;</a>
  </div>
  <div class="book-progress" aria-hidden="true"></div>
</div>
<div class="book-shell">
  <aside class="book-toc" id="book-toc" aria-label="Table of contents">
{toc}
  </aside>
  <article class="reader book-content markdown-content">
    <span class="book-title-src" hidden>{title}</span>
{body}
  </article>
</div>
{{% endblock %}}
{{% block reader_js %}}
  <script defer src="{{{{ url_for('static', filename='js/book.js') }}}}"></script>
{{% endblock %}}
"""


def _assemble_body(book):
    parts = [compile_unit_html(sec["md"], id_prefix=_prefix_for(sec)) for sec in book["sections"]]
    body = "\n".join(parts)
    errs = validate_anchors(body, book["slug"])
    if errs:
        raise SystemExit(
            "ANCHOR VALIDATION FAILED for %s:\n  - %s" % (book["slug"], "\n  - ".join(errs))
        )
    body, _wide = mark_wide_equations(body)
    return body


def compile_book(book):
    """Compile a BOOK dict to templates/books/<slug>.html. Returns (path, body)."""
    body = _assemble_body(book)
    os.makedirs(BOOKS_DIR, exist_ok=True)
    page = _PAGE_TEMPLATE.format(title=book["title"], toc=_toc_html(book), body=body)
    out_path = os.path.join(BOOKS_DIR, book["slug"] + ".html")
    tmp = out_path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(page)
    os.replace(tmp, out_path)
    return out_path, body


def render_book_body_for_pdf(book):
    """Return standalone reader HTML (no Jinja) for WeasyPrint."""
    return _assemble_body(book)


if __name__ == "__main__":
    import sys

    sys.path.insert(0, HERE)
    from book_content import load_book, ALL_SLUGS

    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    slugs = ALL_SLUGS if which == "all" else [which]
    for slug in slugs:
        path, _ = compile_book(load_book(slug))
        print(f"compiled {slug} -> {path}")
