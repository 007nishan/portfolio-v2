# 08 · Security Findings & Risks

> ⚠️ **This is a PUBLIC repository (`github.com/007nishan/portfolio-v2`) that contains live secrets and remote-code-execution surfaces.** Treat everything below as *exposed to the internet* until proven otherwise. Severities are the author's assessment for this project's context.

## 🔴 CRITICAL

### S-1 · Hardcoded server SSH password in a public repo
- **What:** `PASSWORD = "6WKW5_3w2w5121"` for `nishan@192.168.1.150`.
- **Where:** `deploy_tunnel.py`, `deploy_bridge.py`, `security_harden.py`, `server_maintenance.py`, `remote_backfill.py`, `fix_sudo.py`, `push_templates.py` (7 files).
- **Impact:** Anyone who reads the repo has the server login. Combined with `192.168.1.150` being a LAN IP, direct exploitation needs LAN access — **but** the password is very likely reused, and the box is internet-exposed via the tunnel.
- **Fix:** Rotate the password now; switch to SSH keys only; **purge from git history** (`git filter-repo`/BFG); move to `.env`/secrets. Assume compromised.

### S-2 · Live Telegram bot token committed
- **What:** `TOKEN/bot_token = "8571904781:AAEhaViQiEihWOHShd0a0ywJ0BMufSh13p8"`.
- **Where:** `telegram_bridge.py` (line 17) and `app.py` `/api/rate` (line ~591), plus `chat_id = "8687680759"`.
- **Impact:** Anyone can drive the bot's API. Because the bot executes shell/Python on the server (S-3), a leaked token is close to **full server takeover** — the only extra gate is the admin chat-ID check, and the admin ID is auto-claimed by the *first* user to `/start` if `admin_id.txt` doesn't exist (race/land-grab risk on a fresh deploy).
- **Fix:** Revoke via BotFather immediately; issue a new token; store server-side only; purge history.

### S-3 · Remote code execution by design (Telegram bot)
- **What:** `telegram_bridge.py` runs arbitrary **shell** (`$ <cmd>` → `subprocess.run(shell=True)`), arbitrary **Python** (```` ```code``` ```` → temp file executed), and an **LLM ReAct loop** that executes `[RUN_SHELL: …]` the model emits.
- **Impact:** Full command execution as `nishan` (and via NOPASSWD sudo, as root — see S-6). Guarded only by admin chat ID (S-2 caveat).
- **Fix:** If the agent bot is kept: allowlist commands, drop `shell=True`, sandbox, run as an unprivileged user, add explicit human confirmation, and never on a public token.

### S-4 · `/admin` route has no authentication
- **What:** `@app.route("/admin", methods=["GET","POST"])` accepts file uploads and upserts challenges with **zero auth**.
- **Impact:** Anyone who finds the URL can upload files (arbitrary write into `static/images/`) and overwrite/insert any challenge content — defacement + potential storage abuse. `MAX_CONTENT_LENGTH=16MB` and an extension allowlist (`png/jpg/jpeg/gif`) limit but don't prevent abuse.
- **Fix:** Require login + admin role (session already exists); at minimum gate behind auth before exposing publicly.

## 🟠 HIGH

### S-5 · Code injection via f-string in photo pipeline
- **What:** `telegram_bridge.handle_photo()` builds a Python script by f-string-interpolating the OCR-extracted `title` and `target_date` directly into source that is then executed with `python -c`.
- **Impact:** A crafted image whose OCR'd title contains quotes/newlines/code can inject Python. Lower likelihood (needs bot access, S-2), but a real injection sink.
- **Fix:** Pass values as argv/stdin/JSON, not string-interpolated code; or use the ORM in-process.

