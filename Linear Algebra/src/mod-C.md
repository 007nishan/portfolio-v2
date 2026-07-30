<section class="opener" id="mod-C">
<span class="chapter-num">C</span>

# Module C — Orthogonality, Spans & Null Space
<span class="accent-rule"></span>
</section>

### Question 24 {: #q-24 .question .unit }

<span class="question__badge">Q24</span>

Use Geogebra: Draw the vector $\begin{bmatrix} 1 \\ 1 \end{bmatrix}$. Find out all those vectors which are perpendicular to this vector.

<details class="solution" id="q-24-solution" markdown>
<summary>Solution</summary>

The given vector can be drawn with the help of the vector tool in GeoGebra.

All the vectors which have their dot product with the given vector as 0 will be orthogonal to it.

They will be of the form:

$$v = (t, -t),$$

where t is an arbitrary variable.
</details>

### Question 25 {: #q-25 .question .unit }

<span class="question__badge">Q25</span>

Do you observe that we are asking for vectors $\begin{bmatrix} x \\ y \end{bmatrix}$ such that,

$$\begin{bmatrix} 1 & 1 \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix} = 0$$

<details class="solution" id="q-25-solution" markdown>
<summary>Solution</summary>

The given set of matrices lead to the equation which we get while doing the dot of these vectors as 0, i.e.,

$$x + y = 0$$

So, This equation represents all the vectors perpendicular to the given one. These vectors lie along the line with slope -1 passing through the origin in the Cartesian coordinate system.
</details>

### Question 26 {: #q-26 .question .unit }

<span class="question__badge">Q26</span>

Use Geogebra and solve the above question with $\begin{bmatrix} 1 \\ 1 \end{bmatrix}$ replaced by $\begin{bmatrix} a \\ b \end{bmatrix}$. Use $(a,b)$ as parameters and check what happens to $(x,y)$.

<details class="solution" id="q-26-solution" markdown>
<summary>Solution</summary>

As a consequence of this change, the straight line will become:

$$ax + by = 0$$

This will only change the corresponding slope, i.e., the vectors will lie on the line passing through the origin with the slope equal to -a/b.
</details>

### Question 27 {: #q-27 .question .unit }

<span class="question__badge">Q27</span>

What is $(x,y,z)$ satisfying the following equation? (Use Geogebra)

$$\begin{bmatrix} 1 & 2 & 3 \end{bmatrix} \begin{bmatrix} x \\ y \\ z \end{bmatrix} = 0$$

<details class="solution" id="q-27-solution" markdown>
<summary>Solution</summary>

The equation given is $\begin{bmatrix} 1 & 2 & 3 \end{bmatrix}\begin{bmatrix} x \\ y \\ z \end{bmatrix} = 0$. To solve this, we can multiply the matrix $\begin{bmatrix} 1 & 2 & 3 \end{bmatrix}$ by the column vector $\begin{bmatrix} x \\ y \\ z \end{bmatrix}$ using matrix multiplication.

$$\begin{bmatrix} 1 & 2 & 3 \end{bmatrix} \begin{bmatrix} x \\ y \\ z \end{bmatrix} = \begin{bmatrix} 1x + 2y + 3z \end{bmatrix} = 0$$

For the equation to hold true, the result of this multiplication must be zero. Therefore, the solution to the equation is any vector $\begin{bmatrix} x \\ y \\ z \end{bmatrix}$ such that $x + 2y + 3z = 0$.

We will now go plot the equation on GeoGebra.

We observe that this represents an equation of a plane and it contains the collection of position vectors which satisfy the given equation.
</details>

### Question 28 {: #q-28 .question .unit }

<span class="question__badge">Q28</span>

Use Geogebra and plot all the points in the set below.

$$T= \{ \alpha(1,2,1) \mid \alpha \in \mathbb{R}\}$$

<details class="solution" id="q-28-solution" markdown>
<summary>Solution</summary>

To plot all the points, we will create the given vector in the graph.

Then we will use the sequence command in desired range to show the possible vectors under the given expression as in the question.

We observe that the points follow a straight line pattern passing through the Origin.
</details>

### Question 29 {: #q-29 .question .unit }

<span class="question__badge">Q29</span>

Use Geogebra and plot all the points in the set below.

$$S= \{ \beta(2,7,3) \mid \beta \in \mathbb{R}\}$$

<details class="solution" id="q-29-solution" markdown>
<summary>Solution</summary>

The question will be solved exactly similar to the previous one.
</details>

### Question 30 {: #q-30 .question .unit }

<span class="question__badge">Q30</span>

Use Geogebra and plot all the points in the set below.

$$W= \{\alpha(1,2,1) + \beta(2,7,3) \mid \alpha,\beta \in \mathbb{R}\}$$

<details class="solution" id="q-30-solution" markdown>
<summary>Solution</summary>

