#!/usr/bin/env python3
"""
challenge_card.py
-----------------
Generate the daily-challenge landing-page image LOCALLY from FCC-API data we
already sync — no Instagram scraping, no third-party credentials, no ToS risk.

DESIGN (owner decisions, 2026-07-25):
  1. OUR brand kit (Scientific American editorial), NOT freeCodeCamp's.
  2. Python-only (no JavaScript element).
  3. No footer for now — but ALL layout/style lives in one DESIGN dict so a
     later change re-renders every card in one command (`--all --force`).
  4. Reserve a vacant space for a future CHARACTER/mascot.
  5. Standardized text treatment across every card.
  6. GOLDEN RATIO (phi=1.618) drives the whole composition — canvas, element
     sizes, placement, type scale, spacing, accent lengths, and colour areas.
  7. Reserve a vacant space for a future LOGO.

──────────────────────────────────────────────────────────────────────────────
HOW THE GOLDEN RATIO IS APPLIED (the "deep dive")
──────────────────────────────────────────────────────────────────────────────
• Canvas is a golden rectangle: H / W = phi  (1000 x 1618).
• Macro layout = the canvas's OWN golden subdivision:
    - major horizontal cut at y = H/phi = 1000 splits UPPER (title+desc) from
      LOWER (code+character) — i.e. a golden 'square + remainder' split.
    - the LOWER band is split by the vertical golden cut at
      x = M + contentW/phi into  PYTHON-CODE (left, 550w) : CHARACTER (right,
      340w)  ==  phi.
• The code panel is itself a golden rectangle (550 x 340) — self-similar to the
  canvas (a golden-spiral step).
• Type scale = Fibonacci {21,34,55,89,144}: Fibonacci ratios converge to phi, so
  the scale is golden AND lands on clean integers.
• Spacing / margins = Fibonacci (34, 55). Accent rule lengths = block / phi.
• Colour AREA proportion ~ phi:  paper ~61.8% (dominant), ink ~23.6%,
  accents ~14.6%  (derived from phi^0 : phi^-1 : phi^-2, normalized).
• Reserved logo & character zones are golden rectangles placed on golden points.

Run `--guides` to overlay the golden grid + golden points and SEE the structure.

Usage:
    python challenge_card.py --latest --no-apply        # preview newest
    python challenge_card.py --date 2026-07-24 --guides  # preview + golden grid
    python challenge_card.py --missing                   # fill rows w/o an image
    python challenge_card.py --all --force               # re-render EVERY card
"""

import os
import re
import sys
import html
import argparse
from datetime import datetime
from html.parser import HTMLParser

from PIL import Image, ImageDraw, ImageFont

basedir = os.path.abspath(os.path.dirname(__file__))
if basedir not in sys.path:
    sys.path.insert(0, basedir)

IMAGE_DIR = os.path.join(basedir, "static", "images")

# ── The golden constant and a Fibonacci (phi-convergent) modular scale ────────
PHI = (1 + 5 ** 0.5) / 2  # 1.6180339887…
FIB = {"xs": 21, "sm": 34, "md": 55, "lg": 89, "xl": 144, "xxl": 233}

# ── Render resolution (owner ask: crisp up to 4K, no pixel scatter) ───────────
# The card's LOGICAL design is 1000-wide; CARD_SCALE renders it at that many
# device pixels per logical pixel. At 3× the base canvas is 3000×4854 — sharp on
# any display up to 4K and on 2× Retina panels. Because EVERY coordinate derives
# from FIB + the golden math, a single uniform multiplier keeps all golden ratios
# exact; scale=1 reproduces the original 1000px output. NOTE: this scales ONLY the
# challenge-card path — book covers import FIB/Golden/DESIGN and are deliberately
# unaffected (their size is locked by the Book Compilation Standard).
CARD_SCALE = 3


def _scaled_fib(s):
    """FIB modular scale multiplied by the render scale (keeps the type/spacing
    scale golden at any resolution)."""
    return {k: int(round(v * s)) for k, v in FIB.items()}


def _sc(v, s):
    """Scale a raw (non-FIB) logical pixel length by the render scale."""
    return int(round(v * s))


def _wd(v, s):
    """Scale a stroke width by the render scale; never below 1px so a hairline
    rule never disappears at high resolution."""
    return max(1, int(round(v * s)))


