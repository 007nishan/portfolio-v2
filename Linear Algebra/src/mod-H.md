<section class="opener" id="mod-H">
<span class="chapter-num">H</span>

# Module H — Closest Pair & Recursion
<span class="accent-rule"></span>
</section>

### Question 69 {: #q-69 .question .unit }

<span class="question__badge">Q69</span>

Plot and find the distance between points using Geogebra: $A(1,2)$, $B(2,3)$, and $C(5,9)$.

<details class="solution" id="q-69-solution" markdown>
<summary>Solution</summary>

Create points on the graph and find the distances between them using the distance tool from the toolbar.
</details>

### Question 70 {: #q-70 .question .unit }

<span class="question__badge">Q70</span>

Using Geogebra, which two points are the closest ones? What's the distance between them?

<details class="solution" id="q-70-solution" markdown>
<summary>Solution</summary>

The ones with the minimum distance between them will be the closest ones.

Find them and check the distance.
</details>

### Question 71 {: #q-71 .question .unit }

<span class="question__badge">Q71</span>

Add four more points: $D(0,-1)$, $E(4,11)$, $F(8,12)$, $G(-3,6)$ to your graph. What's the closest pair now?

<details class="solution" id="q-71-solution" markdown>
<summary>Solution</summary>

Follow the similar approach for finding the closest pairs.
</details>

### Question 72 {: #q-72 .question .unit }

<span class="question__badge">Q72</span>

Suppose we have 10 points. How many pairs of points do you have to consider for finding the closest pair?

<details class="solution" id="q-72-solution" markdown>
<summary>Solution</summary>

Similar to the previous question, the total combinations possible will be $10 * 9 / 2 = 45$.
</details>

### Question 73 {: #q-73 .question .unit }

<span class="question__badge">Q73</span>

What is the Y sorted order (by default assume ascending) of points $A$, $B$, $C$, $D$, $E$?

<details class="solution" id="q-73-solution" markdown>
<summary>Solution</summary>

For finding the Y - sorted order, we will consider only ordinate values of the coordinates mentioned.

$A = 2$, $B = 3$, $C = 9$, $D = -1$, $E = 11$

The ascending order of these values will be:

$$D < A < B < C < E$$
</details>

### Question 74 {: #q-74 .question .unit }

<span class="question__badge">Q74</span>

Plot a line $L$ parallel to the Y-axis passing through the middle point in the X sorted order of the above points. Divide the set of points into left and right regions around the line.

<details class="solution" id="q-74-solution" markdown>
<summary>Solution</summary>

X - Sorted Order = $G < D < A < B < E < C < F$

Middle Member = $B$

$$L : x = 2$$

Left Region = $D, A, G$

Right Region = $E, C, F$
</details>

### Question 75 {: #q-75 .question .unit }

<span class="question__badge">Q75</span>

Find the closest pair of points in the left region and right region. What's the minimum distance (say $d$) out of the two distances?

<details class="solution" id="q-75-solution" markdown>
<summary>Solution</summary>

Closest Pair in Left Region = $A$ & $D$

Closest Pair in Right Region = $C$ & $E$

Minimum Distance = $2.24$ units, corresponding to the points $C$ & $E$
</details>

### Question 76 {: #q-76 .question .unit }

<span class="question__badge">Q76</span>

Consider a band of width $2d$ around the Line $L$. Find the closest pair in this band. Compare this distance with $d$, the minimum value of the corresponding closest pair of our graph. Is the answer the same as the brute-force method you applied in question 71? (This divide and conquer method is known as the closest pair algorithm).

<details class="solution" id="q-76-solution" markdown>
<summary>Solution</summary>

This band limits the number of points but still the approach remains the same.

The closest pair is also the same as achieved in the question mentioned.
</details>

### Question 77 {: #q-77 .question .unit }

<span class="question__badge">Q77</span>

Astronomers have recorded the positions of stars in a 3D coordinate system where each star is represented as a point. Given the coordinates of stars $(1,2,3)$, $(4,5,6)$, $(6,7,8)$, $(10,11,12)$, find the closest pair of stars. (Use Geogebra). Is the closest pair algorithm valid here?

<details class="solution" id="q-77-solution" markdown>
<summary>Solution</summary>

The method for 3 - Dimensional points is similar to that of 2 - Dimensional points.
</details>

### Question 78 {: #q-78 .question .unit }

<span class="question__badge">Q78</span>

If $F(0) = 0$, $F(1) = 1$, $F(n) = F(n-1) + F(n-2)$ for $n \geq 2$, find the value of $F(5)$.

<details class="solution" id="q-78-solution" markdown>
<summary>Solution</summary>

$$F(5) = F(4) + F(3) = F(3) + F(2) + F(2) + F(1) = \ldots = 5(F(1)) = 5$$
</details>

### Question 79 {: #q-79 .question .unit }

<span class="question__badge">Q79</span>

Dry run and find the output of the following python code:

```python
def f(n):
    if n == 0:
        return 1
    return n * f(n-1)
print(f(5))
```

<details class="solution" id="q-79-solution" markdown>
<summary>Solution</summary>

$$F(5) = 5 * F(4) = \ldots = 5 * 4 * 3 * 2 * 1 * F(0) = 5 * 4 * 3 * 2 * 1 = 120$$
</details>

### Question 80 {: #q-80 .question .unit }

<span class="question__badge">Q80</span>

Does the closest pair algorithm assume that the $x$ coordinates (and $y$ coordinates) of the points are distinct? Is there a problem with the $O(n\log(n))$ performance if they are not distinct (do we have to handle this special case seprately in our algorithm)?

<details class="solution" id="q-80-solution" markdown>
<summary>Solution</summary>

Solution not provided in the source material.
</details>

### Question 81 {: #q-81 .question .unit }

<span class="question__badge">Q81</span>

Given a set of points where most points are far apart, but a few points are very close to each other, can you develop an algorithm more efficient from our original algorithm to find the closest pair in this special case.

<details class="solution" id="q-81-solution" markdown>
<summary>Solution</summary>

Solution not provided in the source material.
</details>
