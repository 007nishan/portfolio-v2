# 10 · Open Questions & TODOs

Things we don't yet know for certain, or that need confirmation from the server owner / future work.

## ❓ Needs confirmation from owner
- [x] **Server access details** — provided 2026-07-12: host `192.168.1.150`, SSH port `22`, user `nishan`. **Password/key still needed** (the repo's hardcoded password `6WKW5_3w2w5121` may or may not still be valid — treat S-1 as unresolved until we log in and rotate).
- [ ] Is the server currently **online and serving**? What is the current public tunnel URL (trycloudflare rotates)?
- [ ] Is there a **named/persistent Cloudflare tunnel** or a custom domain, or only ephemeral `trycloudflare.com` URLs?
- [ ] Is the **Telegram bot** currently running, and has the admin chat ID been claimed (`admin_id.txt`)?
- [ ] Which **LLM key** is configured in `claw_config.json` (Grok vs Gemini), and is it still valid?
- [ ] Are the **server-only Python deps** actually installed in the server venv (opencv, pytesseract+tesseract binary, telegram, openai, paramiko, bs4/lxml)?
- [ ] **Licensing:** is republishing FCC challenge content and the IIT-M BSc Python textbook (with branding scrubbed) acceptable? (attribution/copyright review)

## 🐛 Known bugs / inconsistencies to fix
- [ ] **Home stats are fake:** `home()` sets `mastered = total_challenges` and `in_progress = 1` unconditionally → "100% mastered" regardless of reality.
- [ ] **README port mismatch:** README says `localhost:5000`; app runs on `5001`.
- [ ] **Hardcoded dev paths** in `deploy_bridge.py`, `push_templates.py`, `book_generator.py`, `continuous_notes.py`, `scrub_db.py`, `test_extract.py` point at `Desktop\Test Folder\My Portfolio\portfolio` (old location) — will break if run from this clone.
- [ ] **`book_generator.py`** hardcodes a stale tunnel URL and its `BOOKS_DIR` Windows path; `templates/books/` doesn't exist in the repo, so `/read/<token>` 404s until generated.
- [ ] **`image_processor.clean_image` is not idempotent** — re-running re-crops already-cropped images (the `/clean` bot command reprocesses *all* images).
- [ ] **Requirements gap:** `requirements.txt` omits every non-web dependency (see above) → fresh installs of the scripts fail.
- [ ] **Schema drift:** `fcc_*`, `challenge_number`, `source`, and all user/comment tables exist only via `db.create_all()`, not Alembic migrations → migration state doesn't match the model.
- [ ] **`continuous_notes.py`** summarization is a placeholder (commented out); it only sleeps/logs.
- [ ] **`ConceptStrength` / `UserNotebook`** tables are never written by any live code path → dashboard is always empty.

## 🔐 Security follow-ups (see 08-security.md for full list)
- [ ] Rotate SSH password, revoke Telegram token, purge secrets from git history / make repo private.
- [ ] Auth-gate `/admin`; set Flask `debug=False`; enforce a real `SECRET_KEY`.
- [ ] Remove `NOPASSWD:ALL` sudo; sandbox/allowlist or retire the bot's shell/Python exec.

## 🚀 Feature backlog (from README TODO + code stubs)
- [ ] SQL challenges page (currently "Coming Soon").
- [ ] Python / ML journey pages.
- [ ] Real chatbot integration (README mentions Gemini; bot exists but is admin-only).
- [ ] Complete Google/GitHub OAuth (callbacks are stubbed).
- [ ] Wire the concept-strength reward/penalty scoring to actual gameplay.
- [ ] GitHub API integration for code links; analytics; contact form.

## 🧭 Decisions still open
- [ ] Keep self-hosted laptop + tunnel, or move to a small VPS / static export? (trade cost vs reliability vs the D-001 rationale)
- [ ] Keep the agentic Telegram bot at all, given its risk profile?
