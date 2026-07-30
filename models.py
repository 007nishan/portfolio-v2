from flask_sqlalchemy import SQLAlchemy
import datetime
import markdown

db = SQLAlchemy()

# ==============================================================================
# BOOK MARKDOWN RENDERER (BCS v1.1 §A) — the ONE place book Markdown -> HTML.
# ------------------------------------------------------------------------------
# Frozen extension set: editing it is a Book-Compilation-Standard revision.
# Math is protected by pymdownx.arithmatex (generic mode) here and baked to
# KaTeX HTML in the build step (katex_prerender.render), never at request time.
# ==============================================================================


def _book_output_fence(source, language, css_class, options, md, **kwargs):
    esc = source.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return '<pre class="book-output"><samp>' + esc + "</samp></pre>"


def _book_repl_fence(source, language, css_class, options, md, **kwargs):
    esc = source.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return '<pre class="book-output book-output--repl"><samp>' + esc + "</samp></pre>"


def _inline_md(text):
    """Convert inline markdown WITHOUT re-entering the live parser (fresh
    instance — python-markdown parsers are stateful/non-reentrant)."""
    return markdown.Markdown(extensions=["attr_list"]).convert(text.strip())


def _book_figure_fence(source, language, css_class, options, md, **kwargs):
    """Figure fence. First line = image path under static/ (a `url_for` is applied
    at compile time via {{ }} is not used — path is written relative to static/);
    remaining lines = caption (Markdown). An optional first line prefixed with
    'alt:' supplies explicit alt text; otherwise the caption's plain text is used
    as alt (never empty — satisfies the R040 accessibility gate)."""
    import re as _re
    raw = source.strip().split("\n")
    alt = ""
    if raw and raw[0].lower().startswith("alt:"):
        alt = raw[0][4:].strip()
        raw = raw[1:]
    src_path = raw[0].strip() if raw else ""
    caption_md = "\n".join(raw[1:]).strip()
    caption = _inline_md(caption_md) if caption_md else ""
    if not alt:
        # derive alt from caption plain text (strip tags), fall back to filename
        alt = _re.sub(r"<[^>]+>", "", caption).strip() or src_path.rsplit("/", 1)[-1]
    # escape double-quotes in alt for the attribute
    alt_attr = alt.replace('"', "&quot;")
    src_url = "/static/" + src_path.lstrip("/")
    return (
        f'<figure class="book-figure">'
        f'<img src="{src_url}" alt="{alt_attr}">'
        f'<figcaption class="book-figure__caption">{caption}</figcaption></figure>'
    )


def _rule_banner_fence(source, language, css_class, options, md, **kwargs):
    return '<aside class="rule-banner" role="note">' + _inline_md(source) + "</aside>"


BOOK_MD_EXTENSIONS = [
    "pymdownx.superfences",   # code + custom output/repl/figure/rule fences
    "pymdownx.highlight",     # class-only Pygments token spans
    "pymdownx.arithmatex",    # math source protection (generic mode)
    "tables",
    "attr_list",              # {: #q-3 .question } + figure fence opts
    "md_in_html",             # <details markdown> inner parse
    "admonition",             # STOCK python-markdown ext (NOT pymdownx.admonition)
    "toc",
    "sane_lists",
]
BOOK_MD_CONFIGS = {
    "pymdownx.highlight": {
        "use_pygments": True,
        "guess_lang": False,
        "css_class": "bcs-hl",
        "pygments_lang_class": True,  # add "language-<lang>" to the wrapper div
    },
    "pymdownx.superfences": {
        "css_class": "book-code",
        "disable_indented_code_blocks": True,
        "custom_fences": [
            {"name": "output", "class": "book-output", "format": _book_output_fence},
            {"name": "repl", "class": "book-output", "format": _book_repl_fence},
            {"name": "figure", "class": "book-figure", "format": _book_figure_fence},
            {"name": "rule", "class": "rule-banner", "format": _rule_banner_fence},
        ],
    },
    "pymdownx.arithmatex": {
        "generic": True,
        "smart_dollar": True,
        "block_tag": "div",
        "tex_inline_wrap": ["\\(", "\\)"],
        "tex_block_wrap": ["\\[", "\\]"],
        "preview": False,
    },
    "toc": {"permalink": False},
    "admonition": {},
}


def _slugify_factory(prefix):
    """toc slugify that namespaces auto-generated heading ids with a per-section
    prefix, so generic sub-headings ('Introduction', 'Mutability') that recur
    across chapters do not collide when sections are concatenated. Explicit
    {: #id } anchors bypass slugify and are untouched."""
    from markdown.extensions.toc import slugify as _base

    def _slug(value, sep):
        base = _base(value, sep)
        return "%s-%s" % (prefix, base) if prefix else base

    return _slug


import re as _re

# Container blocks whose INNER Markdown must be parsed (headings, prose, math).
# md_in_html only descends into a raw-HTML block when it carries a `markdown`
# attribute, so we inject one on the opener/project-card wrappers automatically
# (keeps the authored source clean — authors don't write markdown="1").
_MD_BLOCK_OPEN = _re.compile(
    r'<(section|div)\s+class="(opener|project-card)"([^>]*?)>'
)


def _enable_md_in_blocks(text):
    def _add_attr(m):
        tag, cls, rest = m.group(1), m.group(2), m.group(3)
        if "markdown=" in rest:
            return m.group(0)
        return f'<{tag} class="{cls}"{rest} markdown="1">'

    return _MD_BLOCK_OPEN.sub(_add_attr, text)


def render_book_md(text, id_prefix=""):
    """The ONE place book Markdown becomes HTML (BCS v1.1). Fresh, non-reentrant
    Markdown instance per call. Math placeholders (.arithmatex) are baked to
    KaTeX in the build step (katex_prerender.render), NOT here. `id_prefix`
    namespaces auto-generated heading ids to avoid cross-section collisions."""
    if not text:
        return ""
    text = _enable_md_in_blocks(text)
    configs = dict(BOOK_MD_CONFIGS)
    if id_prefix:
        configs = {**BOOK_MD_CONFIGS, "toc": {**BOOK_MD_CONFIGS.get("toc", {}),
                                              "slugify": _slugify_factory(id_prefix)}}
    md = markdown.Markdown(extensions=BOOK_MD_EXTENSIONS, extension_configs=configs)
    return md.convert(text)


try:
    import nh3

    _ALLOWED_TAGS = {
        "p", "br", "pre", "code", "em", "strong", "ul", "ol", "li", "a", "h1", "h2",
        "h3", "h4", "blockquote", "table", "thead", "tbody", "tr", "th", "td", "span",
        "div", "details", "summary", "figure", "figcaption", "img", "aside", "samp",
        "sup", "sub",
    }

    def _sanitize_fcc(html):
        """Sanitize the raw FCC HTML passthrough path (defense in depth; the
        authored-Markdown path is trusted and never re-sanitized)."""
        return nh3.clean(html, tags=_ALLOWED_TAGS, link_rel="noopener noreferrer")

except ImportError:  # nh3 optional at import time; falls back to raw passthrough
    def _sanitize_fcc(html):
        return html

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
    # NOT NULL to match the live schema (the original migration created it NOT
    # NULL and the append-only rule forbids relaxing it). FCC-synced rows use
    # the empty-string sentinel ""; readers must use the `has_image` property,
    # not raw truthiness. (DBN-5 / SSOT-5)
    image_path = db.Column(
        db.String(255), nullable=False, default=""
    )

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


