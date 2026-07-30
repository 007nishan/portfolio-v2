<section class="opener" id="mod-B">
<span class="chapter-num">B</span>

# Module B — Matrices, Systems & Markov Chains
<span class="accent-rule"></span>
</section>

### Question 17 {: #q-17 .question .unit }

<span class="question__badge">Q17</span>

$A$ is assigned $0$, $B:1$, $C:2$, and so on up to $Z:25$.

Assume you denoted every letter with a number, as given in the table above. You need to encrypt the word $SUDARSHANA$ which stands for the numbers: $18, 20, 3, 0, 17, 18, 7, 0, 13, 0$.

You encrypt this using a matrix given by: $\begin{bmatrix} 2 & 3 \\ 3 & 4 \end{bmatrix}$.

So $SUDARSHANA$ will end up becoming: $96, 134, 6, 9, 88, 123, 14, 21, 26, 39$.

Given these numbers, how will you decrypt the message and get back $SUDARSHANA$? This is a well known cryptographic protocol called the Hill Cipher. You can read more online.

<details class="solution" id="q-17-solution" markdown>
<summary>Solution</summary>

To decrypt the message encrypted using the Hill Cipher, we need to apply the inverse of the encryption matrix. Given the encrypted numbers representing "SUDARSHANA" as 96, 134, 6, 9, 88, 123, 14, 21, 26, and 39, we first identify the corresponding encryption matrix, denoted as $\mathbf{E}$, which in this case is $\begin{pmatrix} 2 & 3 \\ 3 & 4 \end{pmatrix}$. Utilizing this matrix, we compute its inverse, considering modulo 26 arithmetic. The decryption matrix, denoted as $\mathbf{D}$, is then obtained. Proceeding with decryption, each pair of encrypted numbers undergoes matrix multiplication with $\mathbf{D}$, followed by modulo 26 reduction. This process retrieves the original numbers corresponding to each letter. The decryption process is represented as $\mathbf{p} = \mathbf{D} \cdot \mathbf{c} \pmod{26}$, where $\mathbf{p}$ represents the decrypted numbers and $\mathbf{c}$ represents the encrypted numbers. Finally, mapping these numbers back to their corresponding letters reveals the decrypted message "SUDARSHANA." This cryptographic protocol, known as the Hill Cipher, leverages linear algebra principles for both encryption and decryption, ensuring a secure communication channel.
</details>

### Question 18 {: #q-18 .question .unit }

<span class="question__badge">Q18</span>

We encounter equations very often in our lives. Consider for example, the following situation at Baker's Cafe. The manager has a very important estimate to make. Mostly, visitors at his cafe happen to be families and they are often comprised of Children and/or Adults. He observes that there are 3 adults and 1 child at a table and their bill turns out to be Rs.1200/-. There is yet another table with 2 children and 1 adult and their bill comes out to be Rs.1000/-. Can the manager estimate the consumption of a Child/Adult? This is popularly called the Simultaneous Equations and we all remember from our school days, multiple ways in which these can be solved.

$$3A + 1C = 1200$$

$$1A + 2C = 1000$$

<details class="solution" id="q-18-solution" markdown>
<summary>Solution</summary>

Let's denote the consumption of an adult as $A$ and that of a child as $C$.

The first observation, with 3 adults and 1 child resulting in a bill of Rs. 1200, can be expressed as the equation:

$$3A + 1C = 1200$$

Similarly, the second observation, with 2 children and 1 adult totaling Rs. 1000, can be represented as:

$$1A + 2C = 1000$$

To solve this system of equations, we can employ various methods such as substitution, elimination, or matrix methods. The values of $A$ and $C$ are determined as $280$ and $360$ respectively.
</details>

### Question 19 {: #q-19 .question .unit }

<span class="question__badge">Q19</span>

While we were taught the so called two variables and two unknowns, what if there were more equations than unknowns?

$$3A + 1C = 1200$$

$$1A + 2C = 1000$$

$$1A + 1C = 900$$

<details class="solution" id="q-19-solution" markdown>
<summary>Solution</summary>

Plot the three lines on 2-D plane. Observe that these do not have any unique solution. So, we cannot have any set of values of A and C which exactly fit in the 3 equations. Therefore, we will have to find the best fit, i.e., we have to find the values of A and C which make the outputs of all the three equations closest to their respective RHS. Think how can we approach this problem.
</details>

### Question 20 {: #q-20 .question .unit }

<span class="question__badge">Q20</span>

Note that the previous question can be modelled as a matrix:

$$3A + 1C = 1200$$

$$1A + 2C = 1000$$

$$1A + 1C = 900$$

Observe this is same as:

$$\begin{bmatrix} 3 & 1 \\ 1 & 2 \\ 1 & 1 \end{bmatrix} \begin{bmatrix} A \\ C \end{bmatrix} = \begin{bmatrix} 1200 \\ 1000 \\ 900 \end{bmatrix}$$

Now try to solve the previous problem.

