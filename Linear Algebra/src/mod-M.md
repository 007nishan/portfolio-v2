<section class="opener" id="mod-M">
<span class="chapter-num">M</span>

# Module M — Rotations, Orthogonal Matrices & Eigenvectors
<span class="accent-rule"></span>
</section>

### Question 126 {: #q-126 .question .unit }

<span class="question__badge">Q126</span>

Recall linear transformation that you studied in previous modules. What do they do?

<details class="solution" id="q-126-solution" markdown>
<summary>Solution</summary>

Solution not provided in the source material.
</details>

### Question 127 {: #q-127 .question .unit }

<span class="question__badge">Q127</span>

Let a vector $v=[3,4]$ and matrix be $A= \begin{bmatrix} 1/\sqrt{2} & -1/\sqrt{2} \\ 1/\sqrt{2} & 1/\sqrt{2} \end{bmatrix}$, find $Av$, what do you observe?

<details class="solution" id="q-127-solution" markdown>
<summary>Solution</summary>

Solution not provided in the source material.
</details>

### Question 128 {: #q-128 .question .unit }

<span class="question__badge">Q128</span>

Let a vector $v=[3,4]$ and matrix be $B= \begin{bmatrix} \sqrt{3}/2 & -1/2 \\ 1/2 & \sqrt{3}/2 \end{bmatrix}$ find $Bv$, what do you observe?

<details class="solution" id="q-128-solution" markdown>
<summary>Solution</summary>

Solution not provided in the source material.
</details>

### Question 129 {: #q-129 .question .unit }

<span class="question__badge">Q129</span>

What similarity can you observe in matrix A and B?

<details class="solution" id="q-129-solution" markdown>
<summary>Solution</summary>

Solution not provided in the source material.
</details>

### Question 130 {: #q-130 .question .unit }

<span class="question__badge">Q130</span>

Let a vector $b=[3,4]$ and a matrix $D=\begin{bmatrix} 2 & 0 \\ 0 & 3 \end{bmatrix}$ find $Db$. Can you observe that the matrix D simply scaled the respective axis of the vector?

<details class="solution" id="q-130-solution" markdown>
<summary>Solution</summary>

Solution not provided in the source material.
</details>

### Question 131 {: #q-131 .question .unit }

<span class="question__badge">Q131</span>

Are you aware of orthogonal matrices? What properties do orthogonal matrices show?

<details class="solution" id="q-131-solution" markdown>
<summary>Solution</summary>

Solution not provided in the source material.
</details>

### Question 132 {: #q-132 .question .unit }

<span class="question__badge">Q132</span>

What is the relation between transpose and inverse of an orthogonal matrix?

<details class="solution" id="q-132-solution" markdown>
<summary>Solution</summary>

Solution not provided in the source material.
</details>

### Question 133 {: #q-133 .question .unit }

<span class="question__badge">Q133</span>

What do you get when you multiply $A$ and $A^T$?

<details class="solution" id="q-133-solution" markdown>
<summary>Solution</summary>

Solution not provided in the source material.
</details>

### Question 134 {: #q-134 .question .unit }

<span class="question__badge">Q134</span>

Find the eigen vectors of $AA^T$ for different matrices A, and find the common feature in these eigen vectors.

<details class="solution" id="q-134-solution" markdown>
<summary>Solution</summary>

Solution not provided in the source material.
</details>

### Question 135 {: #q-135 .question .unit }

<span class="question__badge">Q135</span>

Observe what does a matrix $A =\begin{bmatrix} 1 & 0 \\ 0 & 1 \\ 0 & 0 \end{bmatrix}$ do when applied to a vector in $\mathbb{R}^2$.

<details class="solution" id="q-135-solution" markdown>
<summary>Solution</summary>

Solution not provided in the source material.
</details>

### Question 136 {: #q-136 .question .unit }

<span class="question__badge">Q136</span>

Observe what does a matrix $A =\begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \end{bmatrix}$ do when applied to a vector in $\mathbb{R}^3$.

<details class="solution" id="q-136-solution" markdown>
<summary>Solution</summary>

Solution not provided in the source material.
</details>

<div class="project-card" id="project-8">
<span class="kicker">Project 08</span>

### Knapsack

You have a knapsack (a kind of bag) that can carry a maximum weight of $W$. You also have $N$ items, each with a certain weight and value.

The goal is to determine the most valuable combination of items to include in the knapsack, such that the total weight of the included items is less than or equal to $W$ and the total value is as high as possible. Note that you cannot take partial objects.

You have to first generate a list of 100 objects with random weights and values. Use the following command for that:

```python
items = [[random.randint(1, 100), random.randint(1, 100)] for i in range(100)]
```

Now your goal is to find the combination of objects which you will take to maximize the value within the weight limit.

Note that brute force will become computationally very heavy, so use some optimized algorithm.

Hint: The algorithm was already discussed with some of your friends in the lab, so don't forget to seek help from them. 🙂
</div>
