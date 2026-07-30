<section class="opener" id="mod-N">
<span class="chapter-num">N</span>

# Module N — Convolution, CNNs & Gradient Descent
<span class="accent-rule"></span>
</section>

### Question 137 {: #q-137 .question .unit }

<span class="question__badge">Q137</span>

What do you understand by convolution? Suppose we have two sets $A$ and $B$: $A = \{1, 2, 3, 4\}$, $B = \{5, 6, 7, 8\}$. What is $A \ast B$? And what about $B \ast A$? Are they the same?

<details class="solution" id="q-137-solution" markdown>
<summary>Solution</summary>

Solution not provided in the source material.
</details>

### Question 138 {: #q-138 .question .unit }

<span class="question__badge">Q138</span>

How do you convolve two matrices? Let two matrices be A and B. $A=\begin{pmatrix} 3 & 1 & -1 \\ 1 & 2 & 0 \\ 1 & 1 & 8 \end{pmatrix}$ and $B = \begin{pmatrix} 1 & 0 & -1 \\ 4 & -2 & 0 \\ 6 & 5 & 1 \end{pmatrix}$ then what is $A \ast B$?

<details class="solution" id="q-138-solution" markdown>
<summary>Solution</summary>

Solution not provided in the source material.
</details>

### Question 139 {: #q-139 .question .unit }

<span class="question__badge">Q139</span>

What is the purpose of using filters on images?

<details class="solution" id="q-139-solution" markdown>
<summary>Solution</summary>

Solution not provided in the source material.
</details>

### Question 140 {: #q-140 .question .unit }

<span class="question__badge">Q140</span>

a) How will you create a filter for horizontal edge detection?

b) How will you create a filter for diagonal edge detection?

c) What kind of values you need in a filter used for blurring an image?

<details class="solution" id="q-140-solution" markdown>
<summary>Solution</summary>

Solution not provided in the source material.
</details>

### Question 141 {: #q-141 .question .unit }

<span class="question__badge">Q141</span>

Apply the following filter F on an image M and observe the dimensions of the output. Are the same as previous?

<details class="solution" id="q-141-solution" markdown>
<summary>Solution</summary>

Solution not provided in the source material.
</details>

### Question 142 {: #q-142 .question .unit }

<span class="question__badge">Q142</span>

Given a $32 \times 32 \times 32$ RGB image, calculate the output dimensions after applying a convolutional layer with 16 filters, each of size $3 \times 3$, with a stride of 1 and with no padding. Also find the general formula.

<details class="solution" id="q-142-solution" markdown>
<summary>Solution</summary>

Solution not provided in the source material.
</details>

### Question 143 {: #q-143 .question .unit }

<span class="question__badge">Q143</span>

What is purpose of applying a pooling layer on an image. How is it different from convolution layer?

<details class="solution" id="q-143-solution" markdown>
<summary>Solution</summary>

Solution not provided in the source material.
</details>

### Question 144 {: #q-144 .question .unit }

<span class="question__badge">Q144</span>

a) Apply $2 \ast 2$ Max pooling on the following image.

b) Apply $2 \ast 2$ avg pooling on the following image.

c) What are the dimensions of the image after pooling? Does pooling change the depth of the image?

d) Why don't we use Min pooling?

<details class="solution" id="q-144-solution" markdown>
<summary>Solution</summary>

Solution not provided in the source material.
</details>

### Question 145 {: #q-145 .question .unit }

<span class="question__badge">Q145</span>

Given the following predicted probabilities and true labels, calculate the binary cross-entropy loss:

$$\text{Predicted probabilities} = [0.7, 0.2, 0.1]$$

$$\text{True labels} = [1, 0, 0]$$

<details class="solution" id="q-145-solution" markdown>
<summary>Solution</summary>

Solution not provided in the source material.
</details>

### Question 146 {: #q-146 .question .unit }

<span class="question__badge">Q146</span>

When will this cross entropy loss be minimum?

<details class="solution" id="q-146-solution" markdown>
<summary>Solution</summary>

Solution not provided in the source material.
</details>

### Question 147 {: #q-147 .question .unit }

<span class="question__badge">Q147</span>

For a weight W with a gradient $\frac{\partial L}{\partial W} = 0.01$, a learning rate $\alpha=0.1$, and an initial weight $W_{o} = 0.5$, compute the updated weight using gradient descent.

<details class="solution" id="q-147-solution" markdown>
<summary>Solution</summary>

Solution not provided in the source material.
</details>

### Question 148 {: #q-148 .question .unit }

<span class="question__badge">Q148</span>

a) Differentiate $\frac{1}{1 + e^{-x}}$ with respect to $x$.

b) Differentiate $-\log(2x^2)$ with respect to $x$.

c) Differentiate $\frac{e^i}{\sum e^k}$ with respect to $i$ and $j$.

<details class="solution" id="q-148-solution" markdown>
<summary>Solution</summary>

Solution not provided in the source material.
</details>

### Question 149 {: #q-149 .question .unit }

<span class="question__badge">Q149</span>

Given is a single neuron (shown below), let the loss L be $(\hat{z} - z)^2$, find $\frac{\partial L}{\partial w_{11}}$ and $\frac{\partial L}{\partial p_{2}}$.

```figure
alt: A single-neuron network showing inputs, weights w11, the neuron, and output z-hat used for the loss derivative
books/linear-algebra/figures/neuron-0.jpg
A single neuron: inputs and weights feeding the output used to compute the loss.
```

<details class="solution" id="q-149-solution" markdown>
<summary>Solution</summary>

Solution not provided in the source material.
</details>

### Question 150 {: #q-150 .question .unit }

<span class="question__badge">Q150</span>

Given is another simple neural network (shown below). What is the relation of each layer of the above neural network with the previous layer. Explicitly write relation of each layer's neurons with previous layers.

```figure
alt: A small multi-layer neural network showing neurons connected across successive layers
books/linear-algebra/figures/neuron-1.jpg
A simple multi-layer neural network; each layer's neurons connect to those of the previous layer.
```

<details class="solution" id="q-150-solution" markdown>
<summary>Solution</summary>

Solution not provided in the source material.
</details>

### Question 151 {: #q-151 .question .unit }

<span class="question__badge">Q151</span>

How will you deal with the backpropagation through the max pool layer in CNN?

<details class="solution" id="q-151-solution" markdown>
<summary>Solution</summary>

Solution not provided in the source material.
</details>