<details class="solution" id="q-20-solution" markdown>
<summary>Solution</summary>

$$\begin{pmatrix} 3 & 1 \\ 1 & 2 \\ 1 & 1 \end{pmatrix} \begin{pmatrix} A \\ C \end{pmatrix} = \begin{pmatrix} 1200 \\ 1000 \\ 900 \end{pmatrix}$$

Here, the coefficient matrix on the left represents the coefficients of the unknowns $A$ and $C$ in each equation, while the vector on the right represents the constants on the right-hand side of each equation.

Observe that the LHS of the above equation can be written as

$$\begin{pmatrix} 3 \\ 1 \\ 1 \end{pmatrix} A + \begin{pmatrix} 1 \\ 2 \\ 1 \end{pmatrix} C = \begin{pmatrix} 1200 \\ 1000 \\ 900 \end{pmatrix}$$

Therefore, LHS can only be a linear combination of the vectors $(3,1,1)$ and $(1,2,1).$ But we need a vector which lies closest to our desired output, i.e., (1200,1000,900). So, we will see all the vectors which can be formed by taking a linear combination of the 2 vectors. These all vectors lie on the plane formed by these vectors (Observe how?). Now we find the vector on this plane which is closest to the point in RHS. This will be obtained by taking the foot of perpendicular from the point (1200,1000,900) on the plane. Now we have found the closest fit, which can be represented as a linear combination of the two vectors in LHS. Therefore, now we can find the values of A and C by solving any of the two equations, keeping the new point (closest one) in the RHS.
</details>

### Question 21 {: #q-21 .question .unit }

<span class="question__badge">Q21</span>

One obvious way to solve this, is to guess the values :-). Can you get closer to the solution by guessing? Note that there is no solution to this question. You can just reduce the error. Do you see why?

<details class="solution" id="q-21-solution" markdown>
<summary>Solution</summary>

Solution not provided in the source material.
</details>

### Question 22 {: #q-22 .question .unit }

<span class="question__badge">Q22</span>

In the figure below (a two-state Happy / Stressed transition diagram): If 1000 people were to start in one state, what will be the distribution of people eventually? Write down a python script to find the convergence.

```figure
alt: Two-state Markov transition diagram between Happy and Stressed states, with transition probabilities 0.3, 0.7, 0.5 and 0.5
books/linear-algebra/figures/markov-2state.png
A two-state Markov chain: Happy and Stressed, with the labelled transition probabilities.
```

<details class="solution" id="q-22-solution" markdown>
<summary>Solution</summary>

To find the eventual distribution of people between the Happy (H) and Stressed (S) states, we can use the given system of equations and iterate until we reach convergence.

The equations can be written in matrix form as:

$$\begin{pmatrix} H \\ S \end{pmatrix}_{n+1} = \begin{pmatrix} 0.3 & 0.5 \\ 0.7 & 0.5 \end{pmatrix} \begin{pmatrix} H \\ S \end{pmatrix}_{n}$$

Let's denote the state vector as $\mathbf{v} = \begin{pmatrix} H \\ S \end{pmatrix}$ and the transition matrix as $A = \begin{pmatrix} 0.3 & 0.5 \\ 0.7 & 0.5 \end{pmatrix}$. The iteration process can be represented as:

$$\mathbf{v}_{n+1} = A \mathbf{v}_n$$

We will use Python to perform this iteration and observe the convergence. Here's the script:

```python
import numpy as np
A = np.array([[0.3, 0.5],[0.7, 0.5]])
v = np.array([1000, 0])
def iterate_until_convergence(A, v, tolerance=1e-6, max_iterations=10000):
    for _ in range(max_iterations):
        v_next = A @ v
        if np.allclose(v, v_next, atol=tolerance):
            return v_next
        v = v_next
    return v
final_distribution = iterate_until_convergence(A, v)
total_population = np.sum(final_distribution)
percentage_distribution = final_distribution / total_population * 100
print(final_distribution, percentage_distribution)
```
</details>

### Question 23 {: #q-23 .question .unit }

<span class="question__badge">Q23</span>

In the figure below (a three-state transition diagram): If 1000 people were to start in one state, what will be the distribution of people eventually? Write down a python script to find the convergence.

```figure
alt: Three-state Markov transition diagram between states P, A and R with labelled transition probabilities
books/linear-algebra/figures/markov-3state.png
A three-state Markov chain over states P, A and R with the labelled transition probabilities.
```

<details class="solution" id="q-23-solution" markdown>
<summary>Solution</summary>

This question will be solved similar to the previous one. But, the Matrix equation will be as follow:

$$\begin{pmatrix} P \\ A \\ R \end{pmatrix}_{n+1} = \begin{pmatrix} 0.5 & 0.5 & 0.1 \\ 0.3 & 0.1 & 0.8 \\ 0.2 & 0.4 & 0.1 \end{pmatrix} \begin{pmatrix} P \\ A \\ R \end{pmatrix}_{n}$$
</details>
