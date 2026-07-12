# 04 · Chronological Timeline

Every commit in `main`, oldest → newest, with what it did and why. This is the project's memory of *what happened, when, and in what order.*

> The **repo** (`portfolio-v2`) history runs **2026-03-08 → 2026-03-16** (44 commits). The **challenge content** it manages spans **2025-09-09 → 2026-02-23** (150 images) and the FCC challenge series itself starts **2025-08-11**. So the git dates reflect when this v2 codebase was pushed, not when the learning journey began. Local file paths in deploy scripts (`Desktop\Test Folder\My Portfolio\portfolio`) confirm there was a pre-v2 working copy.

## Phase 0 — Pre-repo (context, not in git)
- **2025-08-11** — FCC daily coding challenge series begins (challenge #1, "Vowel Balance"). Hardcoded as `FCC_START_DATE` in `fcc_sync.py`; also surfaced to users ("Daily coding challenge started from 11th August 2025").
- **2025-09-09 → 2026-02-23** — 150 challenge screenshots accumulated in `static/images/` (`20250909_unique_characters.jpg` … `20260223_challenge_2026_02_23.jpg`).
- **2026-02-22/23** — Initial Alembic schema authored (migration create-dates), predating the v2 push.

## Phase 1 — v2 foundation & interactivity (2026-03-08 → 03-09)
| Date | Commit | Change | Why / notes |
|------|--------|--------|-------------|
| 03-08 | `3ad3c2a` | "Portfolio sync for Pella deployment" | First v2 commit — the baseline app. |
| 03-09 | `dee9cd5` | Auto-refresh daily quote from FCC w/ 24h cache | Autonomy: no manual quote curation. (Later tightened to hourly.) |
| 03-09 | `e1ab782` | Add Pyodide interactive Python interpreter; remove JS tab & auto-sync badge | **Key decision:** run Python in-browser; drop JS focus → Python-only identity. |
| 03-09 | `b09586b` | Fully remove "Auto-Synced" badge | UI cleanup — hide the plumbing from visitors. |
| 03-09 | `62e0b74` | Replace Pyodide loading text with sleek cursor (match FCC) | Perceived-performance / brand polish. |

## Phase 2 — Mobile agent bot & server automation (2026-03-15)
A burst of 18 commits in one day — building the "OpenClaw" Telegram bot and its server tooling.
| Commit | Change | Why / notes |
|--------|--------|-------------|
| `9d9a7c4` | Update Grok model to `grok-2` | Bot brain = xAI Grok. |
| `856249e` | Fix image processor cropping + bot health logging + grok model | Tuning OCR/clean pipeline. |
| `85c2ff4`,`a1c6766`,`92d0bb3` | Add + expand + detailed **DB inspector** tools | Debugging the live DB remotely (`inspect_db*.py`). |
| `3c9926a` | Add **DB fixer** (`fix_db.py`) | Clear a wrong `image_path` on 2026-03-15 to restore API-card fallback. |
| `8696d73` | Quote cache → hourly | Empirical tweak: 24h felt stale; hourly is fresher yet still cached. |
| `c88cf11` | xAI model lister tool | Discover available models. |
| `0af4aaf`,`add2916`,`3a7ddb2`,`cb5b561` | Gemini validation / REST / list / filter tests | Evaluating **Gemini as alternate bot brain**. |
| `76a5a1b` | Dynamic Google Gemini auto-detect + REST fallback | **Decision:** support both Grok and Gemini; auto-detect by key prefix (`AIzaSy…` ⇒ Gemini). |
| `7d49ca2` | Server Config Initializer | Bootstrap `claw_config.json`. |
| `5747577` | **Agentic ReAct loop** for terminal inspections | Bot can emit `[RUN_SHELL: …]`, execute, feed back (≤3 loops). |
| `fa94958`,`3173844`,`9c7bbdf` | Start-trace runner, systemd installer, systemd shell wrapper | Make the bot/app run as resilient services. |
| `f6091eb` | Empty-reply guards on edit turns | Handle LLM empty responses / safety blocks gracefully. |

## Phase 3 — Hardening, cleanup, users & community (2026-03-16)
The final 20 commits: SonarQube fixes, secret scrubbing, user accounts, discussion board, gamified feedback.
| Commit | Change | Why / notes |
|--------|--------|-------------|
| `32f1206` | Fix multiple SonarQube blocking async issues | Static-analysis-driven refactor. |
| `6f3a419`,`b91917f` | API Config scrubber wrapper / shell scrubber | Remove leaked config/keys from artifacts. |
| `e057644` | **Remove all test & deployment shell helper scripts** | Cleanup (some later re-added). |
| `3cf10c3`,`4fbc9a5` | Fix Problem Statement redundancy / remove card header ribbon | Layout polish on detail/home. |
| `6474d5d` | Python textbook scraper + scrub cleaner (`scrape_book.py`,`scrub_db.py`) | Ingest IIT-M BSc Python textbook, scrub "IIT Madras"/"freeCodeCamp" branding. |
| `8f46abb` | **User & Notebook additive tables** | New models: User, ConceptStrength, UserNotebook, Comment. |
| `bd565d9` | Debounced live execution with Pyodide | 800ms live-run as you type. |
| `c5072b1` | User navbar items + **Right-Click Blocker shields** | Anti-copy: disable context menu + F12/Ctrl+Shift+I/J/Ctrl+U. |
| `789903e`,`0f2d264` | Verify-tables + explicit table-creator debug scripts | Ensure new tables exist on server. |
| `23750e4` | Remove "Join Network"; fix black-ribbon white-text contrast | Accessibility/contrast. |
| `cf7aae1` | SonarQube: label association, HTTP methods, string replace, dup literals | Code-quality gate. |
| `c5d8c78` | Social Login buttons + unconditional interpreter + forced contrast | Add Google/GitHub buttons; interpreter always on. |
| `52c265f` | Restructure `register.html`: instant validation + toggles | Client-side email/mobile validation; manual-register toggle. |
| `3f76a88` | Satisfaction popup tracking + API notification bridge | Emoji ratings → `/api/rate` → Telegram. |
| `ef42e9d` | Confetti trigger / "Dopamine multiplier" | Gamification on all-tests-pass. |
| `1cc2c9a` | Satisfaction suggestions + user session name + standard OAuth redirects | Real Google/GitHub OAuth *redirect* structure (callbacks stubbed). |
| `e084129` | **Add "Run Code" button + live stdout capture in console** | Latest commit (HEAD). Manual run separate from tests. |

## What the timeline reveals (patterns)
1. **Three sprints, each a theme:** (1) interactivity, (2) mobile-agent automation, (3) community + hardening.
2. **Heavy automation bias** — a lot of effort went into *autonomous operation* (self-syncing content, self-healing server, phone-driven admin) rather than manual maintenance.
3. **AI-in-the-loop everywhere** — Grok/Gemini bot brain, ReAct shell loop, OCR extraction, "Antigravity" markdown extraction referenced in the admin UI.
4. **Quality gates late** — SonarQube fixes and secret-scrubbing appear in Phase 3, suggesting analysis was bolted on near the end (and secrets remained; see [08-security.md](08-security.md)).
