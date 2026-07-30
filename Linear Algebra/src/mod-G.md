<section class="opener" id="mod-G">
<span class="chapter-num">G</span>

# Module G — Probability & Expectation
<span class="accent-rule"></span>
</section>

### Question 63 {: #q-63 .question .unit }

<span class="question__badge">Q63</span>

A dart is thrown at random onto a board that has the shape of a circle as shown below. Calculate the probability that the dart will hit the shaded region.

```figure
alt: A dartboard of two concentric circles, an outer circle of radius 14 cm and an inner circle of radius 7 cm, with the annular region between them shaded
books/linear-algebra/figures/dartboard.jpg
The dartboard: two concentric circles of radius 14 cm and 7 cm; the shaded region is the annulus between them.
```

<details class="solution" id="q-63-solution" markdown>
<summary>Solution</summary>

The shaded region is the difference in area between two concentric circles (a larger circle and a smaller circle).

- The radius of the larger circle $R$ is 14 units.
- The radius of the smaller circle $r$ is 7 units.

The area of the shaded region $A_{\text{shaded}}$ is given by the difference in the areas of these two circles:

$$A_{\text{shaded}} = \pi R^2 - \pi r^2$$

Substituting the values:

$$A_{\text{shaded}} = \pi (14^2 - 7^2) = \pi (196 - 49) = \pi \cdot 147$$

The total area $A_{\text{total}}$ is the area of the larger circle:

$$A_{\text{total}} = \pi R^2 = \pi \cdot 14^2 = \pi \cdot 196$$

The probability $P$ of a dart hitting the shaded region is the ratio of the area of the shaded region to the total area of the circle:

$$P = \frac{A_{\text{shaded}}}{A_{\text{total}}} = \frac{\pi \cdot 147}{\pi \cdot 196} = \frac{147}{196}$$

Simplifying the fraction:

$$P = \frac{147 \div 49}{196 \div 49} = \frac{3}{4}$$

Thus, the probability of a dart hitting the shaded region is $\frac{3}{4}$ or 0.75.
</details>

### Question 64 {: #q-64 .question .unit }

<span class="question__badge">Q64</span>

Let a pair of dice be thrown and the random variable X be the sum of the numbers that appear on the two dice. Find the mean or expectation of X.

<details class="solution" id="q-64-solution" markdown>
<summary>Solution</summary>

To find the mean or expectation of the random variable X, which represents the sum of the numbers on two dice, you can use the formula:

$$\text{Mean } (\mu) = \sum_{i=2}^{12} i \times P(X=i)$$

Where $P(X=i)$ is the probability that the sum of the two dice equals $i$.

The sum can range from 2 (if both dice show 1) to 12 (if both dice show 6). The probability of getting each sum can be calculated by considering all possible combinations of the dice.

Here's a table of the sums and their probabilities:

$$\begin{array}{|c|c|} \hline \text{Sum} & \text{Probability} \\ \hline 2 & \frac{1}{36} \\ 3 & \frac{2}{36} \\ 4 & \frac{3}{36} \\ 5 & \frac{4}{36} \\ 6 & \frac{5}{36} \\ 7 & \frac{6}{36} \\ 8 & \frac{5}{36} \\ 9 & \frac{4}{36} \\ 10 & \frac{3}{36} \\ 11 & \frac{2}{36} \\ 12 & \frac{1}{36} \\ \hline \end{array}$$

Now, calculate the mean:

$$\mu = (2 \times \tfrac{1}{36}) + (3 \times \tfrac{2}{36}) + (4 \times \tfrac{3}{36}) + \ldots + (12 \times \tfrac{1}{36})$$

$$\mu = \frac{1}{36} \times (252) = \frac{252}{36} = 7$$

So, the mean or expectation of $X$ is approximately $7$.
</details>

### Question 65 {: #q-65 .question .unit }

<span class="question__badge">Q65</span>

A factory produces items, and each item is independently defective with probability 0.2. If 100 items are produced in a day, what is the expected number of defective items?

<details class="solution" id="q-65-solution" markdown>
<summary>Solution</summary>

To find the expected number of defective items produced in a day by the factory, we use the concept of expectation in probability theory.

Given:

- Each item is defective with probability $p = 0.2$.
- The number of items produced in a day $n = 100$.

The expected number of defective items $E(X)$ can be calculated using the formula for the expectation of a binomial distribution:

$$E(X) = n \cdot p$$

Substituting the given values:

$$E(X) = 100 \cdot 0.2 = 20$$

Thus, the expected number of defective items produced in a day is 20.
</details>

### Question 66 {: #q-66 .question .unit }

<span class="question__badge">Q66</span>

A point is chosen at random inside a sphere of radius R. What is the probability that this point is closer to the center of the sphere than to its surface?

<details class="solution" id="q-66-solution" markdown>
<summary>Solution</summary>

To find the probability that a randomly chosen point inside a sphere is closer to the center than to its surface, we analyze the problem geometrically.

Given:

- The sphere has a radius $R$.
- We need to find the probability that a point is closer to the center than to the surface of the sphere.
- A point inside the sphere is closer to the center than to the surface if its distance from the center is less than half the radius of the sphere, $\frac{R}{2}$.

The volume $V_{\text{inner}}$ of the sphere with radius $\frac{R}{2}$ is given by:

$$V_{\text{inner}} = \frac{4}{3} \pi \left( \frac{R}{2} \right)^3 = \frac{4}{3} \pi \cdot \frac{R^3}{8} = \frac{1}{6} \pi R^3$$

The volume $V_{\text{total}}$ of the sphere with radius $R$ is given by:

$$V_{\text{total}} = \frac{4}{3} \pi R^3$$

The probability $P$ that a randomly chosen point inside the sphere is closer to the center than to the surface is the ratio of the volume of the inner sphere to the volume of the entire sphere:

$$P = \frac{V_{\text{inner}}}{V_{\text{total}}} = \frac{\frac{1}{6} \pi R^3}{\frac{4}{3} \pi R^3} = \frac{\frac{1}{6}}{\frac{4}{3}} = \frac{1}{6} \cdot \frac{3}{4} = \frac{1}{8}$$

Thus, the probability that a randomly chosen point inside the sphere is closer to the center than to its surface is $\frac{1}{8}$.
</details>

### Question 67 {: #q-67 .question .unit }

<span class="question__badge">Q67</span>

A point is randomly chosen inside a cube with side length $a$. What is the probability that the point is closer to one of the vertices than to the center of the cube?

<details class="solution" id="q-67-solution" markdown>
<summary>Solution</summary>

Solution not provided in the source material.
</details>

### Question 68 {: #q-68 .question .unit }

<span class="question__badge">Q68</span>

Imagine you have a number line that ranges from -1 to 1. You randomly pick k points on this line. What is the expected distance of the closest point to the midpoint of the line?

<details class="solution" id="q-68-solution" markdown>
<summary>Solution</summary>

Solution not provided in the source material.
</details>

<div class="project-card" id="project-5">
<span class="kicker">Project 05</span>

### The Dart Game

Imagine a scenario where someone hurls k darts randomly at a dartboard shaped like a unit circle, with its center at the origin. The challenge? To find out just how close they can get to the center. Your task is to investigate this intriguing problem and determine the minimum distance achieved after throwing k darts.

Mathematically analyze this result and write a short report on this analysis.

Also write a Python code to simulate 10,000 trials and print the value of the average minimum distance achieved, take $k=100$.
</div>
