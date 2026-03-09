from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

# ==============================================================================
# HARD RULE: APPEND-ONLY, FORWARD-COMPATIBLE DATABASE DESIGN
# ------------------------------------------------------------------------------
# As per project requirements, the database schema must NEVER be destructively 
# altered. Do not DROP tables or DROP columns even if features are deprecated.
# We only expand (ADD new tables, ADD nullable columns) to ensure backward 
# compatibility for all historical data versions throughout the app's lifecycle.
# All migrations MUST be additive.
# ==============================================================================

class Challenge(db.Model):
    """
    Stores daily coding challenges sync'd from the github_challenges folder.
    """
    __tablename__ = 'challenges'

    id = db.Column(db.Integer, primary_key=True)
    date_id = db.Column(db.String(10), unique=True, nullable=False) # Format: YYYY-MM-DD
    title = db.Column(db.String(255), nullable=False)
    image_path = db.Column(db.String(255), nullable=True)  # Nullable: FCC-synced challenges may not have images
    
    # Store the actual markdown/code text for layout rendering
    problem_text = db.Column(db.Text, nullable=True)
    concepts_text = db.Column(db.Text, nullable=True)
    solution_code = db.Column(db.Text, nullable=True)
    quote_text = db.Column(db.Text, nullable=True)
    qa_text = db.Column(db.Text, nullable=True) # New field for Question/Answer section

    # FCC Daily Challenge API data (auto-synced)
    challenge_number = db.Column(db.Integer, nullable=True)       # FCC challenge # (1, 2, ... 211+)
    fcc_description = db.Column(db.Text, nullable=True)           # Full HTML description from FCC API
    fcc_js_tests = db.Column(db.Text, nullable=True)              # JSON string of JS test cases
    fcc_py_tests = db.Column(db.Text, nullable=True)              # JSON string of Python test cases
    fcc_starter_js = db.Column(db.Text, nullable=True)            # JavaScript starter code template
    fcc_starter_py = db.Column(db.Text, nullable=True)            # Python starter code template
    source = db.Column(db.String(20), nullable=True)              # 'manual' or 'fcc_api'
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<Challenge {self.date_id}: {self.title}>"
