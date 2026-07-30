# Solution Recovery Report — Oceanverse Linear-Algebra Curriculum

**Task:** Recover worked solutions that a previous ingestion may have replaced with the
placeholder `Solution not provided in the source material.` by re-reading the collapsed
`<details><summary>Sol.</summary> … </details>` blocks in the raw source HTML.

**Source parsed:** `_oceanverse_raw.html` (parsed with a real HTML parser — `selectolax.parser.HTMLParser`), walked in document order.

## Method

1. Parsed the raw HTML and located every `<details><summary>Sol.</summary> … </details>` block. **139 blocks** were found (summary text `Sol.` on all 139), matching the expected total.
2. Walked the document in order, module by module. Each solution block was paired to its question by **document order within its module**, then **verified by matching the preceding question prompt text/number** in the raw HTML (e.g. the source lead-ins `3.Plot the lines…`, `42.Do you observe…`, `116.What modifications…`, and the lettered sub-parts `6(a).`, `14(a).`, `35(a).`). The per-module count of `<details>` blocks exactly equals the per-module count of authored questions (including sub-labels), so the positional pairing is unambiguous and was confirmed by text.
3. Classified each block: **non-empty** (real solution present) vs **empty** (only `<summary>Sol.</summary>` followed by whitespace before `</details>`).
4. Compared against the current `mod-*.md` files: which question bodies currently hold the exact placeholder, and which already carry real solution text.

## Headline result

| Metric | Count |
|---|---|
| `<details>` Sol. blocks in source | 139 |
| — with real (non-empty) content | 108 |
| — genuinely empty in source | 31 |
| Questions in Modules N & O with **no** Sol. block at all | 27 |
| **RECOVERED** (was placeholder, real content found in HTML, now filled) | **0** |
| **ALREADY-HAD-CONTENT** (real solution already in the `.md`, untouched) | **108** |
| **STILL-BLANK** (genuinely empty / absent in source, placeholder kept) | **58** |

**No edits were made to any solution body.** Every one of the 108 real solutions present in
the raw HTML is **already transcribed** in the current `mod-*.md` files (verified 1:1 — no
non-empty source block maps to a question that still shows the placeholder). Every question
that still shows the placeholder corresponds to a source block that is **genuinely empty**
(31 empty `<details>` bodies) or **entirely absent** (27 questions in Modules N & O, which
carry no `<details>` blocks at all). Per the task's rule against fabricating solutions, these
placeholders were left unchanged.

> Note: the premise that ~27 placeholders masked real answers does **not** hold for the
> current state of the files. Whatever earlier truncation existed (the `INGEST_REPORT.md`
> mentions an earlier pull that truncated near Q154) has already been corrected in the current
> `mod-*.md`; there is nothing left to recover from `_oceanverse_raw.html`.

## STILL-BLANK — definitive list (excluding Module 0)

These question numbers are blank because their solution is genuinely absent from the source.
Use this as the registry list.

**Empty `<details>` block in source (block exists, body empty) — 31 questions:**

```
7, 21, 31, 33, 62, 67, 68, 80, 81, 111, 116,
117, 118, 119, 120, 121, 122, 123, 124, 125,
126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136
```

**No `<details>` block at all in source (Modules N & O are prompt-only) — 27 questions:**

```
137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151,
152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163
```

**Combined STILL-BLANK (58 questions):**

```
7, 21, 31, 33, 62, 67, 68, 80, 81, 111, 116,
117, 118, 119, 120, 121, 122, 123, 124, 125,
126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136,
137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151,
152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163
```

Grouped by module:

- **Module A:** 7
- **Module B:** 21
- **Module C:** 31, 33
- **Module F:** 62
- **Module G:** 67, 68
- **Module H:** 80, 81
- **Module K:** 111, 116
- **Module L:** 117, 118, 119, 120, 121, 122, 123, 124, 125 (entire module empty in source)
- **Module M:** 126–136 (entire module empty in source)
- **Module N:** 137–151 (no Sol. blocks in source)
- **Module O:** 152–163 (no Sol. blocks in source)

## Module 0 (unchanged, out of scope)

Module 0 holds 14 prompt-only warm-up items (`M0.1`–`M0.14`, anchors `#q-0-1 … #q-0-14`).
They have no `<details>` Sol. blocks in the source and are authored with the placeholder by
design. They are **not** part of the numbered Q1…Q163 sequence and were left unchanged.

## Per-question status (Modules A–O)

