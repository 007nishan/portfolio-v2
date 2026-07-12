# 🧠 Portfolio-v2 Knowledge Graph

> A living, chronological record of **everything** that exists in this project: every finding, decision, algorithm, the reasoning behind each decision, the empirical data that drove it, and the technology used behind every corner of the website.
>
> Goal: **never stay in the dark about any part of this project.**

This knowledge graph is maintained inside the repo so it travels with the code and stays version-controlled alongside it.

---

## 📚 How this knowledge graph is organized

| File | What it captures |
|------|------------------|
| [`01-overview.md`](01-overview.md) | What the project is, one-page mental model, tech stack |
| [`02-architecture.md`](02-architecture.md) | System components, request flow, deployment topology, diagrams |
| [`03-data-model.md`](03-data-model.md) | Database schema, every table/column, the append-only rule |
| [`04-timeline.md`](04-timeline.md) | Chronological history of every commit, feature, and decision |
| [`05-decisions.md`](05-decisions.md) | Decision log (ADR-style): what, why, empirical data, alternatives |
| [`06-algorithms.md`](06-algorithms.md) | Every algorithm/technique used and why it was chosen |
| [`07-components.md`](07-components.md) | File-by-file catalog of every module, template, script |
| [`08-security.md`](08-security.md) | Security findings, risks, and remediation status |
| [`09-operations.md`](09-operations.md) | Runbook: how to run, deploy, sync, recover |
| [`10-open-questions.md`](10-open-questions.md) | Unknowns, TODOs, things to confirm with the server owner |
| [`graph.json`](graph.json) | Machine-readable node/edge graph of entities & relationships |
| [`CHANGELOG.md`](CHANGELOG.md) | Append-only log of updates to THIS knowledge graph |

---

## 🔑 The single most important thing to know first

⚠️ **This is a PUBLIC GitHub repo that contains live secrets and remote-code-execution surfaces.**
Read [`08-security.md`](08-security.md) **before** doing anything else. Highest priorities:
- Hardcoded SSH password for `nishan@192.168.1.150` in 7 files.
- Live Telegram bot token in `app.py` and `telegram_bridge.py`.
- A Telegram bot that executes arbitrary shell + Python + LLM-driven commands on the server.
- `/admin` route with **no authentication** (anyone can upload/overwrite content).

---

## 🔄 Maintenance protocol

Whenever we touch the project:
1. Add a dated entry to [`04-timeline.md`](04-timeline.md).
2. If a decision was made, log it in [`05-decisions.md`](05-decisions.md) with the *why* + *empirical data*.
3. If an entity/relationship changed, update [`graph.json`](graph.json).
4. Record the update itself in [`CHANGELOG.md`](CHANGELOG.md).

*Knowledge graph initialized: 2026-07-12 (from repo state at commit `e084129`).*
