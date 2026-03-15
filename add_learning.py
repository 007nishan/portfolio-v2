import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import db, Challenge
import datetime

with app.app_context():
    date_str = datetime.datetime.now().strftime('%Y-%m-%d')
    existing = Challenge.query.filter_by(date_id=date_str).first()
    
    if not existing:
        challenge = Challenge(
            date_id=date_str,
            title="Deploying Local Server Worldwide using Cloudflare Tunnel",
            image_path='',
            problem_text="### How I deployed my local portfolio worldwide\n\nI already hosted my website locally on my old laptop (`192.168.1.150`), but I wanted to make it accessible online globally without needing a VPS like AWS or Render, and without migrating my SQLite database to PostgreSQL.",
            concepts_text="* **Cloudflare Tunnel**: Securely exposes a local server to the Internet without opening any firewall ports.\n* **Local Deployment**: Hosting the application on an old Linux laptop running systemd.\n* **SQLite Optimization**: Ensuring robust multi-threading on the local storage.",
            solution_code="# Installed cloudflared binary\nInvoke-WebRequest -Uri 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe'\n\n# Ran the tunnel pointed to the local laptop's port 80\ncloudflared tunnel --url http://192.168.1.150:80\n\n# The result was a free `trycloudflare.com` URL accessible worldwide!",
            qa_text="**Q: Does this require opening ports?**\nA: No! Cloudflared creates outbound connections from the private network to Cloudflare's global network, bypassing the need for port forwarding.",
            source='manual'
        )
        db.session.add(challenge)
        db.session.commit()
        print("Successfully added learning module to DB!")
    else:
        existing.title = "Deploying Local Server Worldwide using Cloudflare Tunnel"
        existing.problem_text = "### How I deployed my local portfolio worldwide\n\nI already hosted my website locally on my old laptop (`192.168.1.150`), but I wanted to make it accessible online globally without needing a VPS."
        existing.solution_code = "cloudflared tunnel --url http://192.168.1.150:80"
        db.session.commit()
        print("Updated learning module!")
