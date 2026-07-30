r"""
aws_sync.py — turn the AWS-ML-Notes engine's content into the "Notes as We Learn
— AWS ML" book source (BCS-compliant Markdown under `AWS ML/src/ch-*.md`).

This is the "as we learn" bridge. The adaptive-learning engine at
`AWS_ML_NOTES_DIR` (default C:\Users\nishanrh\AWS-ML-Notes) grows content nodes
under `engine/content/M*.md`. This script transforms whatever is written today
into the site's book component vocabulary and drops it into the fixed 8-chapter
MLA-C01 roadmap spine. Chapters with no written node yet render as honest
"coming as we learn" roadmap openers.

Design rules (why this is safe):
  * Content + methodology ONLY are imported. The website BrandKit / book UI is the
    single source of truth — the notes repo's own brandkit.css/reader.js are never
    touched. The output is plain BCS Markdown; the site's frozen renderer + reader
    shell supply 100% of the look-and-feel.
  * Idempotent + atomic: re-running with unchanged notes produces byte-identical
    files (tmp -> os.replace).
  * Safe when the notes repo is absent (other machines, the deploy server): it
    prints a notice, leaves any committed src/*.md untouched, and exits 0.
  * No fabrication: written lessons are the engine's own prose, only structurally
    reshaped (heading levels + anchors + on-brand callouts). Roadmap stubs are
    clearly labelled and built from the user's own KNOWLEDGE_GRAPH.md syllabus map.

Usage:
    python aws_sync.py            # transform notes -> AWS ML/src/ch-*.md
    python aws_sync.py --check    # report what WOULD change; exit 1 if drift (CI)
"""
import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES_DIR = os.environ.get("AWS_ML_NOTES_DIR", r"C:\Users\nishanrh\AWS-ML-Notes")
CONTENT_DIR = os.path.join(NOTES_DIR, "engine", "content")
OUT_DIR = os.path.join(HERE, "AWS ML", "src")

# Domain d (M{d}_...) -> chapter index. Domains 1-4 live in chapters 4-7.
_DOMAIN_TO_CH = {1: 4, 2: 5, 3: 6, 4: 7}

