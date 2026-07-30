<section class="opener" id="mod-A">
<span class="chapter-num">A</span>

# Module A — Lines, Functions & Matrices as Maps
<span class="accent-rule"></span>
</section>

### Question 1 {: #q-1 .question .unit }

<span class="question__badge">Q1</span>

Ram and Lakshman were two brothers, Ram's pocket money was twice as Lakshman. The good boys that Ram and Lakshman were, they did not spend their pocket money on anything. They instead saved the same in their piggy bank. Every week, they would check their savings so far. Assume the first week's savings was $(R_1,L_1)$ and second week's $(R_2,L_2)$ and so on. They try plotting their weekly savings on a graph sheet. How will the points look like?

<details class="solution" id="q-1-solution" markdown>
<summary>Solution</summary>

In GeoGebra, if you plot the weekly savings of Ram and Lakshman on a graph with the x-axis representing Lakshman's savings and the y-axis representing Ram's savings the points will form a straight line. This is because Ram's savings are always proportional to Lakshman's savings.

The points will follow a straight line passing through the origin as:

$$y = 2x$$
</details>

### Question 2 {: #q-2 .question .unit }

<span class="question__badge">Q2</span>

Atul's house is centered at origin $(0,0)$ he walks straight (along the x-axis) for 2 units and then takes a left and walks 1 unit to reach Bala's house, after that he takes a right turn and walks for one unit and then a left turn and walks for one unit and reaches Chetan's house. He continues in a similar style, takes a right turn 1 unit and then left turn one unit and reaches Divya's house. Are the houses of Bala, Chetan and Divya on a straight line? What is the equation of this line? Plot this on Geogebra.

<details class="solution" id="q-2-solution" markdown>
<summary>Solution</summary>

Atul starts his journey from the origin $O = (0, 0).$ He first walks 2 units along the x-axis to reach $(2, 0)$, then takes a left turn and walks 1 unit to reach Bala's house at $(2, 1).$ Next, he continues by taking a right turn from Bala's house and walking 1 unit to $(3, 1),$ followed by another left turn and walking 1 unit to reach Chetan's house at $(3, 2).$ Continuing in the same pattern, Atul takes a right turn from Chetan's house and walks 1 unit to $(4, 2),$ then takes a left turn and walks 1 unit to reach Divya's house at $(4, 3).$

Now, we will plot these points on GeoGebra and make a line out of them taking two at a time.

We can clearly observe that whether the points make a straight line.
</details>

### Question 3 {: #q-3 .question .unit }

<span class="question__badge">Q3</span>

Plot the lines $y=x$, $y=2x$, $y=10x$.

<details class="solution" id="q-3-solution" markdown>
<summary>Solution</summary>

To plot these lines using GeoGebra, in the input bar at the bottom, type the equations and they will be plotted on the graph.

Using GeoGebra to plot these lines provides a clear visual representation of how different linear equations with varying slopes behave.

We can observe that the line $y = 10x$ is the steepest of them all. and the line $y = x$ is the shallowest.
</details>

### Question 4 {: #q-4 .question .unit }

<span class="question__badge">Q4</span>

Observe that they all pass through the origin. Why?

<details class="solution" id="q-4-solution" markdown>
<summary>Solution</summary>

All of the lines provided in the previous question are of the form:

$$y = kx,$$

where k is 1, 2 and 10.

Here, y is defined as k times x, i.e., when we put $k = 0,$ y will definitely be 0 as $0 * t = 0$ for all t belonging to R.

As Origin is $(0,0)$ point, All the lines pass through it.
</details>

### Question 5 {: #q-5 .question .unit }

<span class="question__badge">Q5</span>

Plot $y=2x+1$. Observe, Why doesn't it pass through the origin?

<details class="solution" id="q-5-solution" markdown>
<summary>Solution</summary>

The plotting is done similarly to the previous questions in thew Module.

The line does not pass through the Origin because when x is considered to be 0, y comes out to be 2 * 0 + 1, which gives 1. Hence, it does not pass through the Origin, i.e., $(0,0).$
</details>

### Question 6 {: #q-6 .question .unit }

<span class="question__badge">Q6</span>

Plot $y=ax+b$, with $a$ and $b$ as parameters which you should be able to vary. What do you observe?

<details class="solution" id="q-6-solution" markdown>
<summary>Solution</summary>

To explore the behavior of the linear equation $y=ax+b$ with varying parameters $a$ (slope) and $b$ (y-intercept) using GeoGebra, you can use sliders to dynamically adjust these values and observe the resulting changes on the graph.

