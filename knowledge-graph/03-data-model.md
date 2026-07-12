# 03 · Data Model

Database: **SQLite**, file `data/portfolio.db` (gitignored). URI `sqlite:///.../data/portfolio.db`.
ORM: **Flask-SQLAlchemy**. Defined in [`models.py`](../models.py).

## ⚖️ HARD RULE: Append-only, forward-compatible schema
> From `models.py`: *"the database schema must NEVER be destructively altered. Do not DROP tables or DROP columns even if features are deprecated. We only expand (ADD new tables, ADD nullable columns) to ensure backward compatibility for all historical data versions."* All migrations MUST be additive.

**Why:** preserves all historical challenge data across the app's lifecycle; a solo project where losing months of solved challenges would be catastrophic and hard to recover. New features add nullable columns rather than reshaping existing ones.

**Empirical consequence:** in `fcc_sync.py`, new FCC-synced rows set `image_path=""` (empty string) instead of NULL, because the original `image_path` column was created `NOT NULL` and that constraint can't be altered without a destructive migration. Templates therefore check *truthiness* of `image_path`, not NULL.

---

## Tables

### `challenges` — the central content table
| Column | Type | Constraints | Purpose |
|--------|------|-------------|---------|
| `id` | Integer | PK | |
| `date_id` | String(10) | unique, not null | `YYYY-MM-DD`, the natural key for a day's challenge |
| `title` | String(255) | not null | Challenge title |
| `image_path` | String(255) | **not null** (originally) | Filename in `static/images/`; `""` for API-only rows |
| `problem_text` | Text | nullable | Manual markdown problem statement |
| `concepts_text` | Text | nullable | Manual markdown concepts breakdown |
| `solution_code` | Text | nullable | The final solution code |
| `quote_text` | Text | nullable | Motivational quote (added migration `f8faeae5ecde`) |
| `qa_text` | Text | nullable | Q&A section (added migration `49b711d2aba8`) |
| `challenge_number` | Integer | nullable | FCC challenge # (1, 2, … 211+) |
| `fcc_description` | Text | nullable | Full HTML description from FCC API |
| `fcc_js_tests` | Text | nullable | JSON string of JS test cases |
| `fcc_py_tests` | Text | nullable | JSON string of Python test cases (parsed for Pyodide) |
| `fcc_starter_js` | Text | nullable | JS starter template |
| `fcc_starter_py` | Text | nullable | Python starter template |
| `source` | String(20) | nullable | `'manual'` or `'fcc_api'` |
| `created_at` | DateTime | default utcnow | |
| `updated_at` | DateTime | default utcnow, onupdate | |

> Note: `challenge_number` and all `fcc_*` columns exist in the **model** but are **not** in any Alembic migration file. They are created via `db.create_all()` (called in `fcc_sync.py`, `create_*_tables.py`). So the live schema depends on `create_all()` having run, not purely on migrations. See [10-open-questions.md](10-open-questions.md).

### `users` — registered accounts
| Column | Type | Constraints | Purpose |
|--------|------|-------------|---------|
| `id` | Integer | PK | |
| `name` | String(100) | not null | |
| `email` | String(120) | unique, not null | |
| `mobile` | String(20) | unique, not null | Comment calls it "PRIMARY KEY lookup standard" |
| `dob` | Date | not null | |
| `profile_pic` | String(255) | nullable | |
| `github_id` | String(50) | nullable | 3rd-party integration |
| `github_token` | String(255) | nullable | For repo saving (stored **plaintext**) |
| `claude_token` | String(255) | nullable | Personal API usage (stored **plaintext**) |
| `created_at` | DateTime | default utcnow | |
| `is_verified` | Boolean | default False | OTP verification tracker |

> ⚠️ `github_token` / `claude_token` are designed to hold plaintext third-party API tokens in SQLite. No column-level encryption. See [08-security.md](08-security.md).

### `concept_strengths` — per-user concept mastery scores
| Column | Type | Notes |
|--------|------|-------|
| `id` | Integer PK | |
| `user_id` | FK → `users.id`, not null | |
| `concept` | String(100), not null | |
| `score` | Integer, default **100** | 100 base; +10 reward / −10 penalty (per model comment) |
| `times_encountered` | Integer, default 0 | |
| `updated_at` | DateTime | |

**Algorithm intent (documented, not yet wired to UI):** a reward/penalty model — correct answers `+10`, penalties `−10`, base `100`. The dashboard renders `score` as a progress bar (`max=200`). No code currently writes to this table (no gameplay loop yet).

### `user_notebooks` — personal per-challenge summaries
| Column | Type | Notes |
|--------|------|-------|
| `id` | Integer PK | |
| `user_id` | FK → `users.id`, not null | |
| `challenge_id` | FK → `challenges.id`, not null | |
| `summary_notes` | Text, nullable | "Auto-generated summary of start-to-end nodes mapping" |
| `created_at` | DateTime | |

Intended for the "continuous notes / Learning Ledger" idea (`continuous_notes.py`). Not yet populated by any live code path.

### `comments` — discussion board
| Column | Type | Notes |
|--------|------|-------|
| `id` | Integer PK | |
| `user_id` | FK → `users.id`, not null | |
| `challenge_id` | FK → `challenges.id`, not null | |
| `text` | Text, not null | |
| `created_at` | DateTime | |
| relationship | `user` → `User` (backref `comments`) | for rendering author names |

## Relationships (ER summary)
```
users 1───∞ comments ∞───1 challenges
users 1───∞ concept_strengths
users 1───∞ user_notebooks ∞───1 challenges
```

## Migration history (Alembic)
| Order | Revision | Date | Change |
|-------|----------|------|--------|
| 1 | `704755926c31` | 2026-02-22 | Initial `challenges` table (id, date_id, title, image_path NOT NULL, problem/concepts/solution text, timestamps) |
| 2 | `f8faeae5ecde` | 2026-02-23 | Add `quote_text` (batch_alter, additive) |
| 3 | `49b711d2aba8` | 2026-03-08 | Add `qa_text` (batch_alter, additive) |

The `fcc_*`, `challenge_number`, `source`, and all the user/comment tables are **not** covered by migrations — they rely on `db.create_all()`.

## Caches / non-DB persisted state
- `data/quote_cache.json` — hourly quote cache (key = `YYYY-MM-DD-HH`).
- `data/sync_log.txt`, `data/cron_sync.log`, `data/watchdog.log`, `data/.watchdog_state` — operational logs/state.
- `admin_id.txt`, `claw_config.json` (Grok key), `bot_health.log` — Telegram bot state on the server.
