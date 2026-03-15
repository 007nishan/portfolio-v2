from app import app
from models import db, Comment, User, ConceptStrength, UserNotebook

def create():
    with app.app_context():
        print("[+] Creating missing tables specifically...")
        db.create_all()
        print("[+] Database creation additive run finished.")

if __name__ == "__main__":
    create()
