# Ingestion Report — Oceanverse / Linear Algebra (AI Vicharana Shala @ IIT Ropar)

- **Source:** https://sudarshansudarshan.github.io/aicamp/oceanverse/
- **Ingested:** module-by-module from the live page (raw HTML re-pulled to recover content beyond the earlier Q154 truncation).
- **Files written (18):** `mod-0.md`, `mod-A.md` … `mod-O.md` (16 module files), `projects.md`, and this report.

## 1. Blank-solution question list (rendered as the exact placeholder)

Every question below has its solution body rendered as exactly `Solution not provided in the source material.` because the solution is genuinely blank/absent in the source (empty `<details>` body, or no solution block at all for Modules N & O).

**Modules A–O blank solutions (58 total):**

```
7, 21, 31, 33, 62, 67, 68, 80, 81, 111, 116,
117, 118, 119, 120, 121, 122, 123, 124, 125,
126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136,
137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151,
152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163
```

Grouped by module:

- **Module B:** Q21
- **Module A:** Q7
- **Module C:** Q31, Q33
- **Module F:** Q62
- **Module G:** Q67, Q68
- **Module H:** Q80, Q81
- **Module K:** Q111, Q116
- **Module L:** Q117–Q125 (entire module blank — includes Q118, the unlabeled "Are you able to relate this with matrices?" question)
- **Module M:** Q126–Q136 (entire module blank)
- **Module N:** Q137–Q151 (entire module blank — no `<details>` blocks present)
- **Module O:** Q152–Q163 (entire module blank — no `<details>` blocks present)

**Module 0** (preamble): all 14 items (`M0.1`–`M0.14`) are prompt-only in the source (no worked solutions) and are likewise rendered with the placeholder. They use a separate anchor scheme (`#q-0-1` … `#q-0-14`) and are NOT part of the numbered `Q1…QN` sequence.

## 2. Question numbering — N and contiguity

- **Maximum question number N = 163.** (The source runs continuously Q1→Q163. Earlier scouting truncated at Q154; the live re-pull recovered Modules N/O in full, including an SVM block Q155–Q163 that was previously cut off.)
- The main numeric anchors `#q-1 … #q-163` were validated programmatically: **contiguous 1..163, no gaps, no duplicates.**
- Three source sub-labelled questions are authored with sub-anchors that do **not** consume a main number, matching the source's own labelling: `#q-6a`, `#q-14a` (Module A), `#q-35a` (Module C). Badges are `Q6a`, `Q14a`, `Q35a`.
- Every question anchor has exactly one matching `id="q-<n>-solution"` (180 anchors ↔ 180 solution ids, no duplicate ids).

## 3. Per-module question counts

| File | Module | Questions (incl. sub-labels) | Source Q-range |
|---|---|---|---|
| mod-0.md | 0 | 14 (M0.1–M0.14) | preamble (unnumbered) |
| mod-A.md | A | 18 | Q1–Q16 (+Q6a, Q14a) |
| mod-B.md | B | 7 | Q17–Q23 |
| mod-C.md | C | 16 | Q24–Q38 (+Q35a) |
| mod-D.md | D | 7 | Q39–Q45 |
| mod-E.md | E | 5 | Q46–Q50 |
| mod-F.md | F | 12 | Q51–Q62 |
| mod-G.md | G | 6 | Q63–Q68 |
| mod-H.md | H | 13 | Q69–Q81 |
| mod-I.md | I | 12 | Q82–Q93 |
| mod-J.md | J | 14 | Q94–Q107 |
| mod-K.md | K | 9 | Q108–Q116 |
| mod-L.md | L | 9 | Q117–Q125 |
| mod-M.md | M | 11 | Q126–Q136 |
| mod-N.md | N | 15 | Q137–Q151 |
| mod-O.md | O | 12 | Q152–Q163 |

Total numbered questions Q1–Q163 = **163** (main sequence), + 3 sub-labelled (6a, 14a, 35a) + 14 Module-0 items = **180 question blocks** authored.

These per-module counts were cross-checked against the number of `<details>` (solution) blocks in the source HTML per module and match exactly for Modules A–M; Modules N and O carry no `<details>` blocks in the source (all prompt-only), consistent with their fully-blank status.

## 4. Projects (embedded inline, no clickable links)

Each Google-Doc project was fetched via its public plain-text export endpoint and its full brief embedded as book Markdown (per the print-artifact requirement — no `<a href>` links anywhere). Cards are placed inline where each is chronologically introduced, and re-listed as an appendix in `projects.md` with `-index` ids.

