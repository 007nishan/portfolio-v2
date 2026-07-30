#!/usr/bin/env python3
"""
FCC Daily Challenge Auto-Sync Script
=====================================
Fetches daily coding challenges from the FCC API and upserts them into the
portfolio database. Supports both single-day sync and full backfill.

Usage:
    python fcc_sync.py              # Sync today's challenge only
    python fcc_sync.py --backfill   # Backfill all challenges from 2025-08-11 to today

API Endpoint:
    https://api.freecodecamp.org/daily-coding-challenge/date/{YYYY-MM-DD}

Returns JSON with: id, date, challengeNumber, title, description,
                   javascript{tests[], challengeFiles}, python{tests[], challengeFiles}
"""

import os
import sys
import json
import argparse
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from datetime import datetime, timedelta
import time

# ── Setup Flask app context ──────────────────────────────────────────────────
basedir = os.path.abspath(os.path.dirname(__file__))
if basedir not in sys.path:
    sys.path.insert(0, basedir)

from app import app
from models import db, Challenge

# ── HTTP session with retry + exponential backoff ────────────────────────────
# A single transient blip at the 00:30 cron must not silently drop the day's
# challenge for 24h. Retry 5xx/429 with backoff (Release It! resilience).
_session = requests.Session()
_retry = Retry(
    total=4,
    backoff_factor=1.5,  # 0s, 1.5s, 3s, 6s
    status_forcelist=(429, 500, 502, 503, 504),
    allowed_methods=frozenset(["GET"]),
)
_session.mount("https://", HTTPAdapter(max_retries=_retry))
_session.mount("http://", HTTPAdapter(max_retries=_retry))

# ── Constants ────────────────────────────────────────────────────────────────
FCC_API_BASE = "https://api.freecodecamp.org/daily-coding-challenge/date"
FCC_START_DATE = datetime(2025, 8, 11)  # Challenge #1: Vowel Balance
LOG_DIR = os.path.join(basedir, "data")
LOG_FILE = os.path.join(LOG_DIR, "sync_log.txt")

# ── Helpers ──────────────────────────────────────────────────────────────────


def log(msg):
    """Write to both stdout and the sync log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def fetch_challenge(date_str):
    """Fetch a single challenge from the FCC API.

    Args:
        date_str: Date in YYYY-MM-DD format

    Returns:
        dict with challenge data, or None on failure
    """
    url = f"{FCC_API_BASE}/{date_str}"
    try:
        resp = _session.get(url, timeout=15)  # retries/backoff via _session
        if resp.status_code == 200:
            return resp.json()
        elif resp.status_code == 404:
            log(f"  No challenge found for {date_str} (404)")
            return None
        else:
            log(f"  API error for {date_str}: HTTP {resp.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        log(f"  Network error fetching {date_str} (after retries): {e}")
        return None


def extract_starter_code(challenge_files):
    """Extract starter code from the challengeFiles structure.

    The challengeFiles can be a list of dicts with 'contents' key,
    or a dict with file entries. We extract the first code block found.
    """
    if not challenge_files:
        return None

    # Handle list format: [{"contents": "code...", ...}]
    if isinstance(challenge_files, list):
        for f in challenge_files:
            if isinstance(f, dict) and f.get("contents"):
                return f["contents"]

    # Handle dict format: {"indexjs": {"contents": "code..."}}
    if isinstance(challenge_files, dict):
        for key, val in challenge_files.items():
            if isinstance(val, dict) and val.get("contents"):
                return val["contents"]
            elif isinstance(val, str):
                return val

    return None


def upsert_challenge(data):
    """Insert or update a challenge in the database.

    Args:
        data: Raw JSON dict from the FCC API

    Returns:
        Tuple of (action, date_str) where action is 'inserted', 'updated', or 'skipped'
    """
    # Parse date
    raw_date = data.get("date", "")
    if "T" in raw_date:
        date_str = raw_date.split("T")[0]
    else:
        date_str = raw_date

    if not date_str:
        return ("error", "no-date")

    title = data.get("title", f"Challenge {date_str}")
    challenge_number = data.get("challengeNumber")
    description = data.get("description", "")

    # Extract language-specific data
    js_data = data.get("javascript", {}) or {}
    py_data = data.get("python", {}) or {}

    js_tests = (
        json.dumps(js_data.get("tests", []), ensure_ascii=False)
        if js_data.get("tests")
        else None
    )
    py_tests = (
        json.dumps(py_data.get("tests", []), ensure_ascii=False)
        if py_data.get("tests")
        else None
    )

    js_starter = extract_starter_code(js_data.get("challengeFiles"))
    py_starter = extract_starter_code(py_data.get("challengeFiles"))

    # Check if challenge already exists
    existing = Challenge.query.filter_by(date_id=date_str).first()

    if existing:
        # Only update FCC-specific fields; never overwrite manual data
        if existing.source == "manual" and existing.fcc_description:
            return ("skipped", date_str)

        existing.challenge_number = challenge_number
        existing.fcc_description = description
        existing.fcc_js_tests = js_tests
        existing.fcc_py_tests = py_tests
        existing.fcc_starter_js = js_starter
        existing.fcc_starter_py = py_starter
        if not existing.source:
            existing.source = "fcc_api"
        action = "updated"
    else:
        # Create new challenge entry
        # Note: image_path defaults to '' because SQLite's existing NOT NULL
        # constraint can't be altered. Templates check image_path truthiness.
        challenge = Challenge(
            date_id=date_str,
            title=title,
            image_path="",  # Empty string satisfies NOT NULL; templates check truthiness
            challenge_number=challenge_number,
            fcc_description=description,
            fcc_js_tests=js_tests,
            fcc_py_tests=py_tests,
            fcc_starter_js=js_starter,
            fcc_starter_py=py_starter,
            source="fcc_api",
        )
        db.session.add(challenge)
        action = "inserted"

    db.session.commit()
    return (action, date_str)


# ── Main Sync Logic ─────────────────────────────────────────────────────────


def generate_card(date_str):
    """Best-effort: (re)generate the landing-page card for a synced challenge.
    A card-render failure must NEVER break content sync, so this swallows
    errors and only logs them. Manual /admin uploads are protected inside
    challenge_card.generate_for_challenge (it skips non-generated images)."""
    try:
        import challenge_card
        challenge = Challenge.query.filter_by(date_id=date_str).first()
        if not challenge:
            return
        status, fname = challenge_card.generate_for_challenge(
            challenge, apply=True, force=False
        )
        if status == "generated":
            db.session.commit()
            log(f"  card: generated {fname}")
        elif status == "skipped-manual":
            log(f"  card: kept manual image ({fname})")
    except Exception as e:  # noqa: BLE001 — never let card render abort sync
        log(f"  card: generation failed (non-fatal): {e}")


def sync_today():
    """Fetch and upsert today's challenge only, then refresh its card."""
    today = datetime.now().strftime("%Y-%m-%d")
    log(f"Syncing today's challenge ({today})...")

    data = fetch_challenge(today)
    if data:
        action, date = upsert_challenge(data)
        log(f"  {action.upper()}: {date} — {data.get('title', '?')}")
        generate_card(date)
    else:
        log(f"  No data returned for {today}. Challenge may not be released yet.")


