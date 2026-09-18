# KG Migration — old `knowledge-graph/` → new `graphify-out/`

**Date:** 2026-09-17
**Tool:** graphifyy 0.9.63 (https://github.com/Graphify-Labs/graphify), verified via PyPI project URLs.

## Why
Rebuild the project knowledge graph with an automated, deterministic tool and consolidate to a single KG. Graphify parses code locally (tree-sitter AST) — it regenerates the *code-structure* graph but **cannot** reproduce hand-authored reasoning (decisions/why, timeline, security findings, algorithm rationale, open questions, audit).

## What happened
1. Searched the whole repo — exactly **one** existing KG found: `knowledge-graph/`. No other KG dirs / `graph.json` / reports anywhere.
2. Ran `graphify extract . --code-only` (offline, no API key, nothing left the machine — chosen because the repo contains live secrets) → 425 code files → 498 nodes / 878 edges / 32 communities, then `graphify cluster-only . --no-label`.
3. **Preserved** the irreplaceable content: all 13 hand-authored files copied byte-for-byte from `knowledge-graph/` into `graphify-out/narrative/`.

## Old → new mapping
| Old (`knowledge-graph/`) | Fate |
|---|---|
| `graph.json` | **Superseded** by `graphify-out/graph.json` (auto, richer: 498 vs ~40 nodes) |
| `01-overview.md` … `10-open-questions.md`, `CHANGELOG.md`, `README.md` | **Preserved** → `narrative/` |
| `standardization-audit.json` | **Preserved** → `narrative/` (not Graphify-regenerable) |

## ⚠️ Pending: deletion of old `knowledge-graph/`
All data has been extracted/transferred. The old KG is now fully redundant and safe to remove. **Deletion is on hold** — awaiting the user's decision on scope:
- (a) `git rm -r knowledge-graph/` + commit (recoverable from history), or
- (b) purge from all git history (irreversible; note: per `narrative/08-security.md` this is a public repo, so rewriting shared history is disruptive).

Until then, `knowledge-graph/` remains in place, untouched.