As you adjust the slider for $a$, you will notice that increasing $a$ makes the line steeper, while decreasing it makes the line gentler.

Adjusting the slider for $b$ shifts the entire line vertically. Increasing $b$ moves the line upwards, while decreasing $b$ moves it downwards.

This interactive approach in GeoGebra helps visualize and understand how the parameters a and b influence the equation of a line, providing a clear and dynamic way to grasp the fundamental properties of linear equations.
</details>

### Question 6a {: #q-6a .question .unit }

<span class="question__badge">Q6a</span>

Let a line be $y=5x+6$. For what values of $\alpha$ and $\beta$ will the line $y=\alpha x + \beta$ be parallel to the given line? When will it intersect the given line in the 3rd quadrant?

<details class="solution" id="q-6a-solution" markdown>
<summary>Solution</summary>

Two lines are only parallel if there slopes are equal. So for the line to be parallel to

$$y = 5x + 6,$$

Alpha must be equal to 5, whereas the value of Beta does not change the lines being parallel.

This can be observed by plotting the lines and using sliders on GeoGebra.

For the lines to intersect in third quadrant, solve the two equations and when we will get the values of x and y in the terms of $\alpha$ and $\beta$, make both x and y less than 0.

We will get the values of $\alpha$ and $\beta$ upon solving the inequalities.
</details>

### Question 7 {: #q-7 .question .unit }

<span class="question__badge">Q7</span>

Consider the following simultaneous equation:

$$2x+3y=7$$

$$3x+4y=10$$

Do you see a 2x2 matrix here? What is the importance of seeing a matrix in this problem? Why study matrices in general? Do you observe that this problem can be retold as:

$$\begin{bmatrix} 2 & 3 \\ 3 & 4 \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix} = \begin{bmatrix} 7 \\ 10 \end{bmatrix}$$

<details class="solution" id="q-7-solution" markdown>
<summary>Solution</summary>

Solution not provided in the source material.
</details>

### Question 8 {: #q-8 .question .unit }

<span class="question__badge">Q8</span>

Consider a simple function $f(x) = 3x+2$. This function is invertible right? Can you tell us what is $\alpha$ such that $f(\alpha)=17$? Is such an $\alpha$ unique? How did you find such an $\alpha$? Is this always possible?

<details class="solution" id="q-8-solution" markdown>
<summary>Solution</summary>

An invertible function is one that has a unique inverse function, meaning that for every output value of the function, there is exactly one input value that produced it. This property ensures that each y in the function's range corresponds to exactly one x in the domain. So, yes, this function indeed is invertible.

This equation can be solved by putting the value of the function as 17 in the equation and then solving it.

The value of $\alpha$ comes out to be 5.

Linear functions with non-zero slopes are one-to-one (bijective) and thus have a unique inverse. For any given output y, there is exactly one input x such that f(x)=y.

For such functions, it is always possible to find such a value.
</details>

### Question 9 {: #q-9 .question .unit }

<span class="question__badge">Q9</span>

Consider the function $f(x)=x^2-10$, what is $f(5)$?

<details class="solution" id="q-9-solution" markdown>
<summary>Solution</summary>

f(5) signifies the value of the function at $x = 5$, which is given by $x*x - 10$, i.e., $25 - 10 = 15$.
</details>

### Question 10 {: #q-10 .question .unit }

<span class="question__badge">Q10</span>

Consider the function $f(x)=x^2-10$, if $f(\alpha)=54$, what is $\alpha$?

<details class="solution" id="q-10-solution" markdown>
<summary>Solution</summary>

Here, we have to find x and we know the value of the function. So, $54 = x*x - 10$, i.e., $x = 8$ or $-8$.
</details>

### Question 11 {: #q-11 .question .unit }

<span class="question__badge">Q11</span>

Consider the function $g(x)=x^3-x^2-10x+2$, if $g(x)=-22$ what is $x$?

<details class="solution" id="q-11-solution" markdown>
<summary>Solution</summary>

We can find this by plotting the curve of $g(x) + 22 = 0$ on GeoGebra and then checking the roots of the equation.

On plotting the curve, we observe that it has only one real root and two roots are imaginary as the degree of the equation is 3.
</details>

### Question 12 {: #q-12 .question .unit }

<span class="question__badge">Q12</span>

Do you know what is $\mathbb{R}, \mathbb{R}^2$ and $\mathbb{R}^3$ ?

<details class="solution" id="q-12-solution" markdown>
<summary>Solution</summary>

$\mathbb{R}$ represents the set of all real numbers (one-dimensional), $\mathbb{R}^2$ represents the two-dimensional space of ordered pairs of real numbers, and $\mathbb{R}^3$ represents the three-dimensional space of ordered triples of real numbers.
</details>

