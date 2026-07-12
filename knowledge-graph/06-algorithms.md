# 06 · Algorithms & Techniques

Every non-trivial algorithm/technique in the codebase, what it does, and why it was chosen.

---

## A-1 · FCC test extraction (JS wrapper → pure Python)
**Where:** `app.py` `challenge_detail()`.
**Problem:** FCC stores Python test assertions inside a JavaScript wrapper string like ``runPython(`assert add(1,2)==3`)`` with escaped `\n` and `\"`.
**Algorithm:**
1. `json.loads(challenge.fcc_py_tests)` → list of `{text, testString}`.
2. Regex `runPython\(\`(.*?)\`\)` with `re.DOTALL` extracts the backtick-quoted body.
3. Unescape: `\\n → \n`, `\\" → "`.
4. Store as `fcc_py_tests_parsed` for the template; each assertion later runs in Pyodide.
**Why:** Reuse FCC's real tests without a JS runtime — extract the Python and run it directly in the browser Python VM.

## A-2 · Pyodide client-side execution + test runner
**Where:** `challenge_detail.html` `extra_js`.
**Technique:** Pyodide (CPython→WASM) in the browser.
- **stdout/stderr capture:** `pyodide.setStdout/setStderr({batched})` append to a console `<div>`, HTML-escaping `<`/`>`.
- **Live run (debounced 800ms):** on CodeMirror `change`, redirect `sys.stdout/stderr` to a `StringIO`, run user code, read back the buffer.
- **Run Tests:** run user code once (defines functions in the global namespace), then execute each extracted assertion in sequence; catch exceptions per test → red X, else green check. `AssertionError` messages are collapsed to a friendly line.
- **Reward:** if all pass → `canvas-confetti` burst + "XP GAINED +100".
**Why:** Safe (D-004), free, no server; immediate feedback loop for learners.
**Known caveat:** each debounced run reassigns `sys.stdout/stderr` to a fresh `StringIO` but doesn't restore them; session state persists between runs by design (globals carry over).

## A-3 · Hourly quote cache
**Where:** `app.py` `get_daily_quote()`.
**Algorithm:** cache key = `strftime('%Y-%m-%d-%H')`. If `data/quote_cache.json` matches the current hour, serve it; else fetch a random quote from FCC's `motivation.json`, cache it, and serve. Falls back to a hardcoded Lincoln quote on any error.
**Why:** Fresh-feeling content without hitting the network every request; resilient to network failure. Evolved from 24h (`dee9cd5`) → hourly (`8696d73`) after 24h felt stale.

## A-4 · Calendar matrix rendering
**Where:** `app.py` `challenges()` + `challenges.html`.
**Algorithm:** Collect distinct `(year, month)` from all `date_id`s; for each, use Python's `calendar.monthcalendar(year, month)` to get week-row matrices (0 = padding day); map `day → Challenge`. Template renders a 7-col CSS grid; the most recent month renders as the big grid, older months via a Flatpickr inline archive.
**Client-side guards:** future dates → "you'll need a time machine"; dates < `2025-08-11` → "challenge started 11th August 2025"; missing known date → offer to email the admin. Timezone bug avoided by computing "today" in local time (`Date.now() - tzoffset`).
**Why:** Familiar month-grid mental model; `calendar` stdlib avoids manual week math.

## A-5 · FCC challenge upsert (idempotent, source-aware)
**Where:** `fcc_sync.py` `upsert_challenge()`.
**Algorithm:**
1. Normalize date (`split('T')[0]` if ISO datetime).
2. Serialize JS/Py tests to JSON; extract starter code via `extract_starter_code()` (handles list-of-dicts and dict-of-files shapes, returns first `contents`).
3. If row exists: skip if it's manual+already-described (protect manual content), else update only `fcc_*` fields; set `source='fcc_api'` if unset.
4. Else insert new row with `image_path=""` (append-only constraint, A/D-003).
**Why:** Runs daily and on backfill; must be idempotent and must never clobber hand-authored content.

## A-6 · Backfill with polite rate limiting
**Where:** `fcc_sync.py` `backfill()`.
**Algorithm:** iterate day-by-day from `2025-08-11` → today; fetch+upsert; `time.sleep(0.3)` between requests; tally inserted/updated/skipped/errors.
**Why:** One-shot catch-up of the full history without hammering FCC's API.

## A-7 · OCR challenge-info extraction
**Where:** `ocr_helper.py`.
**Algorithm:** `pytesseract.image_to_string` on the image; regex for `Month DD, YYYY` → `dateparser.parse` → `YYYY-MM-DD`; title = first prominent line that isn't the "Daily Coding Challenge" header, the date line, or a nav arrow (`«`).
**Why:** Turn a phone screenshot into structured `(date_id, title)` automatically for the Telegram pipeline.
**Caveat:** heuristic; brittle to layout/format changes.

## A-8 · Surgical image cleaning + framing
**Where:** `image_processor.py` `clean_image()` (OpenCV).
**Algorithm:**
1. Crop top 12% (FCC logo) and below 94% (mobile-app footer).
2. Sample theme color at `img[top_crop/2, width/2]`.
3. `cv2.copyMakeBorder` a 12px border in that sampled color to "close the frame."
4. Overwrite the file in place.
**Why:** Remove third-party branding and produce a uniform "framed" thumbnail. Cropping % were tuned empirically (`856249e`).
**Caveat:** in-place overwrite is not idempotent — reprocessing re-crops an already-cropped image.

## A-9 · Telegram agent ReAct loop
**Where:** `telegram_bridge.py` `handle_message()`.
**Algorithm:** system prompt instructs the LLM to emit `[RUN_SHELL: <cmd>]` when it needs server facts. Loop ≤3 times: call LLM → regex-detect the tag → run `subprocess.run(cmd, shell=True, timeout=15)` → append output to history → re-ask. Exit when no tag → final reply. Empty replies get a guard message.
**Why:** Let the model ground answers in real server state (files, DB, resource counts).
**⚠️ Risk:** unrestricted shell execution driven by an LLM. See [08-security.md](08-security.md).

## A-10 · Network watchdog state machine
**Where:** `network_watchdog.sh` (systemd timer, 2-min).
**Algorithm:** `ping -c1 -W3 8.8.8.8`; compare to last state in `.watchdog_state`. On `offline→online` transition: run `fcc_sync.py` catch-up, restart `portfolio` and `nginx` if inactive; persist new state.
**Why:** Home-internet outages are expected (D-001); auto-recover missed syncs and dead services without manual intervention.

## A-11 · SSH bootstrap + tunnel URL polling
**Where:** `deploy_tunnel.py`.
**Algorithm:** paramiko connect with password (one-time) → install local pubkey into `authorized_keys` (dedup via `grep -qF`) for passwordless future logins → ensure app is up on 5001 (systemd or nohup) → install `cloudflared` to `~/.local/bin` if missing → kill stale tunnels → start tunnel, poll log up to 35s, regex `https://…trycloudflare\.com` → print URL.
**Why:** One-command "make my site public" from a Windows dev box.

## A-12 · Client-side registration validation
**Where:** `register.html`.
**Algorithm:** live `input` listeners; email regex `^[^\s@]+@[^\s@]+\.[^\s@]+$`; mobile "valid" if length ≥ 10 (a stricter generic phone regex is defined but the length check gates the button). Submit disabled until name+email+mobile valid.
**Why:** Instant feedback UX. **Note:** server re-validates minimally (presence + DOB parse + duplicate check); the strong validation is only client-side.
