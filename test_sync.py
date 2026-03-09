"""Quick test to verify FCC API structure and sync pipeline."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import db, Challenge
import requests, json

with app.app_context():
    # Test 1: Fetch a known challenge from the API
    print("=== Test 1: FCC API Fetch ===")
    resp = requests.get("https://api.freecodecamp.org/daily-coding-challenge/date/2026-03-08", timeout=15)
    print(f"API Status: {resp.status_code}")
    
    if resp.status_code == 200:
        data = resp.json()
        print(f"Title: {data.get('title')}")
        print(f"Challenge #: {data.get('challengeNumber')}")
        print(f"Date: {data.get('date')}")
        desc = data.get("description", "")
        print(f"Description length: {len(desc)} chars")
        print(f"Description preview: {desc[:150]}...")
        
        js = data.get("javascript", {})
        tests = js.get("tests", [])
        print(f"\nJS tests: {len(tests)}")
        if tests:
            print(f"  First test text: {tests[0].get('text', '?')}")
        
        py = data.get("python", {})
        py_tests = py.get("tests", [])
        print(f"Python tests: {len(py_tests)}")
        
        js_files = js.get("challengeFiles", [])
        print(f"\nJS challengeFiles type: {type(js_files).__name__}")
        if isinstance(js_files, list) and js_files:
            for f in js_files:
                if isinstance(f, dict):
                    print(f"  File keys: {list(f.keys())}")
                    contents = f.get("contents", "")
                    print(f"  Starter code ({len(contents)} chars): {contents[:120]}...")
    
    # Test 2: Run sync for that date
    print("\n=== Test 2: Sync Pipeline ===")
    from fcc_sync import fetch_challenge, upsert_challenge
    data = fetch_challenge("2026-03-08")
    if data:
        action, date_str = upsert_challenge(data)
        print(f"Action: {action}, Date: {date_str}")
        
        # Verify it's in the DB
        ch = Challenge.query.filter_by(date_id="2026-03-08").first()
        if ch:
            print(f"DB Record: #{ch.challenge_number} - {ch.title}")
            print(f"Source: {ch.source}")
            print(f"FCC Description: {len(ch.fcc_description or '')} chars")
            print(f"JS Tests: {len(ch.fcc_js_tests or '')} chars")
            print(f"Starter JS: {len(ch.fcc_starter_js or '')} chars")
            print("SUCCESS: Challenge synced to database!")
        else:
            print("ERROR: Challenge not found in database after upsert!")
    else:
        print("ERROR: Could not fetch challenge data from API")
    
    # Test 3: Check total count
    print(f"\n=== Test 3: DB Stats ===")
    total = Challenge.query.count()
    fcc_count = Challenge.query.filter_by(source="fcc_api").count()
    manual_count = Challenge.query.filter(Challenge.source != "fcc_api").count()
    print(f"Total challenges in DB: {total}")
    print(f"FCC API synced: {fcc_count}")
    print(f"Manual entries: {manual_count}")
