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

## 2026-07-12 · Auto-deploy pipeline added
- Owner rule: GitHub is updated in real-time and the server auto-updates from it.
- Added `auto_deploy.sh` (server pull-deploy: fetch origin/main → ff-only → pip install → restart; idempotent, refuses to clobber local changes) and `setup_auto_deploy.sh` (one-time: make ~/portfolio a git checkout, scoped NOPASSWD for `systemctl restart portfolio` only, systemd timer every 60s).
- Model: PULL-based (fits the outbound-only Cloudflare-Tunnel topology, D-001). Owner runs setup_auto_deploy.sh once on the server (off-VPN); thereafter every push to main goes live within ~60s.
