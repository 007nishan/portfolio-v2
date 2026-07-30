# Source Structure — "Notes as We Learn — AWS ML" (MLA-C01)

- **Source repo:** `C:\Users\nishanrh\AWS-ML-Notes\` (override with env `AWS_ML_NOTES_DIR`).
  Content nodes live at `engine/content/M*.md`; the syllabus map is `KNOWLEDGE_GRAPH.md`.
- **Slug / title:** `aws-ml` — *Notes as We Learn — AWS ML*. Kicker "Learning in Public".
- **Institution line:** AWS Certification · MLA-C01 · compiled on portfolio-v2.
- **Nature:** a **living roadmap** book. The full AWS ML Engineer Associate journey is laid out as a
  fixed 8-chapter spine; written lessons render in full, and chapters not yet reached render as honest
  "coming as we learn" roadmap openers that fill in over time.
- **Brand rule (non-negotiable):** import *content + methodology only*. The website BrandKit and book UI
  are the single source of truth — the notes repo's own `brandkit.css`/`reader.js` are ignored. Output is
  plain BCS Markdown; the site's frozen `render_book_md` + reader shell + `book_cover.py` + `make_book_pdf.py`
  supply 100% of the look-and-feel (same as `python` and `linear-algebra`). Lead accent = in-kit gold `#d58000`.

## Chapter spine (fixed) — ids `ch-0 … ch-7`

| id   | Chapter                                                | Source today |
|------|--------------------------------------------------------|--------------|
| ch-0 | Foundations — Math, Programming & "What Is a Model?"   | roadmap stub |
| ch-1 | Core Machine Learning Concepts                         | roadmap stub |
| ch-2 | Deep Learning & Modern AI                              | roadmap stub |
| ch-3 | Responsible AI, Problem Formulation & SageMaker        | roadmap stub |
| ch-4 | **Domain 1 — Data Preparation (28%)**                  | **written: M1_1a–f (6 lessons)** + roadmap tail |
| ch-5 | Domain 2 — Model Development (26%)                      | roadmap stub |
| ch-6 | Domain 3 — Deployment & Orchestration (22%)            | roadmap stub |
| ch-7 | Domain 4 — Monitoring, Maintenance & Security (24%)    | roadmap stub |

**Node → chapter map:** a node file `M<d>_*` belongs to Domain `d`, which maps to a chapter:
`M1_* → ch-4`, `M2_* → ch-5`, `M3_* → ch-6`, `M4_* → ch-7`. Within a chapter, lessons are numbered in
natural node order (`M1_1a` before `M1_1f` before `M1_2`) and anchored `#ch-{n}-lesson-{k}`.

## The transform (`aws_sync.py`)

Run `python aws_sync.py` (also invoked by `dev_sync.sh` step 0). It reads `engine/content/M*.md` and
writes `AWS ML/src/ch-0.md … ch-7.md`. Per written node it:

- turns the H1 `# M1_1a — Title` into a lesson heading `## Title {: #ch-4-lesson-N }`;
- **demotes** every body heading one level (`##`→`###`, `###`→`####`) so sections nest under the lesson
  `<h2>` — matches the site's opener-`h1` → lesson-`h2` → `h3/h4` convention and keeps the lint clean;
- **strips** the header-zone status/meta italics (`_Course …_`, `_Status: …_`) and the trailing
  author-only sections (`### Images for this node …`, `### Overlap / cross-refs noted …`) to EOF. This
  also removes the only image references, so there is nothing for the R040 alt-text / R050 no-links gates
  to catch;
- converts `> **Exam trap:** …` / `> **Watch out:** …` blockquotes into on-brand `!!! warning` callouts,
  and other `> **Label:** …` notes into `!!! note` callouts. Tables, prose, and the bold
  "In real life:" / "Why it matters:" leads pass through unchanged;
- **guards**: fails loudly if any `[text](url)`, bare URL, or `![img]()` leaks into the book body.

The script is **idempotent** (re-running with unchanged notes rewrites byte-identical files, atomic
tmp→replace) and **safe when the notes repo is absent** (prints a notice, leaves committed `src/*.md`
untouched, exits 0). Use `python aws_sync.py --check` in CI to detect drift without writing.

## Ingestion notes

- Only Domain 1 / Course 1.1 (`M1_1a`–`M1_1f`) is written today → all six land in `ch-4`; every other
  chapter is a roadmap opener. As the engine writes more nodes, re-running the sync fills chapters in.
- Roadmap bullets are grounded in the user's own `KNOWLEDGE_GRAPH.md`, not invented.
- **No fabrication:** written lessons are the engine's own prose, only structurally reshaped (heading
  levels + anchors + callout syntax). Roadmap content is clearly labelled "coming as we learn".
- Files under `AWS ML/src/` are generated **but committed**, so the deploy server (which has no notes
  repo) can build HTML + PDF from source like the other two books.
