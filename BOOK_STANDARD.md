# Book Compilation Standard — Canonical Reference

> This is the merged, authoritative standard: **BCS v1.0** (design) + **BCS v1.1 Addenda** (implementation completeness). Build from both. Generated from two deep, adversarially-verified design workflows.

---

# Book Compilation Standard (BCS v1.0)

**Status:** Canonical / Normative
**Applies to:** portfolio-v2 `/read/<token>` book pages (screen) and their WeasyPrint PDF builds (print)
**Serves:** "Programming in Python" (IIT-Madras, chapters 0-8) and "Oceanverse / Linear Algebra" (AI Vicharana Shala, IIT Ropar, modules 0 + A-O)
**Single Source of Truth (SSOT):** `challenge_card.py` (`PHI`, `FIB`, `Golden`, `DESIGN`, `THEMES`) + `static/css/style.css` `:root`

> Keyword conventions: **MUST / MUST NOT / SHOULD** are normative (RFC-2119). All numeric values were verified against `challenge_card.py` and `static/css/style.css` as they exist in the repo.

---

## 0. Reviewer corrections applied (audit trail)

This standard is the consolidation of five dimension specs plus their review corrections. Every reviewer finding was verified against source and applied:

1. **Accent-rule geometry (the load-bearing conflict).** Verified: `challenge_card.py` line 637 draws `Golden.seg(cw) / PHI`. Since `Golden.seg(L) == L / PHI`, the rendered length is `cw / PHI / PHI = cw / PHI²` (≈ `0.382·cw`), the **minor-of-minor** segment — NOT `cw / PHI` as the card docstring (line 33) claims. This is a genuine double-divide bug in the SSOT. **RESOLUTION:** the canonical accent-rule length is `measure / PHI²` (matches what the card actually renders today, so screen/print/card agree pixel-for-pixel), AND `challenge_card.py` line 637 MUST be left as-is (do not "fix" it) so the whole system stays consistent at `1/φ²`. The card docstring line 33 MUST be corrected to read "Accent rule length = block / phi² (the golden minor-of-minor)". Every "= contentWidth/phi" and "measure/phi" accent claim from the source specs is superseded by `1/φ²`.
2. **Color-area label.** Verified: `challenge_card.py` lines 34-35 label `61.8 : 23.6 : 14.6` as `phi^0 : phi^-1 : phi^-2 normalized`, which actually yields `50.0 : 30.9 : 19.1`. **RESOLUTION:** relabel everywhere as a **nested golden cut** (`100/φ = 61.8`; then the `38.2` remainder split again `38.2/φ = 23.6`, minor `14.6`). Fix the card docstring lines 34-35.
3. **Clamp-min formula.** Verified: declared heading mins equal the previous size's max (one √φ step down), not `max/φ`. **RESOLUTION:** the canonical rule is `min(n) = max(n-1) = max(n) / √φ`.
4. **h4 off-chain.** Verified: `1.375 × √φ = 1.749`, not `1.813`. **RESOLUTION:** h4 max = **1.75rem**, and h3/h2/h1 recomputed from it (see §4).
5. **caption vs code same-formula.** **RESOLUTION:** caption = `body/√φ → 0.875rem`; code = `body/√φ + optical compensation → 0.9375rem`, stated as two distinct rules.
6. **Print body-leading exponent.** Verified: `16/11 = 1.4545 = φ^0.779`, not `φ^0.593`. **RESOLUTION:** drop the φ-power framing; state `11pt × 1.4545 = 16pt`.
7. **√φ constant drift.** **RESOLUTION:** one constant everywhere: `--phi: 1.6180339887`; `--sqrt-phi: 1.2720196495`; CSS `calc()` uses full-precision `--phi`.
8. **Page-geometry self-violations.** Verified `--color-primary-black` = `#000000`. **RESOLUTION:** print body/code ink MUST be `--color-neutral-900` (#212529), never `--color-primary-black`. Non-Fibonacci literals (13mm, 65rem, 6px) are either replaced with `--fib-*` values or added to an explicit allow-list (§2.4).
9. **@page margin-boxes in Chromium.** Verified deploy target. **RESOLUTION:** the PDF engine is **WeasyPrint** (§8), which fully supports `@page`/`running()`/`target-counter()`; browser "Print to PDF" is a degraded fallback only.
10. **Card fonts.** Verified: `_FONT_CANDIDATES` maps serif→georgia, sans→arial, mono→consola. The card art is Georgia/Arial/Consolas; the **web** side loads the real brand fonts via `base.html`. **RESOLUTION:** the phrase "matches the card exactly" is retained ONLY for the genuinely exact matches (the `FIB` scale, margin 55, gutter 34, canvas 1000×1618, and the 2-col 38.2/61.8 table split); font parity claims are dropped.

---

## 1. Principles

1. **One system, two books.** A "chapter" (Python) and a "module" (Linear Algebra) are the SAME `.opener` component; a "lesson" and a "question" are the SAME `.unit`. Book identity lives in *content and config*, never in forked CSS or a second code path.
2. **φ is the only ratio.** Every proportion derives from `PHI = 1.6180339887`. Adjacent Fibonacci `{21,34,55,89,144,233}` ratios converge to φ, so they are the golden integer scale.
3. **Extend, never fork.** All book CSS lives in one fenced block in `static/css/style.css`, scoped under `.reader`, reusing `--font-family-*`, the color palette, and `--radius-sm/md`. Never introduce a new font, weight, color, or rounded/bubbly radius.
4. **Editorial, flat, sharp.** Radii 0 (cards/panels) / 2px / 4px max. No shadows. 1px `#ebebeb` borders → `#666` on hover. Crimson Text for reading, Libre Franklin UPPERCASE for chrome, JetBrains Mono for code/numerals.
5. **Screen and print are one artifact family.** The PDF consumes the same Jinja+Markdown HTML; only the pt-scale and `@page` geometry change (§8).
6. **Math and question/solution pairs are first-class**, especially for the LA book.

---

## 2. Master token table

### 2.1 φ constants (SSOT)

| Token | Value | Note |
|---|---|---|
| `--phi` | `1.6180339887` | identical to `PHI` in challenge_card.py |
| `--sqrt-phi` | `1.2720196495` | reading-track minor step; `√φ² = φ`; used as a documented constant, `calc()` uses `--phi` |
| `φ²` | `2.6180339887` | |
| `1/φ` | `0.6180339887` | golden major share |
| `1/φ²` | `0.3819660113` | golden minor-of-minor (accent-rule share) |

### 2.2 Fibonacci scale (px → rem @16px) — type AND spacing SSOT

| Token | px | rem |
|---|---|---|
| `--fib-xs` | 21 | 1.3125rem |
| `--fib-sm` | 34 | 2.125rem (gutter) |
| `--fib-md` | 55 | 3.4375rem (outer margin) |
| `--fib-lg` | 89 | 5.5625rem |
| `--fib-xl` | 144 | 9rem |
| `--fib-xxl` | 233 | 14.5625rem |

Self-check (MUST hold): `144/16=9`, `34/16=2.125`, `89/16=5.5625`, `55/34=1.618`, `233/144=1.618`.

### 2.3 Reading-track type scale (screen, `clamp()`), anchored at the EXISTING body clamp

Every step is one √φ (`1.2720196495`); each `clamp` **min = the previous size's max = max/√φ**; vw slope tuned so max is reached ~1280px. h4 corrected onto the chain; h3/h2/h1 recomputed from it.

| Token | clamp | max derivation |
|---|---|---|
| `--fs-caption` | `clamp(0.79rem, 0.76rem + 0.15vw, 0.875rem)` | body/√φ = 0.884 → floor 0.875 (14px) |
| `--fs-code` | `clamp(0.8125rem, 0.78rem + 0.18vw, 0.9375rem)` | body/√φ **+ optical comp for JetBrains Mono** → 0.9375 (15px) |
| `--fs-body` | `clamp(1rem, 0.95rem + 0.25vw, 1.125rem)` | **UNCHANGED — verbatim style.css l.61** (anchor) |
| `--fs-h6` | `clamp(1.05rem, 1rem + 0.25vw, 1.25rem)` | **identical to existing style.css h5 l.98** (UI label variant) |
| `--fs-h5` | `clamp(1.125rem, 1.06rem + 0.32vw, 1.375rem)` | body × √φ |
| `--fs-h4` | `clamp(1.375rem, 1.2rem + 0.7vw, 1.75rem)` | **h5 × √φ = 1.749 → 1.75** (corrected) |
| `--fs-h3` | `clamp(1.75rem, 1.5rem + 1.25vw, 2.226rem)` | h4 × √φ |
| `--fs-h2` | `clamp(2.226rem, 1.85rem + 1.9vw, 2.832rem)` | h3 × √φ |
| `--fs-h1` | `clamp(2.832rem, 2.3rem + 2.6vw, 3.602rem)` | h2 × √φ (≈58px; safely below display track) |
| `--fs-display` | `clamp(4.5rem, 3rem + 7.5vw, 5.5625rem)` | Fibonacci lg literal = 89px; chapter/module numeral |

> The raw Fibonacci px `89/144/233` are reserved for the display/numeral/drop-cap track only, so long titles never overflow a 320px viewport.

### 2.4 Layout / measure / rhythm tokens

| Token | Value | Formula |
|---|---|---|
| `--measure` | `38rem` (~66ch Crimson at body max) | reading column; the L all cuts derive from |
| `--measure-major` | `23.485rem` | `38 / φ` (0.618) — value col / figure text col |
| `--measure-minor` | `14.515rem` | `38 − 38/φ = 38/φ²` (0.382) — label col / accent rule / figure col |
| `--accent-rule` | `14.515rem` | `measure / φ²` — see §0.1 (matches card render) |
| `--rhythm` | `1.6875rem` (27px) | baseline = 18px × 1.5 |
| `--lh-body` | `1.62` | ≈ φ |
| `--lh-heading` | `1.15` | tight (≈ 1/√φ region) |
| `--lh-code` | `1.45` | scannable listings |
| `--space-para` | `0.618em` | 1em / φ |
| `--book-scroll-offset` | `5.5625rem` | `--fib-lg` = 89px anchor clearance |
| `--book-progress-h` | `4px` | literal (own token; NOT bound to `--radius-md`) |

**Allowed non-Fibonacci literals (explicit allow-list, satisfies "no magic numbers"):** `38rem` measure (chosen so `38/φ ≈ 23.5rem ≈ 66ch`), `27px` rhythm (`18×1.5`), `13mm` print inner margin (prior Fibonacci term), `4px` progress-bar height (`--radius-md` value, used as a literal not a radius). Everything else MUST be `--fib-*` or a `calc()` of `--phi`.

### 2.5 Color tokens (all pre-existing in `:root` or card `DESIGN`; two derived additions only)

| Token | Value | Role |
|---|---|---|
| `--color-primary-blue` | `#00719a` | CTAs, drop cap, Q#/SOLUTION labels |
| `--color-primary-blue-dark` | `#005a7d` | hover |
| `--color-primary-red` | `#a70e13` | accent rule, display numeral, index badge, RULE |
| `--color-bg-tan` | `#e8d3be` | RULE wash, divider zones |
| `--color-secondary-gold` | `#d58000` | bullets, WARNING |
| `--color-secondary-green` | `#007a3d` | SOLUTION tab, code "python" tab |
| `--color-accent-petrol` | `#005863` | LA lead accent, project CTA |
| `--color-neutral-900` | `#212529` | **ink** — dark text / dark code bg / **print body ink** |
| `--color-primary-black` | `#000000` | headings ONLY (never body/code on paper) |
| `--color-primary-white` | `#ffffff` | paper |
| `--color-surface-subtle` | `#f8f9fa` | solution body bg |
| `--color-surface-muted` | `#f1f3f5` | inline code bg |
| `--color-neutral-medium` | `#666666` | captions, muted UI |
| `--color-neutral-light` | `#ebebeb` | 1px borders |
| **DERIVED** `--code-comment` | `#6b7785` | comment tokens (blend ink+muted); declared net-new |
| **DERIVED** `--code-str` | `#007a3d` | string tokens = existing brand green (no new hue) |

**Dark-code palette** (from card `ink`/`midnight` THEME, verbatim): `--code-bg #212529`, `--code-txt #e2e8f0`, `--code-kw #78beff`, `--code-fn #f0c878`, `--code-arg #e68c8c`.

### 2.6 Radii

`--radius-sm: 2px` (chips/badges/buttons), `--radius-md: 4px` (inline code), **0** for cards/panels/openers/covers. No new radii.

### 2.7 Color-AREA budget (corrected derivation)

Paper **61.8%** : ink **23.6%** : accent **14.6%**, derived as a **NESTED golden cut**: `100/φ = 61.8` (paper), remainder `38.2` split again `38.2/φ = 23.6` (ink), minor `14.6` (accent). NOT `φ^0:φ^-1:φ^-2`.

---

## 3. Page geometry & golden grid

### 3.1 Screen — golden two-column shell

The reading shell is a golden rectangle split into a major reading column and minor TOC sidebar, mirroring `Golden.major_x / minor_x`.

| Token | Value | Formula |
|---|---|---|
| `--book-shell-max` | `1200px` | outer shell |
| `--book-reading-w` | `742px` | `1200 / φ` (major 0.618) |
| `--book-toc-w` | `458px` | `1200 − 1200/φ` (minor 0.382) |
| `--book-gutter` | `34px` | `--fib-sm` (= card gutter, exact) |
| `--book-margin` | `55px` | `--fib-md` (= card outer margin, exact) |

The reading **column** (742px) contains the reading **measure** (`--measure` 38rem ≈ 608px); the ~134px difference is an explicitly-declared **non-golden comfort margin** for marginalia/anchors (NOT a golden cut).

Self-check (MUST hold): `1200 − 1200/φ = 458`, `1200/φ = 742`.

### 3.2 Print — golden text block inside a non-golden sheet

A4 (210×297mm) is √2, not φ, so the golden rectangle is enforced in the **text block** via mirrored golden margins:

| Margin | Value | Formula |
|---|---|---|
| spine (inner) | `20mm` | chosen base |
| fore-edge (outer) | `32.4mm` | `20 × φ` = 32.36 |
| top | `16mm` | golden-minor of vertical budget |
| bottom | `25.9mm` | `16 × φ` = 25.89 |

Text block = `210 − 20 − 32.4 = 157.6mm` wide; height = `297 − 16 − 25.9 = 255.1mm` (≈ `157.6 × φ = 255.0`, phi within 0.3%). The annotation MUST read "th = page_h − top − bottom = 255.1 (≈ tw×φ = 255.0)", not "th = tw×φ = 255.1".

`@page :left`/`@page :right` MUST mirror spine/fore-edge for true recto/verso inner-outer margins.

---

## 4. Typography & vertical rhythm

- **Fonts (roles are normative):** Crimson Text → all h1-h6 + body reading; Libre Franklin → UI/nav/buttons/kickers/labels (TIP/WARNING/PROJECT/RULE/Q#/SOLUTION), always UPPERCASE, `letter-spacing:.05em`; JetBrains Mono → code (inline+block), chapter/module numerals, matrix ASCII. No 4th font. No weight beyond those loaded in base.html (Crimson 400/600/700/400i; Franklin 300/400/500/700/900; Mono 400/500). `.rule-banner` heading uses **700** (not 900) unless a 900 is explicitly needed and is loaded (Franklin 900 IS loaded, so 900 is permitted for the banner heading only).
- **Reading track** anchored at the existing body clamp; every size derives by ×/÷ √φ (§2.3). Heading `clamp` min = previous max = `max/√φ`.
- **Vertical rhythm:** body `line-height:1.62`; all block margins are integer multiples of `--rhythm` (27px).
- **Paragraphs:** screen `margin:0 0 0.618em`, no indent. Print continuation paragraphs switch to `text-indent:1em` and zero spacing (classic book setting) via `@media print`.
- **Display numeral** JetBrains Mono, red `#a70e13`. **Drop cap** 3 baseline units, Crimson, blue `#00719a`.
- **Accent rule** under a title: `width:var(--accent-rule)` (`measure/φ²` = 14.515rem), `height:4px` (editorial stroke, on-token), `background:#a70e13`, `border-radius:0`.
- **Print pt scale** (base 11pt, √φ steps, **round to nearest integer**): caption 8.6 / body 11 / h6 14 / h5 17.8 / h4 22.6 / h3 28.8 / h2 36.6 / h1 46.6 / display numeral 75.4pt. Body leading **16pt = 11 × 1.4545** (φ-power framing dropped). Print **code = 8.6pt** (`= 11/√φ`, one clean minor step, equals caption) — no floating 9.8pt.

---

## 5. Reading / navigation UX + numbering

- **One shell:** `.reader` (a.k.a. `.book`) = `.book-toc` (aside, minor col) + `.book-reading` (main, major col, capped at `--measure`). All book styles scoped under `.reader` so they never leak into challenge/dashboard chrome.
- **Persistent brand nav** = base.html navbar unchanged. A second sticky `.book-bar` under it: breadcrumbs (left) + prev/next (right) + a 4px red progress rule pinned to its bottom edge (`aria-hidden`).
- **Anchor scheme (canonical, lowercase, stable, all carry `scroll-margin-top:var(--book-scroll-offset)`):**
  - chapter `#ch-{n}` (n=0..8); lesson `#ch-{n}-lesson-{m}`
  - module `#mod-{id}` (id=0 or A..O uppercase, e.g. `#mod-A`)
  - question `#q-{n}` (n not zero-padded); worked solution `#q-{n}-solution`
  - `#projects`; project `#project-{k}` (k=1..8)
- **Numbering:** display numeral in JetBrains Mono on a red plate. Chapters/modules show the opener numeral plate; lessons show `{chapter}.{lesson}`; questions show bare `{n}` in the chip, `Q{n}` in prose/TOC. Zero and letters are first-class (Chapter 0, Module 0, Module A) — never hidden/renumbered.
- **Breadcrumbs:** `BOOKS / {Book title} / {Chapter|Module}`, uppercase Franklin, `/` in `--color-neutral-medium`, current crumb non-link `--color-primary-black`, updated by scrollspy.
- **Prev/next** is unit-level and wraps across section boundaries; `‹ PREV` / `NEXT ›` uppercase Franklin, `aria-disabled` at book ends.
- **TOC sidebar** sticky + independently scrollable, grouped, scrollspy with exactly one `.active` marked by a **2px red left rule** (flat, no pill). `<992px` collapses to an off-canvas drawer toggled from the book-bar.
- **Solutions** = native `<details class="solution">`; green uppercase SOLUTION `<summary>`; body on `--color-surface-subtle` + 1px `#ebebeb`; collapsed by default; book-bar EXPAND/COLLAPSE ALL; a direct `#q-{n}-solution` hit force-opens on load and before print.
- **GeoGebra RULE** = single data-driven `.rule-banner` (tan bg, 4px red left rule, uppercase Franklin heading + serif body). Rendered from a per-book `site_rule` field; omitted when empty (Python), shown when set (LA). No template forking.

---

## 6. Cover & chapter/module opener generation (`book_cover.py`)

Extends `challenge_card.py`'s `Golden` + `DESIGN` + `THEMES` on the shared **1000×1618** golden canvas, margin 55. Emits a full COVER and per-unit OPENERs.

- **Coordinate systems MUST be named explicitly.** Title/author/institution anchors use the **CONTENT** `Golden(M,M,cw,ch)` whose cuts are `minor_x/major_x = 394.9/605.1` and `minor_y/major_y = 618.0/987.0`. The term "canvas power point" is reserved for the page `Golden(0,0,W,H)` cuts (`500/618/1000`). Do NOT call 987 a "canvas" power point.
- **Anchoring convention (stated once, applied to all four anchors):** text is drawn **top-left anchored** at the power point. The opener numeral is drawn at `(minor_x, minor_y − FIB.xxl)` so its baseline block rests on the `(minor_x, minor_y)` power point; the rule text MUST say this, matching the code.
- **Accent rule = `Golden.seg(cw)/PHI = cw/φ²` = 339.9px**, 6px stroke (this is the card's native 6px art stroke; the *web* accent rule is 4px per §4 — the two media differ and that is documented). This mirrors `challenge_card.py` line 637 exactly.
- **Color-area triad** = nested golden cut 61.8/23.6/14.6 (§2.7); the `count_non_paper` lint is **net-new** (define: paper = within tolerance of `#ffffff`; ink = dark text/blocks; accent = brand-hue pixels incl. motif) and MUST enforce ink ≤ 23.6% and accent ≤ 14.6% within ±3pp, or be a manual checklist item — it does NOT exist in the card today.
- **Radius:** covers/openers use sharp rectangles (radius 0-2). `_draw_reserve`/`_draw_python_code` draw `radius=FIB['xs']//2 = 10px`; therefore book_cover MUST use a sharp-corner variant (parameterize radius, default 10 for cards, 0-2 for covers) — do NOT import them verbatim for covers.
- **Theme wrapper:** `_theme_for(book)` injects a `lead` key (`petrol` for LA, `blue` for Python) onto `dict(THEMES[DEFAULT_THEME])`. Rendering MUST call `_theme_for()`; a raw `THEMES[DEFAULT_THEME]` would `KeyError` on `D['lead']`. The rule is "imports the engine and adds a thin per-book theme wrapper," not "does not fork."
- **Title auto-shrink ladder (single canonical):** `233 → 144 → 89`, re-wrapping at each step. Sample code MUST loop the ladder.
- **Unit counts:** Python 9 openers (0-8). **Oceanverse = 16 openers** (`0` + `A..O`, which is 15 letters). The brief's "15 modules" undercounts; `unit_scheme` length is **16**.
- **JPEG:** `quality=92, subsampling=0` is a deliberate, versioned exception over the card's 90 (documented via `COVER_VERSION`).
- **Fonts:** the generated art renders in Georgia/Arial/Consolas (card font fallbacks), NOT the brand webfonts. Do not claim font parity with the site.
- **CLI parity:** `--book`, `--unit`, `--cover`, `--all`, `--force`, `--guides`, `--no-apply`; `python book_cover.py --all --force` re-renders both books. Outputs to `static/books/covers/` as `<slug>_cover.jpg` / `<slug>_<unit>_opener.jpg`; MUST honor `_is_generated_or_empty`.

---

## 7. Content component library

Scoped under `.reader` / `.book-content`, appended to `static/css/style.css`, extending `.markdown-content`.

- **Inline code:** UNCHANGED — red `#a70e13` on `--color-surface-muted`, `--radius-md`.
- **Block code:** dark card palette (`#212529` bg, kw `#78beff`, fn `#f0c878`, arg `#e68c8c`, txt `#e2e8f0`, comment `#6b7785`, str `#007a3d`), green uppercase "PYTHON" tab, radius **0**. This **overrides** the existing `.markdown-content pre` radius (4px→0) and text color — documented, not "extend-only."
- **Math: KaTeX** (not MathJax). Rationale: synchronous render (no reflow flash), fast for 150+ LA formulas, and its HTML+CSS output **prints in WeasyPrint** (no JS runtime in the PDF). Load `katex.min.css` + pre-rendered markup in the book template only (`{% block extra_css/extra_js %}`), never global base.html. Inline math inherits body (1em); display equations step to h4 max; delimiters `$…$`/`$$…$$`/`\[ \]` with `throwOnError:false`. Matrices `bmatrix`, vectors `pmatrix`, eigenvectors `bmatrix`.
- **Question/solution:** `.question` with red `.question__badge` (`Q{n}`); `<details class="solution">` green tab; body `--color-surface-subtle` + 1px `#ebebeb`.
- **Callouts:** `.callout--{rule|note|tip|warning}`, 3px left accent border (RULE=red+tan wash+red top border, NOTE=blue, TIP=green, WARNING=gold), Franklin 700 uppercase label.
- **Tables:** golden 2-col split via `<colgroup>` — label col `--measure-minor` (0.382), value col `--measure-major` (0.618), matching card line 488 (`c0 = max_w*(1 − 1/PHI)`). Header: Franklin 700 uppercase blue, 2px tan bottom rule. 3+ cols → equal widths.
- **Figures:** `<figure class="book-figure">`, flat img (radius 0, 1px border), Franklin `#666` caption with a leading red rule of length `--accent-rule`.
- **GeoGebra embeds:** responsive 16:9 `.geogebra-embed` wrapper, `loading="lazy"`, preceded by the RULE callout on construction pages.
- **Project cards:** reuse `.card` as `.project-card`; red kicker `PROJECT NN`, serif title, petrol CTA.

CSS scaffold:

```css
/* ===== BOOK READING SHELL + COMPONENTS — append to static/css/style.css ===== */
:root{
  --phi:1.6180339887; --sqrt-phi:1.2720196495;
  --fib-xs:1.3125rem; --fib-sm:2.125rem; --fib-md:3.4375rem;
  --fib-lg:5.5625rem; --fib-xl:9rem; --fib-xxl:14.5625rem;
  --rhythm:1.6875rem; --lh-body:1.62; --lh-heading:1.15; --lh-code:1.45;
  --measure:38rem;
  --measure-major:calc(var(--measure)/var(--phi));            /* 23.485rem */
  --measure-minor:calc(var(--measure) - var(--measure)/var(--phi)); /* 14.515rem */
  --accent-rule:calc(var(--measure)/var(--phi)/var(--phi));   /* measure/φ² = 14.515rem */
  --book-scroll-offset:5.5625rem; --book-progress-h:4px;
  --book-shell-max:1200px;
  --book-reading-w:calc(var(--book-shell-max)/var(--phi));    /* 742px */
  --book-toc-w:calc(var(--book-shell-max) - var(--book-shell-max)/var(--phi)); /* 458px */
  --code-comment:#6b7785;
  --fs-body:clamp(1rem,.95rem+.25vw,1.125rem);
  --fs-h4:clamp(1.375rem,1.2rem+.7vw,1.75rem);
  --fs-h3:clamp(1.75rem,1.5rem+1.25vw,2.226rem);
  --fs-h2:clamp(2.226rem,1.85rem+1.9vw,2.832rem);
  --fs-h1:clamp(2.832rem,2.3rem+2.6vw,3.602rem);
  --fs-display:clamp(4.5rem,3rem+7.5vw,5.5625rem);
}
.reader{max-width:var(--measure);margin-inline:auto;padding-block:calc(var(--rhythm)*2);
  font-family:var(--font-family-serif);font-size:var(--fs-body);
  line-height:var(--lh-body);color:var(--color-neutral-dark);text-wrap:pretty}
.reader p{margin:0 0 .618em}
.reader h1,.reader h2,.reader h3,.reader h4{font-family:var(--font-family-serif);
  font-weight:700;line-height:var(--lh-heading);letter-spacing:-.02em;
  color:var(--color-primary-black);margin:calc(var(--rhythm)*1.5) 0 var(--rhythm)}
.reader h1{font-size:var(--fs-h1)} .reader h2{font-size:var(--fs-h2)}
.reader h3{font-size:var(--fs-h3)} .reader h4{font-size:var(--fs-h4)}
.reader h5,.reader h6,.reader .label{font-family:var(--font-family-sans);
  text-transform:uppercase;letter-spacing:.05em;font-weight:700}
.reader .chapter-num{font-family:var(--font-family-mono);font-size:var(--fs-display);
  line-height:1;color:var(--color-primary-red)}
.reader .accent-rule,.reader h1::after{content:"";display:block;
  width:var(--accent-rule);height:4px;background:var(--color-primary-red);
  border-radius:0;margin:var(--rhythm) 0}                     /* measure/φ² */
.reader pre,.reader .code-block{background:#212529;color:#e2e8f0;border-radius:0;
  font-family:var(--font-family-mono);font-size:.9375rem;line-height:var(--lh-code)}
.reader :not(pre)>code{background:var(--color-surface-muted);color:var(--color-primary-red);
  padding:.2em .4em;border-radius:var(--radius-md)}
.reader table.golden col.label{width:var(--measure-minor)}   /* 38.2% */
.reader table.golden col.value{width:var(--measure-major)}   /* 61.8% */
.rule-banner{background:var(--color-bg-tan);border-left:4px solid var(--color-primary-red);
  padding:var(--spacing-md) var(--spacing-lg);border-radius:0}
.rule-banner .h{font-family:var(--font-family-sans);text-transform:uppercase;
  font-weight:700;letter-spacing:.05em;color:var(--color-primary-red)}
.book-progress{position:absolute;left:0;bottom:0;height:var(--book-progress-h);
  width:0;background:var(--color-primary-red)}
@media print{
  .reader{max-width:33rem;font-size:11pt;line-height:16pt;color:var(--color-neutral-900)}
  .reader p{margin:0;text-indent:1em}
  .reader p:first-of-type,.reader .lead-in{text-indent:0}
  .reader h1{font-size:47pt} .reader h2{font-size:37pt} .reader h3{font-size:29pt}
  .reader h4{font-size:23pt} .reader h5{font-size:18pt} .reader h6{font-size:14pt}
  .reader .chapter-num{font-size:75pt}
  .reader pre,.reader .code-block{font-size:8.6pt;background:#f5f7f9!important;
    color:#212529!important;border:1px solid #d6dfe6!important}
  .callout,.book-figure,.question,table,.katex-display{break-inside:avoid}
}
```

Usage (Jinja, extends base.html; content is `{{ html | safe }}`):

```html
<article class="reader book-content markdown-content">
  <section class="opener" id="mod-A">
    <span class="chapter-num">A</span>
    <h1>Vectors &amp; the Column Space</h1><span class="accent-rule"></span>
  </section>
  {% if site_rule %}<aside class="callout callout--rule rule-banner">
    <span class="h">Rule · {{ site_rule }}</span></aside>{% endif %}
  <section class="question unit" id="q-47">
    <span class="question__badge">Q47</span>
    <h4>Find the null space of \(A\)</h4>
    <details class="solution" id="q-47-solution"><summary>Solution</summary>
      <div class="katex-display">$$A=\begin{bmatrix}2&0\\0&3\end{bmatrix}$$</div>
    </details>
  </section>
</article>
```

---

## 8. Print / PDF pipeline

- **Engine: WeasyPrint** (pure-Python, installs in the existing Flask/gunicorn venv, full CSS Paged Media). MUST NOT use headless Chromium or wkhtmltopdf (no cross-reference page numbers / EOL WebKit). Add `weasyprint` to `requirements.txt`.
- **Math:** pre-render `$…$`/`$$…$$` to KaTeX **HTML+CSS at build time** (WeasyPrint runs no JS); inject `katex.min.css` + `<span class="katex">` markup.
- **Geometry:** `@page{size:A4}` with mirrored golden margins (§3.2) bound to `@page :left`/`@page :right`; `@page :blank` strips header/footer on auto-inserted versos; `@page cover{margin:0}`; `@page frontmatter{@bottom-center{content:counter(page,lower-roman)}}`; `.book-body{counter-reset:page 1}`.
- **Running heads/footers:** `string-set` from the h1; verso header = BOOK TITLE, recto header = current chapter/module (Franklin `#666`); footer `content:counter(page)` centred. Chapter opener recto suppresses the running head.
- **Break control:** `.qa-block, pre, .code-panel, figure, table, .katex-display { break-inside:avoid }`; `h1,h2,h3{break-after:avoid}`; `p{orphans:2;widows:2}`; `.chapter{break-before:recto}`.
- **Ink:** print body/code text `--color-neutral-900` (#212529), NEVER `--color-primary-black` (#000000). Print code panel = editorial light theme (`#f5f7f9` fill, `#d6dfe6` hairline).
- **Accent rule (print):** `width:calc(157.6mm/var(--phi)/var(--phi))` ≈ **60.2mm** (= textblock/φ², consistent with the `1/φ²` system). Do NOT use 100.7mm.
- **Fonts embedded** via `@font-face` (local woff2), so the PDF is self-contained (no CDN at build).
- **Metadata:** title, authors (institution), generator `portfolio-v2 make_book_pdf`, timestamps, PDF outline from h1/h2.
- **Entrypoint:** `python make_book_pdf.py --book python|linear-algebra [--out static/books/<slug>.pdf]`; single `render_pdf(book)` path serves both books; exits non-zero on failure (so `auto_deploy.sh` can self-heal).

```python
# make_book_pdf.py (entrypoint)
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import katex_prerender               # $...$ / $$...$$  ->  KaTeX HTML+CSS
from app import app
from books import build_book_html, BOOKS   # cover + roman TOC + chapters, one template

def make_book_pdf(slug, out):
    with app.app_context():
        html = katex_prerender.render(build_book_html(slug))   # server-side math
    fc = FontConfiguration()
    doc = HTML(string=html, base_url="static/").render(
        stylesheets=[CSS("static/css/style.css"),
                     CSS("static/css/print.css"),
                     CSS("static/vendor/katex.min.css")],
        font_config=fc)
    doc.metadata.title     = BOOKS[slug]["title"]
    doc.metadata.authors   = [BOOKS[slug]["institution"]]
    doc.metadata.generator = "portfolio-v2 make_book_pdf"
    doc.write_pdf(out)        # outline/bookmarks from h1/h2 built automatically
```

---

## 9. File / route plan (Flask)

Verified against repo: route `@app.route("/read/<token>")` → `render_template(f"books/{token}.html")` with `secure_filename(token)`; base.html loads the three Google Fonts + `style.css`; `static/books/` exists.

| Path | Purpose | Change |
|---|---|---|
| `static/css/style.css` | append one fenced `BOOK READING SHELL + COMPONENTS` block (§7) | edit (extend `:root`, add `.reader/.book-*`) |
| `static/css/print.css` | Paged Media geometry + pt scale + `@page` (§8); loaded ONLY by `make_book_pdf.py` | new |
| `templates/books/_shell.html` | the shared reader shell macro both books include (TOC, book-bar, opener, unit, solution, rule-banner) | new |
| `templates/books/<token>.html` | per-book pre-rendered page, `{% extends "base.html" %}`, `{% include "_shell.html" %}`, loads KaTeX in `extra_css/extra_js` | generated |
| `book_cover.py` | cover/opener renderer extending `challenge_card.py` (§6) | new |
| `static/books/covers/` | generated cover/opener JPGs | new dir |
| `make_book_pdf.py` | WeasyPrint PDF entrypoint (§8) | new |
| `challenge_card.py` | fix docstring lines 33 (`block/phi²`) & 34-35 (nested golden cut); leave line 637 code unchanged | edit (comments only) |
| `app.py` | `/read/<token>` route unchanged; optionally add a PDF download link | no route change |
| `book_generator.py` | replace the hardcoded Windows `BOOKS_DIR` with a repo-relative path; emit `.reader` shell markup | edit |

No new route, no per-book CSS file, no change to `secure_filename` handling.

---

## 10. Per-book application notes

### 10.1 Programming in Python (IIT-Madras)

- 9 openers, `#ch-0` … `#ch-8`; units are lessons `#ch-{n}-lesson-{m}` numbered `{chapter}.{lesson}`.
- Content-heavy: prose, inline code, dark PYTHON code blocks, output examples, golden 2-col tables, TIP/NOTE/WARNING callouts.
- `site_rule` empty → `.rule-banner` omitted.
- Cover lead accent = **blue #00719a**. KaTeX may be loaded but is rarely used.

### 10.2 Oceanverse / Linear Algebra (AI Vicharana Shala, IIT Ropar)

- **16 openers**, `#mod-0` + `#mod-A` … `#mod-O` (0 + A-O = 16).
- 150+ questions `#q-{n}` each with a `<details>` worked SOLUTION `#q-{n}-solution`; 8 linked projects `#project-1` … `#project-8`, index `#projects`.
- `site_rule = "Strictly use GeoGebra"` → the RULE `.rule-banner` renders once at top and repeats compactly in each project; GeoGebra embeds use the 16:9 wrapper preceded by the RULE callout.
- HEAVY math: matrices (`bmatrix`), vectors (`pmatrix`), null/column space, eigenvectors, sigmoid, convolution, gradient descent — all authored as `$…$`/`$$…$$`, pre-rendered by KaTeX (screen + WeasyPrint). Display equations step to h4 max and `overflow-x:auto` rather than break the measure.
- Cover lead accent = **petrol #005863** (stays in-kit; only the lead role swaps).

---

## Appendix A — Load-bearing constants (regression self-checks; MUST hold)

```
144/16 = 9            34/16 = 2.125        89/16 = 5.5625
55/34 = 1.618         233/144 = 1.618
1200 - 1200/φ = 458   1200/φ = 742
38/φ = 23.485         38 - 38/φ = 14.515 = 38/φ²
890/φ² = 339.95px     (challenge_card.py line 637 rendered accent — unchanged)
100/φ = 61.8 ; 38.2/φ = 23.6 ; 38.2 - 38.2/φ = 14.6   (nested golden cut)
√φ = 1.2720196495 ; √φ² = φ = 1.6180339887
11 × 1.4545 = 16pt (print leading) ; 11/√φ = 8.6pt (print code = caption)
```

---

# BCS v1.1 Addenda — Implementation-Completeness Layer

**Status: Normative.** This document is the completeness layer on top of the ratified **BCS v1.0** (`BOOK_COMPILATION_STANDARD.md`). MUST / MUST NOT are binding. It **reuses** the frozen v1.0 golden-ratio system and brandkit unchanged: `--phi` (1.6180339887), `--sqrt-phi` (1.2720196495), `--fib-*` (21/34/55/89/144/233), `--measure` 38rem, `--accent-rule` 14.515rem (= measure/φ²), print block 157.6×255.1mm, print ink `#212529`, colour-area 61.8:23.6:14.6. It does **NOT** re-derive any of these and does **NOT** alter `challenge_card.py` line 637 (verified: `d.line([(M, y), (M + Golden.seg(cw) / PHI, y)], fill=D["red"], width=6)`).

Where v1.1 amends a v1.0 §8 detail, it says so explicitly (§B.1) so there is **one** source of truth.

---

## §0 Verified repo baseline (why these addenda are shaped this way)

Confirmed against the working tree so no instruction is a hand-wave:

- `requirements.txt` = Flask 3.0.0, Flask-SQLAlchemy 3.1.1, Flask-Migrate 4.0.5, gunicorn 21.2.0, python-dotenv 1.0.0, **markdown==3.5.1**, requests 2.31.0. (7 lines.)
- Markdown is rendered in **`models.py`**, NOT `app.py`. Four call sites: `problem_html` (L74), `concepts_html` (L78), `qa_html` (L82), `display_description_html` (L95–99, which short-circuits to raw `fcc_description`). **All filePlan edits target `models.py`, not `app.py`.**
- `templates/books/` and `static/books/` and `static/vendor/` **do NOT exist** — they are `new`, not `edit`.
- `static/css/style.css` (369 lines) contains **zero** BCS v1.0 tokens, **no** `:root` golden block, **no** `@media print`, **no** `.reader/.opener/.unit/.book-*` shell. Building the v1.0 reader-shell CSS + `:root` token block is a **hard blocking prerequisite** for every CSS rule below (§E.1).
- `book_generator.py` has a hardcoded Windows `BOOKS_DIR` and only writes a stub — must be rewritten (§A.6).
- `challenge_card.py`: `Golden.seg(length)` returns `length / PHI` (L213–215 docstring "golden (shorter) segment"); line 637 divides `seg(cw)` by PHI **again** → `cw/φ²`. The **stale comment at L33** reads "Accent rule lengths = block / phi" — MUST be corrected to `block / phi²` (§E.6).
- `auto_deploy.sh`: 102 lines. Step-2 clobber guard is `git diff --quiet -- ':!static/images'` (L54). The pip step is labeled **"# 4"** at L86 (there is no "step 3" data block at that point). `git reset --hard` at L77 preserves untracked files. Vars `PORTFOLIO_DIR`, `LOG_FILE`, `log()` exist.
- `.gitignore` has **no** entries for `static/books/qa/`, `static/vendor/`, or `node_modules/` — these MUST be added (§F.4, §E.8).
- `base.html`: loads Bootstrap CSS (L16), Bootstrap-Icons (L19), Google Fonts Crimson 400/600/700+400i · Libre Franklin 300/400/500/700/900 · JetBrains Mono 400/500 (L23), `style.css` (L27), `{% block extra_css %}` (L29), Bootstrap JS bundle (L94), `{% block extra_js %}` (L96). The environment is **not** framework-free (Bootstrap is global); "dependency-free" applies only to `book.js`.

---

## A. Content authoring & markdown pipeline

### A.1 One frozen renderer (SSOT) in `models.py`

All book Markdown → HTML goes through **one** helper, `render_book_md()`, added to `models.py`. This closes the "no extensions" gap and unifies the authoring + math + highlighting tracks into a single extension list (the three tracks proposed conflicting lists; this is the reconciled one).

```python
# models.py — add after `import markdown`
import markdown

# ── FROZEN BCS v1.1 book-rendering extension set. Editing this is a BCS revision. ──
def _book_output_fence(source, language, css_class, options, md, **kwargs):
    esc = source.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return '<pre class="book-output"><samp>' + esc + "</samp></pre>"

def _book_repl_fence(source, language, css_class, options, md, **kwargs):
    esc = source.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return '<pre class="book-output book-output--repl"><samp>' + esc + "</samp></pre>"

def _inline_md(text):
    """Convert inline markdown WITHOUT re-entering the live parser (fresh instance,
    minimal exts). Python-Markdown instances are stateful/non-reentrant."""
    return markdown.Markdown(extensions=["attr_list"]).convert(text.strip())

def _book_figure_fence(source, language, css_class, options, md, **kwargs):
    lines = source.strip().split("\n", 1)
    src_path = lines[0].strip()
    caption = _inline_md(lines[1]) if len(lines) > 1 else ""
    fig_id = options.get("id", "")
    id_attr = f' id="{fig_id}"' if fig_id else ""
    return (f'<figure class="book-figure"{id_attr}>'
            f'<img src="{src_path}" alt="{options.get("alt","")}">'
            f'<figcaption class="book-figure__caption">{caption}</figcaption></figure>')

def _rule_banner_fence(source, language, css_class, options, md, **kwargs):
    return '<aside class="rule-banner" role="note">' + _inline_md(source) + "</aside>"

BOOK_MD_EXTENSIONS = [
    "pymdownx.superfences",   # code + custom output/figure/rule fences
    "pymdownx.highlight",     # class-only token spans, use_pygments controlled below
    "pymdownx.arithmatex",    # math source protection (generic mode)
    "tables",
    "attr_list",              # {: #q-3 .question } and figure fence opts
    "md_in_html",             # <details markdown> inner parse
    "admonition",             # STOCK python-markdown ext — NOT pymdownx.admonition
    "toc",
    "sane_lists",
]
BOOK_MD_CONFIGS = {
    "pymdownx.highlight": {"use_pygments": True, "guess_lang": False, "css_class": "bcs-hl"},
    "pymdownx.superfences": {
        "css_class": "book-code",
        "disable_indented_code_blocks": True,
        "custom_fences": [
            {"name": "output", "class": "book-output", "format": _book_output_fence},
            {"name": "repl",   "class": "book-output", "format": _book_repl_fence},
            {"name": "figure", "class": "book-figure", "format": _book_figure_fence},
            {"name": "rule",   "class": "rule-banner", "format": _rule_banner_fence},
        ],
    },
    "pymdownx.arithmatex": {
        "generic": True, "smart_dollar": True, "block_tag": "div",
        "tex_inline_wrap": ["\\(", "\\)"], "tex_block_wrap": ["\\[", "\\]"], "preview": False,
    },
    "toc": {"permalink": False},
    "admonition": {},
}

def render_book_md(text: str) -> str:
    """The ONE place book Markdown becomes HTML (BCS v1.1). Fresh, non-reentrant
    Markdown instance per call. Math placeholders are baked to KaTeX in the
    build step (katex_prerender.render), NOT here — see §B."""
    if not text:
        return ""
    md = markdown.Markdown(extensions=BOOK_MD_EXTENSIONS, extension_configs=BOOK_MD_CONFIGS)
    return md.convert(text)
```

**Corrections folded in (from reviewer issues):**
- **`admonition`, NOT `pymdownx.admonition`** — the latter does not exist in pymdown-extensions and crashes on first call. Verified stock `admonition` produces `<div class="admonition tip"><p class="admonition-title">Tip</p>…</div>`.
- Custom-fence formatters use a **fresh `_inline_md()`** instance, never the live `md.convert()` (non-reentrant corruption fix).
- `use_pygments: True` with `css_class:"bcs-hl"` — the highlighting track (§C) owns the token→colour map. This supersedes the authoring track's earlier `use_pygments:false` (a cross-track conflict; highlighting wins because §C requires token spans).
- **Markdown floor pinned**: `markdown>=3.5,<4` (repo has 3.5.1; pymdown-extensions 10.9 requires ≥3.5). See master requirements.

### A.2 The four call sites

Rewrite in `models.py`:

```python
    @property
    def problem_html(self):  return render_book_md(self.problem_text)
    @property
    def concepts_html(self): return render_book_md(self.concepts_text)
    @property
    def qa_html(self):       return render_book_md(self.qa_text)
    @property
    def display_description_html(self):
        # FCC ships pre-rendered HTML — sanitize-passthrough, NOT re-rendered.
        if self.fcc_description:
            return _sanitize_fcc(self.fcc_description)   # §A.7
        return render_book_md(self.problem_text)
```

**SSOT is redefined precisely** (resolving the reviewer's "two paths" objection): *`render_book_md` is the ONE Markdown→HTML path; FCC HTML is a separate sanitize-passthrough path.* `grep -rn "markdown.markdown(" .` MUST return zero hits outside `models.py`. Templates (`home.html` L76/L109, `challenge_detail.html` L50) that currently emit `fcc_description | safe` directly MUST be changed to call `display_description_html` so the fcc-vs-markdown precedence lives in exactly one property.

### A.3 Authoring conventions (normative — the ONLY sanctioned markup)

- **Callouts** — `!!! tip "Tip"` / `note` / `warning` (indent body 4 spaces).
- **RULE banner** — the ```` ```rule ```` fence → `<aside class="rule-banner" role="note">`. LA `site_rule="Strictly use GeoGebra"`; Python omits it.
- **Question + solution** — anchors FIXED by v1.0:

  ````markdown
  ### Question 3 {: #q-3 .question .unit }

  Prompt with $inline$ math.

  <span class="question__badge">Q3</span>

  <details class="solution" id="q-3-solution" markdown>
  <summary>Solution</summary>

  Worked solution.
  </details>
  ````

  **Use `<summary>Solution</summary>`, NOT `#### Solution`** — this fixes the reviewer's duplicate-`id="solution"` collision across 150+ questions (a heading under `toc` would emit `id="solution"` on every one). `<summary>` gets no auto-id.
- **Figure** — ```` ```figure {id="fig-1" alt="shear diagram"} ```` , first line = path under `static/books/`, rest = caption. **`alt` is REQUIRED** (R040 gate).
- **Output / REPL** — use the **custom fences** ```` ```output ```` and ```` ```repl ````, NOT ` ```text {.output} `. Reviewer verified `text {.output}` is not recognized as a fence and `attr_list` does not move attrs onto `<pre>`. The custom fences emit `<pre class="book-output"><samp>…</samp></pre>` and `…book-output--repl…` deterministically.
- **Source code** — ```` ```python ```` → `<pre class="book-code"><code class="language-python">…</code></pre>` with Pygments token spans.
- **Math** — `$…$` / `$$…$$`. **Display math (`$$…$$` / `\[…\]`) MUST be on its own line, separated by blank lines**, so arithmatex emits a standalone `<div class="arithmatex">` block sibling — never nested inside a `<p>` (fixes the invalid `<div>`-in-`<p>` nesting the v1.0 proof showed). Authors MUST NOT hand-write `\(` delimiters.

### A.4 Why arithmatex `generic` mode (source protection)

In `generic` mode arithmatex tokenizes `$...$`, `$$...$$`, `\(...\)`, `\[...\]`, `\begin{env}…\end{env}` **before** the em/escape treeprocessors run and emits inert wrappers with the TeX payload stored verbatim. Guarantees `$a_i$` → subscript (not `<em>`), `\begin{bmatrix} a & b \\ c & d \end{bmatrix}` keeps backslashes/braces (`&` is HTML-escaped and undone before KaTeX, §B.2).

### A.5 Deterministic numbering & anchors + build validator

Anchors: `#ch-{n}` (Python 0–8) / `#mod-{ID}` (LA: `0` then `A..O`) / `#ch-{n}-lesson-{m}` / `#q-{n}` (non-padded, 1..N) / `#q-{n}-solution` / `#projects` / `#project-{k}` (1..8). The book generator (§A.6) MUST run a validator that asserts: (a) question numbers contiguous 1..N no gaps/dupes; (b) every `<details class="solution" id="q-{k}-solution">` has a matching `#q-{k}`; (c) module IDs unique and from the fixed set. **Actual validator code is shipped** (not just specified) in `book_generator.py`:

```python
import re
def validate_anchors(html: str, book: str) -> list[str]:
    errs = []
    qs = sorted(int(m) for m in re.findall(r'id="q-(\d+)"', html))
    if qs and qs != list(range(1, qs[-1] + 1)):
        errs.append(f"question numbers not contiguous 1..N: {qs}")
    if len(qs) != len(set(qs)):
        errs.append("duplicate question ids")
    sols = set(re.findall(r'id="q-(\d+)-solution"', html))
    for s in sols:
        if f'id="q-{s}"' not in html:
            errs.append(f"orphan #q-{s}-solution with no #q-{s}")
    allowed = {"0"} | set("ABCDEFGHIJKLMNO") if book == "linear-algebra" else set("012345678")
    mods = re.findall(r'id="(?:mod|ch)-([0-9A-O]+)"', html)
    for mid in mods:
        if mid not in allowed:
            errs.append(f"module/chapter id '{mid}' not in fixed set for {book}")
    if len(mods) != len(set(mods)):
        errs.append("duplicate module/chapter ids")
    return errs
```

### A.6 `book_generator.py` rewrite

Replace the hardcoded `BOOKS_DIR = r"c:\Users\NISHAN\..."` with a repo-relative path `os.path.join(os.path.dirname(__file__), "templates", "books")`. Import `render_book_md` from `models` (no second extension list). Pipe body through `render_book_md` → `wrap_code_blocks` (§C.2) → `katex_prerender.render` (§B) → `validate_anchors` (fail build on any error) → write into `{% block content %}` of `templates/books/<token>.html`.

### A.7 FCC sanitization (security)

Because `attr_list` + `md_in_html` are enabled over authored content that flows through `{{ html | safe }}`, and FCC HTML is injected raw, add **`nh3`** (Rust `ammonia` binding, prebuilt wheels, no native build) sanitization for the FCC passthrough path:

```python
import nh3
_ALLOWED_TAGS = {"p","br","pre","code","em","strong","ul","ol","li","a","h1","h2","h3","h4","blockquote","table","thead","tbody","tr","th","td","span","div","details","summary","figure","figcaption","img","aside","samp","sup","sub"}
def _sanitize_fcc(html: str) -> str:
    return nh3.clean(html, tags=_ALLOWED_TAGS, link_rel="noopener noreferrer")
```

Authored book Markdown is trusted (author-controlled), so `render_book_md` output is not re-sanitized, but `javascript:` URIs and `<script>` are impossible from the frozen extension set.

---

## B. Math pipeline & print-PDF math fidelity

### B.1 AMENDS BCS v1.0 §8 (explicit, single source of truth)

BCS v1.0 §8 referenced `CSS("static/vendor/katex.min.css")` with `base_url="static/"`. **BCS v1.1 relocates** the KaTeX CSS to `static/vendor/katex/katex.min.css` + `static/css/book_math.css`, and feeds WeasyPrint via the **`CSS()` stylesheets list with `base_url` set so `static/` is the base** (the reliable WeasyPrint path — NOT template `<link>` tags). This resolves the reviewer's base_url contradiction and the "which CSS feeds WeasyPrint" ambiguity. All `@font-face` `src` URLs are written **relative to `static/`** as `url("vendor/katex/fonts/…woff2")` — **no `../`** (the double-nesting `static/vendor/vendor/…` bug is thereby eliminated).

### B.2 Single render path: `katex_prerender.render()` via build-time Node `katex` CLI

There is **no** correct pure-Python KaTeX; Node `katex` is the reference implementation. It is a **build-time-only** dependency — it runs once when generating the book HTML, never in the request path and never inside WeasyPrint (so the shipped PDF and served page contain zero JS). This reconciles the assets track's incorrect "arithmatex generic=False emits MathML" claim (it does not — both arithmatex modes need JS) with the math track's correct CLI approach.

```python
# katex_prerender.py — single build-time math render path (no client JS)
import subprocess, re, os
_KATEX_BIN = os.environ.get("KATEX_BIN",
    os.path.join(os.path.dirname(__file__), "node_modules", ".bin", "katex"))
_INLINE_RE  = re.compile(r'<span class="arithmatex">\\\((.*?)\\\)</span>', re.S)
_DISPLAY_RE = re.compile(r'<div class="arithmatex">\\\[(.*?)\\\]</div>',   re.S)

def _unescape(s: str) -> str:
    return s.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")

def _katex(tex: str, display: bool) -> str:
    if not os.path.exists(_KATEX_BIN):
        raise RuntimeError(f"katex CLI missing at {_KATEX_BIN}; run `npm ci`")
    args = [_KATEX_BIN, "--no-throw-on-error"]     # --trust omitted (boolean; no 'false' positional)
    if display:
        args.append("--display-mode")
    proc = subprocess.run(args, input=tex, capture_output=True, text=True,
                          encoding="utf-8", timeout=20)
    if proc.returncode != 0:
        raise RuntimeError(f"KaTeX render failed: {proc.stderr.strip()} | TeX={tex!r}")
    return proc.stdout.strip()

def render(html: str) -> str:
    """html (post-markdown, .arithmatex placeholders) -> final KaTeX HTML.
    Idempotent when no .arithmatex nodes remain. Raises on any TeX error."""
    html = _DISPLAY_RE.sub(lambda m: '<div class="katex-display-wrap">'
                           + _katex(_unescape(m.group(1)), True) + "</div>", html)
    html = _INLINE_RE.sub(lambda m: _katex(_unescape(m.group(1)), False), html)
    return html
```

**Corrections folded in:**
- `_KATEX_BIN` defaults to the **absolute `./node_modules/.bin/katex`** (no ambiguous `npx OR …`); build **fails loud** if missing, never falls back to network `npx`.
- **`--trust` removed** — it is a boolean flag; passing `["--trust","false"]` leaves a stray `false` positional the CLI rejects. Verified form is `[bin, "--no-throw-on-error", ("--display-mode")]`.
- `_unescape` order is `&lt;`/`&gt;` **before** `&amp;` (documented low-risk on literal `&amp;` in TeX, which does not occur in matrix math).
- `render()` MUST be called **exactly once per book** (from `book_generator.py`, reused verbatim for both screen storage and WeasyPrint input — screen==PDF by construction). Optional single-process batching is PERMITTED if byte-identical.

### B.3 Wide-equation behavior — uniform CSS fallback (per-equation `data-fit` REMOVED)

The reviewer proved the `data-fit` scheme is unbuildable: the KaTeX CLI emits **no reliable pixel width** for the whole display block (widths derive from font metrics resolved only by a layout engine). **v1.1 drops per-equation `data-fit` entirely** and uses one deterministic CSS fallback: any `.katex-display` that would exceed the 157.6mm block shrinks uniformly via `max-width` + a single golden-derived floor scale. Screen keeps `overflow-x:auto`. The mislabeled magic numbers (0.85, 0.72) are gone.

```css
/* static/css/book_math.css — screen */
.reader .katex-display{max-width:100%;overflow-x:auto;overflow-y:hidden;-webkit-overflow-scrolling:touch;
  margin-block:var(--fib-34,34px);font-size:var(--fs-h4)}   /* display sized at h4 step, never exceeds it */
.reader .katex{font-size:1em}                                /* inline math = body size */

/* print — uniform shrink-to-fit, golden floor 1/phi */
@media print{
  .reader .katex-display{max-width:var(--textblock-w);overflow:visible;transform-origin:left center}
  .reader .katex-display.is-wide{transform:scale(0.618)}     /* 1/phi hard floor, golden-tied */
}
```

`book_generator.py` marks a display block `is-wide` only when a **real measurement** is available: it runs a throwaway WeasyPrint layout of the standalone `.katex-display` at build time and reads the resulting box width vs the 157.6mm block (157.6/25.4×96 = 595.6 CSS px). If a formula still exceeds the block at `scale(0.618)`, the **build fails** with a clear message (authoring error). If the throwaway-measure step is not run, no equation is marked `is-wide` and screen `overflow-x` remains the only fallback — deterministic either way, no undefined parse.

### B.4 KaTeX fonts embedded for WeasyPrint

All ~20 KaTeX woff2 vendored under `static/vendor/katex/fonts/` (version-matched to CLI): `KaTeX_Main-Regular/Bold/Italic/BoldItalic`, `KaTeX_Math-Italic/BoldItalic`, `KaTeX_AMS-Regular`, `KaTeX_Caligraphic-Regular/Bold`, `KaTeX_Fraktur-Regular/Bold`, `KaTeX_SansSerif-Regular/Bold/Italic`, `KaTeX_Script-Regular`, `KaTeX_Size1-Regular`…`KaTeX_Size4-Regular`, `KaTeX_Typewriter-Regular`. `Size1–4` supply `bmatrix`/`pmatrix` delimiters — all four REQUIRED or brackets are tofu. `@font-face` block in `book_math.css` (relative to `static/`, no `../`):

```css
@font-face{font-family:"KaTeX_Main";src:url("vendor/katex/fonts/KaTeX_Main-Regular.woff2") format("woff2");font-weight:normal;font-style:normal}
@font-face{font-family:"KaTeX_Main";src:url("vendor/katex/fonts/KaTeX_Main-Bold.woff2") format("woff2");font-weight:bold}
@font-face{font-family:"KaTeX_Main";src:url("vendor/katex/fonts/KaTeX_Main-Italic.woff2") format("woff2");font-style:italic}
@font-face{font-family:"KaTeX_Math";src:url("vendor/katex/fonts/KaTeX_Math-Italic.woff2") format("woff2");font-style:italic}
@font-face{font-family:"KaTeX_AMS";src:url("vendor/katex/fonts/KaTeX_AMS-Regular.woff2") format("woff2")}
@font-face{font-family:"KaTeX_Size1";src:url("vendor/katex/fonts/KaTeX_Size1-Regular.woff2") format("woff2")}
@font-face{font-family:"KaTeX_Size2";src:url("vendor/katex/fonts/KaTeX_Size2-Regular.woff2") format("woff2")}
@font-face{font-family:"KaTeX_Size3";src:url("vendor/katex/fonts/KaTeX_Size3-Regular.woff2") format("woff2")}
@font-face{font-family:"KaTeX_Size4";src:url("vendor/katex/fonts/KaTeX_Size4-Regular.woff2") format("woff2")}
@font-face{font-family:"KaTeX_Caligraphic";src:url("vendor/katex/fonts/KaTeX_Caligraphic-Regular.woff2") format("woff2")}
@font-face{font-family:"KaTeX_Fraktur";src:url("vendor/katex/fonts/KaTeX_Fraktur-Regular.woff2") format("woff2")}
@font-face{font-family:"KaTeX_SansSerif";src:url("vendor/katex/fonts/KaTeX_SansSerif-Regular.woff2") format("woff2")}
@font-face{font-family:"KaTeX_Script";src:url("vendor/katex/fonts/KaTeX_Script-Regular.woff2") format("woff2")}
@font-face{font-family:"KaTeX_Typewriter";src:url("vendor/katex/fonts/KaTeX_Typewriter-Regular.woff2") format("woff2")}
```

`make_book_pdf.py` MUST call `weasyprint.HTML(string=html, base_url=os.path.dirname(app.static_folder))` so `static/` is the base, and pass stylesheets via `stylesheets=[CSS("static/vendor/katex/katex.min.css"), CSS("static/css/book_math.css"), CSS("static/css/print.css")]`. No network fetch. KaTeX math text keeps KaTeX fonts by design; body prose stays Crimson Text.

### B.5 No-JS guarantee (grep gate in `make_book_pdf.py`)

The stored/served HTML == WeasyPrint input (empty diff) and MUST NOT match `katex\.js|auto-render|MathJax|arithmatex`. If it does, `make_book_pdf.py` exits non-zero (proves markdown+prerender consumed every placeholder). `contrib/auto-render.js` and `katex.js` MUST NOT be loaded anywhere.

---

## C. Syntax highlighting & output component

### C.1 Server-side Pygments (class-only), reader namespace

`pymdownx.highlight` with `use_pygments: True`, `guess_lang: False`, `css_class: "bcs-hl"` (§A.1) emits `<div class="bcs-hl"><pre>…<span class="k">…</span></pre></div>` — **note: `bcs-hl` REPLACES `highlight`; the wrapper is `<div class="bcs-hl">`, NOT `bcs-hl highlight`** (reviewer-verified; acceptance checks assert the actual class). No Pygments-generated stylesheet; colours come only from the hand-authored token map. No client highlighter — Prism/highlight.js would be blank in WeasyPrint.

**Correct Pygments Python token classes** (reviewer-verified): `None`/`True`/`False` → `kc`; `and`/`or`/`in`/`not` → `ow`; builtins `print`/`len` → `nb`; func name → `nf`; strings → `s s1 s2 sb`; comments → `c c1 cm`; numbers → `mi mf`. A leading empty `<span></span>` and `.w` whitespace class are inert.

### C.2 Language tab wrapping (one normative method)

The "inline wrap OR Jinja post-filter" fork is resolved: **a defined post-render pass** wraps each `div.bcs-hl` node in `<figure class="book-code" data-lang="PYTHON">`, because one Markdown string yields N code blocks. Use `selectolax` (already a dependency):

```python
from selectolax.parser import HTMLParser
def wrap_code_blocks(html: str) -> str:
    tree = HTMLParser(html)
    for div in tree.css("div.bcs-hl"):
        code = div.css_first("code")
        lang = "PYTHON"
        if code:
            for c in (code.attributes.get("class") or "").split():
                if c.startswith("language-"):
                    lang = c[len("language-"):].upper()
        div.insert_before(f'<figure class="book-code" data-lang="{lang}">')
        div.insert_after("</figure>")
    return tree.html
```

This runs in `book_generator.py` **after** `render_book_md` and **before** `katex_prerender.render`. The green uppercase tab is a pure-CSS `::before` on `[data-lang]` (no JS).

### C.3 CSS token→colour map + dark/print variants

Added to `style.css` **after** the BCS `:root` token block (§E.1 prerequisite). Uses only brandkit hex; radius 0/2px; no shadows.

```css
:root{
  --code-bg:#212529; --code-kw:#78beff; --code-fn:#f0c878; --code-arg:#e68c8c;
  --code-str-dark:#4ec9a0;              /* AA-safe green on #212529 (was #007a3d, FAIL 3.9:1) */
  --code-comment:#6b7785; --code-txt:#e2e8f0;
  --code-bg-print:#f5f7f9; --code-ink-print:#212529;
}
.book-code{position:relative;margin:var(--fib-34,34px) 0;max-width:var(--measure,38rem);border-radius:2px}
.book-code::before{content:attr(data-lang);position:absolute;top:0;left:0;transform:translateY(-100%);
  background:#007a3d;color:#fff;font-family:var(--font-sans,"Libre Franklin"),sans-serif;font-weight:600;
  text-transform:uppercase;letter-spacing:.12em;font-size:.68rem;line-height:1;padding:.34rem .55rem;border-radius:2px 2px 0 0}
.book-code .bcs-hl,.book-code pre{margin:0;background:var(--code-bg);color:var(--code-txt);border-radius:0 2px 2px 2px}
.book-code pre{padding:var(--fib-21,21px);overflow-x:auto;font-family:var(--font-mono,"JetBrains Mono"),monospace;
  font-size:.82rem;line-height:1.5;tab-size:4}
.book-code code{background:transparent;color:inherit;padding:0}
.book-code .k,.book-code .kn,.book-code .kd,.book-code .kc,.book-code .kr,.book-code .bp,.book-code .ow{color:var(--code-kw)}
.book-code .nf,.book-code .fm,.book-code .nb,.book-code .nn,.book-code .nc,.book-code .nd{color:var(--code-fn)}
.book-code .s,.book-code .s1,.book-code .s2,.book-code .sb,.book-code .se,.book-code .sd{color:var(--code-str-dark)}
.book-code .c,.book-code .c1,.book-code .cm,.book-code .ch{color:var(--code-comment);font-style:italic}
.book-code .mi,.book-code .mf,.book-code .mh,.book-code .il{color:var(--code-arg)}
.book-code .o,.book-code .p,.book-code .n,.book-code .nv,.book-code .nx{color:var(--code-txt)}
.book-code .err{color:#a70e13}

@media print{
  .book-code::before{background:#007a3d;color:#fff;print-color-adjust:exact}
  .book-code .bcs-hl,.book-code pre{background:var(--code-bg-print);color:var(--code-ink-print);
    border:1px solid #ebebeb;print-color-adjust:exact}
  .book-code{break-inside:avoid}
  .book-code .k,.book-code .kn,.book-code .kd,.book-code .kc,.book-code .kr,.book-code .bp,.book-code .ow{color:#005a7d}
  .book-code .nf,.book-code .fm,.book-code .nb,.book-code .nn,.book-code .nc,.book-code .nd{color:#b06400}
  .book-code .s,.book-code .s1,.book-code .s2,.book-code .sb,.book-code .se,.book-code .sd{color:#007a3d}
  .book-code .c,.book-code .c1,.book-code .cm,.book-code .ch{color:#666}
  .book-code .mi,.book-code .mf,.book-code .mh,.book-code .il{color:#a70e13}
  .book-code .o,.book-code .p,.book-code .n,.book-code .nv,.book-code .nx{color:#212529}
}
```

**`--code-str` `#007a3d` on `#212529` is 3.9:1 = AA FAIL → replaced by `--code-str-dark #4ec9a0` (≈7.3:1)** on the dark screen theme. Print theme keeps `#007a3d` on light `#f5f7f9` (passes). This is a legibility-corrected shade of the existing green role, not a new brand hue.

### C.4 Output / REPL panel (light, distinct)

Emitted by the custom `output`/`repl` fences (§A.1/A.3) — `<pre class="book-output"><samp>…` and `…book-output--repl…`. CSS:

```css
.book-output{max-width:var(--measure,38rem);margin:var(--fib-21,21px) 0 var(--fib-34,34px);
  background:#f8f9fa;color:#212529;border:1px solid #ebebeb;border-left:3px solid #666;
  border-radius:0 2px 2px 0;padding:var(--fib-21,21px);font-family:var(--font-mono,"JetBrains Mono"),monospace;
  font-size:.82rem;line-height:1.5;overflow-x:auto;white-space:pre-wrap;word-break:break-word}
.book-output::before{content:"OUTPUT";display:block;font-family:var(--font-sans,"Libre Franklin"),sans-serif;
  font-weight:600;text-transform:uppercase;letter-spacing:.12em;font-size:.62rem;color:#666;margin-bottom:.5rem}
.book-output--repl{border-left-color:#005863}          /* petrol spine = REPL */
.book-output--repl::before{content:"PYTHON REPL"}
@media print{.book-output{break-inside:avoid;print-color-adjust:exact}}
```

Source = dark card + green PYTHON tab; output = light `#f8f9fa` + neutral/petrol spine + label — separable even at grayscale.

### C.5 Version pins reconciled

Pin `markdown>=3.5,<4` and `Pygments==2.18.0` together (see master requirements). Acceptance render was validated against this pair; do not ship checks validated on a different set.

---

## D. Reader JavaScript (`static/js/book.js`)

### D.1 Loading contract + window-scroll normative statement

Add `{% block reader_js %}{% endblock %}` immediately after `{% block extra_js %}` (base.html L96). Reader templates override it with `<script defer src="{{ url_for('static', filename='js/book.js') }}">`. Non-reader pages MUST NOT load it. `book.js` early-returns when `document.querySelector(".reader")` is null.

**NORMATIVE (resolves scroll-container ambiguity):** on reader pages the **window/document is the scroll port** — content is normal flow; the `.reader` shell CSS (§E.1) MUST NOT introduce an inner `overflow:auto` reading pane. This makes `documentElement.scrollTop` and the default IntersectionObserver root correct.

**NORMATIVE (DOM contract):** `.book-toc` MUST have `id="book-toc"` (fixed) so `aria-controls` always resolves. TOC links MUST carry `data-crumbs` (promoted SHOULD→MUST) so the breadcrumb acceptance check is satisfiable.

### D.2 `book.js` corrections folded in

The v1.0 IIFE is adopted with these binding fixes:

- **`beforePrint()` double-fire guard** (Chromium fires both `beforeprint` and `matchMedia('print')`): `function beforePrint(){ if (printState) return; printState = solutions.map(d=>d.open); solutions.forEach(d=>d.open=true); }` — prevents the second snapshot from capturing all-open state and permanently losing the user's collapsed state.
- **MediaQueryList listener feature-detect** for both `mqPrint` and `mqNarrow` (old Safari — the exact fallback target — lacks `addEventListener('change')`): `if (mq.addEventListener) mq.addEventListener("change",fn); else mq.addListener(fn);`.
- **`inert` CSS fallback**: since no polyfill is loaded, the deferred `.reader` shell CSS MUST also hide the closed off-canvas TOC via `visibility:hidden;pointer-events:none` (belt-and-braces for no-`inert` browsers). Declared as a MUST on the CSS track (§E.1).
- **`currentUnitIndex()` sibling robustness**: after the id/descendant check, also test `document.getElementById(anchor)?.closest(".unit,.opener") === units[i]` so Prev/Next stays consistent with the scrollspy `.active` item.
- **Progress on programmatic jumps**: call `updateProgress()` inside the IO callback and after `scrollIntoView`.

All other v1.0 behaviors stand: one IntersectionObserver scrollspy (exactly one `.active`, `aria-current`), rAF-throttled progress width, wrapping unit prev/next with `aria-disabled` at ends (never HTML `disabled`), <992px off-canvas drawer, expand/collapse-all, force-open solution on deep-link + before print.

### D.3 PDF correctness is CSS, not JS

WeasyPrint runs no JS. `@media print` in the reader stylesheet is the **source of truth** for open solutions — force all `<details>` content visible regardless of the `open` attribute:

```css
@media print{ .reader details.solution:not([open]) > :not(summary){ display:block } }
```

JS `beforeprint` only helps the browser's own "Save as PDF"; it is never relied on for the WeasyPrint PDF.

### D.4 Scope note

`book.js` does NOT satisfy KaTeX-font embedding (§B.4), math-mangling prevention (§A.4), screen==PDF math (§B), or the readability gate (§F). Those are owned by their respective sections; this track's acceptance MUST NOT be read as covering them.

---

## E. Assets, deps, fonts, GeoGebra, token cleanups

### E.1 HARD PREREQUISITE: the BCS v1.0 `:root` token block + reader shell

Verified absent from `style.css`. Before any CSS in §B/§C/§E lands, `style.css` MUST first contain the v1.0 `:root` golden tokens (`--phi`, `--sqrt-phi`, `--fib-21..233`, `--measure`, `--accent-rule`, `--textblock-w`, font stacks), the `@media print` block, and the `.reader/.opener/.unit/.book-*` reader-shell rules (including the `inert` visibility fallback of §D.2 and the window-scroll no-inner-pane rule of §D.1). The `var(--fib-34,34px)` fallbacks in §B/§C/§E CSS are safety nets, NOT the shipping values. `book_cover.py` (v1.0 cover/opener PIL generator) is likewise a prerequisite for cover images.

### E.2 Self-hosted brand fonts (screen + PDF)

`static/vendor/fonts/` with 11 woff2 (exact weights matching base.html L23): `crimson-text-400/-400-italic/-600/-700`, `libre-franklin-300/-400/-500/-700/-900`, `jetbrains-mono-400/-500`, plus `LICENSES.md` (full SIL OFL 1.1 + per-family attribution + Reserved Font Names; do not rename files past a Reserved Font Name). One `@font-face` block at the TOP of `style.css` (before `:root`), paths as `/static/vendor/fonts/…woff2`. **`font-display:swap` removed** (no effect in synchronous WeasyPrint render; harmless-but-misleading). Google Fonts `<link>` becomes an optional screen-only fallback and MAY be removed for a pure self-host build; WeasyPrint MUST NOT rely on it. `challenge_card.py` PIL fonts are a separate path, out of scope.

**Pin the download** (kills the hand-wave): fetch via `gwfh.mranftl.com` with `subset=latin&formats=woff2` for each family/weight, or the upstream OFL release tag. Ship step verifies each file opens as a valid font: `python -c "from fontTools.ttLib import TTFont; TTFont('static/vendor/fonts/crimson-text-400.woff2')"` for each (fonttools is a WeasyPrint transitive dep).

### E.3 GeoGebra print fallback (data-plumbed)

Each construction supplies `ggb_png` (path under `static/books/<token>/ggb/`, PNG exported at 2×, **exactly ~1.618:1**) + `interactive_url`. **Data source defined**: a per-book `constructions` list (Python dict list in the book source module or front-matter parsed by `book_generator.py`), iterated by the template. Jinja partial `templates/books/_geogebra.html` with the **missing-image conditional implemented** (fixes the reviewer's contradiction):

```html
<figure class="ggb-embed">
  <iframe class="ggb-live" src="{{ interactive_url }}" title="{{ caption }}" loading="lazy"></iframe>
  {% if ggb_png %}
    <img class="ggb-static" src="{{ url_for('static', filename=ggb_png) }}" alt="{{ caption }}">
  {% else %}
    <p class="ggb-fallback">Interactive construction — view online: {{ interactive_url }}</p>
  {% endif %}
  <figcaption class="ggb-caption">{{ caption }}
    <a class="ggb-online" href="{{ interactive_url }}">View interactive online</a>
  </figcaption>
</figure>
```

```css
.ggb-embed .ggb-static{display:none}
.ggb-embed .ggb-live{width:100%;aspect-ratio:1.618/1;border:1px solid var(--border,#ebebeb)}
@media print{
  .ggb-embed .ggb-live{display:none !important}
  .ggb-embed .ggb-static{display:block;width:100%;max-width:var(--textblock-w);aspect-ratio:1.618/1;object-fit:contain}
  .ggb-embed .ggb-online{display:inline}
}
```

`aspect-ratio` is now on the **print `.ggb-static` too** (fixes screen/print reflow mismatch). MUST NOT ship a construction with neither image nor URL.

### E.4 Math dependencies (reconciled — supersedes assets track's arithmatex-MathML error)

The assets track's `pymdownx.arithmatex generic=False → MathML` is **rejected**: arithmatex emits no MathML; both modes need JS. The math pipeline is §B (build-time Node `katex` CLI + vendored fonts). No `katex` pip package exists and none is added. KaTeX is a `package.json` build-time-only npm dep (`"katex":"0.16.11"`), version-matched to the vendored CSS/fonts.

### E.5 Native libs + deploy (correct placement)

WeasyPrint 62 native libs installed **once**, guarded by a sentinel under `data/` (untracked, deploy-preserved), inserted **before the `# 4` pip step at L86** (the file has no "step 3" block there; call it `# 3b` relative to the real `# 4`):

```bash
# 3b. One-time: WeasyPrint native libs + Node (for build-time katex CLI). Sentinel-guarded.
WEASY_SENTINEL="$PORTFOLIO_DIR/data/.weasyprint_native_ok"
if [ ! -f "$WEASY_SENTINEL" ] && command -v apt-get >/dev/null 2>&1; then
    log "Installing WeasyPrint native libs + Node (one-time)..."
    if sudo apt-get update -qq && sudo apt-get install -y -qq \
        libpango-1.0-0 libpangocairo-1.0-0 libpangoft2-1.0-0 libcairo2 \
        libgdk-pixbuf-2.0-0 libffi-dev libharfbuzz0b libfontconfig1 libglib2.0-0 \
        fonts-liberation shared-mime-info nodejs npm default-jre-headless >> "$LOG_FILE" 2>&1; then
        touch "$WEASY_SENTINEL"; log "Native libs installed."
    else
        log "WARNING: apt install of native libs failed (PDF/math export may be degraded)."
    fi
fi
```

`nodejs npm` (for the katex CLI) and `default-jre-headless` (for LanguageTool, §F) are folded in. After pip, **before** the QA gate, run `npm ci` in `$PORTFOLIO_DIR` so `node_modules/.bin/katex` exists; fail loud if the binary is absent (no network `npx`).

### E.6 Token cleanups + Golden self-check

Add to `:root`: `--textblock-w:157.6mm;` `--print-accent-rule:60.2mm;` (= 157.6/φ² = 60.198→60.2). No bare `157.6mm`/`60.2mm`/`60.198mm` literal elsewhere. Bind print measure:

```css
@media print{ .reader{ max-width:var(--textblock-w); margin-inline:auto } }
```

`challenge_card.py`: **line 637 unchanged.** Correct the **stale L33 comment** "Accent rule lengths = block / phi" → "= block / phi²". Correct the `Golden.seg` docstring (L213–215) to state `seg(x)=x/PHI` **and** that the accent rule intentionally applies `/PHI` twice (`seg(cw)/PHI = cw/φ²`). Add guard immediately after the `Golden` class:

```python
# BCS invariant guard — DO NOT "fix" without reading Appendix A.
# Golden.seg(x) == x/PHI; accent rule = seg(cw)/PHI == cw/PHI**2, matching CSS --accent-rule (= --measure/phi^2).
assert abs(Golden.seg(890) - 890 / PHI) < 1e-9, "Golden.seg semantics changed"
assert abs(Golden.seg(890) / PHI - 890 / PHI**2) < 1e-9, "accent-rule (cw/phi^2) desynced"
```

**Appendix A (cw derivation):** `cw = W − 2M = 1000 − 2·55 = 890` (canvas W=1000, margin M=FIB["md"]=55; line 590 `content = Golden(M, M, W-2*M, H-2*M)`). Accent rule = `seg(890)/PHI = 890/φ² = 339.95px`. One law `block/φ²` in three units: screen `38rem/φ²=14.515rem`, print `157.6mm/φ²=60.2mm`, card `890/φ²=339.95px`.

### E.7 GeoGebra directory

`static/books/linear-algebra/ggb/` — one 2× ~1.618:1 PNG per construction, committed as book assets.

### E.8 `.gitignore` additions

Add `node_modules/` (npm build-time deps not committed) and keep `static/vendor/fonts/*.woff2` + `static/vendor/katex/**` **tracked** (committed code assets, so the deploy host is self-contained with no CDN). Add `static/books/qa/*.qa.json` and `static/books/qa/*.qa.html` (generated artifacts, §F.4).

---

## F. Error-free readability QA ship-gate (`book_lint.py`)

**HARD SHIP GATE.** No book MAY be served at `/read/<token>` or written to `static/books/<slug>.pdf` unless `python book_lint.py --book <slug> --strict` exits `0` AND `static/books/qa/<slug>.signoff.json` has `signed_off==true` for the current HEAD.

### F.1 Tooling (offline, pure-Python + the shared build-time Node katex)

`markdown-it-py` is **NOT** used to re-render (would diverge from production Python-Markdown). **The gate lints the ACTUAL production-rendered HTML** produced by `render_book_md` + `katex_prerender.render` (imported from the real pipeline). `markdown-it-py` is used ONLY for token-level source checks (fence languages, `$` balance) where mapping to authored `.md` matters; all anchor/ID/structure checks run against the Python-Markdown+`katex_prerender` output. Libs: `selectolax` (HTML parse), `pyspellchecker` (offline), `language_tool_python` (offline JAR), `wcag-contrast-ratio`, `requests` (existing). No Node/Chromium/network API — **except** the same build-time Node `katex` CLI already required by §B (M003 validates the already-baked HTML for `.katex-error`, it does NOT re-render).

### F.2 KaTeX validation reconciled (no separate strict re-render)

The v1.0 M003 self-contradiction (production `throwOnError:false` vs gate strict re-render) is resolved: **the gate inspects the shipped HTML** — ERROR on any `<span class="katex-error">` present. Because `katex_prerender.render` already **raises** on any TeX error (§B.2), a broken equation never reaches the HTML in the first place; M003 is a defense-in-depth grep on the identical shipped artifact, guaranteeing screen==PDF==linted.

### F.3 Check families (severity ERROR fails gate)

- **Structure**: R020 heading hierarchy (one h1, no skips), R030 anchors resolve to BCS scheme, R031 duplicate id ERROR / orphan WARN, R040 `<img>` alt + iframe `title`.
- **Math**: M001 `$$`/`$` balance (source, fences stripped incl. `~~~` and indented), M002 `\begin`/`\end` env balance (allowed set only), M003 no `.katex-error` in shipped HTML, M004 matrix rows equal column count.
- **Code/output**: C001 every fence declares a language, C002 output mislabeled as `python` → ERROR, C003 curly quotes / en-em dash inside code → ERROR.
- **Fidelity/no-fabrication**: F001–F003 against `blank_solutions.json`. Canonical placeholder markup exactly `Solution not provided in the source material.`
- **Readability**: R001 spelling (allowlist), R002 grammar, R010–R013 typography.
- **A11y**: A010/A011 contrast (dark code-string MUST be `#4ec9a0`; `#007a3d`-on-`#212529` = 3.9 FAIL), A020 min sizes, A021 44×44 tap targets, A030 print ink `#212529` never `#000`.
- **Links**: **L001 is WARN at deploy time, ERROR only under `--ci`** (fixes the "transient blip bricks deploy on outbound-tunnel-only host").
- **Grammar JAR**: R002 is **WARN at deploy time; ERROR only under `--ci`** if the JAR is provisioned. If `--ci` and JAR missing → fail LOUD (never silent PASS). JAR pinned/provisioned at `$PORTFOLIO_DIR/data/languagetool/` (untracked, provisioned once).
- **Human sign-off H001**: `signoff.json` `signed_off==true` AND `commit==git -C $PORTFOLIO_DIR rev-parse HEAD`. **Atomic sign-off subcommand** `python book_lint.py --sign --book <slug> --reviewer <name>` stamps current HEAD and writes the file (resolving the circular-commit problem — the sign-off file is committed as the final commit of the content change).

**Blank-solution registry** seeded from SOURCE_STRUCTURE.md: `{"linear-algebra":[7,17,21,31,33,62,67,68,80,81,111,116,118, ...Module-L/M],"python":[]}`. **SOURCE_STRUCTURE.md line 42 says "most of Module L/M" — these MUST be fully enumerated against the live re-pull before first ship** (not left provisional). F002 registry changes between commits emit a WARN (audit trail; not a silent escape hatch).

### F.4 Wiring (does not brick auto-deploy)

- `.gitignore` MUST exclude `static/books/qa/*.qa.json` + `*.qa.html` (written atomically via temp+rename).
- `auto_deploy.sh` step-2 clobber guard MUST also exclude `static/books/qa` exactly as it excludes `static/images`: `git diff --quiet -- ':!static/images' ':!static/books/qa'` — otherwise the artifacts the gate writes abort the next deploy.
- Insert gate **after `npm ci`, before the restart**:
  ```bash
  # 4c. Human-readability QA gate — block deploy on any book error.
  for slug in python linear-algebra; do
    if ! "$PORTFOLIO_DIR/venv/bin/python" book_lint.py --book "$slug" --strict >> "$LOG_FILE" 2>&1; then
      log "ERROR: QA gate failed for '$slug' — see static/books/qa/$slug.qa.json. Aborting deploy."; exit 1
    fi
  done
  ```
- `make_book_pdf.py` calls `book_lint.check(slug, strict=True)` and `raise SystemExit(rc)` before `doc.write_pdf(out)`.
- `book_lint.py` uses `git -C "$PORTFOLIO_DIR"` for `rev-parse` so it never fails on the deploy host.

### F.5 Sample-code bug fixes (normative reference must be correct)

- M001 fence stripping handles ` ``` `, `~~~`, and indented code; escaped `\$` excluded before counting.
- `check_F_fidelity` removes the unused `text` var.
- M004 splits rows on `\\` guarding escaped `\\\\` and env-internal `&` inside `\text{}`.

---

## Round-trip proof (matrix, end-to-end)

Author writes display math on its own blank-line-separated line:

```
$$A=\begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix},\quad \vec{v}=\begin{pmatrix} 1 \\ -1 \end{pmatrix}$$
```

After `render_book_md`: `<div class="arithmatex">\[A=\begin{bmatrix} 2 &amp; 1 \\ 1 &amp; 2 \end{bmatrix}…\]</div>` (block sibling, not in `<p>`; `_`,`\`,`{}` intact). After `katex_prerender.render`: `<div class="katex-display-wrap"><span class="katex-display"><span class="katex">…</span></span></div>` with `bmatrix`/`pmatrix` brackets drawn from `KaTeX_Size1/2` woff2 (§B.4) — real delimiters in the PDF, no tofu. Screen and WeasyPrint consume the identical string (no JS on either); grep gate (§B.5) confirms no `arithmatex`/`katex.js` remains.