# ==============================================================================
# SINGLE SOURCE OF TRUTH — change here, re-render all cards with `--all --force`
# ==============================================================================
DESIGN = {
    "version": 3,  # bump when the look changes (useful for cache-busting later)

    # Canvas is a golden rectangle (H/W == phi).
    "canvas_w": 1000,
    "canvas_h": 1618,
    "margin": FIB["md"],           # 55 — outer margin (Fibonacci)

    # ── Brand kit (mirrors static/css/style.css :root) ──
    "paper":   (255, 255, 255),    # dominant surface  (#ffffff)
    "ink":     (33, 37, 41),       # text + code panel (#212529)
    "blue":    (0, 113, 154),      # primary accent    (#00719a)
    "red":     (167, 14, 19),      # accent / index    (#a70e13)
    "tan":     (232, 211, 190),    # subtle dividers   (#e8d3be)
    "gold":    (213, 128, 0),      # bullets / hi-lite (#d58000)
    "green":   (0, 122, 61),       # secondary         (#007a3d)
    "muted":   (102, 102, 102),    # secondary text    (#666666)
    "code_bg": (33, 37, 41),       # code panel bg (ink)
    "code_kw": (120, 190, 255),    # code keyword
    "code_fn": (240, 200, 120),    # code function name
    "code_arg":(230, 140, 140),    # code argument
    "code_txt":(226, 232, 240),    # code default

    # Standardized copy.
    "kicker": "DAILY PYTHON CHALLENGE",

    # Reserved-zone visibility. OFF for the public look: the logo (top-left)
    # and character (right golden column) ZONES are still reserved by the
    # layout — we simply don't draw the placeholder outline+label. Flip to True
    # while designing to see where the future logo/character will sit.
    "show_reserves": False,
    "reserve_logo_label": "LOGO",
    "reserve_char_label": "CHARACTER",

    "footer": None,  # removed for now (owner will add later)

    # Code-panel treatment (overridable per theme; see THEMES below).
    "code_border": None,           # None = no border (solid fill)
    "code_tab": None,              # None = fall back to brand green
}


# ==============================================================================
# THEMES — colour treatments only. The golden-ratio LAYOUT engine is shared and
# untouched; a theme just overrides colours (esp. the code panel, which read as
# harsh in pure black). Pick with `--theme <name>`; set DEFAULT_THEME to lock it.
# All themes stay inside the brand kit (blue/red/tan/gold/green/ink on paper).
# ==============================================================================
def _merge(*overrides):
    """Compose a theme dict on top of the base DESIGN (last wins)."""
    out = dict(DESIGN)
    for o in overrides:
        out.update(o)
    return out


THEMES = {
    # 0) The current look — kept for comparison.
    "ink": _merge({
        "code_bg": (33, 37, 41), "code_tab": (0, 122, 61),
        "code_kw": (120, 190, 255), "code_fn": (240, 200, 120),
        "code_arg": (230, 140, 140), "code_txt": (226, 232, 240),
        "code_border": None,
    }),

    # 1) EDITORIAL — light "paper" code card: soft blue-grey fill, hairline
    #    border, dark ink code. Matches a printed-magazine code listing; the
    #    most cohesive with the serif body. (Recommended.)
    "editorial": _merge({
        "code_bg": (245, 247, 249),          # near-paper, faint cool tint
        "code_border": (214, 223, 230),      # hairline rule
        "code_tab": (0, 113, 154),           # brand blue tab
        "code_kw": (167, 14, 19),            # brand red keywords
        "code_fn": (0, 88, 99),              # petrol function names
        "code_arg": (0, 122, 61),            # green args
        "code_txt": (33, 37, 41),            # ink code text
    }),

    # 2) PARCHMENT — warm tan-tinted code card echoing the brand tan; cohesive,
    #    softer than white, still light and professional.
    "parchment": _merge({
        "code_bg": (247, 240, 230),          # warm off-white (tan-derived)
        "code_border": (223, 205, 182),      # tan hairline
        "code_tab": (167, 14, 19),           # red tab
        "code_kw": (0, 88, 99),              # petrol keywords
        "code_fn": (167, 14, 19),            # red function names
        "code_arg": (0, 122, 61),            # green args
        "code_txt": (51, 42, 33),            # warm dark-brown ink
    }),

    # 3) MIDNIGHT-BLUE — if a DARK panel is wanted, use the brand's deep petrol/
    #    navy instead of pure black: richer, less harsh, on-brand.
    "midnight": _merge({
        "code_bg": (18, 34, 42),             # deep petrol-navy (brand-derived)
        "code_border": (0, 88, 99),          # petrol edge
        "code_tab": (94, 200, 160),          # mint tab
        "code_kw": (120, 190, 255),
        "code_fn": (240, 200, 120),
        "code_arg": (230, 150, 150),
        "code_txt": (223, 232, 238),
    }),
}

DEFAULT_THEME = "editorial"


