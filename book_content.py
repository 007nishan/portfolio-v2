"""
book_content.py — assemble a BOOK dict from Markdown sources on disk.

Each book's chapters/modules live as .md files under its folder's src/ dir:
    Python Book/src/ch-0.md .. ch-8.md
    Linear Algebra/src/mod-0.md, mod-A.md .. mod-O.md, projects.md

A BOOK dict has:
    slug, title, subtitle, kicker, institution,
    sections: [{"md": "<markdown>", "unit": "<label>"}...]  (compiled in order)
    toc:      [{"title": grp, "items": [{"id","label","crumb"}...]}...]

The TOC is derived from the section files' opener ids + question/lesson anchors
so a human never hand-maintains it.
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))

_LA_MODULES = ["0"] + list("ABCDEFGHIJKLMNO")
_PY_CHAPTERS = [str(n) for n in range(9)]
_AWS_CHAPTERS = [str(n) for n in range(8)]   # aws-ml: ch-0..7 (MLA-C01 roadmap spine)

BOOKS = {
    "python": {
        "slug": "python",
        "title": "Programming in Python",
        "subtitle": "A hands-on companion, from the shell to object-oriented design.",
        "kicker": "A Portfolio Book",
        "institution": "IIT Madras Online Degree · compiled on portfolio-v2",
        "src_dir": os.path.join(HERE, "Python Book", "src"),
        "unit_files": ["ch-%s.md" % n for n in _PY_CHAPTERS],
        "site_rule": "",
    },
    "linear-algebra": {
        "slug": "linear-algebra",
        "title": "Linear Algebra for AI",
        "subtitle": "Oceanverse — a GeoGebra-first path from vectors to neural networks.",
        "kicker": "AI Vicharana Shala",
        "institution": "AI Vicharana Shala · IIT Ropar · compiled on portfolio-v2",
        "src_dir": os.path.join(HERE, "Linear Algebra", "src"),
        "unit_files": ["mod-%s.md" % m for m in _LA_MODULES] + ["projects.md"],
        "site_rule": "Strictly use GeoGebra",
    },
    "aws-ml": {
        "slug": "aws-ml",
        "title": "Notes as We Learn — AWS ML",
        "subtitle": "A living notebook for the AWS ML Engineer Associate (MLA-C01), filling in as the learning happens.",
        "kicker": "Learning in Public",
        "institution": "AWS Certification · MLA-C01 · compiled on portfolio-v2",
        "src_dir": os.path.join(HERE, "AWS ML", "src"),
        "unit_files": ["ch-%s.md" % n for n in _AWS_CHAPTERS],
        "site_rule": "",
    },
}

ALL_SLUGS = list(BOOKS.keys())

_OPENER_RE = re.compile(r'<section class="opener" id="(?P<id>[^"]+)">.*?<span class="chapter-num">(?P<num>[^<]*)</span>.*?#\s*(?P<title>[^\n<]+)', re.S)
_H2_RE = re.compile(r'^##\s+(?P<label>.+?)\s*\{:\s*#(?P<id>[\w-]+)', re.M)
_Q_RE = re.compile(r'^###\s+Question\s+(?P<n>\d+)\s*\{:\s*#q-(?P=n)\b', re.M)
_PROJECT_RE = re.compile(r'<div class="project-card" id="(?P<id>project-\d+)">.*?###\s*(?P<title>[^\n<]+)', re.S)


def _derive_toc_group(md, filename):
    """Build one TOC group for a section file from its opener + anchors."""
    m = _OPENER_RE.search(md)
    if not m:
        return None
    grp_title = m.group("title").strip()
    grp_id = m.group("id")
    items = [{"id": grp_id, "label": grp_title, "crumb": grp_title}]
    # lessons (Python) or questions (LA) or projects
    for lm in _H2_RE.finditer(md):
        items.append({"id": lm.group("id"), "label": lm.group("label").strip(), "crumb": grp_title})
    for qm in _Q_RE.finditer(md):
        n = qm.group("n")
        items.append({"id": "q-%s" % n, "label": "Q%s" % n, "crumb": grp_title})
    for pm in _PROJECT_RE.finditer(md):
        items.append({"id": pm.group("id"), "label": pm.group("title").strip(), "crumb": grp_title})
    return {"title": grp_title, "items": items}


def load_book(slug):
    if slug not in BOOKS:
        raise SystemExit("unknown book slug: %s (have %s)" % (slug, ALL_SLUGS))
    meta = BOOKS[slug]
    sections, toc = [], []
    missing = []
    for fname in meta["unit_files"]:
        path = os.path.join(meta["src_dir"], fname)
        if not os.path.isfile(path):
            missing.append(fname)
            continue
        with open(path, encoding="utf-8") as f:
            md = f.read()
        if not md.strip():
            continue
        sections.append({"md": md, "file": fname})
        grp = _derive_toc_group(md, fname)
        if grp:
            toc.append(grp)
    if not sections:
        raise SystemExit(
            "no source content for '%s' in %s (expected %s). "
            "Run content ingestion first." % (slug, meta["src_dir"], meta["unit_files"])
        )
    book = dict(meta)
    book["sections"] = sections
    book["toc"] = toc
    book["_missing_files"] = missing
    return book


if __name__ == "__main__":
    import sys

    for slug in (sys.argv[1:] or ALL_SLUGS):
        try:
            b = load_book(slug)
            print("%s: %d sections, %d TOC groups, missing=%s"
                  % (slug, len(b["sections"]), len(b["toc"]), b["_missing_files"]))
        except SystemExit as e:
            print("%s: %s" % (slug, e))