### S-6 · Passwordless sudo (`NOPASSWD:ALL`)
- **What:** `server_maintenance.py` and `fix_sudo.py` write `nishan ALL=(ALL) NOPASSWD:ALL` to `/etc/sudoers.d/`.
- **Impact:** Any code running as `nishan` (incl. the bot, S-3) escalates to root with no prompt.
- **Fix:** Remove the NOPASSWD rule; scope sudo to specific commands if automation truly needs it.

### S-7 · Flask debug mode in the entrypoint
- **What:** `app.run(debug=True, host="127.0.0.1", port=5001)`.
- **Impact:** If ever bound to a public interface (or proxied without care), the Werkzeug interactive debugger enables **RCE** via the console PIN, plus verbose stack traces. Currently bound to localhost and fronted by the tunnel, which reduces but doesn't eliminate risk.
- **Fix:** `debug=False` in production; run under gunicorn (already a dependency).

### S-8 · Weak `SECRET_KEY` default
- **What:** `SECRET_KEY` falls back to `"default-dev-key-change-this-in-env"` if the env var is unset.
- **Impact:** If the server runs without `.env`, session cookies are forgeable → session hijack / privilege issues once auth matters.
- **Fix:** Fail closed (refuse to boot) if `SECRET_KEY` is missing in production.

## 🟡 MEDIUM

### S-9 · Telegram notification uses unescaped GET URL
- **What:** `/api/rate` sends the message via `requests.get(f".../sendMessage?...&text={msg}")` with user-supplied `suggestion` unescaped in the query string.
- **Impact:** URL/param injection into the Telegram call; malformed/oversized input; minor SSRF-ish surface. Wrapped in try/except (fault tolerant) so failures are silent.
- **Fix:** Use `params=`/POST body with proper encoding; validate/limit input length.

### S-10 · Plaintext third-party tokens in DB
- **What:** `users.github_token`, `users.claude_token` (String(255)), no encryption. GitHub OAuth requests broad `repo` scope.
- **Impact:** DB compromise leaks users' GitHub/Claude tokens; broad scope amplifies blast radius.
- **Fix:** Encrypt at rest or use a secrets store; request minimal OAuth scopes.

### S-11 · Mock OTP / stubbed OAuth presented as auth
- **What:** OTP is shown to the user in a flash message; OAuth callbacks are stubbed. Anyone can register/verify.
- **Impact:** No real identity assurance; not a breach by itself, but don't rely on it for access control (S-4 shouldn't depend on it either).
- **Fix:** Wire a real SMS/OTP provider and complete OAuth token exchange before treating accounts as trusted.

### S-12 · Client-side "security" is cosmetic
- **What:** Right-click/devtools blockers, `pointer-events:none`, `oncontextmenu=return false`.
- **Impact:** Trivially bypassed; provides *no* protection and slightly harms UX/accessibility. Do not mistake for a control.

## Positive notes / good practices already present
- ✅ Visitor code runs **client-side** (Pyodide) — no server exec of untrusted user code (contrast with S-3, which is the bot, not visitors).
- ✅ Uploads use `secure_filename`, an extension allowlist, and a 16MB cap.
- ✅ SQLite `foreign_keys=ON` enforces referential integrity.
- ✅ `.gitignore` correctly excludes `.env`, `data/`, `*.db` (so the DB & env aren't committed — but secrets are hardcoded in source, defeating this).
- ✅ `security_harden.py` sets up UFW + Fail2Ban + disables root SSH login (partial hardening intent).

## Remediation priority (recommended order)
1. **Rotate** SSH password (S-1) and **revoke** Telegram token (S-2) — do this first.
2. **Purge secrets from git history** and force-push (or make repo private).
3. **Auth-gate `/admin`** (S-4) and set `debug=False` (S-7).
4. Remove **NOPASSWD sudo** (S-6); fix the bot exec surface (S-3/S-5) or take the bot offline.
5. Enforce a real `SECRET_KEY` (S-8); encrypt tokens (S-10); fix `/api/rate` encoding (S-9).

*Nothing here has been changed yet — this is a findings inventory. Await the user's go-ahead before remediating.*