# ---------------------------------------------------------------------------
# Fixed MLA-C01 roadmap spine (ids ch-0 .. ch-7). Titles/leads/roadmap bullets
# are grounded in the user's own KNOWLEDGE_GRAPH.md — not invented here.
# ---------------------------------------------------------------------------
SPINE = [
    {
        "title": "Foundations — Math, Programming & “What Is a Model?”",
        "lead": "The floor everything else rests on: the math, data, and programming intuition an ML engineer keeps reaching back to.",
        "roadmap": [
            "Math for ML: vectors, matrices & dot products → features and weights.",
            "Probability & statistics: distributions, mean/variance, conditional probability.",
            "Calculus intuition: derivatives & gradients → how models “learn”.",
            "Programming & data: Python, data structures, JSON; tabular data (rows = observations, columns = features).",
            "What a “model” really is: a function mapping features → prediction, tuned by data.",
        ],
    },
    {
        "title": "Core Machine Learning Concepts",
        "lead": "The vocabulary that the whole certification is built on.",
        "roadmap": [
            "Feature vs. label; ML as a subset of AI that learns patterns without explicit rules.",
            "The three learning paradigms: supervised, unsupervised, reinforcement.",
            "Classification vs. regression; clustering, dimensionality reduction, anomaly detection.",
            "Overfitting vs. underfitting; the train / validate / test split.",
        ],
    },
    {
        "title": "Deep Learning & Modern AI",
        "lead": "From artificial neurons to the foundation models behind generative AI.",
        "roadmap": [
            "Deep learning as a subset of ML; artificial neural networks and hidden layers.",
            "Automatic feature extraction (input → edges → parts → object).",
            "Generative AI: creating new text, image, audio, video, and code.",
            "Foundation Models and Large Language Models: pre-train once, adapt to many tasks.",
        ],
    },
    {
        "title": "Responsible AI, Problem Formulation & SageMaker",
        "lead": "Turning a business problem into a well-posed ML problem — responsibly — and the platform it runs on.",
        "roadmap": [
            "Responsible AI — the eight dimensions (fairness, explainability, privacy & security, safety, controllability, veracity & robustness, governance, transparency).",
            "Problem formulation: define the business problem, choose the data, set measurable ML success criteria.",
            "Feasibility = f(data availability, problem complexity).",
            "Amazon SageMaker & SageMaker Studio: the managed build / train / deploy platform.",
        ],
    },
    {
        "title": "Domain 1 — Data Preparation",
        "lead": "Collecting, ingesting and storing data, then transforming and validating it — the front door of the whole ML process and 28% of the MLA-C01 exam.",
        "roadmap": [
            "Data extraction (M1_1g) — awaiting course input.",
            "Data merging (M1_1h) — awaiting course input.",
            "Ingestion & storage troubleshooting (M1_1i) — awaiting course input.",
            "Transform Data (M1_2): cleaning, encoding, feature engineering; Feature Store, Data Wrangler, Glue.",
            "Validate & Prepare for Modeling (M1_3): bias mitigation, split/shuffle/augment; DataBrew, Data Quality.",
        ],
        "roadmap_title": "Still to come in this chapter",
    },
    {
        "title": "Domain 2 — Model Development",
        "lead": "Choosing an approach, training and tuning, then evaluating the result — 26% of the exam.",
        "roadmap": [
            "Choosing a modelling approach for the problem and data.",
            "Training and hyperparameter tuning.",
            "Model evaluation and metrics.",
        ],
    },
    {
        "title": "Domain 3 — Deployment & Orchestration",
        "lead": "Getting a working model into dependable production — infrastructure, CI/CD and pipelines — 22% of the exam.",
        "roadmap": [
            "Deployment infrastructure and endpoints.",
            "CI/CD for ML.",
            "Orchestrating ML pipelines.",
        ],
    },
    {
        "title": "Domain 4 — Monitoring, Maintenance & Security",
        "lead": "Keeping a live model healthy — drift, cost/performance and security — 24% of the exam.",
        "roadmap": [
            "Monitoring for data and model drift.",
            "Cost and performance optimisation.",
            "Securing ML workloads.",
        ],
    },
]

_LINK_RE = re.compile(r"\[[^\]]+\]\([^)]+\)")          # [text](url)
_IMG_RE = re.compile(r"!\[[^\]]*\]\([^)]*\)")          # ![alt](src)
_URL_RE = re.compile(r"https?://")                     # bare URL
_TITLE_RE = re.compile(r"^#\s+(?:M\d+_\d+[a-z]?\s*[—-]\s*)?(.+)$")
_NODE_ID_RE = re.compile(r"^#\s+(M(\d+)_(\d+)([a-z]?))\b")
_BLOCKQUOTE_RE = re.compile(r"^>\s*(?:\*\*(?P<label>[^*]+?):\*\*\s*)?(?P<body>.*)$")
_META_ITALIC_RE = re.compile(r"^_[^_].*_$")
_TRAILING_META_RE = re.compile(r"^###\s+(images?|overlap)\b", re.I)
# The notes engine embeds its OWN inline figure markers `{{img: file | caption}}`
# (and empty `{{img:}}` placeholders). We render text-first books with no imported
# binaries, and — critically — the compiled book is served through a Jinja template,
# so a raw `{{ … }}` would be parsed as a Jinja print statement and 500 the reader.
_IMG_TOKEN_RE = re.compile(r"\{\{\s*img:.*?\}\}", re.S)
# Any residual Jinja-hostile delimiter must never reach the reader template.
_JINJA_HOSTILE_RE = re.compile(r"\{\{|\}\}|\{%|%\}")


# ---------------------------------------------------------------------------
# Per-node transform
# ---------------------------------------------------------------------------
def _node_sort_key(name):
    """Natural order: M1_1a < M1_1f < M1_2 < M1_3 < M2_1 ..."""
    m = _NODE_ID_RE.match("# " + name)
    if not m:
        return (99, 99, "z")
    return (int(m.group(2)), int(m.group(3)), m.group(4) or "")


