#!/usr/bin/env python3
"""
import_challenges.py
--------------------
Rebuild the ``challenges`` table from the committed per-day JSON files in
``content/challenges/``. This is the JSON→DB half of the GitHub-as-buffer
round-trip (``export_challenges.py`` is the DB→JSON half).

ROLE IN THE ARCHITECTURE
    Every host is a pure CONSUMER of git: it pulls the repo and runs this to make
    its local DB reflect the committed content. No FCC-API call is needed at boot,
    so a fresh ``git clone`` — on this laptop, the server, or a cloud runner —
    yields an identical, fully-populated site. The daily GitHub Action is the only
    thing that WRITES new content; this only READS committed JSON into a DB.

SAFETY INVARIANTS (deliberate, load-bearing — see knowledge-graph)
    1. IDEMPOTENT UPSERT, never drop/recreate. Re-running changes nothing if the
       JSON matches the DB. The table is only ever expanded/updated in place.
    2. NEVER TOUCHES USER TABLES. This only writes ``challenges``. User-generated
       data (users, comments, concept_strengths, user_notebooks) lives ONLY in the
       gitignored DB and is never in git — so importing must never delete or alter
       it. We upsert challenge rows and leave every other table untouched.
    3. PROTECTS AUTHORED CONTENT. A manual /admin row (source='manual' with a real
       description) is not clobbered by a blank imported field — mirrors the guard
       in fcc_sync.upsert_challenge. JSON is authoritative for challenge content,
       but we still won't overwrite a non-empty authored field with an empty one.

USAGE
    python import_challenges.py            # import all JSON → DB (upsert)
    python import_challenges.py --date 2026-07-30
    python import_challenges.py --quiet
"""

import os
import sys
import json
import argparse

basedir = os.path.abspath(os.path.dirname(__file__))
if basedir not in sys.path:
    sys.path.insert(0, basedir)

from app import app
from models import db, Challenge

CONTENT_DIR = os.path.join(basedir, "content", "challenges")

# Fields the import is allowed to write. Kept in sync with export_challenges.
# date_id is the key and is handled separately.
IMPORT_FIELDS = [
    "challenge_number",
    "title",
    "source",
    "image_path",
    "fcc_description",
    "fcc_js_tests",
    "fcc_py_tests",
    "fcc_starter_js",
    "fcc_starter_py",
    "problem_text",
    "concepts_text",
    "solution_code",
    "quote_text",
    "qa_text",
]

# NOT NULL columns need a safe default if the JSON somehow omits them.
_NOT_NULL_DEFAULTS = {"title": "Untitled Challenge", "image_path": ""}


def _load_json_files(single_date=None):
    """Yield (date_id, data_dict) for each JSON file, sorted by date."""
    if not os.path.isdir(CONTENT_DIR):
        return
    names = sorted(f for f in os.listdir(CONTENT_DIR) if f.endswith(".json"))
    for name in names:
        date_id = name[:-5]  # strip ".json"
        if single_date and date_id != single_date:
            continue
        path = os.path.join(CONTENT_DIR, name)
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            print(f"  ! skipping {name}: {e}")
            continue
        # Trust the filename as the canonical date_id (guards against a mismatched
        # 'date_id' field inside the file).
        data["date_id"] = date_id
        yield date_id, data


def _apply(existing, data):
    """Copy importable fields from JSON onto a Challenge row. Returns True if any
    value actually changed (so callers can report insert/update/nochange)."""
    changed = False
    for field in IMPORT_FIELDS:
        if field not in data:
            continue
        new_val = data[field]
        # SAFETY INVARIANT #3: don't overwrite an existing non-empty authored value
        # with an empty/None imported one.
        if new_val in (None, "") and getattr(existing, field, None):
            continue
        # Keep NOT NULL columns satisfied.
        if new_val in (None,) and field in _NOT_NULL_DEFAULTS:
            new_val = _NOT_NULL_DEFAULTS[field]
        if getattr(existing, field, None) != new_val:
            setattr(existing, field, new_val)
            changed = True
    return changed


def import_all(single_date=None, quiet=False):
    inserted = updated = nochange = 0
    for date_id, data in _load_json_files(single_date):
        existing = Challenge.query.filter_by(date_id=date_id).first()
        if existing:
            if _apply(existing, data):
                updated += 1
                if not quiet:
                    print(f"  ~ updated  {date_id}  #{data.get('challenge_number','?')}  {data.get('title','?')}")
            else:
                nochange += 1
        else:
            row = Challenge(date_id=date_id)
            # Ensure NOT NULL columns have a value before the first flush.
            row.title = data.get("title") or _NOT_NULL_DEFAULTS["title"]
            row.image_path = data.get("image_path") or _NOT_NULL_DEFAULTS["image_path"]
            _apply(row, data)
            db.session.add(row)
            inserted += 1
            if not quiet:
                print(f"  + inserted {date_id}  #{data.get('challenge_number','?')}  {data.get('title','?')}")

    db.session.commit()
    print(f"Import complete: {inserted} inserted, {updated} updated, {nochange} unchanged.")
    return inserted, updated, nochange


def main():
    parser = argparse.ArgumentParser(description="Import per-day JSON → challenges table (idempotent upsert)")
    parser.add_argument("--date", help="Import only this YYYY-MM-DD")
    parser.add_argument("--quiet", action="store_true", help="Only print the summary")
    args = parser.parse_args()

    with app.app_context():
        # Additive only — creates the challenges table if missing; never drops.
        db.create_all()
        import_all(single_date=args.date, quiet=args.quiet)


if __name__ == "__main__":
    main()