We can simply add the two previous sets to create the third one as given in the question in GeoGebra.
</details>

### Question 31 {: #q-31 .question .unit }

<span class="question__badge">Q31</span>

In the above set $W$ find out all the points $(x,y,z)$ satisfying the following: (Use Geogebra)

$$\begin{bmatrix} w_1 & w_2 & w_3 \end{bmatrix} \begin{bmatrix} x \\ y \\ z \end{bmatrix} = 0$$

where $(w_1,w_2,w_3) \in W$. Note that $w_i$s are real numbers.

<details class="solution" id="q-31-solution" markdown>
<summary>Solution</summary>

Solution not provided in the source material.
</details>

### Question 32 {: #q-32 .question .unit }

<span class="question__badge">Q32</span>

Given the matrix $A=\begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 9 \end{bmatrix}$, find out all the possible $(x,y,z)$ such that:

$$\begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 9 \end{bmatrix} \begin{bmatrix} x \\ y \\ z \end{bmatrix} = 0$$

Observe carefully, what has this question got to do with previous five questions in this module.

<details class="solution" id="q-32-solution" markdown>
<summary>Solution</summary>

Given the matrix $A = \begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 9 \end{bmatrix}$, we need to find out all the possible $(x, y, z)$ such that:

$$A \begin{bmatrix} x \\ y \\ z \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \\ 0 \end{bmatrix}$$

This represents a homogeneous system of linear equations. To find the solution, we need to determine the null space (kernel) of matrix $A$. Let's write down the system of equations:

$$\begin{cases} 1x + 2y + 3z = 0 \\ 4x + 5y + 6z = 0 \\ 7x + 8y + 9z = 0 \end{cases}$$

Therefore, the solution to the system is:

$$\begin{bmatrix} x \\ y \\ z \end{bmatrix} = \begin{bmatrix} t \\ -2t \\ t \end{bmatrix} = t \begin{bmatrix} 1 \\ -2 \\ 1 \end{bmatrix}$$

where $t$ is any real number. The solution set is:

$$\{(t, -2t, t) \mid t \in \mathbb{R}\}$$

This means all points $(x, y, z)$ lie on the line parametrized by $(t, -2t, t)$.
</details>

### Question 33 {: #q-33 .question .unit }

<span class="question__badge">Q33</span>

Given the matrix $A=\begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 9 \end{bmatrix}$ what does the following three sets represent?

(i) $\mathscr{R}=\{\alpha(1,2,3) + \beta(4,5,6) + \gamma(7,8,9) \mid \alpha, \beta, \gamma\in \mathbb{R}\}$

(ii) $C=\{\alpha(1,4,7) + \beta(2,5,8) + \gamma(3,6,9) \mid \alpha, \beta, \gamma \in \mathbb{R}\}$

(iii) $N=\{(x,y,z) \mid x(1,4,7) + y(2,5,8) + z(3,6,9) = 0 \}$

Use only Geogebra :)

<details class="solution" id="q-33-solution" markdown>
<summary>Solution</summary>

Solution not provided in the source material.
</details>

### Question 34 {: #q-34 .question .unit }

<span class="question__badge">Q34</span>

Did you observe that every vector of $\mathscr{R}$ is perpendicular to every vector of $N$?

<details class="solution" id="q-34-solution" markdown>
<summary>Solution</summary>

This observation can easily be made once the graphs are plotted in GeoGebra.
</details>

### Question 35 {: #q-35 .question .unit }

<span class="question__badge">Q35</span>

Consider the matrix $B=\begin{bmatrix} 1 & 2 \\ 2 & 4 \end{bmatrix}$. Draw the line $2y+x=4$. Seeing the matrix $B$ as a function $B:\mathbb{R}^2\mapsto \mathbb{R}^2$, where does $B$ takes the line $2y+x=4$?

Where does it take:

i) $2y+x=10$

ii) $2y+x=62$

iii) $2y+x=1800$

<details class="solution" id="q-35-solution" markdown>
<summary>Solution</summary>

For $x + 2y = 4$,

$$B \begin{pmatrix} x \\ y \end{pmatrix} = \begin{pmatrix} 1 & 2 \\ 2 & 4 \end{pmatrix} \begin{pmatrix} x \\ -\frac{1}{2}x + 2 \end{pmatrix} = \begin{pmatrix} x + 2\left(-\frac{1}{2}x + 2\right) \\ 2x + 4\left(-\frac{1}{2}x + 2\right) \end{pmatrix}$$

Simplifying, we get:

$$\begin{pmatrix} x + 2(2 - \frac{1}{2}x) \\ 2x + 4(2 - \frac{1}{2}x) \end{pmatrix} = \begin{pmatrix} 4 \\ 8 \end{pmatrix}$$

So, every point lying on the line $x + 2y = 4$ is transformed to the point $(4,8)$ by the matrix B.