def _domain_of(name):
    m = re.match(r"^M(\d+)_", name)
    return int(m.group(1)) if m else None


def _convert_blockquote(line):
    """`> **Exam trap:** ...` -> on-brand admonition. Trap/watch-out -> warning,
    everything else -> note. Returns a list of output lines (blank-separated)."""
    m = _BLOCKQUOTE_RE.match(line)
    if not m:
        return [line]
    label = (m.group("label") or "").strip()
    body = m.group("body").strip()
    if label:
        kind = "warning" if re.search(r"trap|watch out|caution", label, re.I) else "note"
        return ["", '!!! %s "%s"' % (kind, label), "", "    " + body, ""]
    return ["", '!!! note', "", "    " + body, ""]


def _demote_headings(line):
    """Body `## x` -> `### x`, `### x` -> `#### x` so sections nest under the
    lesson <h2>. Capped at h6."""
    m = re.match(r"^(#{2,5})(\s+.*)$", line)
    if m:
        return "#" + m.group(1) + m.group(2)
    return line


def transform_node(md, node_id):
    """One engine node .md -> a book lesson body (no heading id yet). Returns
    (title, body_lines)."""
    lines = md.splitlines()

    # 1. Lesson title from the H1 (strip the "M1_1a — " node prefix).
    title, start = node_id, 0
    for i, l in enumerate(lines):
        if l.startswith("# "):
            mt = _TITLE_RE.match(l)
            title = mt.group(1).strip() if mt else l[2:].strip()
            start = i + 1
            break
    body = lines[start:]

    # 2. Cut the trailing author-only sections (Images / Overlap) to EOF.
    cut = len(body)
    for i, l in enumerate(body):
        if _TRAILING_META_RE.match(l.strip()):
            cut = i
            break
    body = body[:cut]
    while body and body[-1].strip() in ("", "---"):
        body.pop()

    # 3. Drop the header-zone status/meta italics (before the first section).
    first_h2 = next((i for i, l in enumerate(body) if l.strip().startswith("## ")), len(body))
    kept = []
    for i, l in enumerate(body):
        if i < first_h2 and _META_ITALIC_RE.match(l.strip()):
            continue
        kept.append(l)
    body = kept

    # 4. Demote headings + convert blockquotes; drop the engine's inline
    #    {{img: ...}} figure markers (text-first book; no imported binaries).
    out = []
    for l in body:
        if _IMG_TOKEN_RE.search(l):
            l = _IMG_TOKEN_RE.sub("", l)
            if l.strip() == "":
                continue
        if l.lstrip().startswith(">"):
            out.extend(_convert_blockquote(l))
        else:
            out.append(_demote_headings(l))

    # collapse >1 blank line
    squashed, blank = [], False
    for l in out:
        if l.strip() == "":
            if not blank:
                squashed.append("")
            blank = True
        else:
            squashed.append(l)
            blank = False
    while squashed and squashed[0] == "":
        squashed.pop(0)
    while squashed and squashed[-1] == "":
        squashed.pop()

    # 5. Guard: a printed book has no links/URLs/inline images (R050/R040), and
    #    the reader is a Jinja template so no `{{ }}` / `{% %}` may survive.
    joined = "\n".join(squashed)
    if _LINK_RE.search(joined) or _IMG_RE.search(joined) or _URL_RE.search(joined):
        raise SystemExit(
            "aws_sync: link/URL/image leaked from node %s — the book forbids them "
            "(R050/R040). Offending text near: %r" % (node_id, joined[:160])
        )
    mh = _JINJA_HOSTILE_RE.search(joined)
    if mh:
        s = max(0, mh.start() - 60)
        raise SystemExit(
            "aws_sync: Jinja-hostile delimiter %r leaked from node %s — it would "
            "break the reader template. Near: %r"
            % (mh.group(0), node_id, joined[s:mh.end() + 60])
        )
    return title, squashed


