# 05 · Decision Log (ADR-style)

Each decision records **what** was decided, **why**, the **empirical data / reasoning** behind it, **alternatives considered**, and **consequences**. Inferred from code, comments, commit messages, and the self-documenting `add_learning.py`.

---

### D-001 · Host on a self-owned Linux laptop + Cloudflare Tunnel (not a cloud VPS)
- **Decision:** Serve the app from an old laptop at `192.168.1.150` and expose it globally with `cloudflared tunnel --url http://localhost:5001`.
- **Why:** Wanted worldwide access with **$0 hosting cost**, no AWS/Render, and **no SQLite→Postgres migration**.
- **Empirical data / reasoning (from `add_learning.py`, self-documented as a challenge):** Cloudflare Tunnel makes **outbound** connections to Cloudflare's edge, so **no firewall ports need opening** and no public IP/port-forwarding is required. Verified working → produced a free `*.trycloudflare.com` URL.
- **Alternatives:** AWS/Render (cost + Postgres migration), ngrok/localhost.run/serveo (kept as fallbacks in `get_public_url.sh`).
- **Consequences:** Availability depends on a home laptop + home internet → drove the **watchdog + systemd Restart=always + lid-close=ignore** resilience work. Tunnel URLs are ephemeral (`trycloudflare` rotates) unless a named tunnel is configured.

### D-002 · SQLite (not Postgres/MySQL), hardened for concurrency
- **Decision:** Keep SQLite as the production DB; tune it for threaded gunicorn.
- **Why:** Simplicity, zero-ops, single-file portability; avoids a migration the owner explicitly didn't want (D-001).
- **Empirical data / reasoning:** Under concurrent writes SQLite throws "database is locked." Mitigations applied on *every* connection: `PRAGMA journal_mode=WAL` (concurrent read/write), `synchronous=NORMAL` (fast but crash-safe), `cache_size=-64000` (64MB), `foreign_keys=ON`; plus `check_same_thread=False` and `timeout=15`.
- **Alternatives:** Postgres (rejected: ops + migration cost).
- **Consequences:** Fine for a low-traffic portfolio; would not scale to high write concurrency. WAL files (`*.db-wal`,`*.db-shm`) live alongside the DB.

### D-003 · Append-only, forward-compatible schema
- **Decision:** Never DROP tables/columns; only ADD tables or nullable columns. All migrations additive.
- **Why:** Protect months of historical challenge data; a solo project where data loss is unrecoverable.
- **Empirical consequence:** The `NOT NULL` `image_path` couldn't be relaxed, so FCC-synced rows use `image_path=""` and templates test truthiness. New features (`quote_text`, `qa_text`, user tables) were added, never reshaped.
- **Alternatives:** Normal destructive migrations (rejected by policy).
- **Consequences:** Schema accretes columns; some model columns bypass Alembic and rely on `db.create_all()`.

### D-004 · Run visitor Python **client-side** with Pyodide (WASM)
- **Decision:** Execute user code and challenge tests in the browser via Pyodide, not on the server.
- **Why:** Let visitors practice safely; **no server-side sandbox, no infra cost, no RCE risk** from untrusted code.
- **Empirical data / reasoning:** FCC provides real Python tests. The app regex-extracts the pure Python from FCC's JS wrapper `runPython(\`…\`)`, unescapes `\n`/`\"`, and runs each assertion in Pyodide. Pass=green tick+confetti; fail=red+truncated traceback.
- **Alternatives:** Server-side exec (rejected: security), Judge0/remote executor (rejected: cost/complexity).
- **Consequences:** ~heavy first-load (Pyodide WASM download); mitigated with a "sleek cursor" loading affordance (`62e0b74`). Debounced live-run at 800ms balances responsiveness vs CPU.

### D-005 · Autonomous daily content via FCC API sync
- **Decision:** A cron job runs `fcc_sync.py` daily at 00:30 US Central; a watchdog re-syncs after outages.
- **Why:** Content should stay current with **zero daily manual effort**.
- **Empirical data / reasoning:** 00:30 Central chosen to align with FCC's release + the owner's timezone (comment: "= 6:00 AM IST"). 0.3s inter-request delay during backfill to "be polite to FCC's servers." Sync **won't overwrite** manual content (`source=='manual' and fcc_description` ⇒ skip).
- **Alternatives:** Manual entry only (rejected: toil), webhook (FCC offers none).
- **Consequences:** Depends on FCC API stability & schema; 404 handled as "not released yet."