# ==============================================================================
# Golden-ratio geometry engine
# ==============================================================================
class Golden:
    """Golden-ratio guides for a rectangle. All layout reads from here so the
    composition stays golden if the canvas size ever changes."""

    def __init__(self, x0, y0, w, h):
        self.x0, self.y0, self.w, self.h = x0, y0, w, h

    # Golden cuts (major = longer part measured from the near edge).
    @property
    def major_x(self):  # ~0.618 across from the left
        return self.x0 + self.w / PHI

    @property
    def minor_x(self):  # ~0.382 across from the left
        return self.x0 + self.w - self.w / PHI

    @property
    def major_y(self):
        return self.y0 + self.h / PHI

    @property
    def minor_y(self):
        return self.y0 + self.h - self.h / PHI

    @property
    def points(self):
        """The four golden 'power points' (phi analogue of thirds)."""
        return [
            (self.minor_x, self.minor_y), (self.major_x, self.minor_y),
            (self.minor_x, self.major_y), (self.major_x, self.major_y),
        ]

    @staticmethod
    def seg(length):
        """The golden (shorter) segment of `length`."""
        return length / PHI


# ── Font loading (brand fonts → Windows/Linux system fonts → default) ─────────
_FONT_DIRS = [
    os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts"),
    "/usr/share/fonts", "/usr/share/fonts/truetype",
    "/usr/share/fonts/truetype/dejavu", "/Library/Fonts",
]
_FONT_CANDIDATES = {
    "serif":      ["georgia.ttf", "times.ttf", "DejaVuSerif.ttf", "LiberationSerif-Regular.ttf"],
    "serif_bold": ["georgiab.ttf", "timesbd.ttf", "DejaVuSerif-Bold.ttf", "LiberationSerif-Bold.ttf"],
    "sans":       ["arial.ttf", "DejaVuSans.ttf", "LiberationSans-Regular.ttf"],
    "sans_bold":  ["arialbd.ttf", "DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf"],
    "mono":       ["consola.ttf", "DejaVuSansMono.ttf", "LiberationMono-Regular.ttf"],
}
_font_cache = {}


def load_font(kind, size):
    key = (kind, size)
    if key in _font_cache:
        return _font_cache[key]
    for fname in _FONT_CANDIDATES.get(kind, []):
        for d in _FONT_DIRS:
            path = os.path.join(d, fname)
            if os.path.exists(path):
                try:
                    f = ImageFont.truetype(path, size)
                    _font_cache[key] = f
                    return f
                except OSError:
                    pass
    f = ImageFont.load_default()
    _font_cache[key] = f
    return f


# ==============================================================================
# Text standardization (owner ask #5) — one clean pipeline for every card
# ==============================================================================
_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")
_BRAND_RE = re.compile(r"\bfree ?code ?camp\b|\bFCC\b", re.IGNORECASE)
_BULLET_SPLIT_RE = re.compile(r"(?<=\.)\s+(?=(?:Each|Return|If|Use|Allow|For|The|Given|Note)\b)")


def clean_text(raw):
    """Canonical text cleaner: strip HTML, unescape entities, drop third-party
    branding, collapse whitespace, tidy spacing before punctuation."""
    if not raw:
        return ""
    text = _TAG_RE.sub(" ", raw)
    text = html.unescape(text)
    text = _BRAND_RE.sub("", text)
    text = _WS_RE.sub(" ", text).strip()
    text = re.sub(r"\s+([,.;:])", r"\1", text)
    return text


def standardize_title(title):
    return clean_text(title) or "Untitled Challenge"


def standardize_index(n):
    return f"#{n}" if n else ""


def standardize_date(date_id):
    try:
        dt = datetime.strptime(date_id, "%Y-%m-%d")
        return dt.strftime("%B %-d, %Y") if os.name != "nt" else dt.strftime("%B %#d, %Y")
    except (ValueError, TypeError):
        return date_id or ""


def split_intro_bullets(raw):
    """(intro, [bullet,...]) — bullets detected from FCC's rule-sentence style.
    Fallback only; prefer parse_description_blocks() which reads real HTML."""
    text = clean_text(raw)
    parts = _BULLET_SPLIT_RE.split(text)
    if len(parts) <= 1:
        return text, []
    return parts[0], [p.strip() for p in parts[1:] if p.strip()]


