import os
import sys
from flask import Flask, render_template, jsonify, request, flash, redirect, url_for
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
import json
from datetime import datetime
import calendar

from dotenv import load_dotenv

# Setup paths for robust importing and DB storage
basedir = os.path.abspath(os.path.dirname(__file__))
if basedir not in sys.path:
    sys.path.insert(0, basedir)

# Load environment variables from .env file
load_dotenv(os.path.join(basedir, '.env'))

from models import db, Challenge

app = Flask(__name__)
# Use an environment variable for the secret key in production
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-dev-key-change-this-in-env')

# Database Configuration (Append-only schema rule enforced in models.py)
data_dir = os.path.join(basedir, 'data')
os.makedirs(data_dir, exist_ok=True)
db_path = os.path.join(data_dir, 'portfolio.db')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'images')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ==============================================================================
# HARD RULE: PRODUCTION CLUSTER SQLITE HARDENING 
# ------------------------------------------------------------------------------
# These settings ensure SQLite NEVER crashes in a threaded/concurrent 
# environment (like Gunicorn) and handles writes properly.
# ==============================================================================
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "connect_args": {
        "check_same_thread": False, # Allows Gunicorn threads to share connections safely
        "timeout": 15               # Prevents 'Database is locked' errors on concurrent writes
    }
}

db.init_app(app)

# Apply Pragmas for crash-proofing on every connection
from sqlalchemy import event
from sqlalchemy.engine import Engine

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")      # Write-Ahead Logging (Concurrent Read/Write)
    cursor.execute("PRAGMA synchronous=NORMAL")    # Fast but crash-safe writes
    cursor.execute("PRAGMA cache_size=-64000")     # Optional: 64MB cache
    cursor.execute("PRAGMA foreign_keys=ON")       # Enforce relational integrity
    cursor.close()

migrate = Migrate(app, db)

# Load challenge data
def load_challenges():
    """Load all challenges from project folder"""
    challenges = []
    project_dir = app.config['UPLOAD_FOLDER']
    
    # Create directory if it doesn't exist
    os.makedirs(project_dir, exist_ok=True)
    
    # Get all jpg files
    try:
        files = sorted([f for f in os.listdir(project_dir) if f.endswith('.jpg')])
    except FileNotFoundError:
        files = []
    
    for filename in files:
        # Parse filename: YYYYMMDD_challengename.jpg
        date_str = filename[:8]
        name = filename[9:-4].replace('_', ' ').title()
        
        challenge = {
            'date': f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}",
            'name': name,
            'image': filename,
            'status': 'not_started',  # not_started, in_progress, mastered
            'github_link': None,
            'concepts': []
        }
        challenges.append(challenge)
    
    return challenges

import markdown

@app.route('/')
def home():
    """Homepage"""
    # Load Latest Daily Challenge from DB
    challenge = None
    try:
        challenge = Challenge.query.order_by(Challenge.date_id.desc()).first()
    except Exception as e:
        print(f"Error loading daily challenge: {e}")

    total_challenges = 141
    mastered = Challenge.query.count()
    in_progress = 1
    
    stats = {
        'total': total_challenges,
        'mastered': mastered,
        'in_progress': in_progress,
        'progress_percent': round((mastered / total_challenges) * 100, 1) if total_challenges > 0 else 0
    }
    
    return render_template('home.html', stats=stats, daily_challenge=challenge)

@app.route('/challenges')
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
        matrix = calendar.monthcalendar(year, month) # e.g. [[0,0,1,2,3,4,5], [6,7...]]
        month_name = calendar.month_name[month]
        
        month_challenges = {}
        for c in all_challenges:
            try:
                dt = datetime.strptime(c.date_id, "%Y-%m-%d")
                if dt.year == year and dt.month == month:
                    month_challenges[dt.day] = c
            except ValueError:
                pass
                
        calendar_data.append({
            'year': year,
            'month': month,
            'month_name': month_name,
            'matrix': matrix,
            'challenges': month_challenges
        })
        
    return render_template('challenges.html', calendar_data=calendar_data, total_challenges=len(all_challenges))

@app.route('/challenge/<date_id>')
def challenge_detail(date_id):
    """Individual challenge detail"""
    challenge = Challenge.query.filter_by(date_id=date_id).first_or_404()
    
    # Render markdown content safely
    problem_html = markdown.markdown(challenge.problem_text or "")
    concepts_html = markdown.markdown(challenge.concepts_text or "")
    qa_html = markdown.markdown(challenge.qa_text or "")
    
    return render_template('challenge_detail.html', 
                           challenge=challenge,
                           problem_html=problem_html,
                           concepts_html=concepts_html,
                           qa_html=qa_html)

@app.route('/sql')
def sql_challenges():
    """SQL challenges stub page"""
    return render_template('sql.html')

import requests
import random

def get_fcc_quote():
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
                return f"\"{q}\"\n- {a}"
    except Exception as e:
        print(f"Failed to fetch quote: {e}")
    return '"Whatever you are, be a good one."\n- Abraham Lincoln'

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    """Admin page for updating daily challenges"""
    if request.method == 'POST':
        # Get data from form
        date_str = request.form.get('date')
        title = request.form.get('title')
        problem = request.form.get('problem')
        concepts = request.form.get('concepts')
        code = request.form.get('code')
        quote = request.form.get('quote')
        qa = request.form.get('qa')
        
        # Automate quote fetching if empty
        if not quote or quote.strip() == "":
            quote = get_fcc_quote()
        
        # Handle file uploads
        def save_uploaded_file(field_name, prefix):
            if field_name not in request.files:
                return None
            file = request.files[field_name]
            if file.filename == '' or not allowed_file(file.filename):
                return None
            ext = file.filename.rsplit('.', 1)[1].lower()
            # If title is missing (extracted later), use 'challenge' as slug
            safe_title = "".join([c if (title and c.isalnum()) else "_" for c in (title or "challenge")]).lower()
            filename = f"{date_str.replace('-', '')}_{prefix}_{safe_title}.{ext}"
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return filename

        main_image = save_uploaded_file('image', 'main')
        prob_screenshot = save_uploaded_file('problem_screenshot', 'prob')
        qa_screenshot = save_uploaded_file('qa_screenshot', 'qa')

        if not main_image:
            flash('Main challenge thumbnail is required', 'error')
            return redirect(request.url)
        
        # Upsert into DB
        challenge = Challenge.query.filter_by(date_id=date_str).first()
        if not challenge:
            challenge = Challenge(date_id=date_str)
            db.session.add(challenge)
        
        challenge.title = title or f"Challenge {date_str}"
        challenge.image_path = main_image
        challenge.problem_text = problem
        challenge.concepts_text = concepts
        challenge.solution_code = code
        challenge.quote_text = quote
        challenge.qa_text = qa
        
        db.session.commit()
        
        # Provide feedback about OCR duty
        if prob_screenshot or qa_screenshot:
            flash('Challenge saved! Screenshots uploaded. I (Antigravity) will now extract the text for you.', 'success')
        else:
            flash('Portfolio optimized and updated successfully!', 'success')
            
        return redirect(url_for('home'))
            
    return render_template('admin.html', today=datetime.now().strftime('%Y-%m-%d'))

@app.route('/api/challenges')
def api_challenges():
    """API endpoint for challenges data"""
    challenges = Challenge.query.order_by(Challenge.date_id.desc()).all()
    return jsonify([{
        'date_id': c.date_id,
        'title': c.title,
        'image_path': c.image_path
    } for c in challenges])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

