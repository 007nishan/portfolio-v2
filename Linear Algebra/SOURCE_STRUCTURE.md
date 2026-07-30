# Source Structure — "Oceanverse" / Linear Algebra (AI Vicharana Shala)

- **Source:** https://sudarshansudarshan.github.io/aicamp/oceanverse/
- **Title:** Oceanverse
- **Program:** AI Vicharana Shala (AI camp, hosted at IIT Ropar)
- **Site-wide HARD RULE:** "Strictly use GeoGebra to solve all the questions"
- **Nature:** 15 modules (0, then A–O), 150+ **questions** each with a worked **solution**, plus 8 linked **projects**. Heavy math (matrices, vectors, null/column space, eigenvectors, sigmoid, convolution, gradient descent). Question numbering runs continuously 1 → 154+ across lettered modules.

## Navigation (source site)
Introduction · FAQ · Handbook · Student Dashboard · Arriving at IIT Ropar · Course Content · Feedback

## Module outline

- **Module 0** — ~14 items: plotting points/distance, vectors & angles, perpendicular bisectors, lines, quadratic behavior (vertex/roots), angle of depression, right triangle & centroid, parametric circle, 3D planes & intersection angle.
- **Module A** — Q1–16 (incl. 6a, 14a): proportional savings/lines, collinearity, slope w/ sliders, parallel lines, simultaneous equations as matrices, invertible functions, ℝ/ℝ²/ℝ³, linear maps φ:ℝ²→ℝ², matrix invertibility & determinants, matrices as functions, null space.
- **Module B** — Q17–23: Hill cipher encrypt/decrypt, simultaneous equations (café bills), overdetermined systems & best fit, matrix modeling, error reduction, Markov chains with Python convergence.
- **Module C** — Q24–38 (incl. 35a): perpendicular vectors, dot product = 0, planes from matrix equations, spans/sets, null space, column/row space intuition, transformations of lines, magnitude ratios, "collapses a dimension."
- **Module D** — Q39–45: row/column/null space (𝓡, 𝓒, 𝓝), orthogonality (C(M)⊥N(Mᵀ), R(M)⊥N(M)), 3×3 null spaces, 4×4 range dimensions, range-as-subspace proofs.
- **Module E** — Q46–50: 2-dim subspaces in ℝ³, orthogonal complements, matrix with given null/column space, bijections between subspaces.
- **Module F** — Q51–62: wartime cryptography, Caesar cipher & shift-by-1 weakness, encoding "VICHARANASHALA," frequency analysis, substitution key space (26!), collision frequency, secure encoding.
- **Module G** — Q63–68: dartboard probability, dice-sum expectation, defective items (binomial expectation), sphere/cube geometric probability, expected closest-point distance.
- **Module H** — Q69–81: distances between points, closest pair (brute force → divide-and-conquer), sorting, banding, 3D stars, Fibonacci & factorial recursion, O(n log n) edge cases.
- **Module I** — Q82–93: equally likely events, coin probability, inclusion-exclusion, Bayes' theorem (alarm/exam, stock prediction, spam filter), perceptron weights/bias, weighted sum, sigmoid range fitting.
- **Module J** — Q94–107: binary conversion, ASCII (8 bits), prefix-code ambiguity ("shannon"), fixed vs variable-length codes, frequency distributions, shorter codes for frequent chars, tree structures, prefix property, node depth vs access time.
- **Module K** — Q108–116: PageRank, random walk & equal-points distribution, iterative matrix ops on a vector, convergence & independence from initial vector, link influence, coin-passing buckets, highly-connected-node bias & fixes.
- **Module L** — Q117–125 (Q118 label missing): image as matrices, matrix invertibility probability, pixel removal effects, retrieval, adjacent pixel differences, systematic pixel removal (compression).
- **Module M** — Q126–136: linear transformations, rotation matrices, scaling matrices, orthogonal matrices, transpose/inverse relation, AAᵀ, eigenvectors, dimension-changing matrices.
- **Module N** — Q137–151: convolution (sets, matrices, commutativity), image filters (edge detection, blur), CNN output dims/stride/padding, pooling (max/avg/min), cross-entropy loss, gradient descent, derivatives (sigmoid, log, softmax), backprop.
- **Module O** — Q152–154+ (truncated in source): sign of linear expression at points, distance of line from origin.

## Linked projects
1. Vigenère Cipher (Google Doc)
2. PageRank (Google Doc)
3. Recommender System (Google Doc)
4. Huffman Encoding (Google Doc)
5. The Dart Game (Google Doc)
6. Vector/plane droplet direction (in-text, GeoGebra parametric — "Do not use Mathematics anywhere…")
7. Data Compression 1 (Google Doc)
8. Knapsack (Google Doc)

## Ingestion notes
- Several solutions are blank in the source (e.g. Q7, Q17, Q21, Q31, Q33, Q62, Q67–68, Q80–81, Q111, Q116, most of Module L/M) — must be flagged, not fabricated.
- Content beyond Q154 was truncated when scouted; full ingestion must re-pull the live page.
- First-class needs: numbered **question + collapsible worked-solution** pairs, **LaTeX matrix/vector math** (screen + PDF), a **"Strictly use GeoGebra" rule banner**, **GeoGebra embeds**, and a **linked-projects** section.
