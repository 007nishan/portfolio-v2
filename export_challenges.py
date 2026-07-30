#!/usr/bin/env python3
"""
export_challenges.py
--------------------
Serialize every Challenge row from the database into git-friendly JSON — one
file per day at ``content/challenges/<YYYY-MM-DD>.json``.

WHY THIS EXISTS (GitHub-as-buffer architecture)
    The live DB (data/portfolio.db) is gitignored and does NOT travel with the
    repo. To make GitHub the single source of truth for CONTENT — so any host
    (this laptop, the server, a fresh clone, a cloud runner) can rebuild an
    identical site with no FCC-API dependency at boot — the challenge data is
    exported to diffable per-day JSON that IS committed. A scheduled GitHub
    Action runs this after each daily sync; the committed JSON + card image are
    what every host pulls.

    This is the DB→JSON half of the round-trip. ``import_challenges.py`` is the
    JSON→DB half. Together they are lossless for challenge content.

DETERMINISTIC OUTPUT
    Keys are sorted and indentation is fixed so re-exporting unchanged data
    produces a byte-identical file (no noisy git diffs). Volatile metadata
    (created_at/updated_at) is intentionally omitted for the same reason.

USAGE
    python export_challenges.py                 # export all challenges
    python export_challenges.py --date 2026-07-30
    python export_challenges.py --quiet         # only print the summary line
"""

import os
import sys
import json
import argparse

basedir = os.path.abspath(os.path.dirname(__file__))
if basedir not in sys.path:
    sys.path.insert(0, basedir)

from app import app
from models import Challenge

CONTENT_DIR = os.path.join(basedir, "content", "challenges")

# The content fields that define a challenge. Order here is cosmetic (output is
# sorted); this list is the SsOT for "what travels in git". created_at/updated_at
# are deliberately excluded (volatile → noisy diffs; not needed to rebuild).
EXPORT_FIELDS = [
    "date_id",
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
    "solution_code",   # ← authored solutions travel here too (owner ask)
    "quote_text",
    "qa_text",
]


def challenge_to_dict(c):
    """Project a Challenge row onto the exportable content fields."""
    return {f: getattr(c, f) for f in EXPORT_FIELDS}


def _filename(date_id):
    return f"{date_id}.json"


def export_one(c):
    """Write a single challenge to its per-day JSON file. Returns the path."""
    os.makedirs(CONTENT_DIR, exist_ok=True)
    path = os.path.join(CONTENT_DIR, _filename(c.date_id))
    payload = challenge_to_dict(c)
    # sort_keys + trailing newline → stable, diff-friendly, POSIX-clean files.
    text = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    return path


def main():
    parser = argparse.ArgumentParser(description="Export challenges to per-day JSON")
    parser.add_argument("--date", help="Export only this YYYY-MM-DD")
    parser.add_argument("--quiet", action="store_true", help="Only print the summary")
    args = parser.parse_args()

    with app.app_context():
        if args.date:
            rows = Challenge.query.filter_by(date_id=args.date).all()
            if not rows:
                print(f"No challenge found for {args.date}.")
                return
        else:
            rows = Challenge.query.order_by(Challenge.date_id.asc()).all()

        count = 0
        for c in rows:
            path = export_one(c)
            count += 1
            if not args.quiet:
                print(f"  + {c.date_id}  #{c.challenge_number or '?'}  {c.title}")
        print(f"Exported {count} challenge(s) -> {os.path.relpath(CONTENT_DIR, basedir)}/")


if __name__ == "__main__":
    main()
