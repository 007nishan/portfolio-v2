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