### Question 13 {: #q-13 .question .unit }

<span class="question__badge">Q13</span>

Consider the function $\varphi : \mathbb{R}^2\rightarrow \mathbb{R}^2$ defined by $\varphi(x,y)=(2x+3y,3x+4y)$. Find x and y such that $\varphi(x,y)=(5,6)$. Observe that (5,6) as well as (x,y) lies in $\mathbb{R}^2$.

<details class="solution" id="q-13-solution" markdown>
<summary>Solution</summary>

To find the values of $x$ and $y$ such that the function $\varphi: \mathbb{R}^2 \to \mathbb{R}^2$, defined by $\varphi(x, y) = (2x + 3y, 3x + 4y)$, maps to the point $(5, 6)$, we need to solve the corresponding system of linear equations. Specifically, we set $\varphi(x, y) = (5, 6)$, which gives us the system of equations:

$$2x + 3y = 5$$

$$3x + 4y = 6$$

To solve this system, we can use the elimination method. First, we multiply the first equation by 3 and the second equation by 2 to align the coefficients of $x$. This yields

$$6x + 9y = 15$$

$$6x + 8y = 12$$

Next, we subtract the second equation from the first to eliminate $x$, resulting in

$$6x + 9y - 6x - 8y = 15 - 12$$

which simplifies to

$$y = 3$$

With $y$ determined, we substitute $y = 3$ back into one of the original equations to solve for $x$. Using the first equation, $2x + 3(3) = 5$, we get

$$2x + 9 = 5$$

Subtracting 9 from both sides, we find

$$2x = -4$$

and dividing by 2, we obtain

$$x = -2$$

Therefore, the values of $x$ and $y$ that satisfy $\varphi(x, y) = (5, 6)$ are $x = -2$ and $y = 3$.

It is important to observe that both the point $(5, 6)$ and the pair $(x, y)$ lie in $\mathbb{R}^2$. This means that $(5, 6)$ and $(-2, 3)$ are both elements of the two-dimensional real number space, $\mathbb{R}^2$, which is consistent with the domain and codomain of the function $\varphi$.
</details>

### Question 14 {: #q-14 .question .unit }

<span class="question__badge">Q14</span>

Is the function $\varphi$ invertible? In the question above on matrices, we see that it is of the form $A\vec{x}=b$. Note that we can invert the matrix, using the method that was taught to us in our high school to find out the value for the variables $x$ and $y$. This is one of the many applications of matrices.

<details class="solution" id="q-14-solution" markdown>
<summary>Solution</summary>

To determine if the function $\varphi$ is invertible, we need to analyze the function $\varphi: \mathbb{R}^2 \to \mathbb{R}^2$ defined by $\varphi(x, y) = (2x + 3y, 3x + 4y)$. This problem can be expressed in matrix form as $A \vec{x} = \vec{b}$, where $A$ is the matrix of coefficients, $\vec{x}$ is the column vector of variables $(x, y)$, and $\vec{b}$ is the result vector $(5, 6)$.

The matrix $A$ corresponding to the linear transformation is:

$$A = \begin{pmatrix} 2 & 3 \\ 3 & 4 \end{pmatrix}$$

For $\varphi$ to be invertible, the matrix $A$ must be invertible. A matrix is invertible if its determinant is non-zero. We calculate the determinant of $A$:

$$\det(A) = \begin{vmatrix} 2 & 3 \\ 3 & 4 \end{vmatrix} = (2 \cdot 4) - (3 \cdot 3) = 8 - 9 = -1$$

Since the determinant of $A$ is $-1$, which is non-zero, the matrix $A$ is invertible. Consequently, the function $\varphi$ is also invertible.

To find the inverse function, we use the inverse of the matrix $A$. The inverse of $A$ is calculated using the formula for the inverse of a $2 \times 2$ matrix:

$$A^{-1} = \frac{1}{\det(A)} \begin{pmatrix} d & -b \\ -c & a \end{pmatrix} = \frac{1}{-1} \begin{pmatrix} 4 & -3 \\ -3 & 2 \end{pmatrix} = \begin{pmatrix} -4 & 3 \\ 3 & -2 \end{pmatrix}$$

Therefore, the inverse function $\varphi^{-1}$ can be written as:

$$\varphi^{-1}(x', y') = \begin{pmatrix} -4 & 3 \\ 3 & -2 \end{pmatrix} \begin{pmatrix} x' \\ y' \end{pmatrix} = \begin{pmatrix} -4x' + 3y' \\ 3x' - 2y' \end{pmatrix}$$