# ---------------------------------------------------------------------------
# Chapter assembly
# ---------------------------------------------------------------------------
def _opener(ch_idx, title):
    return (
        '<section class="opener" id="ch-%d">\n'
        '<span class="chapter-num">%d</span>\n\n'
        "# %s\n"
        '<span class="accent-rule"></span>\n'
        "</section>\n" % (ch_idx, ch_idx, title)
    )


def _roadmap_block(spec, written):
    title = spec.get("roadmap_title", "Coming as we learn")
    if written:
        intro = "More of this chapter is on the roadmap and will fill in as the notes are written. Planned topics:"
    else:
        intro = ("This chapter is on the roadmap. It will fill in with worked notes as the "
                 "learning gets there — for now, here is what it will cover:")
    out = ["", '!!! note "%s"' % title, "", "    " + intro, ""]
    for b in spec["roadmap"]:
        out.append("    - " + b)
    out.append("")
    return out


def build_chapter(ch_idx, nodes):
    """nodes: sorted list of (node_id, md_text) whose domain maps to this chapter."""
    spec = SPINE[ch_idx]
    parts = [_opener(ch_idx, spec["title"]), ""]
    if spec.get("lead"):
        parts += ["*" + spec["lead"] + "*", ""]

    lesson_no = 0
    for node_id, md in nodes:
        lesson_no += 1
        ltitle, lbody = transform_node(md, node_id)
        parts.append("## %s {: #ch-%d-lesson-%d }" % (ltitle, ch_idx, lesson_no))
        parts.append("")
        parts.extend(lbody)
        parts.append("")

    if spec.get("roadmap"):
        parts.extend(_roadmap_block(spec, written=bool(nodes)))

    text = "\n".join(parts).rstrip() + "\n"
    return text


def collect_nodes():
    """Read engine/content/M*.md grouped by chapter index. Returns
    {ch_idx: [(node_id, md), ...] sorted}."""
    by_ch = {i: [] for i in range(len(SPINE))}
    if not os.path.isdir(CONTENT_DIR):
        return by_ch, False
    files = [f for f in os.listdir(CONTENT_DIR)
             if re.match(r"^M\d+_.*\.md$", f) and not f.startswith("_")]
    for f in sorted(files, key=lambda n: _node_sort_key(os.path.splitext(n)[0])):
        node_id = os.path.splitext(f)[0]
        dom = _domain_of(node_id)
        ch = _DOMAIN_TO_CH.get(dom)
        if ch is None:
            continue
        with open(os.path.join(CONTENT_DIR, f), encoding="utf-8") as fh:
            md = fh.read()
        if md.strip():
            by_ch[ch].append((node_id, md))
    return by_ch, True


def _write_atomic(path, text):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    os.replace(tmp, path)


def sync(check=False):
    by_ch, have_notes = collect_nodes()
    if not have_notes:
        print("aws_sync: notes repo not found at %s — leaving committed src/*.md "
              "untouched (nothing to do here)." % NOTES_DIR)
        return 0

    os.makedirs(OUT_DIR, exist_ok=True)
    changed, written_ct = [], 0
    for ch_idx in range(len(SPINE)):
        nodes = by_ch[ch_idx]
        written_ct += len(nodes)
        text = build_chapter(ch_idx, nodes)
        path = os.path.join(OUT_DIR, "ch-%d.md" % ch_idx)
        old = None
        if os.path.isfile(path):
            with open(path, encoding="utf-8") as f:
                old = f.read()
        if old != text:
            changed.append("ch-%d.md" % ch_idx)
            if not check:
                _write_atomic(path, text)

    total_lessons = sum(len(by_ch[i]) for i in range(len(SPINE)))
    if check:
        if changed:
            print("aws_sync --check: DRIFT in %s (run `python aws_sync.py`)" % ", ".join(changed))
            return 1
        print("aws_sync --check: up to date (%d lessons across %d chapters)."
              % (total_lessons, len(SPINE)))
        return 0

    print("aws_sync: wrote %d chapter file(s); %d changed (%s). %d written lesson(s) total."
          % (len(SPINE), len(changed), ", ".join(changed) or "none", total_lessons))
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="report drift without writing; exit 1 if out of date")
    args = ap.parse_args()
    sys.exit(sync(check=args.check))
