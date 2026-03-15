from app import app
from models import db

def create():
    with app.app_context():
        print("[+] Syncing database designs via additive append loop...")
        db.create_all()
        print("[+] Added User management nodes safely.")

if __name__ == "__main__":
    create()
