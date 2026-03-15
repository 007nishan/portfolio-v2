import sys
import os
basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, basedir)

from app import app
from models import db, Challenge

with app.app_context():
    print("=== DB INSPECTION BEFORE FIX ===")
    chs = Challenge.query.order_by(Challenge.date_id.desc()).limit(5).all()
    for c in chs:
        print(f"| {c.date_id} | {c.title} | {c.image_path} | {c.source}")
    
    # Check if 2026-03-15 has an issue
    c = Challenge.query.filter_by(date_id='2026-03-15').first()
    if c:
        print(f"\n[2026-03-15 DETAILS]")
        print(f"Title: {c.title}")
        print(f"Image: {c.image_path}")
        print(f"Source: {c.source}")
        print(f"Problem Text (preview): {c.problem_text[:100] if c.problem_text else 'None'}")
        
        # If it has a manual image but was created by API, maybe we need to fix it?
        # User says "Image is from Feb 16". If the image path is indeed recent, 
        # but the content is wrong, we should probably remove the image_path so it falls back to description.
        # Let's check if the user uploaded something on the wrong date.
        
    print("\n=== END ===")
