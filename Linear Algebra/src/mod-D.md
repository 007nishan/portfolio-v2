<section class="opener" id="mod-D">
<span class="chapter-num">D</span>

# Module D — Row, Column & Null Spaces
<span class="accent-rule"></span>
</section>

### Question 39 {: #q-39 .question .unit }

<span class="question__badge">Q39</span>

Given the matrix $M=\begin{bmatrix} 1 & 3 \\ 2 & 6 \end{bmatrix}$. Use Geogebra to plot $\mathscr{R}$, $\mathscr{C}$ & $\mathscr{N}$. What do you observe?

(i) $\mathscr{R}=\{\alpha(1,3) + \beta(2,6) \mid \alpha, \beta\in \mathbb{R}\}$

(ii) $\mathscr{C}=\{\alpha(1,2) + \beta(3,6) \mid \alpha, \beta\in \mathbb{R}\}$

(iii) $\mathscr{N}=\{(x,y) \mid x(1,3) + y(2,6) = 0, \forall x,y\in \mathbb{R} \}$

<details class="solution" id="q-39-solution" markdown>
<summary>Solution</summary>

(A) Upon plotting these graphs on Geogebra, we observe that the set R, which shows the possible combinations of the rows of matrix M, leads to set of points which lie on a straight line, which can be plotted with the help of in built functions provided.

(B) Similarly, the set C, that signifies the possible combinations of the columns of the matrix M, plots the points, lying on another straight line, on an angle to the previous one.

(C) The set N represents the solutions to a specific equation involving the rows and columns of M. It also forms a straight line on the graph, starting from the origin and having a different orientation compared to R and C.

This observation clarifies the visual representation of the relations between rows, columns and their combinations.
</details>

### Question 40 {: #q-40 .question .unit }

<span class="question__badge">Q40</span>

Note that $\mathscr{C}$ and $\mathscr{N}$ are orthogonal.

<details class="solution" id="q-40-solution" markdown>
<summary>Solution</summary>

We observed in the previous question that the points on both C and N follow a straight line path.

When we plot the straight line on the graph with the function using origin as the point and our vector as defined in the question, we get the lines as $y = 2x$ and $x = -2y.$ Here, we can observe from both the equations and also by looking at the graph itself that the two lines come out to be perpendicular to each other.
</details>

### Question 41 {: #q-41 .question .unit }

<span class="question__badge">Q41</span>

What is the null-space of $M=\begin{bmatrix} 1 & 3 \\ 2 & 6 \end{bmatrix}$ & the null-space of $M^T$?

<details class="solution" id="q-41-solution" markdown>
<summary>Solution</summary>

Null Space of a Matrix is defined as the set of points such that their column matrix X when post multiplied by the matrix M itself produces the Null Matrix O of relevant order, i.e., $MX = O.$

When we multiply these matrices, we get two equations in two variables.

$$x + 3y = 0$$

$$2x + 6y = 0$$

We can observe that the two equations are same and the solution for the null space of the matrix comes out to be the straight line from the equation, i.e., $x = -3y.$

Similarly, we can do it for the transpose matrix of M.

Let the transpose matrix of M be N.

Now, as we learnt earlier, Null space of N will be found by the following equation:

$$NX = O$$

This leads us to the equations:

$$x + 2y = 0$$

$$3x + 6y = 0$$

Similar to the previous example, the solution for the null space for N, the transpose of the matrix M, comes out to be a straight line, $x = -2y.$
</details>

### Question 42 {: #q-42 .question .unit }

<span class="question__badge">Q42</span>

Do you observe that $C(M) \perp N(M^T)$, $R(M) \perp N(M)$ ?

<details class="solution" id="q-42-solution" markdown>
<summary>Solution</summary>

This observation can easily be made by plotting the two graphs on Geogebra.
</details>

### Question 43 {: #q-43 .question .unit }

<span class="question__badge">Q43</span>

Consider $A=\begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 9 \end{bmatrix}$. What is $N(A)$, $C(A)$, $R(A)$, $N(A^T)$.

<details class="solution" id="q-43-solution" markdown>
<summary>Solution</summary>

Let us first check the Null Space.

As the square matrix used is of the order of 3 now, not of the order of 2, we will have three equations in 3 variables. But the basic approach for Null Space will be the same, i.e., $AX = O.$

We will get the following equations:

$$x + 2y + 3z = 0$$

$$4x + 5y + 6z = 0$$

$$7x + 8y + 9z = 0$$

We can use Geogebra to solve these equations.

We get the solution as:

$$x = - y/2 = z,$$

which is the null space of the provided matrix.

Similarly, for the transpose of the provided matrix, we will get the following equations:

$$x + 4y + 7z = 0$$

$$2x + 5y + 8z = 0$$

$$3x + 6y + 9z = 0$$

We get the solution as:

$$x = -y/2 = z,$$

which, we can observe, is exactly similar to the Null Space of A itself.

Now, we will check the Column Space of the given matrix.

We have seen how $C(M)$ is defined previously in this module.

Going with the similar approach, we get the set C(A) as:

$$C(A) = \{a(1,4,7) + b(2,5,8) + c(3,6,9) : a, b, c \in \mathbb{R}\}$$

Similarly,

$$R(A) = \{a(1,2,3) + b(4,5,6) + c(7,8,9) : a, b, c \in \mathbb{R}\}$$
</details>

### Question 44 {: #q-44 .question .unit }

<span class="question__badge">Q44</span>

Consider a 4x4 matrix $M$: $\mathbb{R}^4\mapsto \mathbb{R}^4$ whose range is

a) $4$-Dimension

b) $3$-Dimension

c) $2$-Dimension

d) $1$-Dimension

e) $0$-Dimension

Give an example each for all the above 5 cases.

<details class="solution" id="q-44-solution" markdown>
<summary>Solution</summary>

(a) $A=\begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}$

(b) $A=\begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 1 & 0 \end{bmatrix}$

(c) $A=\begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \end{bmatrix}$

(d) $A=\begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \end{bmatrix}$

(e) $A=\begin{bmatrix} 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \end{bmatrix}$

Note that any other example which satisfies the given condition is also a correct answer for the question.
</details>

### Question 45 {: #q-45 .question .unit }

<span class="question__badge">Q45</span>

Consider $A : \mathbb{R}^{3} \to \mathbb{R}^{3}$

a) Show that if the range contains a point $(a,b,c)$, then it should contain the entire set $S$, defined by: $S= \{\alpha(a, b,c) \mid \alpha \in \mathbb{R}\}$.

b) Show that if the range contains the points $(a,b,c)$ and $(d,e,f)$, then the range contains the entire set $T$ defined by: $T=\{\alpha(a,b,c) + \beta(d,e,f) \mid \alpha,\beta\in \mathbb{R}\}$.

c) Note: $S$ is of the dimension $1$, but $T$ need'nt be of dimension $2$. Think!

<details class="solution" id="q-45-solution" markdown>
<summary>Solution</summary>

(A) Given that the range contains a point $(a,b,c)$, it means that there exists a vector x such that $A(x) = (a,b,c).$

But, since A is a linear transformation; for any scalar a, $A(ax) = a(a,b,c),$ which implies that the entire set S is also in the range.

(B) Similarly, as long as the linearity of the transformation is sustained, $A(ax + by) = a \cdot x + b \cdot y$ for 2 scalars a and b and existing vectors $x = (a,b,c)$ and $y = (d,e,f).$ This indicates that the entire set T is in the range.

(C) Yes, the dimension of T needn't be 2 as it depends upon the linear dependency of the two vectors with each other.
</details>
