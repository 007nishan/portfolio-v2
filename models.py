from flask_sqlalchemy import SQLAlchemy
import datetime
import markdown

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

    __tablename__ = "challenges"

    id = db.Column(db.Integer, primary_key=True)
    date_id = db.Column(
        db.String(10), unique=True, nullable=False
    )  # Format: YYYY-MM-DD
    title = db.Column(db.String(255), nullable=False)
    image_path = db.Column(
        db.String(255), nullable=True
    )  # Nullable: FCC-synced challenges may not have images

    # Store the actual markdown/code text for layout rendering
    problem_text = db.Column(db.Text, nullable=True)
    concepts_text = db.Column(db.Text, nullable=True)
    solution_code = db.Column(db.Text, nullable=True)
    quote_text = db.Column(db.Text, nullable=True)
    qa_text = db.Column(db.Text, nullable=True)  # New field for Question/Answer section

    # FCC Daily Challenge API data (auto-synced)
    challenge_number = db.Column(
        db.Integer, nullable=True
    )  # FCC challenge # (1, 2, ... 211+)
    fcc_description = db.Column(
        db.Text, nullable=True
    )  # Full HTML description from FCC API
    fcc_js_tests = db.Column(db.Text, nullable=True)  # JSON string of JS test cases
    fcc_py_tests = db.Column(db.Text, nullable=True)  # JSON string of Python test cases
    fcc_starter_js = db.Column(
        db.Text, nullable=True
    )  # JavaScript starter code template
    fcc_starter_py = db.Column(db.Text, nullable=True)  # Python starter code template
    source = db.Column(db.String(20), nullable=True)  # 'manual' or 'fcc_api'

    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )

    def __repr__(self):
        return f"<Challenge {self.date_id}: {self.title}>"

    # ── Rendered-content properties (single place markdown is rendered) ──
    # Views previously each called markdown.markdown(field or "") with slightly
    # different null-guards. Centralizing here keeps rendering consistent (DRY).
    @property
    def problem_html(self):
        return markdown.markdown(self.problem_text) if self.problem_text else ""

    @property
    def concepts_html(self):
        return markdown.markdown(self.concepts_text) if self.concepts_text else ""

    @property
    def qa_html(self):
        return markdown.markdown(self.qa_text) if self.qa_text else ""

    @property
    def has_image(self):
        """The canonical 'does this challenge have an image' test. FCC-synced
        rows use image_path="" (empty-string sentinel); manual rows have a
        real filename. All readers should use this, not raw truthiness."""
        return bool(self.image_path)

    @property
    def display_description_html(self):
        """Single source for the challenge's problem description as HTML:
        prefer FCC's pre-rendered HTML, else render the manual markdown."""
        if self.fcc_description:
            return self.fcc_description
        if self.problem_text:
            return markdown.markdown(self.problem_text)
        return ""

# ==============================================================================
# ADDITIVE: USER MANAGEMENT & NOTEBOOK PROGRESS TABLES
# ==============================================================================

USERS_ID_REF = 'users.id'

class User(db.Model):

    """
    Stores registered users with GAuth/GitHub support credentials mapping.
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile = db.Column(db.String(20), unique=True, nullable=False) # PRIMARY KEY lookup standard
    dob = db.Column(db.Date, nullable=False)
    profile_pic = db.Column(db.String(255), nullable=True)
    
    # 3rd Party Integrations
    github_id = db.Column(db.String(50), nullable=True)
    github_token = db.Column(db.String(255), nullable=True) # Repo saving
    claude_token = db.Column(db.String(255), nullable=True) # Personal API usage
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    is_verified = db.Column(db.Boolean, default=False) # OTP Verification tracker

    def __repr__(self):
        return f"<User {self.name} ({self.email})>"

class ConceptStrength(db.Model):
    """
    Tracks User Concept understanding score mapping reward/penalties models.
    """
    __tablename__ = "concept_strengths"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(USERS_ID_REF), nullable=False)

    concept = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, default=100) # 100 Base Score, penalty penalizes -10, correct answers reward +10
    times_encountered = db.Column(db.Integer, default=0)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class UserNotebook(db.Model):
    """
    Saves personal summaries referencing learning journey timelines.
    """
    __tablename__ = "user_notebooks"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(USERS_ID_REF), nullable=False)

    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'), nullable=False)
    summary_notes = db.Column(db.Text, nullable=True) # Auto-generated summary of start to end nodes mapping
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Comment(db.Model):
    """
    Saves discussion board triggers conversation nodes thread mapped setups.
    """
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(USERS_ID_REF), nullable=False)

    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    # Relationship to render names
    user = db.relationship('User', backref=db.backref('comments', lazy=True))


