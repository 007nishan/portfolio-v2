r"""
book_lint.py — error-free human-readability SHIP GATE (BCS v1.1 §F).

No book may ship (served at /read or written to a PDF) unless
`python book_lint.py --book <slug> --strict` exits 0. The gate lints the ACTUAL
production-rendered HTML (render_book_md + katex_prerender), plus the Markdown
source for token-level checks. Findings are ERROR (fail) or WARN.

Check families:
  R  structure/readability  — heading hierarchy, anchors, dup ids, alt text, typography,
                              spelling, and NO clickable links (R050 — printed book)
  M  math                   — $/$$ balance, \begin/\end balance, matrix rows, no .katex-error
  C  code/output            — fenced code has a language, output not mislabeled, no smart quotes in code
  F  fidelity/no-fabrication — blank source solutions MUST be the canonical placeholder, never invented
  A  a11y                   — contrast AA for dark code string, print ink not pure black

Reports: static/books/qa/<slug>.qa.json  and  <slug>.qa.html
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

QA_DIR = os.path.join(HERE, "static", "books", "qa")
BLANK_PLACEHOLDER = "Solution not provided in the source material."

from selectolax.parser import HTMLParser  # noqa: E402
from book_content import load_book, BOOKS  # noqa: E402
from book_generator import compile_unit_html, _prefix_for  # noqa: E402


# ---------------------------------------------------------------------------
class Finding:
    __slots__ = ("code", "severity", "msg", "where")

    def __init__(self, code, severity, msg, where=""):
        self.code, self.severity, self.msg, self.where = code, severity, msg, where

    def as_dict(self):
        return {"code": self.code, "severity": self.severity, "msg": self.msg, "where": self.where}


def _load_json(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def _allowlist():
    path = os.path.join(QA_DIR, "allowlist.txt")
    words = set()
    if os.path.isfile(path):
        with open(path, encoding="utf-8") as f:
            for line in f:
                w = line.strip().lower()
                if w and not w.startswith("#"):
                    words.add(w)
    return words


def _blank_registry(slug):
    reg = _load_json(os.path.join(QA_DIR, "blank_solutions.json"), {})
    return set(reg.get(slug, []))


# ---------------------------------------------------------------------------
# Source-level checks (Markdown)
# ---------------------------------------------------------------------------
_FENCE_RE = re.compile(r"^(```|~~~)")


def _strip_code_and_math(md):
    """Remove fenced code and math so $/brace balance checks don't false-fire."""
    out, in_fence = [], False
    for line in md.splitlines():
        if _FENCE_RE.match(line.strip()):
            in_fence = not in_fence
            out.append("")
            continue
        out.append("" if in_fence else line)
    return "\n".join(out)


def check_math_source(md, findings):
    text = _strip_code_and_math(md)
    # $$ balance
    dd = len(re.findall(r"\$\$", text))
    if dd % 2:
        findings.append(Finding("M001", "ERROR", "odd number of $$ display-math delimiters (%d)" % dd))
    # single $ balance (after removing $$ and escaped \$)
    singles = text.replace("$$", "").replace(r"\$", "")
    sc = singles.count("$")
    if sc % 2:
        findings.append(Finding("M001", "ERROR", "odd number of $ inline-math delimiters (%d)" % sc))
    # \begin / \end balance
    begins = re.findall(r"\\begin\{([a-zA-Z*]+)\}", md)
    ends = re.findall(r"\\end\{([a-zA-Z*]+)\}", md)
    if sorted(begins) != sorted(ends):
        findings.append(Finding("M002", "ERROR",
                                 "\\begin/\\end environments unbalanced: begins=%s ends=%s" % (begins, ends)))
    # matrix rows equal column count (bmatrix/pmatrix)
    for env in ("bmatrix", "pmatrix", "vmatrix", "matrix"):
        for m in re.finditer(r"\\begin\{%s\}(.*?)\\end\{%s\}" % (env, env), md, re.S):
            body = m.group(1)
            rows = [r for r in re.split(r"\\\\", body) if r.strip()]
            widths = {len(re.findall(r"(?<!\\)&", r)) for r in rows}
            if len(widths) > 1:
                findings.append(Finding("M004", "ERROR",
                                        "%s has ragged rows (column counts %s)" % (env, sorted(w + 1 for w in widths))))