class _DescriptionParser(HTMLParser):
    """Turn FCC's description HTML into an ordered list of typed blocks so we
    can render paragraphs, bullet lists, and tables PROPERLY (owner ask #6:
    'fix now, preserve structure'). The full HTML is already stored in
    fcc_description, so no re-sync is needed — we parse what we have.

    Emits blocks like:
        {"type": "para",   "text": "..."}
        {"type": "bullets","items": ["...", "..."]}
        {"type": "table",  "head": ["Coin","Value"], "rows": [["pennies","$0.01"], ...]}
    """

    def __init__(self):
        super().__init__()
        self.blocks = []
        self._buf = []            # text accumulator for the current leaf
        self._mode = None         # None | 'p' | 'li'
        self._list_items = None   # collecting <li> under a <ul>/<ol>
        self._table = None        # {"head": [...], "rows": [[...]]}
        self._row = None          # current <tr> cells
        self._in_head = False

    # --- helpers ---
    def _flush_text(self):
        txt = _WS_RE.sub(" ", "".join(self._buf)).strip()
        self._buf = []
        return txt

    def handle_starttag(self, tag, attrs):
        if tag in ("p",):
            self._mode = "p"; self._buf = []
        elif tag in ("ul", "ol"):
            self._list_items = []
        elif tag == "li":
            self._mode = "li"; self._buf = []
        elif tag == "table":
            self._table = {"head": [], "rows": []}
        elif tag == "thead":
            self._in_head = True
        elif tag == "tr":
            self._row = []
        elif tag in ("td", "th"):
            self._buf = []

    def handle_endtag(self, tag):
        if tag == "p":
            txt = self._flush_text()
            if txt:
                self.blocks.append({"type": "para", "text": txt})
            self._mode = None
        elif tag == "li":
            txt = self._flush_text()
            if txt and self._list_items is not None:
                self._list_items.append(txt)
            self._mode = None
        elif tag in ("ul", "ol"):
            if self._list_items:
                self.blocks.append({"type": "bullets", "items": self._list_items})
            self._list_items = None
        elif tag in ("td", "th"):
            if self._row is not None:
                self._row.append(self._flush_text())
        elif tag == "tr":
            if self._table is not None and self._row:
                if self._in_head:
                    self._table["head"] = self._row
                else:
                    self._table["rows"].append(self._row)
            self._row = None
        elif tag == "thead":
            self._in_head = False
        elif tag == "table":
            if self._table and (self._table["head"] or self._table["rows"]):
                self.blocks.append({"type": "table", **self._table})
            self._table = None

    def handle_data(self, data):
        # Collect text for whichever leaf we're inside (p / li / td / th).
        if self._mode in ("p", "li") or self._row is not None:
            self._buf.append(data)


def parse_description_blocks(raw):
    """Parse fcc_description HTML into typed blocks. Falls back to a single
    paragraph (cleaned) if there's no markup to parse."""
    if not raw:
        return []
    if "<" not in raw:  # plain text (manual problem_text)
        return [{"type": "para", "text": clean_text(raw)}]
    p = _DescriptionParser()
    try:
        p.feed(raw)
    except Exception:
        return [{"type": "para", "text": clean_text(raw)}]
    # Scrub branding from every parsed string.
    for b in p.blocks:
        if b["type"] == "para":
            b["text"] = _BRAND_RE.sub("", b["text"]).strip()
        elif b["type"] == "bullets":
            b["items"] = [_BRAND_RE.sub("", i).strip() for i in b["items"]]
        elif b["type"] == "table":
            b["head"] = [_BRAND_RE.sub("", c).strip() for c in b["head"]]
            b["rows"] = [[_BRAND_RE.sub("", c).strip() for c in r] for r in b["rows"]]
    return p.blocks or [{"type": "para", "text": clean_text(raw)}]


def wrap_text(draw, text, font, max_width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=font) <= max_width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def spaced(text, gap=" "):
    """Letter-spacing for kickers (Pillow lacks a tracking control)."""
    return gap.join(text.upper())


# ==============================================================================
# Rendering primitives
# ==============================================================================
def _draw_reserve(d, box, label, design, s=1):
    """Faint outlined placeholder for a future asset (logo / character)."""
    if not design["show_reserves"]:
        return
    F = _scaled_fib(s)
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, radius=F["xs"] // 2, outline=design["tan"], width=_wd(2, s))
    f = load_font("sans_bold", F["xs"])
    tw = d.textlength(label, font=f)
    d.text(((x0 + x1) / 2 - tw / 2, (y0 + y1) / 2 - F["xs"] / 2),
           label, font=f, fill=design["tan"])