Now, let's compute the transformations for each specific case:

(i) For the line $2y + x = 10$, we rewrite it as $y = -\frac{1}{2}x + 5$. Approaching with the similar method, we get that every point here is directed towards $(10,20)$.

(ii) For the line $2y + x = 62$, we rewrite it as $y = -\frac{1}{2}x + 31$. Applying the transformation $B$ to this line, we'll follow the same steps as above.

(iii) For the line $2y + x = 1800$, we rewrite it as $y = -\frac{1}{2}x + 900$. Applying the transformation $B$ to this line, we'll follow the same steps as above.
</details>

### Question 35a {: #q-35a .question .unit }

<span class="question__badge">Q35a</span>

In general $B=\begin{bmatrix} 1 & 2 \\ 2 & 4 \end{bmatrix}:\mathbb{R}^2\mapsto \mathbb{R}^2$, where does this function take $2y+x=k$? (where $k$ is a constant)

<details class="solution" id="q-35a-solution" markdown>
<summary>Solution</summary>

Following the same procedure, we get that the points on such a line when undergo transformation through the matrix B, all lead to a point, i.e., $(k,2k)$.
</details>

### Question 36 {: #q-36 .question .unit }

<span class="question__badge">Q36</span>

Consider a matrix $A=\begin{bmatrix} 1 & 4 \\ 2 & 3 \end{bmatrix}$ and a vector $v = \begin{bmatrix} 1 \\ 1 \end{bmatrix}$ to what is it transformed?

(a) Is it rotated?

(b) Is the magnitude preserved?

(c) What is the ratio of magnitude of $Av$ to $v$?

<details class="solution" id="q-36-solution" markdown>
<summary>Solution</summary>

To transform the vector $v$ using the matrix $A$, we perform matrix multiplication:

$$Av = \begin{bmatrix} 1 & 4 \\ 2 & 3 \end{bmatrix} \begin{bmatrix} 1 \\ 1 \end{bmatrix}$$

$$Av = \begin{bmatrix} 1*1 + 4*1 \\ 2*1 + 3*1 \end{bmatrix}$$

$$Av = \begin{bmatrix} 1 + 4 \\ 2 + 3 \end{bmatrix} = \begin{bmatrix} 5 \\ 5 \end{bmatrix}$$

So, the vector $v$ is transformed to $Av = \begin{bmatrix} 5 \\ 5 \end{bmatrix}$.

(a) No, it is not rotated. A rotation would imply a change in direction, but here, the direction of the vector remains the same after transformation.

(b) No, the magnitude is not preserved. The original vector $v$ had a magnitude of $\sqrt{1^2 + 1^2} = \sqrt{2}$, while the transformed vector $Av$ has a magnitude of $\sqrt{5^2 + 5^2} = \sqrt{50}$, which is larger.

(c) The magnitude of $Av$ is $\sqrt{50}$, and the magnitude of $v$ is $\sqrt{2}$. So, the ratio is:

$$\frac{\|Av\|}{\|v\|} = \frac{\sqrt{50}}{\sqrt{2}} = \sqrt{\frac{25}{1}} = 5$$

So, the ratio of the magnitude of $Av$ to $v$ is 5.
</details>

### Question 37 {: #q-37 .question .unit }

<span class="question__badge">Q37</span>

Given $B=\begin{bmatrix} 1 & 2 \\ 2 & 4 \end{bmatrix}:\mathbb{R}^2\mapsto \mathbb{R}^2$. What is the range of this function?

<details class="solution" id="q-37-solution" markdown>
<summary>Solution</summary>

The range of this function is a straight line pasing through the Origin with slope equal to 2, i.e., $y = 2x$.
</details>

### Question 38 {: #q-38 .question .unit }

<span class="question__badge">Q38</span>

You have achieved the required wisdom if you have realized that: $B=\begin{bmatrix} 1 & 2 \\ 2 & 4 \end{bmatrix}:\mathbb{R}^2\mapsto \mathbb{R}^2$. "$B$ collapses a dimension".

<details class="solution" id="q-38-solution" markdown>
<summary>Solution</summary>

Indeed, the matrix $B = \begin{pmatrix} 1 & 2 \\ 2 & 4 \end{pmatrix}$ represents a transformation that collapses a dimension. This can be inferred from the fact that the range of the transformation is a straight line in $\mathbb{R}^2$. In other words, applying the transformation $B$ to any input vector in $\mathbb{R}^2$ results in an output vector lying along a one-dimensional subspace of $\mathbb{R}^2$.

This collapse of dimensionality is evident in the transformation because the second row of the matrix $B$ is a scalar multiple of the first row, indicating that the transformation essentially scales one dimension (the $y$-dimension) by a factor of 2 relative to the other dimension (the $x$-dimension), ultimately resulting in a line where the two dimensions are equal.
</details>
