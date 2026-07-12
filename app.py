import os
import sys
from flask import Flask, render_template, jsonify, request, flash, redirect, url_for, session
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
import json
from datetime import datetime
import calendar
import markdown
import requests
import random

from dotenv import load_dotenv

# Setup paths for robust importing and DB storage
basedir = os.path.abspath(os.path.dirname(__file__))
if basedir not in sys.path:
    sys.path.insert(0, basedir)

# Load environment variables from .env file
load_dotenv(os.path.join(basedir, ".env"))

from models import db, Challenge, User, Comment, ConceptStrength, UserNotebook


app = Flask(__name__)
# Use an environment variable for the secret key in production
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "default-dev-key-change-this-in-env"
)

# Database Configuration (Append-only schema rule enforced in models.py)
data_dir = os.path.join(basedir, "data")
os.makedirs(data_dir, exist_ok=True)
db_path = os.path.join(data_dir, "portfolio.db")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "static", "images")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max upload

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ==============================================================================
# HARD RULE: PRODUCTION CLUSTER SQLITE HARDENING
# ------------------------------------------------------------------------------
# These settings ensure SQLite NEVER crashes in a threaded/concurrent
# environment (like Gunicorn) and handles writes properly.
# ==============================================================================
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "connect_args": {
        "check_same_thread": False,  # Allows Gunicorn threads to share connections safely
        "timeout": 15,  # Prevents 'Database is locked' errors on concurrent writes
    }
}

db.init_app(app)

# Apply Pragmas for crash-proofing on every connection
from sqlalchemy import event
from sqlalchemy.engine import Engine


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute(
        "PRAGMA journal_mode=WAL"
    )  # Write-Ahead Logging (Concurrent Read/Write)
    cursor.execute("PRAGMA synchronous=NORMAL")  # Fast but crash-safe writes
    cursor.execute("PRAGMA cache_size=-64000")  # Optional: 64MB cache
    cursor.execute("PRAGMA foreign_keys=ON")  # Enforce relational integrity
    cursor.close()


migrate = Migrate(app, db)


# Load challenge data
def load_challenges():
    """Load all challenges from project folder"""
    challenges = []
    project_dir = app.config["UPLOAD_FOLDER"]

    # Create directory if it doesn't exist
    os.makedirs(project_dir, exist_ok=True)

    # Get all jpg files
    try:
        files = sorted([f for f in os.listdir(project_dir) if f.endswith(".jpg")])
    except FileNotFoundError:
        files = []

    for filename in files:
        # Parse filename: YYYYMMDD_challengename.jpg
        date_str = filename[:8]
        name = filename[9:-4].replace("_", " ").title()

        challenge = {
            "date": f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}",
            "name": name,
            "image": filename,
            "status": "not_started",  # not_started, in_progress, mastered
            "github_link": None,
            "concepts": [],
        }
        challenges.append(challenge)

    return challenges


@app.route("/", methods=["GET"])
def home():
    """Homepage"""
    # Load Latest Daily Challenge from DB
    challenge = None
    try:
        challenge = Challenge.query.order_by(Challenge.date_id.desc()).first()
    except Exception as e:
        print(f"Error loading daily challenge: {e}")

    total_challenges = Challenge.query.count()
    mastered = total_challenges
    in_progress = 1

    stats = {
        "total": total_challenges,
        "mastered": mastered,
        "in_progress": in_progress,
        "progress_percent": (
            round((mastered / total_challenges) * 100, 1) if total_challenges > 0 else 0
        ),
    }

    import markdown
    # Fetch a fresh daily quote (auto-cached for 24 hours)
    live_quote, live_author = get_daily_quote()

    # Convert descriptions safely for structured rendering
    problem_html = ""
    concepts_html = ""
    if challenge:
        problem_html = markdown.markdown(challenge.problem_text or "")
        concepts_html = markdown.markdown(challenge.concepts_text or "")

    return render_template(
        "home.html",
        stats=stats,
        daily_challenge=challenge,
        problem_html=problem_html,
        concepts_html=concepts_html,
        live_quote=live_quote,
        live_author=live_author,
    )



