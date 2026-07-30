<section class="opener" id="mod-E">
<span class="chapter-num">E</span>

# Module E — Subspaces & Orthogonal Complements
<span class="accent-rule"></span>
</section>

### Question 46 {: #q-46 .question .unit }

<span class="question__badge">Q46</span>

Give an example of two $2$-dim subspaces in $\mathbb{R}^{3}$. Let us call it $S_1, S_2$.

<details class="solution" id="q-46-solution" markdown>
<summary>Solution</summary>

To provide an example of two 2 - dimensional subspaces in 3 - dimensional Real space, we need to define two different planes through the origin in the whole space.

For example, they can be the xy and the zx - planes. Therefore,

$$S_1 = \{(x,y,0) : x,y \text{ belong to } \mathbb{R}\}$$

$$S_2 = \{(x,0,z) : x,z \text{ belong to } \mathbb{R}\}$$
</details>

### Question 47 {: #q-47 .question .unit }

<span class="question__badge">Q47</span>

Let $S_3$ be all those vectors perpendicular to $S_1$. $S_4$ be that of $S_2$.

<details class="solution" id="q-47-solution" markdown>
<summary>Solution</summary>

Let us define $S_3$ and $S_4$ on the basis of their orthogonality towards $S_1$ and $S_2$ respectively.

As $S_3$ contains all the vectors perpendicular to $S_1$, i.e., the xy - plane, they will lie along the z-axis. Therefore,

$$S_3 = \{x : x \text{ lies along the z - axis}\}$$

Similarly,

$$S_4 = \{x : x \text{ lies along the y - axis}\}$$
</details>

### Question 48 {: #q-48 .question .unit }

<span class="question__badge">Q48</span>

Find a matrix $M$ whose Null-Space is $S_3$. Column space is $S_2$.

<details class="solution" id="q-48-solution" markdown>
<summary>Solution</summary>

$$A=\begin{bmatrix} 1 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 1 & 0 \end{bmatrix}$$

As we know that row space and null space of a matrix are orthogonal to each other. It can clearly be observed from this matrix that its row space is xy plane and hence, as z - axis is orthogonal to it, it is its null space.
</details>

### Question 49 {: #q-49 .question .unit }

<span class="question__badge">Q49</span>

What does $S_1$ and $S_4$ represent?

<details class="solution" id="q-49-solution" markdown>
<summary>Solution</summary>

$S_1$ represents a 2 - dimensional subspace within $\mathbb{R}^3.$ Specifically, it signifies any plane passing through the origin in 3 - dimensional space.

$S_4$ represents the orthogonal complement of a 2 - dimensional subspace $(S_2)$. In other words, it consists of all vectors that are perpendicular to every vector in $S_2$. Geometrically, it could signify a line, a plane, or even all of $\mathbb{R}^3$ itself, depending upon the orientation ad the dimensionality of $S_2.$
</details>

### Question 50 {: #q-50 .question .unit }

<span class="question__badge">Q50</span>

Do you observe there is a bijection from $S_1 \to S_2$?

<details class="solution" id="q-50-solution" markdown>
<summary>Solution</summary>

There is indeed a bijection from $S_1$ to $S_2$ given by the map:

$$f(x,y,0) = (x,0,y)$$

This map pairs each vector in $S_1$ with a unique vector in $S_2$ and covers all vectors in $S_2$ maintaining the conditions of both injectivity and surjectivity.
</details>