| # | Title | Inline placement (canonical id) | Doc fetched? | Embedded word count (approx.) |
|---|---|---|---|---|
| 1 | Vigenère Cipher | mod-F.md (`#project-1`) | Yes | ~170 |
| 2 | PageRank | mod-K.md (`#project-2`) | Yes | ~90 |
| 3 | Recommender System | mod-K.md (`#project-3`) | Yes | ~120 |
| 4 | Huffman Encoding | mod-J.md (`#project-4`) | Yes | ~130 |
| 5 | The Dart Game | mod-G.md (`#project-5`) | Yes | ~75 |
| 6 | Water Droplet on a Plane | mod-K.md (`#project-6`) | In-text (no doc; embedded verbatim from source page) | ~75 |
| 7 | Data Compression 1 | mod-L.md (`#project-7`) | Yes | ~105 |
| 8 | Knapsack | mod-M.md (`#project-8`) | Yes | ~110 |

Appendix copies live in `projects.md` with ids `#project-1-index` … `#project-8-index` (identical content/title, distinct ids to avoid duplicate-anchor build failures).

Project source-doc IDs (recorded as plain reference, not embedded as links):

- P1 Vigenère: `1JFNRu3x5loBsF-PBPcdpfEhRz9-8Oex5uQ1iy1njp8E`
- P2 PageRank: `1OoQoTu-PMqWEjOp7qpF6Le62zyoN-aO_kGOYDw5yRow`
- P3 Recommender: `1mRlW9wG99tRpn5GUr7iNxNB8J--hNRg0Wr1pkpzh_YU`
- P4 Huffman: `11uH6E21NdTJmHFBJk5N_OM6HjgZbHNg4VUbXX9i9wDM`
- P5 Dart Game: `1hjT8teTRsQiW-NDj37Y6JmzCMTEE2xNHOv6iC9NKkDU`
- P6 Water Droplet: in-text on source page (no external doc)
- P7 Data Compression 1: `1ohvOA586DLM_bZPKpFJv_EXBtdcI9rMAEcQ_sivrnxM`
- P8 Knapsack: `1ekC18qOB47I6cCkq2Wca9NA5S0SBXEw83fn0NGvFFVc`

## 5. Content caveats

1. **N is 163, not 154.** The earlier scouting (recorded in SOURCE_STRUCTURE.md as "Q152–154+ truncated") undercounted Module O. The live page's Module O actually contains Q152–Q163; Q155–Q163 introduce Support Vector Machines (margins, hard/soft margin, kernel, multi-class). Module O's title in this ingest reflects that ("Lines, Margins & Support Vector Machines").
2. **Module 0 is unnumbered in the source** (a plain bullet list of GeoGebra warm-up tasks with no solution blocks). To keep the primary `Q1…Q163` sequence contiguous and aligned with the source's own numbering (which starts "1." at Module A) and with the blank-solution keying (Q7 = Module A), Module 0 items were given a separate `#q-0-n` / `M0.n` label scheme.
3. **Sub-labelled questions (6a, 14a, 35a)** exist in the source as lettered sub-parts and are preserved with matching sub-anchors; they do not occupy a main number.
4. **Q118 is unlabeled in the source** — the source skips the visible "118." label but a real question ("Are you able to relate this with matrices? If yes, then is this matrix invertible?") occupies that slot between Q117 and Q119. It is authored as Q118 with its real prompt and a blank-solution placeholder (no stub needed; the question text exists, only the solution is blank).
4a. Similarly, the source omits the visible number label on a few questions (e.g., "129") but the question is present and correctly positioned; numbering was reconstructed from document order and validated for contiguity.
5. **Verbatim fidelity:** prompts and worked solutions were transcribed from the source's raw HTML (not paraphrased), including original minor typos in the source (e.g., "thew Module", "pasing", "strangths", "ditsnce", "ti e taken", "sae length", "possiblity", "repitition"). LaTeX was normalized to the book's math conventions (`$...$` inline, `$$...$$` on their own lines; `bmatrix`/`pmatrix`, `\begin{cases}`, etc.). Python code from Q22/Q79 and the project briefs is embedded in fenced ```python blocks.
6. **Figures/images** referenced in the source (Markov diagrams for Q22/Q23; dartboard for Q63; neural-net figures n0.jpg/n1.jpg for Q149/Q150; the loss-points figure for Q162) are described in the prompt text as they appear in the source but the image assets themselves are not embedded. The affected prompts note "the figure below" / "the following image" as in the original.
7. **Site-wide rule** "Strictly use GeoGebra to solve all the questions" is emitted once as a `rule` fence banner at the top of `mod-0.md` (immediately after the opener), per the authoring standard.