### D-006 · Telegram bot as mobile admin / AI agent gateway ("OpenClaw")
- **Decision:** Control the server & publish content from a phone via Telegram, with an LLM brain and shell/Python execution.
- **Why:** Owner wanted to run/admin the server and add challenges on the go (photo → website in one step).
- **Empirical data / reasoning:** Photo pipeline = OCR date/title + OpenCV branding-crop + DB upsert. Chat routes to Grok or Gemini (auto-detected by API-key prefix). A ReAct loop (`[RUN_SHELL: …]`, ≤3 iterations) lets the model inspect the server to answer accurately.
- **Alternatives:** SSH-only admin (rejected: not mobile-friendly), a real web admin (partially exists but unauthenticated).
- **Consequences:** ⚠️ Major attack surface — arbitrary shell/Python/LLM-driven execution. Guarded only by a single admin chat ID; the **bot token is committed to a public repo**. See [08-security.md](08-security.md).

### D-007 · Dual LLM backend (Grok primary, Gemini fallback), auto-detected
- **Decision:** Support xAI Grok (`grok-2`) and Google Gemini; pick by key prefix (`AIzaSy…` ⇒ Gemini REST, else Grok via OpenAI SDK w/ `base_url=https://api.x.ai/v1`).
- **Why:** Flexibility / resilience if one provider fails or a key is unavailable.
- **Empirical data / reasoning:** The 03-15 commit burst (`0af4aaf`→`76a5a1b`) shows iterative testing of Gemini model names (`gemini-1.5-flash`, `2.0-flash`, `2.5-flash`, `pro`) with fallback iteration until one responds.
- **Consequences:** Two code paths for history/formatting; keys read from `claw_config.json` on the server.

### D-008 · Editorial "Scientific American"-inspired brand kit
- **Decision:** Serif (Crimson Text) headings, sans (Libre Franklin) UI, JetBrains Mono code; palette blue `#00719a`, red `#a70e13`, tan `#e8d3be`; sharp corners (`radius-sm=2px`).
- **Why:** A distinctive, magazine-like editorial identity vs generic Bootstrap.
- **Consequences:** CSS variables in `style.css`; many templates use inline styles referencing these tokens.

### D-009 · Anti-copy "shields" (right-click + devtools blockers)
- **Decision:** Disable context menu and F12/Ctrl+Shift+I/J/Ctrl+U in `base.html`; images `pointer-events:none` / `oncontextmenu=return false`.
- **Why:** Deter casual copying of solutions/images.
- **Empirical reality:** These are **trivially bypassed** (disable JS, view-source, network tab). Cosmetic deterrent only; also mildly hostile to legitimate users. Recorded as a known-weak control.

### D-010 · Mock OTP registration + stubbed OAuth
- **Decision:** Registration collects name/email/mobile/DOB, then a **mock** 6-digit OTP (shown in a flash message) creates the user. Google/GitHub buttons redirect to real OAuth authorize URLs but callbacks are stubbed (just flash + redirect).
- **Why:** Ship the auth *flow/UX* without wiring an SMS provider or completing OAuth token exchange yet.
- **Consequences:** Not real security — the OTP is displayed to the user; anyone can register. GitHub OAuth requests `repo` scope (comment: "for automated pushes!") — a broad scope to keep in mind when it's completed.

### D-011 · Store third-party tokens in the `users` table
- **Decision:** `github_token` and `claude_token` columns on `User` to persist per-user API tokens.
- **Why:** Enable future automated GitHub pushes and per-user Claude usage.
- **Consequences:** ⚠️ Plaintext token storage in SQLite; needs encryption-at-rest or a secrets manager before real use.

### D-012 · Scrub third-party branding from ingested content
- **Decision:** `scrub_db.py` strips "freeCodeCamp"; `scrape_book.py` rewrites "IIT Madras"/"IITM"/"BSc Degree" → "University"/"Python Course".
- **Why:** Present a clean, self-branded learning surface.
- **Consequences:** ⚠️ Attribution/licensing consideration when republishing others' content (FCC, IIT-M textbook). Worth a licensing review. See [10-open-questions.md](10-open-questions.md).

### D-013 · SonarQube-driven code quality pass
- **Decision:** Late refactors to satisfy SonarQube (async issues, label-for association, HTTP method correctness, duplicate literals like `USERS_ID_REF`, string ops).
- **Why:** Enforce a maintainability/quality bar.
- **Consequences:** Introduced constants (e.g. `USERS_ID_REF='users.id'`, `NO_OUTPUT_MSG`) and cleaner handlers; secrets were *not* caught/removed by this pass.
