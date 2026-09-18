# 07 · Component Catalog (file-by-file)

Every file in the repo, what it does, and how it connects. Grouped by role.

## 🌐 Web application core
| File | Role | Key details |
|------|------|-------------|
| [`app.py`](../app.py) (611 L) | Flask app, all routes | Config, SQLite pragmas, 20+ routes, quote cache, admin form, `/api/rate` |
| [`models.py`](../models.py) (139 L) | SQLAlchemy models | `Challenge`, `User`, `ConceptStrength`, `UserNotebook`, `Comment`; append-only rule |
| [`requirements.txt`](../requirements.txt) | Web deps only | Flask, SQLAlchemy, Migrate, gunicorn, dotenv, markdown, requests |

### Routes in `app.py`
| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Home: latest challenge + quote + stats |
| `/challenges` | GET | Calendar view of all challenges |
| `/challenge/<date_id>` | GET | Detail page: problem, concepts, code, tests, interpreter, comments |
| `/challenge/<date_id>/comment` | POST | Post a comment (login required) |
| `/sql` | GET | "Coming soon" stub |
| `/admin` | GET/POST | ⚠️ **Unauthenticated** content upload/upsert |
| `/api/challenges` | GET | JSON list of challenges |
| `/api/rate` | POST | Emoji rating → Telegram notify |
| `/read/<token>` | GET | Serve generated book page `templates/books/<token>.html` |
| `/register`,`/verify_otp` | GET/POST | Mock-OTP registration |
| `/dashboard` | GET | User's concept strengths + notebooks |
| `/logout` | GET | Clear session |
| `/login/gauth`,`/gauth/callback` | GET | Google OAuth redirect + stubbed callback |
| `/login/github`,`/github/callback` | GET | GitHub OAuth redirect + stubbed callback |

## 🎨 Templates (`templates/`)
| File | Renders |
|------|---------|
| [`base.html`](../templates/base.html) | Layout, navbar, footer, anti-copy JS shields |
| [`home.html`](../templates/home.html) | Quote banner, latest-challenge showcase, "Let's Connect" CTA |
| [`challenges.html`](../templates/challenges.html) | Calendar grid + Flatpickr archive + lightbox modal |
| [`challenge_detail.html`](../templates/challenge_detail.html) (630 L) | Problem/concepts/code, **Pyodide interpreter + test runner**, Q&A, satisfaction widget, comments |
| [`admin.html`](../templates/admin.html) | Content form w/ paste-to-upload zones + live markdown preview |
| [`register.html`](../templates/register.html) | Social buttons + manual register w/ live validation |
| [`verify_otp.html`](../templates/verify_otp.html) | 6-digit OTP entry |
| [`dashboard.html`](../templates/dashboard.html) | Concept strength bars + notebook list |
| [`sql.html`](../templates/sql.html) | "Coming Soon" placeholder |
| `templates/books/` | (dir not in repo) generated on-demand by `book_generator.py` |

## 🔄 Content ingestion
| File | Role |
|------|------|
| [`fcc_sync.py`](../fcc_sync.py) (274 L) | FCC API → DB upsert; `--backfill`; logs to `data/sync_log.txt` |
| [`ocr_helper.py`](../ocr_helper.py) | pytesseract OCR → `(date_id, title)` |
| [`image_processor.py`](../image_processor.py) | OpenCV crop FCC branding + themed border |
| [`scrape_book.py`](../scrape_book.py) | Scrape IIT-M BSc Python textbook, scrub branding → `data/textbook/` |
| [`continuous_notes.py`](../continuous_notes.py) | (scaffold) loop over FCC news URLs → "Learning Ledger" (summarization is a placeholder) |
| [`add_learning.py`](../add_learning.py) | Inserts a self-documenting "Cloudflare Tunnel deployment" challenge row |

## 🤖 Bot & notifications
| File | Role |
|------|------|
| [`telegram_bridge.py`](../telegram_bridge.py) (327 L) | "OpenClaw" bot: chat (Grok/Gemini), shell, Python, `/status`, `/clean`, photo→DB sync, ReAct loop |
| [`book_generator.py`](../book_generator.py) | Generate expiring "book" HTML pages w/ token URLs (uses a hardcoded old tunnel URL) |

