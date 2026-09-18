# 🧠 Portfolio-v2 Knowledge Graph (Graphify)

The single, canonical knowledge graph for this project. It has two halves:

## 1. Auto-generated code graph (Graphify)
Deterministic, local, no LLM — rebuilt from the codebase with [Graphify](https://github.com/Graphify-Labs/graphify) (`graphifyy`, tree-sitter AST).

| File | What it is |
|------|-----------|
| [`graph.json`](graph.json) | Machine-readable graph — 498 nodes, 878 edges, 32 communities |
| [`graph.html`](graph.html) | Interactive browser view — click/filter/search nodes |
| [`GRAPH_REPORT.md`](GRAPH_REPORT.md) | God-nodes, communities, highlights |
| `.graphify_analysis.json`, `manifest.json`, `cache/` | Incremental-rebuild state |

**Regenerate after code changes (no API cost):**
```bash
graphify update .          # incremental re-extract of changed code
graphify cluster-only . --no-label   # regenerate report + html locally
```
Community names were generated with `graphify cluster-only . --backend claude-cli` (one LLM pass via the local Claude CLI). Re-run it after large refactors to refresh names; use `--no-label` to stay fully offline.

## 2. Preserved human narrative ([`narrative/`](narrative/))
Hand-authored reasoning that Graphify **cannot** regenerate — carried forward verbatim from the previous knowledge graph. Maintain these manually.

| File | What it captures |
|------|------------------|
| `narrative/01-overview.md` … `03-data-model.md` | Project mental model, architecture, schema |
| `narrative/04-timeline.md` | Chronological history of commits/features/decisions |
| `narrative/05-decisions.md` | Decision log: what, **why**, empirical data, alternatives |
| `narrative/06-algorithms.md` | Every algorithm/technique and why it was chosen |
| `narrative/07-components.md` | File-by-file catalog |
| `narrative/08-security.md` | ⚠️ Security findings, live-secret inventory, remediation status |
| `narrative/09-operations.md` | Runbook: run, deploy, sync, recover |
| `narrative/10-open-questions.md` | Unknowns / TODOs |
| `narrative/CHANGELOG.md` | Append-only log of KG updates |
| `narrative/standardization-audit.json` | Book-content standardization audit + plan |

## Maintenance protocol
1. Code changed → `graphify update .` (auto graph stays fresh).
2. A decision was made → append to `narrative/05-decisions.md` (with *why* + data) and `narrative/04-timeline.md`.
3. Record the update in `narrative/CHANGELOG.md`.

See [`MIGRATION.md`](MIGRATION.md) for how this replaced the old `knowledge-graph/`.