Applying this to find the values of $x$ and $y$ for $\varphi(x, y) = (5, 6)$:

$$\begin{pmatrix} x \\ y \end{pmatrix} = \begin{pmatrix} -4 & 3 \\ 3 & -2 \end{pmatrix} \begin{pmatrix} 5 \\ 6 \end{pmatrix} = \begin{pmatrix} -4(5) + 3(6) \\ 3(5) - 2(6) \end{pmatrix} = \begin{pmatrix} -20 + 18 \\ 15 - 12 \end{pmatrix} = \begin{pmatrix} -2 \\ 3 \end{pmatrix}$$

Thus, $x = -2$ and $y = 3$.
</details>

### Question 14a {: #q-14a .question .unit }

<span class="question__badge">Q14a</span>

Take a random looking 2*2 matrix. Is it invertible? How often is it invertible?

<details class="solution" id="q-14a-solution" markdown>
<summary>Solution</summary>

To determine whether a random $2 \times 2$ matrix is invertible, we need to consider the properties of the matrix. A $2 \times 2$ matrix is invertible if and only if its determinant is non-zero.

Let's take a random $2 \times 2$ matrix:

$$A = \begin{pmatrix} a & b \\ c & d \end{pmatrix}$$

The determinant of this matrix $A$ is calculated as follows:

$$\det(A) = ad - bc$$

For the matrix $A$ to be invertible, $\det(A)$ must not be equal to zero. Therefore, the condition for invertibility is:

$$ad - bc \neq 0$$
</details>

### Question 15 {: #q-15 .question .unit }

<span class="question__badge">Q15</span>

We will now see matrices as functions. Instead of $\varphi$ we will write the matrix itself: $\begin{bmatrix} 2 & 3 \\ 3 & 4 \end{bmatrix} : \mathbb{R}^2 \rightarrow \mathbb{R}^2$.

<details class="solution" id="q-15-solution" markdown>
<summary>Solution</summary>

We can view matrices as functions that map vectors from one space to another. For example, consider the matrix:

$$A = \begin{pmatrix} 2 & 3 \\ 3 & 4 \end{pmatrix}$$

This matrix $A$ can be seen as a function $A: \mathbb{R}^2 \to \mathbb{R}^2$ that takes a vector from $\mathbb{R}^2$ and maps it to another vector in $\mathbb{R}^2$. Specifically, for a vector $\vec{x} = \begin{pmatrix} x \\ y \end{pmatrix}$, the matrix function $A$ acts on $\vec{x}$ as follows:

$$A \vec{x} = \begin{pmatrix} 2 & 3 \\ 3 & 4 \end{pmatrix} \begin{pmatrix} x \\ y \end{pmatrix} = \begin{pmatrix} 2x + 3y \\ 3x + 4y \end{pmatrix}$$
</details>

### Question 16 {: #q-16 .question .unit }

<span class="question__badge">Q16</span>

Consider the function $\begin{bmatrix} 1 & 2 \\ 2 & 4 \end{bmatrix} : \mathbb{R}^2 \rightarrow \mathbb{R}^2$. This matrix takes a few elements to the origin. What are those elements? Plot this using Geogebra.

<details class="solution" id="q-16-solution" markdown>
<summary>Solution</summary>

Consider the function represented by the matrix $A$:

$$A = \begin{pmatrix} 1 & 2 \\ 2 & 4 \end{pmatrix}$$

This matrix $A: \mathbb{R}^2 \to \mathbb{R}^2$ maps vectors from $\mathbb{R}^2$ to $\mathbb{R}^2$. We are interested in finding which vectors $\vec{x} = \begin{pmatrix} x \\ y \end{pmatrix}$ are mapped to the origin by this matrix, i.e., we want to solve the equation:

$$A \vec{x} = \begin{pmatrix} 1 & 2 \\ 2 & 4 \end{pmatrix} \begin{pmatrix} x \\ y \end{pmatrix} = \begin{pmatrix} 0 \\ 0 \end{pmatrix}$$

This leads to the system of linear equations:

$$\begin{cases} 1x + 2y = 0 \\ 2x + 4y = 0 \end{cases}$$

We can simplify this system by noting that the second equation is just twice the first equation. Therefore, it suffices to solve the first equation:

$$x + 2y = 0 \implies x = -2y$$

This means that any vector of the form $\vec{x} = \begin{pmatrix} -2y \\ y \end{pmatrix}$ will be mapped to the origin by the matrix $A$. In other words, the vectors that are mapped to the origin lie along the line $x = -2y$.

This line will be called as the Null Space of the Matrix.
</details>