def _draw_description_blocks(d, blocks, x, y, max_w, design, render=True, s=1):
    """Render (or, when render=False, MEASURE) parsed description blocks
    (paragraphs, bullet lists, tables) with a shared golden line-rhythm, and
    return the end-y.

    GOLDEN RULE (never auto-truncate): nothing is ever clipped here — the caller
    grows the canvas to fit whatever height this returns. `render=False` runs the
    identical layout math WITHOUT drawing, so the canvas can be pre-sized to the
    exact content height (one source of truth for measure + draw — no drift)."""
    D = design
    F = _scaled_fib(s)
    body = load_font("serif", F["sm"])
    row_f = load_font("sans", F["xs"] + _sc(3, s))
    head_f = load_font("sans_bold", F["xs"] + _sc(3, s))
    line_h = int(body.size * 1.42)

    for block in blocks:
        if block["type"] == "para":
            for line in wrap_text(d, block["text"], body, max_w):
                if render:
                    d.text((x, y), line, font=body, fill=(60, 60, 60))
                y += line_h
            y += F["xs"] // 2

        elif block["type"] == "bullets":
            for item in block["items"]:
                blines = wrap_text(d, item, body, max_w - F["sm"])
                for i, line in enumerate(blines):
                    if render:
                        if i == 0:
                            d.ellipse([x + _sc(6, s), y + _sc(12, s),
                                       x + _sc(18, s), y + _sc(24, s)], fill=D["gold"])
                        d.text((x + F["sm"], y), line, font=body, fill=(70, 70, 70))
                    y += line_h
            y += F["xs"] // 2

        elif block["type"] == "table":
            head = block.get("head", [])
            rows = block.get("rows", [])
            ncol = max(len(head), max((len(r) for r in rows), default=0)) or 1
            # Golden column split for 2-col tables: label column is the minor
            # (0.382) share, value column the major — else equal columns.
            if ncol == 2:
                c0 = max_w * (1 - 1 / PHI)
                cols = [c0, max_w - c0]
            else:
                cols = [max_w / ncol] * ncol
            row_h = int(row_f.size * 1.7)

            if head:
                if render:
                    cx = x
                    for j, cell in enumerate(head):
                        d.text((cx + _sc(10, s), y + _sc(6, s)), cell, font=head_f, fill=D["blue"])
                        cx += cols[j] if j < len(cols) else cols[-1]
                y += row_h
                if render:
                    d.line([(x, y), (x + max_w, y)], fill=D["tan"], width=_wd(2, s))
            for r in rows:
                if render:
                    cx = x
                    for j in range(ncol):
                        cell = r[j] if j < len(r) else ""
                        d.text((cx + _sc(10, s), y + _sc(6, s)), cell, font=row_f, fill=(70, 70, 70))
                        cx += cols[j] if j < len(cols) else cols[-1]
                y += row_h
                if render:
                    d.line([(x, y), (x + max_w, y)], fill=(238, 238, 238), width=_wd(1, s))
            y += F["xs"] // 2

    return y


def _code_font_and_metrics(s=1):
    """Shared code-panel font + geometry constants (one source for measure+draw)."""
    F = _scaled_fib(s)
    font = load_font("mono", F["xs"] + _sc(4, s))   # 25 @1x
    line_h = int(font.size * 1.4)
    pad = F["sm"]
    head = F["xs"] + F["md"]  # vertical space for the "python" tab
    return font, line_h, pad, head


def _wrap_code_lines(d, code, font, inner_w):
    """Soft-wrap code so long lines CONTINUE on the next visual row instead of
    being clipped (GOLDEN RULE: never truncate). Wrapped continuation rows are
    indented to signal they belong to the line above. Returns a list of
    (text, is_continuation) visual rows — the true rendered line count.

    Splitting favors natural break points (after '(', ',', space) so signatures
    like `def f(l1, l2, is_large):` wrap cleanly rather than mid-token."""
    code = (code or "def solve():\n    ...").replace("\t", "    ")
    rows = []
    for logical in code.splitlines():
        if d.textlength(logical, font=font) <= inner_w:
            rows.append((logical, False))
            continue
        # Preserve leading indentation on continuation rows for readability.
        indent = logical[: len(logical) - len(logical.lstrip())] + "    "

        def _emit(text, is_cont):
            """Append a visual row, char-breaking any piece still wider than the
            panel (e.g. one enormous unbreakable token) so NOTHING overflows the
            panel edge — the Golden Rule applied to code too."""
            prefix = indent if is_cont else ""
            if d.textlength(prefix + text, font=font) <= inner_w:
                rows.append((prefix + text if is_cont else text, is_cont))
                return
            # Hard character wrap for the overflowing remainder.
            piece = ""
            for ch in text:
                if d.textlength((indent if (is_cont or piece and rows) else "") + piece + ch,
                                font=font) <= inner_w or not piece:
                    piece += ch
                else:
                    rows.append(((indent + piece) if is_cont else piece, is_cont))
                    is_cont = True
                    piece = ch
            if piece:
                rows.append(((indent + piece) if is_cont else piece, is_cont))

        # Tokenize keeping delimiters so we can break after ( , or spaces.
        toks = [t for t in re.split(r"(\s+|(?<=[(,]))", logical) if t]
        cur, first = "", True
        for tok in toks:
            trial = cur + tok
            prefix = "" if first else indent
            if d.textlength(prefix + trial, font=font) <= inner_w or not cur.strip():
                cur = trial
            else:
                _emit(cur if first else cur, not first)
                first = False
                cur = tok.lstrip()
        if cur:
            _emit(cur, not first)
    return rows