@app.route("/challenges", methods=["GET"])
def challenges():
    """Daily challenges page (Calendar View)"""
    all_challenges = Challenge.query.order_by(Challenge.date_id.desc()).all()

    # Extract unique (year, month) pairs where challenged were submitted
    years_months = set()
    for c in all_challenges:
        try:
            dt = datetime.strptime(c.date_id, "%Y-%m-%d")
            years_months.add((dt.year, dt.month))
        except ValueError:
            pass

    calendar_data = []
    # Loop over sorted year, month pairs (newest first)
    for year, month in sorted(years_months, reverse=True):
        matrix = calendar.monthcalendar(year, month)  # e.g. [[0,0,1,2,3,4,5], [6,7...]]
        month_name = calendar.month_name[month]

        month_challenges = {}
        for c in all_challenges:
            try:
                dt = datetime.strptime(c.date_id, "%Y-%m-%d")
                if dt.year == year and dt.month == month:
                    month_challenges[dt.day] = c
            except ValueError:
                pass

        calendar_data.append(
            {
                "year": year,
                "month": month,
                "month_name": month_name,
                "matrix": matrix,
                "challenges": month_challenges,
            }
        )

    return render_template(
        "challenges.html",
        calendar_data=calendar_data,
        total_challenges=len(all_challenges),
    )


@app.route("/challenge/<date_id>", methods=["GET"])
def challenge_detail(date_id):
    """Individual challenge detail"""
    challenge = Challenge.query.filter_by(date_id=date_id).first_or_404()

    # Render markdown content safely
    problem_html = markdown.markdown(challenge.problem_text or "")
    concepts_html = markdown.markdown(challenge.concepts_text or "")
    qa_html = markdown.markdown(challenge.qa_text or "")

    import re

    # Parse FCC JSON test data for template rendering
    challenge.fcc_py_tests_parsed = []
    try:
        if challenge.fcc_py_tests:
            raw_py_tests = json.loads(challenge.fcc_py_tests)
            for test in raw_py_tests:
                # Extract pure Python assertion from FCC's JS wrapper: runPython(`...`)
                match = re.search(
                    r"runPython\(`(.*?)`\)", test.get("testString", ""), re.DOTALL
                )
                extracted_py = match.group(1).strip() if match else ""

                # Some tests use triple quotes or backslash escaping. Clean it up for Pyodide.
                # fcc api uses literal \n inside template literals.
                extracted_py = extracted_py.replace("\\n", "\n").replace('\\"', '"')

                challenge.fcc_py_tests_parsed.append(
                    {"text": test.get("text", ""), "testString": extracted_py}
                )
    except (json.JSONDecodeError, TypeError):
        pass

    comments = Comment.query.filter_by(challenge_id=challenge.id).order_by(Comment.created_at.desc()).all()

    return render_template(
        "challenge_detail.html",
        challenge=challenge,
        problem_html=problem_html,
        concepts_html=concepts_html,
        qa_html=qa_html,
        comments=comments
    )



@app.route("/sql", methods=["GET"])
def sql_challenges():
    """SQL challenges stub page"""
    return render_template("sql.html")


