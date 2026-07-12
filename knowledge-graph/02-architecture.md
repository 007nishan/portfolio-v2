# 02 · Architecture

## System components

### 1. Web application (`app.py`)
A single-file Flask app. Responsibilities:
- Serves public pages (home, calendar, challenge detail, SQL stub).
- Serves auth flow (register → mock OTP → dashboard; OAuth redirect stubs).
- Handles the discussion board (comments) and satisfaction ratings.
- Hosts the unauthenticated `/admin` content-management form.
- Exposes a small JSON API (`/api/challenges`, `/api/rate`).
- Serves dynamically-generated "book" pages from `templates/books/<token>.html`.

### 2. Data layer (`models.py` + SQLite)
- SQLAlchemy models: `Challenge`, `User`, `ConceptStrength`, `UserNotebook`, `Comment`.
- SQLite at `data/portfolio.db`, configured for concurrency (WAL, `check_same_thread=False`, 15s busy timeout).
- **Hard rule: append-only schema** (never drop tables/columns — see [03-data-model.md](03-data-model.md)).

### 3. Content ingestion pipelines (three independent paths into the DB)
1. **FCC API sync** (`fcc_sync.py`) — fetches `https://api.freecodecamp.org/daily-coding-challenge/date/{YYYY-MM-DD}`, upserts challenge rows. Single-day or `--backfill` from 2025-08-11.
2. **Manual admin upload** (`/admin` → `_handle_admin_post`) — owner uploads main image + problem/Q&A screenshots + solution code; stored as `source='manual'`.
3. **Telegram bot** (`telegram_bridge.py`) — owner sends a photo from phone → OCR extracts date/title (`ocr_helper.py`) → image cleaned (`image_processor.py`) → row upserted via a subprocess script.

### 4. Client-side execution engine (in `challenge_detail.html`)
- **Pyodide** (Python compiled to WASM) runs entirely in the browser.
- **CodeMirror** editor with debounced live execution (800ms) + explicit "Run Code" / "Run Tests" buttons.
- Test cases come from FCC's Python tests (`fcc_py_tests`), where the pure Python assertion is regex-extracted from FCC's JS `runPython(\`...\`)` wrapper server-side, then executed against the user's code. All-pass → confetti + "XP GAINED +100".

### 5. Notification & agent bridge (`telegram_bridge.py`, "OpenClaw")
- Telegram bot locked to a single admin chat ID (auto-claimed on first `/start`).
- Capabilities: chat via **Grok (xAI)** or **Gemini**, run shell (`$ cmd`), run Python (code fences), `/status`, `/clean`, photo-sync.
- LLM **ReAct loop**: model can emit `[RUN_SHELL: <cmd>]`, backend executes and feeds output back (max 3 loops).
- `app.py /api/rate` sends a Telegram message when a visitor rates a challenge.

### 6. Deployment & resilience automation (paramiko + shell + systemd)
- SSH-driven deploy scripts push files and (re)start services on `192.168.1.150`.
- `cloudflared` exposes port 5001 to the internet via a `trycloudflare.com` URL.
- `network_watchdog.sh` (systemd timer, every 2 min) detects internet outages and, on recovery, re-syncs FCC + restarts services.
- `setup_server.sh` configures lid-close=ignore, daily cron, watchdog timer, and `Restart=always`.

## Request / data flow

### Public page render (e.g. home)
```
Browser GET / ─► Flask home()
   ├─ Challenge.query.order_by(date_id desc).first()   # latest challenge
   ├─ get_daily_quote()   # hourly file cache in data/quote_cache.json, else FCC motivation.json
   ├─ markdown.markdown(problem_text / concepts_text)
   └─ render_template("home.html", ...)
```

### Interactive test run (client-side, no server round-trip)
```
Detail page load ─► load Pyodide (WASM) ─► user edits code in CodeMirror
   ├─ on change (debounced 800ms): run user code, capture stdout to console
   └─ "Run Tests": run user code, then each extracted assertion; pass=green/confetti, fail=red
```

### Daily autonomous sync
```
cron 00:30 Central ─► venv/python fcc_sync.py ─► FCC API ─► upsert row ─► (logs to data/cron_sync.log)
watchdog (every 2m) ─► if internet just recovered ─► fcc_sync.py + restart portfolio/nginx
```

### Telegram photo → website
```
Phone photo ─► telegram_bridge handle_photo
   ├─ download highest-res
   ├─ ocr_helper.extract_challenge_info() → (date_id, title)
   ├─ image_processor.clean_image() → crop FCC branding + add themed border
   ├─ rename to <YYYYMMDD>_<msgid>_sync.jpg
   └─ subprocess python -c "<f-string DB script>" → upsert Challenge.image_path
```

## Deployment topology

```
                Internet
                   │
                   ▼
        *.trycloudflare.com  (Cloudflare edge)
                   │  outbound tunnel (no open ports)
                   ▼
   ┌──────────────────────────────────────────┐
   │  Linux laptop  192.168.1.150 (user nishan)│
   │  ~/portfolio/                              │
   │   ├─ gunicorn/flask app  :5001            │
   │   ├─ cloudflared tunnel                   │
   │   ├─ telegram_bridge.py (bot)             │
   │   ├─ systemd: portfolio.service (Restart) │
   │   ├─ systemd timer: portfolio-watchdog    │
   │   ├─ cron: fcc_sync.py @ 00:30 Central    │
   │   └─ data/portfolio.db (SQLite WAL)       │
   └──────────────────────────────────────────┘
```

**Why this topology (from `add_learning.py` self-documentation):** the owner wanted global access *without* a cloud VPS (AWS/Render) and *without* migrating SQLite → Postgres. Cloudflare Tunnel makes outbound connections, so no firewall ports need opening. Empirical outcome recorded in the DB as a "learning module."

## Notable cross-cutting design choices
- **SQLite hardening pragmas** applied on every connection: `journal_mode=WAL`, `synchronous=NORMAL`, `cache_size=-64000` (64MB), `foreign_keys=ON`. Rationale: survive concurrent writes under gunicorn threads without "database is locked."
- **Client-side code execution** (Pyodide) instead of a server sandbox: zero server-side security exposure for running untrusted visitor code, no infra cost.
- **Three ingestion paths converge on one `Challenge` table**, disambiguated by a `source` column (`'manual'` vs `'fcc_api'`); sync logic refuses to overwrite manual content.
