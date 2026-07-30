<section class="opener" id="mod-J">
<span class="chapter-num">J</span>

# Module J — Binary Encoding & Prefix Codes
<span class="accent-rule"></span>
</section>

### Question 94 {: #q-94 .question .unit }

<span class="question__badge">Q94</span>

Write the number 25 in its binary form.

<details class="solution" id="q-94-solution" markdown>
<summary>Solution</summary>

$11001$
</details>

### Question 95 {: #q-95 .question .unit }

<span class="question__badge">Q95</span>

Given a text data, how will you convert it into binary form?

<details class="solution" id="q-95-solution" markdown>
<summary>Solution</summary>

We have to use some algorithm to efficiently find a transformation from text to binary for each character. Can you think of any such algorithm?
</details>

### Question 96 {: #q-96 .question .unit }

<span class="question__badge">Q96</span>

What if we use the binary code for each character according to the ASCII convention? How much space would each character take up?

<details class="solution" id="q-96-solution" markdown>
<summary>Solution</summary>

Let us discuss how ASCII algorithm works.

First, convert each character in the text into its corresponding ASCII value. ASCII (American Standard Code for Information Interchange) is a character encoding standard that represents text in computers.

Then, convert each ASCII value into its binary representation. This is typically done by converting the decimal value to binary.

But here, each character in ASCII convention takes up 8 bits of space. This is a fixed-width encoding scheme, where each character is represented using the same amount of space.
</details>

### Question 97 {: #q-97 .question .unit }

<span class="question__badge">Q97</span>

Suppose I take the following notation for the letters s, o, n, h and a:

- s: 00
- o: 001
- a: 010
- h: 011
- n: 1

Decode the following string: '00011010110011'

<details class="solution" id="q-97-solution" markdown>
<summary>Solution</summary>

The given string can be broken w.r.t. the codes given as:

(A) 00, 011, 010, 1, 1, 001, 1

(B) 00, 011, 010, 1, 1, 00, 1, 1

This led us to 2 different answers.
</details>

### Question 98 {: #q-98 .question .unit }

<span class="question__badge">Q98</span>

Do you observe that the above string can have 2 different interpretations?

<details class="solution" id="q-98-solution" markdown>
<summary>Solution</summary>

Continuing from the previous solution, we get two different interpretations:

(A) shannon

(B) shannsnn
</details>

### Question 99 {: #q-99 .question .unit }

<span class="question__badge">Q99</span>

Can this issue occur if we take each code of the same length? Can you define one such coding for the above example, i.e., s, o, n, h and a? At least how many digits would you have to take for each character?

<details class="solution" id="q-99-solution" markdown>
<summary>Solution</summary>

No, if we take each code of the sae length, there is no possiblity of two different interpretations of the string.

For the given example with the codes "s", "o", "n", "h", and "a", let's consider a simple substitution cipher where each letter is replaced by a numeric code. Since there are 5 distinct codes (s, o, n, h, a), we would need to represent each character using at least 3 digits to ensure that each code is uniquely identifiable.

Here's one possible encoding scheme:

- "s" is represented by "001"
- "o" is represented by "010"
- "n" is represented by "011"
- "h" is represented by "100"
- "a" is represented by "101"

With this encoding scheme, each character is represented by 3 digits, ensuring that there are no ambiguities in decoding.
</details>

### Question 100 {: #q-100 .question .unit }

<span class="question__badge">Q100</span>

Observe that for 5 unique letters, I cannot have unique binary representations if I take length of each notation exactly 2. Why?

<details class="solution" id="q-100-solution" markdown>
<summary>Solution</summary>

If we use 2 bits for each letter, we have a total of 5 unique letters: "a," "b," "c," "d," and "e."

With 2 bits, we can represent up to 4 different values (since $2^2=4$).

Therefore, we need at least 5 unique binary codes to represent all 5 letters uniquely.
</details>

### Question 101 {: #q-101 .question .unit }

<span class="question__badge">Q101</span>

Suppose you go to buy apples. There are three varieties of apples available. Your mom has given you a task that you have to buy 2 apples of any one type, 3 of the any other type, and 5 of the third. How will you minimise the total money spent?

<details class="solution" id="q-101-solution" markdown>
<summary>Solution</summary>

To minimize the total money spent, we should choose the cheapest option for the largest quantity required:

1. Buy 5 apples of one type:
    - Choose the cheapest type. Let's say it's type A.