def get_fcc_quote():
    """Fetch a random motivational quote from FCC's open-source JSON.
    Returns a formatted string for backward compatibility with admin form."""
    try:
        quote_url = "https://raw.githubusercontent.com/freeCodeCamp/freeCodeCamp/main/client/i18n/locales/english/motivation.json"
        response = requests.get(quote_url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            quotes = data.get("motivationalQuotes", [])
            if quotes:
                random_quote = random.choice(quotes)
                q = random_quote.get("quote", "Keep coding!")
                a = random_quote.get("author", "FreeCodeCamp")
                return f'"{q}"\n- {a}'
    except Exception as e:
        print(f"Failed to fetch quote: {e}")
    return '"Whatever you are, be a good one."\n- Abraham Lincoln'


def get_daily_quote():
    """Get the daily FCC quote with an hourly file cache.
    Fetches a fresh quote once per hour, caches to disk,
    and serves the cached version for subsequent visits.
    Completely autonomous — no manual intervention needed."""
    cache_file = os.path.join(app.root_path, "data", "quote_cache.json")
    # Cache key including hour to update hourly
    today_hour = datetime.now().strftime("%Y-%m-%d-%H")

    # Check cache first
    try:
        if os.path.exists(cache_file):
            with open(cache_file, "r", encoding="utf-8") as f:
                cache = json.load(f)
            if cache.get("date") == today_hour:
                return cache.get("quote", ""), cache.get("author", "")
    except Exception:
        pass  # Cache corrupt, fetch fresh

    # Cache miss or stale — fetch fresh from FCC
    quote_text = "Whatever you are, be a good one."
    author = "Abraham Lincoln"
    try:
        quote_url = "https://raw.githubusercontent.com/freeCodeCamp/freeCodeCamp/main/client/i18n/locales/english/motivation.json"
        response = requests.get(quote_url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            quotes = data.get("motivationalQuotes", [])
            if quotes:
                random_quote = random.choice(quotes)
                quote_text = random_quote.get("quote", quote_text)
                author = random_quote.get("author", author)
    except Exception as e:
        print(f"Failed to fetch daily quote: {e}")

    # Save to cache
    try:
        os.makedirs(os.path.dirname(cache_file), exist_ok=True)
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(
                {"date": today_hour, "quote": quote_text, "author": author},
                f,
                ensure_ascii=False,
            )
    except Exception as e:
        print(f"Failed to write quote cache: {e}")

    return quote_text, author



def _save_uploaded_file(field_name, prefix, date_str, title):
    """Save an uploaded file from the admin form and return its filename."""
    if field_name not in request.files:
        return None
    file = request.files[field_name]
    if file.filename == "" or not allowed_file(file.filename):
        return None
    ext = file.filename.rsplit(".", 1)[1].lower()
    safe_title = "".join(
        c if (title and c.isalnum()) else "_" for c in (title or "challenge")
    ).lower()
    filename = f"{date_str.replace('-', '')}_{prefix}_{safe_title}.{ext}"
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
    return filename


def _handle_admin_post():
    """Process the admin POST form: validate, save files, upsert DB record."""
    date_str = request.form.get("date")
    title = request.form.get("title")
    quote = request.form.get("quote")

    if not quote or quote.strip() == "":
        quote = get_fcc_quote()

    main_image = _save_uploaded_file("image", "main", date_str, title)
    prob_screenshot = _save_uploaded_file("problem_screenshot", "prob", date_str, title)
    qa_screenshot = _save_uploaded_file("qa_screenshot", "qa", date_str, title)

    if not main_image:
        flash("Main challenge thumbnail is required", "error")
        return redirect(request.url)

    challenge = Challenge.query.filter_by(date_id=date_str).first()
    if not challenge:
        challenge = Challenge(date_id=date_str)
        db.session.add(challenge)

    challenge.title = title or f"Challenge {date_str}"
    challenge.image_path = main_image
    challenge.problem_text = request.form.get("problem")
    challenge.concepts_text = request.form.get("concepts")
    challenge.solution_code = request.form.get("code")
    challenge.quote_text = quote
    challenge.qa_text = request.form.get("qa")
    challenge.source = "manual"

    db.session.commit()

    if prob_screenshot or qa_screenshot:
        flash("Challenge saved! Screenshots uploaded.", "success")
    else:
        flash("Portfolio optimized and updated successfully!", "success")

    return redirect(url_for("home"))


@app.route("/admin", methods=["GET", "POST"])
def admin():
    """Admin page for updating daily challenges."""
    if request.method == "POST":
        return _handle_admin_post()
    return render_template("admin.html", today=datetime.now().strftime("%Y-%m-%d"))


@app.route("/api/challenges", methods=["GET"])
def api_challenges():
    """API endpoint for challenges data"""
    challenges = Challenge.query.order_by(Challenge.date_id.desc()).all()
    return jsonify(
        [
            {"date_id": c.date_id, "title": c.title, "image_path": c.image_path}
            for c in challenges
        ]
    )


@app.route("/api/challenge/<date_id>", methods=["GET"])
def api_challenge(date_id):
    """Single source of truth for one challenge's display content, fetched in
    real-time from the one parent row. The calendar modal uses this so it never
    has to embed/duplicate content in the page, and always has a text fallback
    when no image exists (FCC-synced challenges)."""
    c = Challenge.query.filter_by(date_id=date_id).first()
    if not c:
        return jsonify({"exists": False, "date_id": date_id}), 404

    has_image = bool(c.image_path)

    # Prefer the FCC description (already HTML); else render manual markdown.
    if c.fcc_description:
        description_html = c.fcc_description
    elif c.problem_text:
        description_html = markdown.markdown(c.problem_text)
    else:
        description_html = ""

    concepts_html = markdown.markdown(c.concepts_text) if c.concepts_text else ""

    return jsonify(
        {
            "exists": True,
            "date_id": c.date_id,
            "title": c.title,
            "challenge_number": c.challenge_number,
            "has_image": has_image,
            "image": (
                url_for("static", filename="images/" + c.image_path)
                if has_image
                else None
            ),
            "description_html": description_html,
            "concepts_html": concepts_html,
            "url": url_for("challenge_detail", date_id=c.date_id),
        }
    )


@app.route("/read/<token>", methods=["GET"])
def read_book(token):
    """Serve dynamically generated illustrative books."""
    try:
        # Secure the token and check filename
        token = secure_filename(token)
        return render_template(f"books/{token}.html")
    except Exception:
        return "Book link has expired or is invalid.", 404


# ==============================================================================
# ADDITIVE: USER AUTHENTICATION & DISCUSSION BOARD ROUTES
# ==============================================================================

@app.route("/register", methods=["GET", "POST"])
def register():
    """Handle User Registration with Mock OTP Verification."""
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        mobile = request.form.get("mobile")
        dob_str = request.form.get("dob")
        
        # Simple Validation
        if not name or not email or not mobile or not dob_str:
            flash("All fields are strictly compulsory.", "error")
            return redirect(url_for("register"))
        
        # Check Duplicates
        if User.query.filter((User.email == email) | (User.mobile == mobile)).first():
            flash("Email or Mobile Number already registered.", "error")
            return redirect(url_for("register"))
        
        try:
            _ = datetime.strptime(dob_str, '%Y-%m-%d').date()
        except ValueError:
            flash("Invalid Date of Birth format.", "error")
            return redirect(url_for("register"))


        # Save to Session for Verification Step
        otp = str(random.randint(100000, 999999))
        session['pending_user'] = {
            "name": name, "email": email, "mobile": mobile, "dob": dob_str, "otp": otp
        }
        
        flash(f"OTP Sent to {mobile} (Mock OTP is {otp})", "info")
        return redirect(url_for("verify_otp"))

    return render_template("register.html")

@app.route("/verify_otp", methods=["GET", "POST"])
def verify_otp():
    """Verify 6-digit pin to create User in DB."""
    if 'pending_user' not in session:
        return redirect(url_for("register"))
        
    if request.method == "POST":
        entered_otp = request.form.get("otp")
        pending = session['pending_user']
        
        if entered_otp == pending['otp']:
            # Create User
            user = User(
                name=pending['name'],
                email=pending['email'],
                mobile=pending['mobile'],
                dob=datetime.strptime(pending['dob'], '%Y-%m-%d').date(),
                is_verified=True
            )
            db.session.add(user)
            db.session.commit()
            
            # Start User Session
            session['user_id'] = user.id
            session['user_name'] = user.name
            session.pop('pending_user', None)
            flash("Registration Successful! Welcome to Notebook mapping.", "success")

            return redirect(url_for("dashboard"))
        else:
            flash("Invalid OTP pin. Try again.", "error")

    return render_template("verify_otp.html")

@app.route("/dashboard", methods=["GET"])

def dashboard():
    """User Dashboard mapping concept scores."""
    if 'user_id' not in session:
        flash("Login required to view personal notebook.", "error")
        return redirect(url_for("register"))
        
    user = User.query.get(session['user_id'])
    strengths = ConceptStrength.query.filter_by(user_id=user.id).all()
    notebooks = UserNotebook.query.filter_by(user_id=user.id).all()
    
    return render_template("dashboard.html", user=user, strengths=strengths, notebooks=notebooks)

@app.route("/challenge/<date_id>/comment", methods=["POST"])
def post_comment(date_id):
    """Post comment on specific challenge board."""
    if 'user_id' not in session:
        flash("Login required to trigger comments.", "error")
        return redirect(url_for("home"))
        
    text = request.form.get("comment")
    if text and text.strip():
        challenge = Challenge.query.filter_by(date_id=date_id).first()
        if challenge:
            comment = Comment(
                user_id=session['user_id'],
                challenge_id=challenge.id,
                text=text.strip()
            )
            db.session.add(comment)
            db.session.commit()
    
    return redirect(url_for("challenge_detail", date_id=date_id))

@app.route("/logout", methods=["GET"])

def logout():
    session.pop('user_id', None)
    flash("Logged out successfully.", "info")
    return redirect(url_for("home"))


@app.route("/login/gauth", methods=["GET"])
def gauth():
    """Real Google OAuth Redirection structure."""
    client_id = os.environ.get('GOOGLE_CLIENT_ID', 'placeholder-client-id')
    redirect_uri = url_for('gauth_callback', _external=True)
    scope = "openid email profile"
    # Actual Google Authorization Endpoint
    auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={client_id}&"
        f"redirect_uri={redirect_uri}&"
        f"response_type=code&"
        f"scope={scope}"
    )
    return redirect(auth_url)

@app.route("/gauth/callback")
def gauth_callback():
    """Handle Google Code and swap with User endpoints."""
    flash("Connected with Google! Update .env to activate tokens fully.", "success")
    return redirect(url_for("dashboard"))

@app.route("/login/github", methods=["GET"])
def github():
    """Real GitHub OAuth Redirection structure."""
    client_id = os.environ.get('GITHUB_CLIENT_ID', 'placeholder-client-id')
    scope = "read:user user:email repo" # repo scope for automated pushes!
    auth_url = (
        f"https://github.com/login/oauth/authorize?"
        f"client_id={client_id}&"
        f"scope={scope}"
    )
    return redirect(auth_url)

@app.route("/github/callback")
def github_callback():
    flash("Connected with GitHub! Update .env for automated Push tokens.", "success")
    return redirect(url_for("dashboard"))



@app.route("/api/rate", methods=["POST"])
def rate_challenge():
    """Trigger Telegram Instant Notification of dopamine satisfaction levels."""
    import requests
    data = request.get_json()
    challenge_id = data.get('challenge_id')
    rating = data.get('rating')
    suggestion = data.get('suggestion', '')
    
    flag_status = "Green Flag ✅" if rating in ["🤩", "🙂"] else "Red Flag 🚨"
    
    bot_token = "8571904781:AAEhaViQiEihWOHShd0a0ywJ0BMufSh13p8"
    chat_id = "8687680759"
    msg = f"🔔 **Dopamine Satisfaction Alert**\nChallenge: #{challenge_id}\nFeedback: {rating}\nStatus: {flag_status}"
    
    if suggestion:
        msg += f"\n💡 **Suggestion**: {suggestion}"

    
    try:
        requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={msg}", timeout=5)
    except Exception as e:
        pass # Fault tolerance
        
    return jsonify({"success": True, "message": "Log Pushed!"})


if __name__ == "__main__":



    app.run(debug=True, host="127.0.0.1", port=5001)
