import sys
import os
basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, basedir)

from app import app
from models import Challenge

with app.app_context():
    print("--- LATEST 10 CHALLENGES ---")
    chs = Challenge.query.order_by(Challenge.date_id.desc()).limit(10).all()
    for c in chs:
        print(f"| {c.date_id} | {c.title[:30]:<30} | {c.image_path[:20]:<20} | {c.source}")
    
    # Check for today's entries
    import datetime
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    today_ch = Challenge.query.filter_by(date_id=today).first()
    if today_ch:
        print(f"\n[FOUND TODAY] {today_ch.date_id} | {today_ch.title}")
    else:
        print(f"\n[NOT FOUND] No entry for today ({today})")
