# Knowledge Graph — Changelog

Append-only log of updates to the knowledge graph itself (not the app).

## 2026-07-12 · Initialization
- Cloned `github.com/007nishan/portfolio-v2` at HEAD `e084129`.
- Read every file: 28 Python modules, 9 templates, 5 shell scripts, 3 migrations, CSS, full 44-commit history.
- Created knowledge graph: `01-overview`, `02-architecture`, `03-data-model`, `04-timeline`, `05-decisions`, `06-algorithms`, `07-components`, `08-security`, `09-operations`, `10-open-questions`, `graph.json`.
- Key findings surfaced: 4 CRITICAL security issues (hardcoded SSH password, public Telegram token, bot RCE, unauth /admin). See `08-security.md`.
- Recorded 13 decisions (D-001…D-013) and 12 risks (S-1…S-12).

## 2026-07-12 · Server access received
- Owner provided: host `192.168.1.150`, SSH port `22`, user `nishan`, private key `portfolio-v2/id_rsa` (now gitignored).
- ⚠️ Cannot reach the server: the dev box is on Amazon Cisco AnyConnect full-tunnel VPN, which routes/blocks the home LAN `192.168.1.x`. Must disconnect VPN to SSH in. Same VPN/proxy intermittently returns 403 on outbound web fetches.
- Owner directives: repo stays public/test for now (secure+rotate at production time); roadmap = standardize (one brand kit + speed) → hardcode+test → lineage/SSOT → domain/production. New Task 4: server program to auto-fetch FCC daily image from X/IG/FB (FCC API has no image field) and auto-strip/tag by date like image_processor.py.

## 2026-07-12 · FIX: FCC calendar visibility bug (branch `fix/calendar-fcc-visibility`)
- **Bug:** clicking a calendar cell for an FCC-synced challenge showed a blank/broken lightbox and never surfaced the question, because `openModal()` is image-only and FCC rows have `image_path=""` (content is in `fcc_description`). Manual (image-backed) challenges worked → intermittent-looking symptom.
- **Fix (templates/challenges.html only, look preserved):**
  1. `allChallenges` JS lookup now carries `has_image` + empty-safe `image`.
  2. `handleDateClick()` is source-aware: image-backed → lightbox; FCC (no image) → navigate to `/challenge/<date>` detail page where `fcc_description` renders.
  3. Grid cell renders a clickable text tile (`.challenge-thumb-text`) for FCC rows instead of a broken `<img src="/static/images/">`; `data-image` emitted only when an image exists.
  4. Modal `<img>` `onerror` now navigates to the detail URL instead of a nonexistent `placeholder.jpg`.
- **Verified** via Flask test_client: manual→lightbox, FCC→detail with description shown, zero empty image tags, both detail pages 200. Test rows cleaned up.
- **Left intentionally:** RC3 (`calendar_data[:1]` renders only newest month) — older months remain reachable via the Flatpickr archive picker, which now also routes FCC challenges correctly. Rendering all months is a layout change, deferred to the standardization pass.

## 2026-07-12 · REWORK: Ack-pattern modal + live single-source fetch (owner live feedback)
- Owner tested and reported: (a) calendar **flickering**, (b) recent past dates fetch **nothing**, (c) need an automatic **fallback to the question text when no image exists**, using an **acknowledge (Ack) algorithm**.
- **Reworked the fix (challenges.html + app.py):**
  1. New endpoint `GET /api/challenge/<date_id>` = single source of truth; returns image URL when present else `description_html` (FCC desc or rendered markdown) + concepts. 404 when absent.
  2. Modal is now an **Ack state machine**: click → open + spinner (instant acknowledge) → fetch one source → render IMAGE or TEXT panel; image `onerror` → text fallback; network/404 → error panel with direct link. Never blank/broken.
  3. `handleDateClick` now **always fetches live** from the API instead of the embedded `allChallenges` lookup (which was stale/missing recent dates). Removed the embedded lookup entirely (also helps SSOT — page no longer duplicates challenge data).
  4. **Flicker fixed:** removed `.has-challenge:hover { transform: scale(0.98) }` (hover/unhover loop) → inset box-shadow highlight; `transition: all` → color/shadow only.
- **Verified** via test_client: /challenges 200 with loader+text panels; manual→image; FCC→text (description_html present); missing→404. Test rows cleaned.

