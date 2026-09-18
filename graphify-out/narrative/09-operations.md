# 09 · Operations Runbook

How to run, deploy, sync, and recover the project.

## Local development (Windows / this machine)
```bash
# from repo root
python -m venv venv && source venv/Scripts/activate   # (Windows bash)
pip install -r requirements.txt
python app.py                 # serves http://127.0.0.1:5001  (debug=True)
```
- DB auto-creates at `data/portfolio.db` on first model access. To populate: `python fcc_sync.py --backfill`.
- `setup.sh` is a Linux convenience (mkdir static dirs, copy `/mnt/project/*.jpg`, pip install).
- Note the README says port 5000, but `app.py` actually uses **5001**.

## Production (server `192.168.1.150`, user `nishan`, dir `~/portfolio`)
Managed by systemd + cron + a Cloudflare tunnel.

| Concern | Mechanism |
|---------|-----------|
| App process | `portfolio.service` (systemd), `Restart=always`, `RestartSec=5` |
| Public URL | `cloudflared tunnel --url http://localhost:5001` → `*.trycloudflare.com` |
| Daily content | cron `30 0 * * *` → `venv/bin/python fcc_sync.py` (00:30 US Central ≈ 06:00 IST) |
| Outage recovery | `portfolio-watchdog.timer` every 2 min → `network_watchdog.sh` |
| Stay-on | `HandleLidSwitch=ignore` in logind.conf (laptop lid closed = keep running) |
| Bot | `telegram_bridge.py` (started by `deploy_bridge.py`, ideally a service) |

### First-time server setup
```bash
# on the server, once:
bash setup_server.sh    # lid-ignore, cron, watchdog timer, Restart=always
```

### Deploy from dev box (SSH/paramiko) — ⚠️ scripts contain hardcoded password (see 08-security.md)
```bash
python deploy_bridge.py     # SFTP app.py/telegram_bridge/book_generator/image_processor, restart app+bot
python push_templates.py    # SFTP templates, restart flask
python deploy_tunnel.py     # ensure app up, install cloudflared, start tunnel, PRINT PUBLIC URL
python remote_backfill.py   # run fcc_sync --backfill on server, restart app
```
> Before running these: update the hardcoded `LOCAL_DIR` Windows paths in `deploy_bridge.py`/`push_templates.py` — they point at the old `Desktop\Test Folder\My Portfolio\portfolio` location, not this clone.

### Get a public URL (fallback chain)
```bash
bash get_public_url.sh   # tries cloudflared → ngrok → localhost.run → serveo, 3 attempts
```

## Content operations
| Task | Command / action |
|------|------------------|
| Sync today's challenge | `python fcc_sync.py` |
| Backfill all history | `python fcc_sync.py --backfill` (from 2025-08-11) |
| Add challenge manually | Browse to `/admin`, upload image + screenshots + code (⚠️ no auth) |
| Add via phone | Telegram bot: send a photo (OCR→clean→DB) |
| Scrape Python textbook | `bash run_scraper.sh` → `data/textbook/` |
| Scrub "freeCodeCamp" text | `python scrub_db.py` |

## Telegram bot (OpenClaw) commands
| Input | Effect |
|-------|--------|
| `/start` | Claims admin (if unset), shows keyboard |
| `/set_grok <key>` | Set LLM key (Grok `xai-…`, or Gemini `AIzaSy…` auto-detected) |
| free text | Chat via Grok/Gemini (may trigger `[RUN_SHELL]` ReAct loop) |
| `$ <cmd>` | Run shell (15s timeout) |
| ` ```code``` ` | Run Python (15s timeout) |
| `📊 Status` | `uptime && free -h` |
| `🧼 Clean` | Run `image_processor.py` over all images |
| send photo | OCR + clean + DB upsert a new challenge |

## Diagnostics
| Question | Tool |
|----------|------|
| What's the latest challenge? | `python check_db_server.py` or `inspect_db.py` |
| Are all tables present? | `python verify_tables.py` / `create_missing_tables.py` |
| Is the FCC API + sync healthy? | `python test_sync.py` |
| Any residual branding in DB? | `python check_fcc_text.py` |
| Logs (server) | `data/sync_log.txt`, `data/cron_sync.log`, `data/watchdog.log`, `bot_health.log` |

## Landing-challenge cards (generated, own-brand)
- **`challenge_card.py`** renders a self-branded, Python-only, **golden-ratio** landing card per challenge from synced FCC data (title/description/`fcc_starter_py`), Editorial theme. Output: `static/images/<YYYYMMDD>_card.jpg`. One `DESIGN`/`THEMES` config → `python challenge_card.py --all --force` re-renders every card. Logo (top-left) and character (right golden column) zones are reserved for future assets.
- **Daily hook:** `fcc_sync.py` calls `generate_card()` after each upsert (best-effort; a render failure never breaks content sync). Manual `/admin` uploads are protected — only empty or `*_card.jpg` rows regenerate.
- **FCC images removed (2026-07-25):** the 150 FCC-sourced `static/images/*.jpg` + `daily_challenges/*` were replaced by branded cards and **purged from the ENTIRE git history** (repo `.git` 56M→35M). `main` was force-pushed with rewritten history. Backup bundle: `C:\tmp\portfolio-v2-backup-20260725.bundle` (all refs, pre-purge tip `baa2536`).
- **Cards ARE committed** to git now (site serves them from our own server, not GitHub CDN). The daily cron regenerates them in place; `auto_deploy.sh` ignores `static/images/` drift so that never blocks a deploy.

## Key operational facts / gotchas
- **Timezone:** sync cron is 00:30 **US Central**; watchdog compensates for missed runs after outages.
- **Tunnel URLs are ephemeral** (trycloudflare rotates on restart) unless a *named* tunnel is set up — `book_generator.py` hardcodes a stale URL (`allowing-together-accepts-apache.trycloudflare.com`).
- **`data/` is gitignored** — the live DB does not travel with the repo. Challenge **images are now the generated `*_card.jpg` cards** (committed to git); the old FCC `*.jpg` set was removed.
- **History rewrite → server self-heals:** `auto_deploy.sh` now falls back from `merge --ff-only` to `reset --hard origin/main` when a fast-forward is impossible (as after the history purge). Server converges automatically on next 60s tick; untracked `data/`, `venv/`, `.env`, and manual uploads are preserved. If ever doing this manually: `cd ~/portfolio && git fetch origin && git reset --hard origin/main && sudo systemctl restart portfolio`.
- **Server-only Python deps** (pytesseract, Pillow, dateparser, opencv-python, numpy, python-telegram-bot, openai, paramiko, beautifulsoup4, lxml) are **not** in `requirements.txt` — install manually where those scripts run.
