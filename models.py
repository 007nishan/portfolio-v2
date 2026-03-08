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
    image_path = db.Column(db.String(255), nullable=False)
    
    # Store the actual markdown/code text for layout rendering
    problem_text = db.Column(db.Text, nullable=True)
    concepts_text = db.Column(db.Text, nullable=True)
    solution_code = db.Column(db.Text, nullable=True)
    quote_text = db.Column(db.Text, nullable=True)
    qa_text = db.Column(db.Text, nullable=True) # New field for Question/Answer section
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<Challenge {self.date_id}: {self.title}>"
