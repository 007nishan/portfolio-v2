"""
book_cover.py — golden-ratio COVER + per-unit OPENER images for compiled books
(BCS v1.0 §6). Extends challenge_card.py's Golden/DESIGN/load_font on the shared
1000x1618 golden canvas. One config re-renders all with `--all --force`.

Outputs JPGs to static/books/covers/:
    <slug>_cover.jpg
    <slug>_<unit>_opener.jpg    (unit = 0..8 for python; 0,A..O for LA)

Text anchors read from the CONTENT Golden(M,M,cw,ch); accent rule = Golden.seg(cw)/PHI
= cw/phi^2 (mirrors challenge_card.py line 637). Covers use sharp corners (radius 0).
"""
import argparse
import os

from PIL import Image, ImageDraw

from challenge_card import PHI, FIB, DESIGN, Golden, load_font, IMAGE_DIR  # noqa

HERE = os.path.dirname(os.path.abspath(__file__))
COVERS_DIR = os.path.join(HERE, "static", "books", "covers")
COVER_VERSION = 1

W, H = DESIGN["canvas_w"], DESIGN["canvas_h"]      # 1000 x 1618
M = DESIGN["margin"]                                # 55
CW, CH = W - 2 * M, H - 2 * M                       # content box 890 x 1508

PAPER = DESIGN["paper"]
INK = DESIGN["ink"]
RED = DESIGN["red"]
MUTED = DESIGN["muted"]

# Per-book lead accent (only the lead role swaps; stays in-kit)
_LEAD = {"linear-algebra": DESIGN["blue"], "python": DESIGN["blue"], "aws-ml": DESIGN["blue"]}
_LEAD_COVER = {
    "linear-algebra": (0, 88, 99),   # petrol #005863
    "python": (0, 113, 154),         # blue    #00719a
    "aws-ml": (213, 128, 0),         # gold    #d58000 (--color-secondary-gold, in-kit)
}

BOOK_META = {
    "python": {
        "title": "Programming in Python",
        "subtitle": "From the shell to object-oriented design",
        "kicker": "A PORTFOLIO BOOK",
        "institution": "IIT MADRAS ONLINE DEGREE",
        "units": [str(n) for n in range(9)],
    },
    "linear-algebra": {
        "title": "Linear Algebra for AI",
        "subtitle": "Oceanverse — vectors to neural networks",
        "kicker": "AI VICHARANA SHALA",
        "institution": "IIT ROPAR",
        "units": ["0"] + list("ABCDEFGHIJKLMNO"),
    },
    "aws-ml": {
        "title": "Notes as We Learn — AWS ML",
        "subtitle": "A living notebook for the AWS ML Engineer Associate",
        "kicker": "LEARNING IN PUBLIC",
        "institution": "AWS CERTIFICATION · MLA-C01",
        "units": [str(n) for n in range(8)],
    },
}


def _wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def _fit_title(draw, title, max_w):
    """Auto-shrink ladder 233 -> 144 -> 89, re-wrapping at each step."""
    for size in (FIB["xxl"], FIB["xl"], FIB["lg"]):
        font = load_font("serif_bold", size)
        lines = _wrap(draw, title, font, max_w)
        if all(draw.textlength(ln, font=font) <= max_w for ln in lines) and len(lines) <= 4:
            return font, lines, size
    font = load_font("serif_bold", FIB["lg"])
    return font, _wrap(draw, title, font, max_w), FIB["lg"]


def render_cover(slug):
    meta = BOOK_META[slug]
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    content = Golden(M, M, CW, CH)
    lead = _LEAD_COVER.get(slug, DESIGN["blue"])

    # Kicker on the upper-left, baseline near the minor_y power point.
    kfont = load_font("sans_bold", FIB["xs"])
    ky = int(content.minor_y - FIB["xxl"])
    d.text((M, ky), meta["kicker"], font=kfont, fill=lead)

    # Title — golden auto-shrink ladder, top-left anchored below the kicker.
    tfont, tlines, tsize = _fit_title(d, meta["title"], CW)
    ty = ky + int(FIB["sm"])
    lh = int(tsize * 1.05)
    for ln in tlines:
        d.text((M, ty), ln, font=tfont, fill=INK)
        ty += lh

    # Accent rule = Golden.seg(cw)/PHI = cw/phi^2 (mirrors card line 637), 6px.
    ry = ty + int(FIB["sm"])
    rule_len = Golden.seg(CW) / PHI
    d.line([(M, ry), (M + rule_len, ry)], fill=RED, width=6)

    # Subtitle (serif italic-ish; use serif) under the rule.
    sfont = load_font("serif", FIB["sm"])
    sy = ry + int(FIB["sm"])
    for ln in _wrap(d, meta["subtitle"], sfont, CW):
        d.text((M, sy), ln, font=sfont, fill=INK)
        sy += int(FIB["sm"] * 1.3)

    # Institution near the bottom margin (major_y region), muted uppercase sans.
    ifont = load_font("sans", FIB["xs"])
    d.text((M, H - M - FIB["sm"]), meta["institution"], font=ifont, fill=MUTED)

    return img


def render_opener(slug, unit):
    meta = BOOK_META[slug]
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    lead = _LEAD_COVER.get(slug, DESIGN["blue"])

    # Big numeral/letter on a power point (mono, red), like the screen opener.
    nfont = load_font("mono", FIB["xxl"])
    label = "MODULE" if slug == "linear-algebra" else "CHAPTER"
    kfont = load_font("sans_bold", FIB["xs"])
    d.text((M, int(H / PHI) - FIB["xxl"] - FIB["sm"]), f"{label} {unit}", font=kfont, fill=lead)
    d.text((M, int(H / PHI) - FIB["xxl"]), str(unit), font=nfont, fill=RED)

    # Accent rule under the numeral.
    ry = int(H / PHI) + int(FIB["xs"])
    d.line([(M, ry), (M + Golden.seg(CW) / PHI, ry)], fill=RED, width=6)
    return img


def _save(img, name):
    os.makedirs(COVERS_DIR, exist_ok=True)
    path = os.path.join(COVERS_DIR, name)
    img.save(path, "JPEG", quality=92, subsampling=0)
    return path


def build(slug, do_cover=True, do_openers=True):
    written = []
    if do_cover:
        written.append(_save(render_cover(slug), f"{slug}_cover.jpg"))
    if do_openers:
        for u in BOOK_META[slug]["units"]:
            written.append(_save(render_opener(slug, u), f"{slug}_{u}_opener.jpg"))
    return written


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", default="all", help="python | linear-algebra | all")
    ap.add_argument("--cover-only", action="store_true")
    ap.add_argument("--force", action="store_true")  # accepted for CLI parity
    args = ap.parse_args()
    slugs = list(BOOK_META) if args.book == "all" else [args.book]
    for s in slugs:
        w = build(s, do_cover=True, do_openers=not args.cover_only)
        print(f"{s}: wrote {len(w)} image(s) -> {COVERS_DIR}")