def _latest_synced_date():
    """The newest date_id already in the DB, or the day before FCC_START_DATE if
    the DB is empty (so a first run backfills from the very first challenge)."""
    latest = Challenge.query.order_by(Challenge.date_id.desc()).first()
    if latest and latest.date_id:
        try:
            return datetime.strptime(latest.date_id, "%Y-%m-%d")
        except ValueError:
            pass
    return FCC_START_DATE - timedelta(days=1)


def sync_catchup():
    """Gap-filling daily sync: fetch every day from the day AFTER the newest
    synced challenge through today, so a missed run (outage, Action failure) is
    automatically caught up on the next run instead of leaving a permanent hole.

    This is what the daily automation calls. It self-heals: if the newest synced
    day is already today, it does exactly one fetch (today) and is a no-op if the
    challenge is unchanged."""
    today = datetime.now()
    start = _latest_synced_date() + timedelta(days=1)
    if start > today:
        # Already current; still refresh today in case it was updated upstream.
        start = today
    log(f"Catch-up sync: {start.strftime('%Y-%m-%d')} -> {today.strftime('%Y-%m-%d')}")

    current = start
    inserted = updated = errors = 0
    while current <= today:
        date_str = current.strftime("%Y-%m-%d")
        data = fetch_challenge(date_str)
        if data:
            action, _ = upsert_challenge(data)
            if action == "inserted":
                inserted += 1
            elif action == "updated":
                updated += 1
            log(f"  {action.upper()}: {date_str} — {data.get('title', '?')}")
            generate_card(date_str)
        else:
            errors += 1  # a 404 for a not-yet-released future day is expected/benign
        current += timedelta(days=1)
        time.sleep(0.3)  # be polite to FCC

    log(f"Catch-up complete: {inserted} inserted, {updated} updated, {errors} no-data.")


def backfill():
    """Fetch all challenges from FCC_START_DATE to today."""
    today = datetime.now()
    current = FCC_START_DATE
    total = (today - FCC_START_DATE).days + 1

    log(
        f"Starting backfill: {FCC_START_DATE.strftime('%Y-%m-%d')} -> {today.strftime('%Y-%m-%d')} ({total} days)"
    )

    inserted = 0
    updated = 0
    skipped = 0
    errors = 0

    while current <= today:
        date_str = current.strftime("%Y-%m-%d")
        data = fetch_challenge(date_str)

        if data:
            action, _ = upsert_challenge(data)
            if action == "inserted":
                inserted += 1
                log(
                    f"  + INSERTED #{data.get('challengeNumber', '?')}: {data.get('title', '?')} ({date_str})"
                )
            elif action == "updated":
                updated += 1
                log(
                    f"  ~ UPDATED  #{data.get('challengeNumber', '?')}: {data.get('title', '?')} ({date_str})"
                )
            else:
                skipped += 1
        else:
            errors += 1

        current += timedelta(days=1)

        # Be polite to FCC's servers — small delay between requests
        time.sleep(0.3)

    log(
        f"\nBackfill complete: {inserted} inserted, {updated} updated, {skipped} skipped, {errors} errors"
    )


# ── Entry Point ──────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="FCC Daily Challenge Sync")
    parser.add_argument(
        "--backfill",
        action="store_true",
        help="Backfill all challenges from 2025-08-11 to today",
    )
    parser.add_argument(
        "--catchup",
        action="store_true",
        help="Gap-filling sync: newest-synced+1 -> today (self-heals missed runs). "
             "Use this for the daily automation.",
    )
    args = parser.parse_args()

    with app.app_context():
        # Ensure all tables exist (handles new columns gracefully)
        db.create_all()

        if args.backfill:
            backfill()
        elif args.catchup:
            sync_catchup()
        else:
            sync_today()


if __name__ == "__main__":
    main()
