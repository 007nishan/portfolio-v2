"""
katex_prerender.py — build-time math bake (BCS v1.1 §B.2).

Consumes post-Markdown HTML containing pymdownx.arithmatex placeholders
  inline:  <span class="arithmatex">\\(...\\)</span>
  display: <div class="arithmatex">\\[...\\]</div>
and replaces each with static KaTeX HTML rendered by the vendored KaTeX via
`katex_render.js` (ONE Node process for the whole book — no per-equation
subprocess). Raises on ANY TeX error, so a broken formula aborts the build and
never reaches the shipped HTML (screen == PDF == linted, zero JS at runtime).
"""
import json
import os
import re
import subprocess

_HERE = os.path.dirname(os.path.abspath(__file__))
_RENDER_JS = os.path.join(_HERE, "katex_render.js")
_NODE = os.environ.get("NODE_BIN", "node")

_INLINE_RE = re.compile(r'<span class="arithmatex">\\\((.*?)\\\)</span>', re.S)
_DISPLAY_RE = re.compile(r'<div class="arithmatex">\\\[(.*?)\\\]</div>', re.S)


def _unescape(s):
    # arithmatex HTML-escapes & inside math (e.g. bmatrix column separator).
    # Order: &lt;/&gt; before &amp; (documented; literal &amp; does not occur in matrix TeX).
    return s.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")


def render(html):
    """html (post-markdown, .arithmatex placeholders) -> final KaTeX HTML.
    Idempotent when no .arithmatex nodes remain. Raises RuntimeError on TeX error."""
    if "arithmatex" not in html:
        return html

    # 1) Collect every equation in document order, remembering display flag + span.
    jobs = []          # {tex, display}
    slots = []         # (start, end, display_index)

    for m in _DISPLAY_RE.finditer(html):
        slots.append((m.start(), m.end(), len(jobs)))
        jobs.append({"tex": _unescape(m.group(1)), "display": True})
    for m in _INLINE_RE.finditer(html):
        slots.append((m.start(), m.end(), len(jobs)))
        jobs.append({"tex": _unescape(m.group(1)), "display": False})

    if not jobs:
        return html

    # 2) One Node process renders them all.
    if not os.path.exists(_RENDER_JS):
        raise RuntimeError(f"katex_render.js missing at {_RENDER_JS}")
    proc = subprocess.run(
        [_NODE, _RENDER_JS],
        input=json.dumps(jobs),
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=120,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"KaTeX batch render failed:\n{proc.stderr.strip()}")
    rendered = json.loads(proc.stdout)
    if len(rendered) != len(jobs):
        raise RuntimeError(f"KaTeX returned {len(rendered)} of {len(jobs)} equations")

    # 3) Splice back, right-to-left so offsets stay valid. Display math wrapped.
    slots.sort(key=lambda s: s[0], reverse=True)
    out = html
    for start, end, idx in slots:
        frag = rendered[idx]
        if jobs[idx]["display"]:
            frag = '<div class="katex-display-wrap">' + frag + "</div>"
        out = out[:start] + frag + out[end:]
    return out


if __name__ == "__main__":
    import sys

    src = sys.stdin.read()
    sys.stdout.write(render(src))