## 2026-07-12 · Standardization slices 1–11 COMPLETE (pushed to main)
Method-grounded standardization from the 9-dimension audit (knowledge-graph/standardization-audit.json). All code-safe; deploys via GitHub auto-deploy. Commits 17d403f→3915568.
- **S1 Code hygiene:** removed fabricated home() stats, dead load_challenges(), inline imports.
- **S2 DRY:** markdown → Challenge model properties (problem_html/concepts_html/qa_html/display_description_html/has_image); merged quote fetchers; print()→logger; /api/rate reads env creds, honest status.
- **S3 Tokens (foundation):** added --color-accent-petrol, --color-primary-blue-dark, --font-family-mono, neutral/surface scale, brand-github; removed dead Inter font.
- **S4 Literals→tokens:** petrol/red/github/mono + calendar grey cluster.
- **S5 Classes:** one canonical .markdown-content (+--compact) in style.css; removed 2 duplicate <style> blocks; moved hover-zoom/blink there.
- **S6 Anti-copy shields removed** (base.html keydown/contextmenu, modal pointer-events/oncontextmenu) — a11y + honesty.
- **S7 A11y (WCAG 2.2 AA):** calendar tiles role=button/tabindex/keydown/focus-visible; emoji ratings → <button aria-label> in role=group; lightbox role=dialog + <button> close; navbar/register ARIA; contrast fixes (day-number, Let's-Connect).
- **S8 Perf (CWV):** lazy Pyodide (ensurePyodide on focus/Run), defer CodeMirror/Pyodide/confetti, calendar img loading=lazy+decoding=async, home hero fetchpriority=high, preconnect + icons-in-head.
- **S9 Responsive:** clamp() fluid type (body+h1–h5), calendar horizontal-scroll <480px, fluid CodeMirror height, fluid modal chrome.
- **S10 Self-healing:** GET /health + /readiness (DB SELECT 1), 404/500 errorhandlers (JSON for /api/*), home() DB guarded, fcc_sync retry+backoff session, FLASK_DEBUG/HOST/PORT from env (debug default OFF).
- **S11 Security (code-level):** SECRET_KEY fail-closed in prod; /admin @admin_required (404 unset / 403 wrong / 200 right — closes S-4 unauth upload); image_path NOT NULL default='' matches live schema; .env.example added.
- **Deferred to production window (12 items):** schema-reconciling Alembic migration, WebP derivatives, cache/gzip headers, gunicorn/systemd runtime, sudoers cleanup, secret rotation, watchdog→/readiness rewire, FCC-HTML sanitization. See standardization-audit.json deferredServerItems.

## 2026-07-12 · Auto-deploy pipeline added
- Owner rule: GitHub is updated in real-time and the server auto-updates from it.
- Added `auto_deploy.sh` (server pull-deploy: fetch origin/main → ff-only → pip install → restart; idempotent, refuses to clobber local changes) and `setup_auto_deploy.sh` (one-time: make ~/portfolio a git checkout, scoped NOPASSWD for `systemctl restart portfolio` only, systemd timer every 60s).
- Model: PULL-based (fits the outbound-only Cloudflare-Tunnel topology, D-001). Owner runs setup_auto_deploy.sh once on the server (off-VPN); thereafter every push to main goes live within ~60s.

## 2026-07-30 · Third book: "Notes as We Learn — AWS ML" (living roadmap + notes-engine sync)
- Owner goal: turn the AWS-ML-Notes adaptive-learning engine's output into a website book that **fills in as learning happens**, while **strictly** keeping the site's BrandKit / book UI (the notes repo's own brandkit.css/reader.js are ignored — content + methodology only).
- **New book** `aws-ml`, title *Notes as We Learn — AWS ML*, kicker "Learning in Public", institution "AWS Certification · MLA-C01". Reuses the entire existing book pipeline (frozen `render_book_md`, reader shell, `book_cover.py`, `make_book_pdf.py`, `book_lint.py` gate) — **zero AWS-specific CSS/JS**. Lead accent = in-kit gold `#d58000` (`--color-secondary-gold`, unused by the other two books); accent rule stays brand red.
- **Structure = living roadmap:** fixed 8-chapter MLA-C01 spine (`ch-0` Foundations … `ch-7` Domain 4). Written lessons render in full; not-yet-reached chapters render honest `!!! note "Coming as we learn"` roadmap openers grounded in the notes repo's `KNOWLEDGE_GRAPH.md`. Today only Domain 1 / Course 1.1 (`M1_1a`–`M1_1f`, 6 lessons) is written → all land in `ch-4`.
- **New `aws_sync.py`** (the "as we learn" bridge): reads `AWS_ML_NOTES_DIR/engine/content/M*.md`, maps node `M<d>_*` → Domain `d` chapter, and transforms each node → a BCS lesson (H1→`## … {: #ch-{n}-lesson-{k} }`, demote body headings one level, strip status/meta italics + author-only Images/Overlap tails, `> **Exam trap:**` → `!!! warning`). Guards against links/URLs/images leaking into the book (R050/R040). Idempotent + atomic; safe no-op when the notes repo is absent. `--check` flag for CI drift.
- **Wiring:** `book_content.py` (`aws-ml` BOOKS entry + `_AWS_CHAPTERS`), `book_generator.py` (`_CHAPTER_SETS` generalizes `validate_anchors`), `book_cover.py` + `make_book_pdf.py` (gold lead), `app.py` (`_BOOKS_CATALOG`), `dev_sync.sh` (step 0 runs `aws_sync.py` locally before push), `auto_deploy.sh` (added `aws-ml` to the build/gate/PDF loop). `AWS ML/src/ch-*.md` are generated **but committed** so the deploy server (no notes repo) builds like the other books.
- **Data flow:** notes engine → `aws_sync.py` (local only) → commit `AWS ML/src/*.md` → push → `auto_deploy.sh` rebuilds HTML+PDF from committed source. The sync is deliberately NOT in `auto_deploy.sh` because the server has no notes repo.
