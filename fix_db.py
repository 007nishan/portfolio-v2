import sys
import os
basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, basedir)

from app import app
from models import db, Challenge

with app.app_context():
    print("=== FIXING DB ===")
    c = Challenge.query.filter_by(date_id='2026-03-15').first()
    if c:
        print(f"Found 2026-03-15. Current Image: {c.image_path}")
        # Clear the image path to force fallback to API description card
        if c.image_path:
             print(f"Clearing image_path '{c.image_path}' to restore proper sync display.")
             c.image_path = ""
             db.session.commit()
             print("[+] Fixed 2026-03-15.")
    else:
        print("[-] 2026-03-15 not found.")

    # Also clean up any other orphan manual images that might have synced to wrong dates
    # if they were uploaded today and are in fact for yesterday or similar.
    # For now, just fixing the landing page is the priority.
    
    print("=== END ===")