def _draw_python_code(d, box, code, design, render=True, s=1):
    """Draw (or, when render=False, no-op) the Python starter in a code panel
    with light keyword/def highlighting. `box` is (x0,y0,x1,y1).

    GOLDEN RULE: no line cap and no horizontal clip — long lines soft-wrap and
    ALL lines render. The panel height is sized by the caller from
    code_panel_height() so every line fits."""
    F = _scaled_fib(s)
    x0, y0, x1, y1 = box
    if render:
        border = design.get("code_border")
        d.rounded_rectangle(box, radius=F["xs"] // 2, fill=design["code_bg"],
                            outline=border, width=_wd(2, s) if border else 0)
        # A small "python" tab, upper-left (themed; defaults to the brand green).
        tab_f = load_font("mono", F["xs"])
        d.text((x0 + F["sm"], y0 + F["xs"]), "python", font=tab_f,
               fill=design.get("code_tab", design["green"]))
    if not render:
        return

    kw = {"def", "return", "for", "if", "in", "else", "elif", "while",
          "None", "True", "False", "and", "or", "not", "import", "from"}
    font, line_h, pad, head = _code_font_and_metrics(s)
    inner_w = (x1 - x0) - 2 * pad
    top = y0 + head

    rows = _wrap_code_lines(d, code, font, inner_w)
    y = top
    for raw, _is_cont in rows:
        cx = x0 + pad
        seen_def = False
        for tok in re.split(r"(\s+|[(),:\[\]=])", raw):
            if not tok:
                continue
            if tok in kw:
                color = design["code_kw"]
                if tok == "def":
                    seen_def = True
            elif seen_def and re.fullmatch(r"[A-Za-z_]\w*", tok):
                color = design["code_fn"]; seen_def = False
            elif re.fullmatch(r"[a-z_]\w*", tok) and cx > x0 + pad + _sc(160, s):
                color = design["code_arg"]
            else:
                color = design["code_txt"]
            d.text((cx, y), tok, font=font, fill=color)
            cx += d.textlength(tok, font=font)
        y += line_h


def code_panel_height(d, code, inner_w, s=1):
    """Height the code panel needs to show ALL (soft-wrapped) lines — used to
    grow the canvas so nothing is clipped. Mirrors _draw_python_code geometry."""
    font, line_h, pad, head = _code_font_and_metrics(s)
    rows = _wrap_code_lines(d, code, font, inner_w)
    return head + len(rows) * line_h + pad


def _draw_guides(d, page, design, s=1):
    """Overlay the golden grid + golden points (review aid, `--guides`)."""
    g = page
    c = (0, 180, 220)
    r = _sc(7, s)
    for x in (g.minor_x, g.major_x):
        d.line([(x, g.y0), (x, g.y0 + g.h)], fill=c, width=_wd(1, s))
    for y in (g.minor_y, g.major_y):
        d.line([(g.x0, y), (g.x0 + g.w, y)], fill=c, width=_wd(1, s))
    for (px, py) in g.points:
        d.ellipse([px - r, py - r, px + r, py + r], outline=design["red"], width=_wd(3, s))