## 🚀 Deployment & server automation (paramiko/SSH + shell)
| File | Role |
|------|------|
| [`deploy_tunnel.py`](../deploy_tunnel.py) (176 L) | Install SSH key, ensure app up, install cloudflared, start tunnel, print public URL |
| [`deploy_bridge.py`](../deploy_bridge.py) | SFTP app/bot files, restart app + bot |
| [`push_templates.py`](../push_templates.py) | SFTP templates, restart Flask |
| [`remote_backfill.py`](../remote_backfill.py) | Run `fcc_sync --backfill` on server, restart app |
| [`security_harden.py`](../security_harden.py) | UFW + Fail2Ban + SSH hardening over SSH |
| [`server_maintenance.py`](../server_maintenance.py) | LVM extend + **NOPASSWD sudo** |
| [`fix_sudo.py`](../fix_sudo.py) | Force passwordless sudo |
| [`setup.sh`](../setup.sh) | Local dev setup (dirs, copy images, pip install) |
| [`setup_server.sh`](../setup_server.sh) (138 L) | Server: lid-ignore, cron, watchdog timer, Restart=always |
| [`network_watchdog.sh`](../network_watchdog.sh) | Outage detection + recovery |
| [`get_public_url.sh`](../get_public_url.sh) | 4-method tunnel fallback (cloudflared→ngrok→localhost.run→serveo) |
| [`run_scraper.sh`](../run_scraper.sh) | pip install bs4/lxml + run textbook scraper |

## 🔧 DB / debug utilities (throwaway ops tools)
| File | Role |
|------|------|
| [`inspect_db.py`](../inspect_db.py) | Print latest + Feb challenges + today's entry |
| [`inspect_db_detailed.py`](../inspect_db_detailed.py) | Deep inspect a specific date (2026-03-15) |
| [`check_db_server.py`](../check_db_server.py) | Print latest entry (machine-parseable line) |
| [`fix_db.py`](../fix_db.py) | Clear a bad `image_path` to restore API-card fallback |
| [`scrub_db.py`](../scrub_db.py) | Strip "freeCodeCamp" from challenge text fields |
| [`create_missing_tables.py`](../create_missing_tables.py) / [`create_user_tables.py`](../create_user_tables.py) | `db.create_all()` on server |
| [`verify_tables.py`](../verify_tables.py) | List tables via sqlite3 (server path) |
| [`check_fcc_text.py`](../check_fcc_text.py) | Find residual "FCC" strings in DB |
| [`test_sync.py`](../test_sync.py) | Verify FCC API structure + sync pipeline |
| [`test_extract.py`](../test_extract.py) | Verify FCC JS→Python test extraction |

## 🗄️ Migrations (`migrations/`)
| File | Purpose |
|------|---------|
| `alembic.ini`, `env.py`, `script.py.mako`, `README` | Alembic scaffolding |
| `versions/704755926c31_initial_schema.py` | Initial `challenges` table |
| `versions/f8faeae5ecde_add_quote_text.py` | + `quote_text` |
| `versions/49b711d2aba8_add_qa_text_field.py` | + `qa_text` |

## 📦 Static assets (`static/`)
| Path | Contents |
|------|----------|
| `static/css/style.css` (250 L) | Brand-kit CSS variables + component styles |
| `static/images/*.jpg` | **150** challenge thumbnails (`20250909`→`20260223`) |
| `static/daily_challenges/2026-01-31_zodiac-sign.jpg` | 1 stray image (different naming) |

## ⚠️ Path/portability inconsistencies (worth knowing)
- `book_generator.py`, `continuous_notes.py`, `scrub_db.py`, `test_extract.py`, `deploy_bridge.py`, `push_templates.py` hardcode **Windows** paths like `c:\Users\NISHAN\Desktop\Test Folder\My Portfolio\portfolio\…`.
- `scrape_book.py`, `verify_tables.py`, `inspect_db.py` (partly) hardcode **Linux** server paths `/home/nishan/portfolio/…`.
- The app itself uses `basedir`-relative paths (portable); the utilities do not. These utilities are environment-specific one-offs.