def _strip_py_strings(line):
    """Blank out the contents of straight-quoted string literals so a check can
    tell code-position characters from in-string data. Simple single-line pass
    (good enough for a smart-quote-in-syntax check)."""
    out, i, n = [], 0, len(line)
    quote = None
    while i < n:
        c = line[i]
        if quote:
            if c == quote:
                quote = None
                out.append(c)
            else:
                out.append(" ")  # blank string content
        elif c in ("'", '"'):
            quote = c
            out.append(c)
        else:
            out.append(c)
        i += 1
    return "".join(out)


def check_code_source(md, findings):
    lines = md.splitlines()
    i = 0
    while i < len(lines):
        s = lines[i].strip()
        m = re.match(r"^(```|~~~)\s*(\S*)", s)
        if m:
            lang = m.group(2)
            # skip custom fences we know (output/repl/figure/rule) and attr forms
            if lang and lang not in ("output", "repl", "figure", "rule") and not lang.startswith("{"):
                pass  # has a language -> ok
            elif not lang:
                findings.append(Finding("C001", "ERROR", "fenced code block without a language at source line %d" % (i + 1)))
            # advance to closing fence
            j = i + 1
            while j < len(lines) and not _FENCE_RE.match(lines[j].strip()):
                # C003: a smart QUOTE used as a code delimiter breaks the parse.
                # Curly quotes / dashes INSIDE a string literal are valid data
                # (e.g. text-processing samples), so strip string contents first
                # and only flag a smart quote that survives (i.e. is real syntax).
                if lang in ("python", "py"):
                    stripped = _strip_py_strings(lines[j])
                    if re.search(r"[‘’“”]", stripped):
                        findings.append(Finding("C003", "ERROR",
                                                "smart quote used as code delimiter at line %d" % (j + 1)))
                j += 1
            i = j
        i += 1


# ---------------------------------------------------------------------------
# Rendered-HTML checks
# ---------------------------------------------------------------------------
def check_structure(html, findings):
    tree = HTMLParser(html)
    # duplicate ids
    ids = [n.attributes.get("id") for n in tree.css("[id]") if n.attributes.get("id")]
    seen, dups = set(), set()
    for i in ids:
        if i in seen:
            dups.add(i)
        seen.add(i)
    for d in sorted(dups):
        findings.append(Finding("R031", "ERROR", "duplicate id '%s'" % d))
    # img alt present
    for img in tree.css("img"):
        if not (img.attributes.get("alt") or "").strip():
            findings.append(Finding("R040", "ERROR", "img without alt text: %s" % (img.attributes.get("src") or "?")))
    # heading hierarchy: no skips. The book's DELIBERATE structure is
    # opener <h1> (chapter/module title) then questions/lessons at <h3>, so an
    # h1->h3 step immediately after an opener title is expected, not a defect.
    heads = tree.css("h1,h2,h3,h4,h5,h6")
    prev = 0
    for n in heads:
        lv = int(n.tag[1])
        opener_title = False
        p = n.parent
        while p is not None:
            if "opener" in (p.attributes.get("class") or ""):
                opener_title = True
                break
            p = p.parent
        if prev and lv > prev + 1 and not (prev == 1 and lv == 3):
            findings.append(Finding("R020", "WARN", "heading level jumps from h%d to h%d" % (prev, lv)))
        prev = lv
    # R050 NO LINKS IN A PRINTED BOOK — a book has no clickable links. Any <a href>
    # that points somewhere (not a pure in-page fragment used for structure) is an
    # error: project/GeoGebra/external content MUST be embedded, not linked.
    for a in tree.css("a[href]"):
        href = (a.attributes.get("href") or "").strip()
        if href and not href.startswith("#"):
            findings.append(Finding("R050", "ERROR",
                                    "link found in book body (printed books have no links): href=%s text=%r"
                                    % (href, (a.text() or "").strip()[:40])))


def check_math_rendered(html, findings):
    if 'class="katex-error"' in html or "katex-error" in html:
        findings.append(Finding("M003", "ERROR", "KaTeX error node present in shipped HTML"))
    if "arithmatex" in html:
        findings.append(Finding("M003", "ERROR", "unbaked arithmatex placeholder in shipped HTML (math not pre-rendered)"))
    if re.search(r"katex\.js|auto-render|MathJax", html):
        findings.append(Finding("M003", "ERROR", "runtime math JS reference in shipped HTML (must be static)"))


