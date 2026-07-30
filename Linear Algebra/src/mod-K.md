<section class="opener" id="mod-K">
<span class="chapter-num">K</span>

# Module K — PageRank & Random Walks
<span class="accent-rule"></span>
</section>

### Question 108 {: #q-108 .question .unit }

<span class="question__badge">Q108</span>

In a huge network of webpages, how does the browser decides which webpage should be appeared on top?

<details class="solution" id="q-108-solution" markdown>
<summary>Solution</summary>

The pages inside of a huge network of webpages are ranked on the basis of core concept of PageRank.

PageRank is based on the idea that the importance of a webpage can be determined by the number and quality of links to it. In essence, it treats links from other webpages as "votes" for the target page's importance. However, these votes are weighted by the importance of the pages they come from.
</details>

### Question 109 {: #q-109 .question .unit }

<span class="question__badge">Q109</span>

Read about the Algorithms Random Walk and Equal points Distribution and try to figure out how they are able to find the importance of the webpages?

<details class="solution" id="q-109-solution" markdown>
<summary>Solution</summary>

RANDOM WALK: Imagine a scenario where a person starts on a random web page and begins clicking on links randomly. Eventually, this random process will converge towards certain pages more frequently than others. Pages that are frequently visited during this random walk are considered more important because they are more likely to be stumbled upon by users.

EQUAL POINTS DISTRIBUTION: In this approach, each web page starts with an equal amount of importance points. As the algorithm iterates through the network of pages, it distributes points based on various factors like incoming links, outgoing links, and possibly other criteria like the relevance of content. Pages that are linked to by many other pages will accumulate more points, indicating their importance.
</details>

### Question 110 {: #q-110 .question .unit }

<span class="question__badge">Q110</span>

Are you able to visualize that the Equal points distribution method is nothing but a repetitive matrix operation on a vector?

<details class="solution" id="q-110-solution" markdown>
<summary>Solution</summary>

The iterative calculation of PageRank, can be visualized as a repetitive matrix operation on a vector. The web's link structure is represented by a transition matrix $M$, where each element $M_{ij}$ indicates the probability of moving from one page to the other.

Starting with an initial PageRank vector $P$, where each element corresponds to the PageRank of a page, the algorithm updates this vector through matrix multiplication. The PageRank vector $P$ is recalculated iteratively using the formula $P_{new} = M \cdot P_{old}$. In each iteration, the new PageRank vector is obtained by multiplying the transition matrix $M$ with the current PageRank vector $P$. This process continues until $P$ converges to a stable distribution. This repetitive multiplication demonstrates how the Equal Points Distribution method leverages matrix operations to determine the final PageRank values.
</details>

### Question 111 {: #q-111 .question .unit }

<span class="question__badge">Q111</span>

Will the points of the webpages calculated the Equal points distribution method converge? If yes how can you be sure about it?

<details class="solution" id="q-111-solution" markdown>
<summary>Solution</summary>

Solution not provided in the source material.
</details>

### Question 112 {: #q-112 .question .unit }

<span class="question__badge">Q112</span>

Is this convergence dependent on the initial vector?

<details class="solution" id="q-112-solution" markdown>
<summary>Solution</summary>

The initial vector $P$ can be any probability distribution, often starting with equal values or completely unbalanced values.

Because of the properties of the transition matrix $M$, the process $P_{new} = M \cdot P_{old}$ will converge to the same stationary distribution for any initial vector $P$.

The convergence of the PageRank values is guaranteed by the structure and properties of the transition matrix $M$ and is not dependent on the initial vector. Any starting vector will eventually lead to the same steady-state distribution.
</details>

### Question 113 {: #q-113 .question .unit }

<span class="question__badge">Q113</span>

If you have three websites, A, B, and C, and all are linked to each other, what happens to the importance of each website if:

- Website A is linked to by both B and C.
- B is linked to by A.
- C is linked to by A.

How does the number of links pointing to a website affect its perceived importance?

<details class="solution" id="q-113-solution" markdown>
<summary>Solution</summary>

The importance or perceived authority of a website is often measured by search engines through a metric called "PageRank," which considers the number and quality of links pointing to that website. In this scenario:

1. Website A: Since it is linked to by both B and C, it gains importance from both of them. Having multiple incoming links suggests that it might be more authoritative or relevant. Therefore, Website A would likely have higher perceived importance compared to the others.
2. Website B: It is linked to by A, which adds to its importance. However, it doesn't have any other external links in this scenario, so its perceived importance might be lower than Website A.
3. Website C: Similarly, it is linked to by A, which adds to its importance. However, like Website B, it doesn't have any other external links in this scenario, so its perceived importance might be lower than Website A.

The number of links pointing to a website does affect its perceived importance. Generally, more incoming links from reputable sources indicate higher authority and relevance in the eyes of search engines. However, the quality of those links also matters. A few high-quality links from authoritative websites can outweigh many low-quality links.
</details>

### Question 114 {: #q-114 .question .unit }

<span class="question__badge">Q114</span>

Given 4 buckets (A, B, C, and D):

- A passes its coins to B and C
- B passes its coins to D
- C passes its coins to A
- D passes its coins to B

If each bucket starts with 1 coin, calculate the number of coins in each bucket after first round and second round.

<details class="solution" id="q-114-solution" markdown>
<summary>Solution</summary>

After First Round:

A = 1; B = 1.5; C = 0.5; D = 1

After Second Round:

A = 0.5; B = 1.5; C = 0.5; D = 1.5
</details>

### Question 115 {: #q-115 .question .unit }

<span class="question__badge">Q115</span>

In both the algorithms (Random Walk and Equal Distributions) what problem would you face if we have some highly connected nodes? Would it affect the evaluation of other nodes?

<details class="solution" id="q-115-solution" markdown>
<summary>Solution</summary>

In both the Random Walk and Equal Distributions algorithms used for calculating PageRank, highly connected nodes can pose challenges and potentially affect the evaluation of other nodes. This issue primarily arises due to the potential for bias introduced by the presence of highly connected nodes, because of which random walkers may frequently get trapped in these nodes, leading to an uneven distribution of visits across the network.

Highly connected nodes tend to accumulate more random walkers, leading to inflated PageRank values for these nodes. Consequently, the importance of other nodes may be underestimated, as random walkers are less likely to visit them.
</details>

### Question 116 {: #q-116 .question .unit }

<span class="question__badge">Q116</span>

What modifications in the algorithm can you think to solve this problem?

<details class="solution" id="q-116-solution" markdown>
<summary>Solution</summary>

Solution not provided in the source material.
</details>

<div class="project-card" id="project-2">
<span class="kicker">Project 02</span>

### PageRank

An experiment is conducted in a class of approx. 150 students, in which students randomly interacted with each other and made a note of those people whom they found impressive. This data is given to you as a csv file. The first column stores the name of person A and the remaining columns store the names of those people who appeared impressive to person A.

Now using this data you have to find the top 10 most important persons in this network, using both the Random Walk and Equal Points Distribution algorithms.

Caution: Do take care of the 'Sinkholes'.

Dataset reference: Impression Network.
</div>

<div class="project-card" id="project-3">
<span class="kicker">Project 03</span>

### Recommender System

An experiment is conducted in a class of approx. 150 students, in which students randomly interacted with each other and made a note of those people whom they found impressive. This data is given to you as a csv file. The first column stores the name of person A and the remaining columns store the names of those people who appeared impressive to person A.

Now using this data you have to find the 'Missing Links' i.e. if there is no edge between two nodes (which implies that they haven't met each other) then you have to predict that if they would have met, then what kind of edge would be there (both liked each other, one liked the other, didn't like each other).

As in this project you have to make predictions, predictions can be made by various methods. So you are allowed to think out of the box and come up with a new method to make predictions and also write a short report to convince us about the accuracy of your method.

Dataset reference: Impression Data.
</div>

<div class="project-card" id="project-6">
<span class="kicker">Project 06</span>

### Water Droplet on a Plane

On GeoGebra, take a vector in the 3-D axis system starting from the origin and going to some random point. Plot the plane passing through that point and perpendicular to the vector. Suppose you drop a water droplet randomly somewhere on this plane. Plot the direction (as a vector) in which the droplet moves on the plane. This vector should accordingly vary as you vary the coordinates of the random point you took in the beginning, i.e., do everything in the parametric format.

Do not use Mathematics anywhere…
</div>