# ==============================================================================
# The card renderer — reads DESIGN + Golden for every position/size
# ==============================================================================
def render_card(title, challenge_number, date_id, description,
                starter_py=None, design=None, draw_guides=False, scale=CARD_SCALE):
    """Render a golden-ratio challenge card.

    GOLDEN RULE + GOLDEN RATIO reconciled: WIDTH is fixed at 1000 (logical) so
    every HORIZONTAL golden relationship (column split, code-panel width,
    Fibonacci margins/type scale) is exact. HEIGHT is content-driven with a
    MINIMUM of the golden ideal (1000×1618): short cards keep the exact golden
    canvas and layout; content-heavy cards GROW taller so nothing is truncated.
    A measure pass computes the needed height before drawing.

    `scale` multiplies every pixel quantity uniformly, so the card renders at high
    resolution (default 3× → 3000-wide, crisp up to 4K and on 2× Retina panels).
    Every golden ratio is preserved exactly; scale=1 reproduces the 1000px card."""
    s = scale
    D = design or THEMES[DEFAULT_THEME]
    F = _scaled_fib(s)
    W, M = _sc(D["canvas_w"], s), _sc(D["margin"], s)
    canvas_h = _sc(D["canvas_h"], s)
    cw = W - 2 * M                                 # content width (fixed)

    # ── Fonts (Fibonacci sizes, scaled) ──
    f_kicker = load_font("sans_bold", F["xs"])            # 21 @1x
    f_index  = load_font("mono", F["sm"])                 # 34 @1x
    f_date   = load_font("sans", F["xs"])                 # 21 @1x
    f_title  = load_font("serif_bold", F["lg"])           # 89 @1x

    # A scratch draw context for MEASURING (text metrics need a draw object but
    # not the final-size canvas — the layout math is identical whether measuring
    # or drawing, so measure→size→draw can never drift).
    scratch = Image.new("RGB", (W, 8), D["paper"])
    dm = ImageDraw.Draw(scratch)

    logo_w, logo_h = F["xxl"], round(F["xxl"] / PHI)  # 233 x 144 (golden) @1x
    div_y = M + logo_h + F["sm"]

    # ── Title layout (shared by measure + draw): shrink one golden step if long,
    #    but NEVER cap the number of lines (Golden Rule — no title truncation). ──
    tf = f_title
    tlines = wrap_text(dm, standardize_title(title), tf, cw)
    if len(tlines) > 2:
        tf = load_font("serif_bold", F["md"] + _sc(5, s))  # ~60 @1x
        tlines = wrap_text(dm, standardize_title(title), tf, cw)
    title_line_h = int(tf.size * 1.12)

    y_title = div_y + F["md"]
    y_after_title = y_title + len(tlines) * title_line_h
    y_accent = y_after_title + F["xs"] // 2
    y_desc = y_accent + F["md"]

    # ── Description height (measure-only pass; never clipped) ──
    blocks = parse_description_blocks(description)
    desc_end = _draw_description_blocks(dm, blocks, M, y_desc, cw, D, render=False, s=s)

    # ── Lower band geometry: golden vertical split → CODE | CHARACTER ──
    split_x = M + cw / PHI              # x = M + contentW/phi  (golden cut)
    gap = F["sm"]
    code_w = (split_x - M) - gap
    code_h_ideal = round(code_w / PHI)  # golden rectangle (the ideal)
    inner_w = code_w - 2 * F["sm"]
    code_h_needed = code_panel_height(dm, starter_py, inner_w, s)
    code_h = max(code_h_ideal, code_h_needed)   # grow vertically if code overflows

    gap_upper_lower = F["lg"]           # breathing space between desc and band

    # Where the lower band starts. For a card that fits the golden ideal, this is
    # exactly the canvas's documented major golden cut (canvas_h/phi = 1000), which
    # reproduces the original composition. For a taller card it sits just below the
    # description. We first compute the minimal height the content needs, then take
    # the golden cut of the FINAL height so the major/minor split stays golden at
    # whatever size the canvas ends up (fixes: don't hard-code the 1618 cut).
    ideal_cut = canvas_h / PHI
    lower_top = max(ideal_cut, desc_end + gap_upper_lower)

    # Final canvas height: never below the golden ideal; grows to fit everything.
    H = int(max(canvas_h, lower_top + code_h + M))
    # Re-anchor the band to the FINAL canvas's golden cut when it doesn't crowd
    # the description (keeps the golden 'square + remainder' split self-similar as
    # the canvas grows; for the ideal 1618 canvas this is a no-op = 1000).
    lower_top = max(lower_top, min(H / PHI, H - M - code_h))

    # Centre the code+character group within the lower band [lower_top, H-M].
    # For the ideal canvas this reproduces the original centred placement; for a
    # grown canvas the band exactly equals the group (no dead space).
    band_top, band_bot = lower_top, H - M
    group_top = band_top + ((band_bot - band_top) - code_h) / 2
    group_bot = group_top + code_h

    # ── Now draw onto the correctly-sized canvas ──
    img = Image.new("RGB", (W, H), D["paper"])
    d = ImageDraw.Draw(img)
    page = Golden(0, 0, W, H)

    # (reserved) LOGO zone: a golden rectangle, top-left.
    _draw_reserve(d, (M, M, M + logo_w, M + logo_h), D["reserve_logo_label"], D, s=s)

    # Masthead text: kicker + date to the right of the logo; index top-right.
    tx = M + logo_w + F["sm"]
    d.text((tx, M + F["xs"]), spaced(D["kicker"]), font=f_kicker, fill=D["blue"])
    d.text((tx, M + F["xs"] + F["sm"]), standardize_date(date_id),
           font=f_date, fill=D["muted"])
    idx = standardize_index(challenge_number)
    if idx:
        iw = d.textlength(idx, font=f_index)
        pad = F["xs"] // 2
        d.rectangle([W - M - iw - 2 * pad, M, W - M, M + F["sm"] + pad],
                    fill=D["red"])
        d.text((W - M - iw - pad, M + pad // 2), idx, font=f_index, fill=D["paper"])

    # Divider under masthead.
    d.line([(M, div_y), (W - M, div_y)], fill=D["ink"], width=_wd(2, s))

    # UPPER region — title (all lines).
    y = y_title
    for line in tlines:
        d.text((M, y), line, font=tf, fill=D["ink"])
        y += title_line_h

    # Red accent rule — length is the golden segment of the content width.
    d.line([(M, y_accent), (M + Golden.seg(cw) / PHI, y_accent)], fill=D["red"], width=_wd(6, s))

    # Description: real HTML structure (paragraphs / bullet lists / tables),
    # rendered in FULL — the canvas was sized to fit it (Golden Rule).
    _draw_description_blocks(d, blocks, M, y_desc, cw, D, render=True, s=s)

    # LOWER region — LEFT: Python code panel (golden rect, grown if needed).
    code_box = (M, group_top, M + code_w, group_bot)
    _draw_python_code(d, code_box, starter_py, D, render=True, s=s)

    # LOWER region — RIGHT: reserved CHARACTER zone, matching the code height.
    char_box = (split_x + gap, group_top, W - M, group_bot)
    _draw_reserve(d, char_box, D["reserve_char_label"], D, s=s)

    if draw_guides:
        _draw_guides(d, page, D, s=s)

    return img


# ==============================================================================
# DB integration
# ==============================================================================
def _card_filename(date_id):
    return f"{date_id.replace('-', '')}_card.jpg"


def _is_generated_or_empty(image_path):
    """A row is safe to (re)generate only if it has no image or its image is a
    card WE generated. Manual /admin uploads are protected."""
    return (not image_path) or image_path.endswith("_card.jpg")


def generate_for_challenge(challenge, apply=True, force=False, draw_guides=False, scale=CARD_SCALE):
    if not force and challenge.image_path and not _is_generated_or_empty(challenge.image_path):
        return ("skipped-manual", challenge.image_path)
    try:
        img = render_card(
            title=challenge.title,
            challenge_number=challenge.challenge_number,
            date_id=challenge.date_id,
            description=challenge.fcc_description or challenge.problem_text,
            starter_py=challenge.fcc_starter_py,
            draw_guides=draw_guides,
            scale=scale,
        )
        os.makedirs(IMAGE_DIR, exist_ok=True)
        fname = _card_filename(challenge.date_id)
        # quality=92 + subsampling=0 (4:4:4, no chroma subsampling) keeps text
        # edges and the red index chip crisp at high resolution; optimize trims
        # bytes. progressive lets a large card paint as it loads.
        img.save(os.path.join(IMAGE_DIR, fname), "JPEG",
                 quality=92, subsampling=0, optimize=True, progressive=True)
    except Exception as e:  # never let one bad row abort a batch
        print(f"  ! error rendering {challenge.date_id}: {e}")
        return ("error", None)
    if apply:
        challenge.image_path = fname
    return ("generated", fname)


def main():
    parser = argparse.ArgumentParser(description="Generate golden-ratio daily-challenge cards from synced FCC data")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--date", help="Generate for a single YYYY-MM-DD")
    group.add_argument("--latest", action="store_true", help="Generate for the newest challenge")
    group.add_argument("--all", action="store_true", help="(Re)generate for every challenge")
    group.add_argument("--missing", action="store_true", help="Only rows without an image (default)")
    parser.add_argument("--no-apply", dest="apply", action="store_false", help="Write image but do NOT set image_path in the DB")
    parser.add_argument("--force", action="store_true", help="Overwrite generated cards too (never manual images)")
    parser.add_argument("--guides", action="store_true", help="Overlay the golden grid + golden points")
    parser.add_argument("--scale", type=int, default=CARD_SCALE,
                        help=f"Render resolution multiplier (default {CARD_SCALE} -> {1000 * CARD_SCALE}px wide, 4K-crisp). Use 1 for the legacy 1000px card.")
    args = parser.parse_args()

    from app import app
    from models import db, Challenge

    with app.app_context():
        if args.date:
            rows = Challenge.query.filter_by(date_id=args.date).all()
            if not rows:
                print(f"No challenge found for {args.date}.")
                return
        elif args.latest:
            row = Challenge.query.order_by(Challenge.date_id.desc()).first()
            rows = [row] if row else []
        elif args.all:
            rows = Challenge.query.order_by(Challenge.date_id.asc()).all()
        else:
            rows = [c for c in Challenge.query.order_by(Challenge.date_id.asc()).all() if not c.has_image]

        print(f"Generating cards for {len(rows)} challenge(s)  [DESIGN v{DESIGN['version']}, scale {args.scale}x -> {1000 * args.scale}px]...")
        gen = skip = err = 0
        for c in rows:
            status, fname = generate_for_challenge(c, apply=args.apply, force=args.force,
                                                   draw_guides=args.guides, scale=args.scale)
            if status == "generated":
                gen += 1
                print(f"  + {c.date_id}  #{c.challenge_number or '?'}  {c.title}  ->  {fname}")
            elif status == "skipped-manual":
                skip += 1
                print(f"  = {c.date_id}  kept manual image ({fname})")
            else:
                err += 1
        if args.apply and gen:
            db.session.commit()
            print(f"\nCommitted image_path for {gen} row(s).")
        print(f"Done: {gen} generated, {skip} skipped (manual), {err} errors.")


if __name__ == "__main__":
    main()
