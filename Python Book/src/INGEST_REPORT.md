# Ingest Report — "Programming in Python" (IIT-Madras)

- **Source:** https://bsc-iitm.github.io/python-textbook/
- **Ingested:** 2026-07-26
- **Output:** `Python Book/src/ch-0.md` … `ch-8.md` (9 chapter files)
- **Method:** Each lesson page fetched individually via WebFetch at the URL pattern `https://bsc-iitm.github.io/python-textbook/<chapter>/<lesson>/`, then authored into Markdown following the Book Standard (chapter opener sections, `## Lesson n.m — Title {: #ch-n-lesson-m }` headers, ```python``` for source, ```output``` for program output, ```repl``` for interactive `>>>` sessions, admonitions for tips/notes/warnings, GitHub tables, `$…$`/`$$…$$` for math).

## Lessons captured vs unavailable

All lessons listed in `SOURCE_STRUCTURE.md` (Chapters 0–8) were fetched successfully and captured. **No lesson page 404'd or was empty.** No `<!-- lesson X.Y unavailable -->` markers were needed.

| Chapter | Title | Lessons captured | Unavailable |
|---|---|---|---|
| 0 | Warm-up | Lesson 0 | — |
| 1 | Introduction to Python | 1.1, 1.2, 1.3, 1.4, 1.5, 1.6 | — |
| 2 | Conditionals | 2.1, 2.2, 2.3, 2.4 | — |
| 3 | Loops | 3.1, 3.2, 3.3, 3.4, 3.5, 3.6 | — |
| 4 | Functions | 4.1, 4.2, 4.3, 4.4 | — |
| 5 | Lists and Tuples | 5.1, 5.2, 5.3, 5.4, 5.5, 5.6 | — |
| 6 | Dictionaries and Sets | 6.1, 6.2, 6.3, 6.4, 6.5 | — |
| 7 | File Handling | 7.1, 7.2, 7.3, 7.4, 7.5 | — |
| 8 | Object Oriented Programming | 8.1, 8.2, 8.3, 8.4 | — |

**Total: 40 lessons across 9 chapters.**

The "Extras" section from `SOURCE_STRUCTURE.md` (Shorts at `extras/limits/`, Resources at `extras/resources/`) was NOT ingested. These are supplementary pages, not numbered lessons, and fall outside the ch-0…ch-8 chapter scope requested. (Chapter 3, Lesson 3.6 already covers the "limits/recurrence/rational-approximation" mathematics material that the Shorts relate to.)

## Word and code-block counts per chapter

Word counts are raw `wc -w` over the authored Markdown (prose + code). Code-block counts are opening fences by language.

| File | Words | Total fenced blocks | `python` | `output` | `repl` |
|---|---|---|---|---|---|
| ch-0.md | 688 | 1 | 1 | 0 | 0 |
| ch-1.md | 4,056 | 99 | 38 | 20 | 41 |
| ch-2.md | 2,999 | 62 | 46 | 15 | 1 |
| ch-3.md | 3,775 | 74 | 50 | 24 | 0 |
| ch-4.md | 3,448 | 57 | 46 | 11 | 0 |
| ch-5.md | 4,949 | 110 | 92 | 18 | 0 |
| ch-6.md | 4,893 | 85 | 76 | 9 | 0 |
| ch-7.md | 2,574 | 42 | 31 | 11 | 0 |
| ch-8.md | 1,929 | 24 | 19 | 5 | 0 |
| **Total** | **29,311** | **554** | **399** | **113** | **42** |

Note: `python + output + repl` per row does not always equal "Total fenced blocks" because a few fenced blocks use no language tag — these are literal file-contents / plain-text listings (e.g. the income-expenditure tables in Lesson 7.1, the multi-line target-file listings in Chapter 7, and a couple of bare-syntax templates). They are still counted in the "Total fenced blocks" column.

## Formatting notes

- **Chapter 1** uses the ```repl``` fence heavily because Lesson 1.1–1.3 are taught in the interactive Python shell (`>>>`). From Lesson 1.4 onward the source switches to the Replit editor (no prompt), so later chapters use ```python``` + ```output``` instead.
- **Math** appears in Chapter 3 (Lesson 3.5 tolerance/probability, Lesson 3.6 limits/recurrence/rational approximation) and Chapter 8 (Lesson 8.4 vector operations), rendered as `$…$` / `$$…$$`.
- **Wrong-code snippets** from the source (delimited with `##### Alarm! Wrong code snippet! #####`) are preserved verbatim inside ```python``` fences, as they are part of the pedagogy.

## Content caveats

1. **Prose faithfulness.** The fetch step (WebFetch) returned a mix of verbatim and lightly-paraphrased prose; for several lessons it declined to reproduce prose word-for-word and instead returned close restatements. Authored prose therefore closely follows the source's structure, wording, and all technical claims, with direct quotes preserved where the fetch supplied them (e.g. definitions, "Zen of Python," Guido excerpt in 6.2). **All code, program output, error tracebacks, tables, and numeric results are reproduced exactly as in the source** and were not "fixed" or altered.
2. **Images not reproduced.** The source contains illustrative images (precedence tables in 1.3, debugging-loop and stack/recursion diagrams in 1.4 / 4.4, the neighborhood/Manhattan-distance map in 4.2, matrix and vector figures in 5.5 / 8.4, hash-table rack analogy in 6.1, file-object PA analogy in 7.3). These are described in prose where they carry load-bearing meaning but the image files themselves are not embedded.
3. **No hyperlinks.** Per the printed-book constraint, all links were removed. Two Markdown links to the Python documentation (Chapter 1 string methods; Chapter 2 built-in functions) were converted to plain-text references ("Python documentation (docs.python.org, …)"). No `<a href>` anchors or `[text](url)` links or bare URLs remain in any chapter file.
4. **Chapter 6 title.** `SOURCE_STRUCTURE.md` names Chapter 6 "Dictionaries and Sets"; the source's own outline (in Lesson 0) lists it as "Sets and dictionaries." The requested title/order ("Dictionaries and Sets") was used, and lessons are presented in the source's actual order (dictionaries 6.1–6.4, then sets 6.5).
5. **Minor source typos preserved.** Comments in the source that contain typos (e.g. `# actuall call` in Lesson 4.2, variable `words_` usages, the `print()` vs `__str__()` mismatch in Lesson 8.4) are reproduced as-is, since the instruction was to keep code exactly as in the source. The 8.4 mismatch is additionally flagged in an in-text note.
