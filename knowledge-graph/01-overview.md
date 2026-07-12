# 01 · Project Overview

## What it is

**Nishan's Portfolio Website** — a Flask-based personal portfolio built around **FreeCodeCamp (FCC) Daily Coding Challenges**. It presents a solving journey (Sep 2025 → Feb/Mar 2026) as a browsable calendar, with per-challenge detail pages that include an **in-browser Python interpreter and test runner (Pyodide)**, plus lightweight community features (registration, discussion comments, satisfaction ratings).

The tagline in the header: *"Transportation Specialist at @amzn | Ex-Teaching Assistant - Joy of Computing using Python (NPTEL) | Mechanical Engineer."* The README frames it as a *"journey to becoming an Amazon Business Analyst."*

## One-page mental model

```
   FCC public API ─────────────┐
   (daily challenge JSON)       │  fcc_sync.py (cron @ 00:30 Central)
                                ▼
   Telegram (photos/cmds) ─► SQLite  ◄─── /admin manual upload (screenshots, code, Q&A)
        │  telegram_bridge     (portfolio.db)
        │  OCR + image clean         │
        ▼                            ▼
   image_processor / ocr_helper   Flask app.py  ──► Jinja2 templates ──► Browser
                                     │                                     │
                                     │                                     ├─ Pyodide runs Python client-side
                                     │                                     ├─ CodeMirror editor
                                     └─ /api/rate ──► Telegram notify       └─ Bootstrap 5 UI
```

## Who it's for
- **Primary user / owner:** Nishan (portfolio owner, admin, sole developer).
- **Visitors:** people viewing the coding journey; can register, comment, run code, rate challenges.

## Core value propositions
1. **Learning showcase** — every FCC daily challenge with problem statement, concepts breakdown, and final solution code.
2. **Interactive practice** — visitors can write and run Python in the browser and check it against the challenge's real FCC test cases, entirely client-side (Pyodide/WASM).
3. **Autonomous content pipeline** — challenges self-populate daily from the FCC API; the owner can also push content from their phone via a Telegram bot (photo → OCR → cleaned image → DB).

## Tech stack (at a glance)

| Layer | Technology | Notes |
|-------|-----------|-------|
| Web framework | **Flask 3.0.0** | Single-file app (`app.py`) |
| ORM | **Flask-SQLAlchemy 3.1.1** | Models in `models.py` |
| Migrations | **Flask-Migrate 4.0.5 / Alembic** | 3 migrations, append-only policy |
| Database | **SQLite** (WAL mode) | `data/portfolio.db`, gitignored |
| Templating | **Jinja2** + **Bootstrap 5.3.0** (CDN) | Editorial "Scientific American" theme |
| In-browser Python | **Pyodide 0.25.1** (WASM) | Client-side execution & tests |
| Code editor | **CodeMirror 5.65.13** | Python mode, Monokai theme |
| Gamification | **canvas-confetti 1.9.3** | Fires on all-tests-pass |
| Markdown | **markdown 3.5.1** (server) + **marked** (client preview) | |
| WSGI server | **gunicorn 21.2.0** | Production |
| Config | **python-dotenv 1.0.0** | `.env` (gitignored) |
| Content sync | **requests 2.31.0** → FCC API | |
| OCR pipeline | **pytesseract, Pillow, dateparser** | Not in requirements.txt (server-only) |
| Image cleaning | **OpenCV (cv2), numpy** | Not in requirements.txt (server-only) |
| Bot | **python-telegram-bot, openai SDK** (xAI Grok / Gemini) | Not in requirements.txt (server-only) |
| Deploy/automation | **paramiko** (SSH), **cloudflared** (tunnel), **systemd**, **cron** | |
| Hosting | Self-hosted Linux laptop `192.168.1.150` + Cloudflare Tunnel | Not a cloud VPS |

> ⚠️ **Dependency gap:** `requirements.txt` only lists 7 web deps. The OCR, OpenCV, Telegram, and paramiko stacks are used by scripts but **not declared** — they must be installed manually on the server. See [10-open-questions.md](10-open-questions.md).

## Repository facts (as of clone, 2026-07-12)
- **44 commits**, single branch `main`, author `Nishanur`.
- First commit `3ad3c2a` on **2026-03-08**; latest `e084129` on **2026-03-16**. (The README claims Sep 2025–Feb 2026 for the *challenge content*, but the *repo* history is Mar 2026 — this is `portfolio-v2`, a re-push; earlier local paths reference `Desktop\Test Folder\My Portfolio\portfolio`.)
- **28 Python modules**, **9 HTML templates**, **5 shell scripts**, **3 Alembic migrations**.
- **150 challenge images** in `static/images/` spanning `20250909` → `20260223`, plus 1 in `static/daily_challenges/`.
- App runs locally on **port 5001** (`app.run(debug=True, host=127.0.0.1, port=5001)`).