Legend: `ALREADY` = real solution already present (untouched); `STILL-BLANK(empty)` = empty
`<details>` in source; `STILL-BLANK(no-block)` = no Sol. block in source.

| Module | Question | Status |
|---|---|---|
| A | 1 | ALREADY-HAD-CONTENT |
| A | 2 | ALREADY-HAD-CONTENT |
| A | 3 | ALREADY-HAD-CONTENT |
| A | 4 | ALREADY-HAD-CONTENT |
| A | 5 | ALREADY-HAD-CONTENT |
| A | 6 | ALREADY-HAD-CONTENT |
| A | 6a | ALREADY-HAD-CONTENT |
| A | 7 | STILL-BLANK (empty in source) |
| A | 8 | ALREADY-HAD-CONTENT |
| A | 9 | ALREADY-HAD-CONTENT |
| A | 10 | ALREADY-HAD-CONTENT |
| A | 11 | ALREADY-HAD-CONTENT |
| A | 12 | ALREADY-HAD-CONTENT |
| A | 13 | ALREADY-HAD-CONTENT |
| A | 14 | ALREADY-HAD-CONTENT |
| A | 14a | ALREADY-HAD-CONTENT |
| A | 15 | ALREADY-HAD-CONTENT |
| A | 16 | ALREADY-HAD-CONTENT |
| B | 17 | ALREADY-HAD-CONTENT |
| B | 18 | ALREADY-HAD-CONTENT |
| B | 19 | ALREADY-HAD-CONTENT |
| B | 20 | ALREADY-HAD-CONTENT |
| B | 21 | STILL-BLANK (empty in source) |
| B | 22 | ALREADY-HAD-CONTENT |
| B | 23 | ALREADY-HAD-CONTENT |
| C | 24 | ALREADY-HAD-CONTENT |
| C | 25 | ALREADY-HAD-CONTENT |
| C | 26 | ALREADY-HAD-CONTENT |
| C | 27 | ALREADY-HAD-CONTENT |
| C | 28 | ALREADY-HAD-CONTENT |
| C | 29 | ALREADY-HAD-CONTENT |
| C | 30 | ALREADY-HAD-CONTENT |
| C | 31 | STILL-BLANK (empty in source) |
| C | 32 | ALREADY-HAD-CONTENT |
| C | 33 | STILL-BLANK (empty in source) |
| C | 34 | ALREADY-HAD-CONTENT |
| C | 35 | ALREADY-HAD-CONTENT |
| C | 35a | ALREADY-HAD-CONTENT |
| C | 36 | ALREADY-HAD-CONTENT |
| C | 37 | ALREADY-HAD-CONTENT |
| C | 38 | ALREADY-HAD-CONTENT |
| D | 39 | ALREADY-HAD-CONTENT |
| D | 40 | ALREADY-HAD-CONTENT |
| D | 41 | ALREADY-HAD-CONTENT |
| D | 42 | ALREADY-HAD-CONTENT |
| D | 43 | ALREADY-HAD-CONTENT |
| D | 44 | ALREADY-HAD-CONTENT |
| D | 45 | ALREADY-HAD-CONTENT |
| E | 46 | ALREADY-HAD-CONTENT |
| E | 47 | ALREADY-HAD-CONTENT |
| E | 48 | ALREADY-HAD-CONTENT |
| E | 49 | ALREADY-HAD-CONTENT |
| E | 50 | ALREADY-HAD-CONTENT |
| F | 51 | ALREADY-HAD-CONTENT |
| F | 52 | ALREADY-HAD-CONTENT |
| F | 53 | ALREADY-HAD-CONTENT |
| F | 54 | ALREADY-HAD-CONTENT |
| F | 55 | ALREADY-HAD-CONTENT |
| F | 56 | ALREADY-HAD-CONTENT |
| F | 57 | ALREADY-HAD-CONTENT |
| F | 58 | ALREADY-HAD-CONTENT |
| F | 59 | ALREADY-HAD-CONTENT |
| F | 60 | ALREADY-HAD-CONTENT |
| F | 61 | ALREADY-HAD-CONTENT |
| F | 62 | STILL-BLANK (empty in source) |
| G | 63 | ALREADY-HAD-CONTENT |
| G | 64 | ALREADY-HAD-CONTENT |
| G | 65 | ALREADY-HAD-CONTENT |
| G | 66 | ALREADY-HAD-CONTENT |
| G | 67 | STILL-BLANK (empty in source) |
| G | 68 | STILL-BLANK (empty in source) |
| H | 69 | ALREADY-HAD-CONTENT |
| H | 70 | ALREADY-HAD-CONTENT |
| H | 71 | ALREADY-HAD-CONTENT |
| H | 72 | ALREADY-HAD-CONTENT |
| H | 73 | ALREADY-HAD-CONTENT |
| H | 74 | ALREADY-HAD-CONTENT |
| H | 75 | ALREADY-HAD-CONTENT |
| H | 76 | ALREADY-HAD-CONTENT |
| H | 77 | ALREADY-HAD-CONTENT |
| H | 78 | ALREADY-HAD-CONTENT |
| H | 79 | ALREADY-HAD-CONTENT |
| H | 80 | STILL-BLANK (empty in source) |
| H | 81 | STILL-BLANK (empty in source) |
| I | 82 | ALREADY-HAD-CONTENT |
| I | 83 | ALREADY-HAD-CONTENT |
| I | 84 | ALREADY-HAD-CONTENT |
| I | 85 | ALREADY-HAD-CONTENT |
| I | 86 | ALREADY-HAD-CONTENT |
| I | 87 | ALREADY-HAD-CONTENT |
| I | 88 | ALREADY-HAD-CONTENT |
| I | 89 | ALREADY-HAD-CONTENT |
| I | 90 | ALREADY-HAD-CONTENT |
| I | 91 | ALREADY-HAD-CONTENT |
| I | 92 | ALREADY-HAD-CONTENT |
| I | 93 | ALREADY-HAD-CONTENT |
| J | 94 | ALREADY-HAD-CONTENT |
| J | 95 | ALREADY-HAD-CONTENT |
| J | 96 | ALREADY-HAD-CONTENT |
| J | 97 | ALREADY-HAD-CONTENT |
| J | 98 | ALREADY-HAD-CONTENT |
| J | 99 | ALREADY-HAD-CONTENT |
| J | 100 | ALREADY-HAD-CONTENT |
| J | 101 | ALREADY-HAD-CONTENT |
| J | 102 | ALREADY-HAD-CONTENT |
| J | 103 | ALREADY-HAD-CONTENT |
| J | 104 | ALREADY-HAD-CONTENT |
| J | 105 | ALREADY-HAD-CONTENT |
| J | 106 | ALREADY-HAD-CONTENT |
| J | 107 | ALREADY-HAD-CONTENT |
| K | 108 | ALREADY-HAD-CONTENT |
| K | 109 | ALREADY-HAD-CONTENT |
| K | 110 | ALREADY-HAD-CONTENT |
| K | 111 | STILL-BLANK (empty in source) |
| K | 112 | ALREADY-HAD-CONTENT |
| K | 113 | ALREADY-HAD-CONTENT |
| K | 114 | ALREADY-HAD-CONTENT |
| K | 115 | ALREADY-HAD-CONTENT |
| K | 116 | STILL-BLANK (empty in source) |
| L | 117 | STILL-BLANK (empty in source) |
| L | 118 | STILL-BLANK (empty in source) |
| L | 119 | STILL-BLANK (empty in source) |
| L | 120 | STILL-BLANK (empty in source) |
| L | 121 | STILL-BLANK (empty in source) |
| L | 122 | STILL-BLANK (empty in source) |
| L | 123 | STILL-BLANK (empty in source) |
| L | 124 | STILL-BLANK (empty in source) |
| L | 125 | STILL-BLANK (empty in source) |
| M | 126 | STILL-BLANK (empty in source) |
| M | 127 | STILL-BLANK (empty in source) |
| M | 128 | STILL-BLANK (empty in source) |
| M | 129 | STILL-BLANK (empty in source) |
| M | 130 | STILL-BLANK (empty in source) |
| M | 131 | STILL-BLANK (empty in source) |
| M | 132 | STILL-BLANK (empty in source) |
| M | 133 | STILL-BLANK (empty in source) |
| M | 134 | STILL-BLANK (empty in source) |
| M | 135 | STILL-BLANK (empty in source) |
| M | 136 | STILL-BLANK (empty in source) |
| N | 137–151 | STILL-BLANK (no Sol. block in source) |
| O | 152–163 | STILL-BLANK (no Sol. block in source) |

## Post-check

`grep -c "Solution not provided in the source material\."` across all `mod-*.md`:

- Total remaining placeholders: **72**
- Expected: 31 (empty `<details>` in source) + 27 (Modules N & O, no block) + 14 (Module 0) = **72** ✓

The remaining-placeholder count matches (genuinely-empty + absent) + Module-0, exactly as required.