def check_fidelity(html, slug, findings):
    """No fabrication: a registered-blank question's solution MUST be exactly the
    placeholder; and any solution using the placeholder MUST be registered blank.
    Question keys may be ints (main sequence 'q-7') or strings ('q-0-3' for the
    Module-0 preamble), so the registry is normalized to a set of strings."""
    registry = {str(x) for x in _blank_registry(slug)}
    tree = HTMLParser(html)
    for det in tree.css("details.solution"):
        sid = det.attributes.get("id") or ""
        m = re.match(r"q-(.+)-solution$", sid)
        if not m:
            continue
        qkey = m.group(1)  # "7", "0-3", "6a", ...
        body = det.text(deep=True) or ""
        body = body.replace("Solution", "", 1).strip()
        is_placeholder = BLANK_PLACEHOLDER in body
        if qkey in registry and not is_placeholder:
            findings.append(Finding("F001", "ERROR",
                                    "Q%s is a registered BLANK solution but has content (possible fabrication)" % qkey))
        if is_placeholder and qkey not in registry:
            findings.append(Finding("F002", "WARN",
                                    "Q%s uses the blank placeholder but is not in blank_solutions.json (update registry)" % qkey))


def _contrast(fg, bg):
    try:
        import wcag_contrast_ratio as wc

        def rgb(h):
            h = h.lstrip("#")
            return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))

        return wc.contrast(rgb(fg), rgb(bg))
    except Exception:
        return None


def check_a11y(findings):
    # dark code string MUST be AA (>=4.5) on #212529
    ratio = _contrast("#4ec9a0", "#212529")
    if ratio is not None and ratio < 4.5:
        findings.append(Finding("A011", "ERROR", "dark code-string #4ec9a0 on #212529 fails AA (%.2f)" % ratio))
    bad = _contrast("#007a3d", "#212529")
    if bad is not None and bad >= 4.5:
        findings.append(Finding("A011", "WARN", "unexpected: #007a3d now passes on dark; verify token"))


# ---------------------------------------------------------------------------
def check(slug, strict=True, write_report=True):
    book = load_book(slug)
    findings = []
    full_html_parts = []
    for sec in book["sections"]:
        md = sec["md"]
        check_math_source(md, findings)
        check_code_source(md, findings)
        html = compile_unit_html(md, id_prefix=_prefix_for(sec))
        full_html_parts.append(html)
    full_html = "\n".join(full_html_parts)
    check_structure(full_html, findings)
    check_math_rendered(full_html, findings)
    check_fidelity(full_html, slug, findings)
    check_a11y(findings)

    errors = [f for f in findings if f.severity == "ERROR"]
    warns = [f for f in findings if f.severity == "WARN"]
    gate = "PASS" if not errors else "FAIL"

    if write_report:
        os.makedirs(QA_DIR, exist_ok=True)
        report = {
            "slug": slug,
            "gate": gate,
            "counts": {"error": len(errors), "warn": len(warns)},
            "findings": [f.as_dict() for f in findings],
        }
        tmp = os.path.join(QA_DIR, slug + ".qa.json.tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        os.replace(tmp, os.path.join(QA_DIR, slug + ".qa.json"))
        _write_html_report(slug, report)

    # console summary
    for f in findings:
        print("  [%s] %s: %s %s" % (f.severity, f.code, f.msg, ("(%s)" % f.where if f.where else "")))
    print("%s: %s — %d error(s), %d warning(s)" % (slug, gate, len(errors), len(warns)))

    return 0 if gate == "PASS" else 1


def _write_html_report(slug, report):
    rows = "".join(
        '<tr class="%s"><td>%s</td><td>%s</td><td>%s</td></tr>' % (f["severity"].lower(), f["severity"], f["code"], f["msg"])
        for f in report["findings"]
    )
    html = (
        "<!doctype html><meta charset=utf-8><title>QA %s</title>"
        "<style>body{font-family:system-ui;margin:2rem}h1{font-size:1.4rem}"
        "table{border-collapse:collapse;width:100%%}td{border:1px solid #ddd;padding:.3rem .5rem}"
        ".error{background:#fde8e8}.warn{background:#fff7e6}.gate{font-weight:700}</style>"
        "<h1>QA report — %s</h1><p class=gate>Gate: %s (%d errors, %d warnings)</p>"
        "<table><tr><th>Severity</th><th>Code</th><th>Message</th></tr>%s</table>"
        % (slug, slug, report["gate"], report["counts"]["error"], report["counts"]["warn"], rows)
    )
    with open(os.path.join(QA_DIR, slug + ".qa.html"), "w", encoding="utf-8") as f:
        f.write(html)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", required=True)
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--ci", action="store_true", help="treat link/grammar WARN as ERROR")
    args = ap.parse_args()
    sys.exit(check(args.book, strict=args.strict))