2. Buy 3 apples of another type:
    - Choose the cheapest type again. Let's say it's type B.
3. Buy 2 apples of the third type:
    - This is the last remaining type, type C.

So, you would buy 5 apples of type A, 3 apples of type B, and 2 apples of type C to minimize the total money spent.
</details>

### Question 102 {: #q-102 .question .unit }

<span class="question__badge">Q102</span>

Given the text 'this is a new experience'. Write the frequency distribution of these characters for this sentence.

<details class="solution" id="q-102-solution" markdown>
<summary>Solution</summary>

Following is the frequency distribution of the characters in the text 'this is a new experience':

- t: 1
- h: 1
- i: 3
- s: 2
- (space): 4
- a: 1
- n: 2
- e: 4
- w: 1
- x: 1
- p: 1
- r: 1
- c: 1
</details>

### Question 103 {: #q-103 .question .unit }

<span class="question__badge">Q103</span>

To which characters should I give a shorter notation as compared to the others?

<details class="solution" id="q-103-solution" markdown>
<summary>Solution</summary>

The characters with the maximum frequency must be given shorter notations in order to minimize the space they take together.
</details>

### Question 104 {: #q-104 .question .unit }

<span class="question__badge">Q104</span>

Do you observe that the issue occurred in fifth question was because the code of 's' is a prefix of the code for 'o'?

<details class="solution" id="q-104-solution" markdown>
<summary>Solution</summary>

Certainly, due to the code of 's' being prefix of the code of 'o', there were two possiblilities, which did arise as the code of 's' was itself a part of the code of 'o' and 'o' can also be broken down into 's' and the rest of it.
</details>

### Question 105 {: #q-105 .question .unit }

<span class="question__badge">Q105</span>

What all do you think should be the properties of a proper encoding rule?

<details class="solution" id="q-105-solution" markdown>
<summary>Solution</summary>

In a proper encoding rule, there should not be any repitition of codes so that there is no confusion at all for the codes of various characters.

The encoding rule should be consistent, meaning the same input should always produce the same output.

The encoded data should be as compact as possible, reducing storage and transmission requirements. This is particularly important for large datasets or in bandwidth-constrained environments.

Also for sensitive data, the encoding should provide a level of security, ensuring that the encoded data is not easily interpretable by unauthorized parties. This may involve incorporating encryption techniques.
</details>

### Question 106 {: #q-106 .question .unit }

<span class="question__badge">Q106</span>

Get some quite basic knowledge about trees as data structures.

<details class="solution" id="q-106-solution" markdown>
<summary>Solution</summary>

Trees are hierarchical data structures composed of nodes connected by edges.

Trees consist of a root node, which is the topmost node in the hierarchy, and zero or more child nodes connected to it.

- Parent: A node that has child nodes connected to it. Every node in a tree, except the root, has exactly one parent.
- Leaf: A node with no children.
- Depth: The level of a node in the tree. The depth of the root node is 0, and the depth increases as you move away from the root.
- Height: The maximum depth of any node in the tree. It represents the longest path from the root node to a leaf node.
- Binary Tree: A special type of tree where each node has at most two children, known as the left child and the right child.
</details>

### Question 107 {: #q-107 .question .unit }

<span class="question__badge">Q107</span>

Observe that the lower is a node in a tree, the more is the time you would take to reach till it from the top node.

<details class="solution" id="q-107-solution" markdown>
<summary>Solution</summary>

This observation can be justified with the fact that the distance increases between the parent node and the root node as the root node keeps on going down further.

As the ditsnce increases, the ti e taken will also correspondingly increase.
</details>

<div class="project-card" id="project-4">
<span class="kicker">Project 04</span>

### Huffman Encoding

Form teams of 2. You will be given a text file containing long plain text (use any of the files given below), consisting of only alphabets, spaces, full stops, and commas. You need to encode the given text data so that the resultant binary string takes the least possible amount of space in terms of the length of the string. (Hint: Use the Huffman Encoding Algorithm discussed in the class).

You may gamify it as: one person will write a Python code to encode a text string (given sample texts), give the binary string as well as the encoding tree/table to the other person, who will write another Python code to decode the binary string using that table, and verify the resultant text with the original text (which is with the first person). You may decide your roles yourself and can even do the activity both ways, by using both of the samples given below.

Sample texts: Sample 1, Sample 2.
</div>
