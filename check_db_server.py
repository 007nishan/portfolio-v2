import sys
import os
basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, basedir)

from app import app
from models import Challenge

with app.app_context():
    chs = Challenge.query.order_by(Challenge.date_id.desc()).limit(1).all()
    if chs:
        c = chs[0]
        print(f"LATEST_ENTRY|DATE:{c.date_id}|TITLE:{c.title}|IMG:{c.image_path}")
    else:
        print("NO_ENTRIES_FOUND")
