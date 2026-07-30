<section class="opener" id="projects">
<span class="chapter-num">P</span>

# Projects
<span class="accent-rule"></span>
</section>

This appendix collects all eight linked projects of the Oceanverse Linear Algebra curriculum in one place. Each project is also embedded inline in the module where it is chronologically introduced.

<div class="project-card" id="project-1-index">
<span class="kicker">Project 01</span>

### Vigenère Cipher

**Implement the breaking of the Vigenère Cipher.**

You should read the first 2 chapters of *The Code Book* and upload a two page report (not compulsory to upload the report). You cannot execute the following code without reading this book. The book is fun to read.

1. Import `string` and understand the different functions.
2. After assigning `s='rupnagar'`, understand what `s.find` and `s.replace` do. Also try looking at other functions and have a working knowledge of a few functions that make sense to you.
3. Understand how one can read a text file from your hard disk and store it as a string. The following two lines open a file and assign its content to the string `s`:

    ```python
    f = open('filename')
    s = f.read()
    ```

4. Understand the idea of *dictionaries* in Python. They are similar to lists but very powerful structures.
5. You are given the file `english_random`. You can consider any other big text file with english words, preferably a story book. Learn about the Vigenère Cipher. Encode the text using it.
6. Write a code which takes the encrypted string as input and returns the decrypted string as well as the password. Download this Python file and fill in the functions one by one.
</div>

<div class="project-card" id="project-2-index">
<span class="kicker">Project 02</span>

### PageRank

An experiment is conducted in a class of approx. 150 students, in which students randomly interacted with each other and made a note of those people whom they found impressive. This data is given to you as a csv file. The first column stores the name of person A and the remaining columns store the names of those people who appeared impressive to person A.

Now using this data you have to find the top 10 most important persons in this network, using both the Random Walk and Equal Points Distribution algorithms.

Caution: Do take care of the 'Sinkholes'.

Dataset reference: Impression Network.
</div>

<div class="project-card" id="project-3-index">
<span class="kicker">Project 03</span>

### Recommender System

An experiment is conducted in a class of approx. 150 students, in which students randomly interacted with each other and made a note of those people whom they found impressive. This data is given to you as a csv file. The first column stores the name of person A and the remaining columns store the names of those people who appeared impressive to person A.

Now using this data you have to find the 'Missing Links' i.e. if there is no edge between two nodes (which implies that they haven't met each other) then you have to predict that if they would have met, then what kind of edge would be there (both liked each other, one liked the other, didn't like each other).

As in this project you have to make predictions, predictions can be made by various methods. So you are allowed to think out of the box and come up with a new method to make predictions and also write a short report to convince us about the accuracy of your method.

Dataset reference: Impression Data.
</div>

<div class="project-card" id="project-4-index">
<span class="kicker">Project 04</span>

### Huffman Encoding

Form teams of 2. You will be given a text file containing long plain text (use any of the files given below), consisting of only alphabets, spaces, full stops, and commas. You need to encode the given text data so that the resultant binary string takes the least possible amount of space in terms of the length of the string. (Hint: Use the Huffman Encoding Algorithm discussed in the class).

You may gamify it as: one person will write a Python code to encode a text string (given sample texts), give the binary string as well as the encoding tree/table to the other person, who will write another Python code to decode the binary string using that table, and verify the resultant text with the original text (which is with the first person). You may decide your roles yourself and can even do the activity both ways, by using both of the samples given below.

Sample texts: Sample 1, Sample 2.
</div>

<div class="project-card" id="project-5-index">
<span class="kicker">Project 05</span>

### The Dart Game

Imagine a scenario where someone hurls k darts randomly at a dartboard shaped like a unit circle, with its center at the origin. The challenge? To find out just how close they can get to the center. Your task is to investigate this intriguing problem and determine the minimum distance achieved after throwing k darts.

Mathematically analyze this result and write a short report on this analysis.

Also write a Python code to simulate 10,000 trials and print the value of the average minimum distance achieved, take $k=100$.
</div>

<div class="project-card" id="project-6-index">
<span class="kicker">Project 06</span>

### Water Droplet on a Plane

On GeoGebra, take a vector in the 3-D axis system starting from the origin and going to some random point. Plot the plane passing through that point and perpendicular to the vector. Suppose you drop a water droplet randomly somewhere on this plane. Plot the direction (as a vector) in which the droplet moves on the plane. This vector should accordingly vary as you vary the coordinates of the random point you took in the beginning, i.e., do everything in the parametric format.

Do not use Mathematics anywhere…
</div>

<div class="project-card" id="project-7-index">
<span class="kicker">Project 07</span>

### Data Compression 1

You are given the marks of students all over India in 10 tests conducted nationwide (these tests are taken by the same set of students each time). Organizing each test costs the institution a lot. You, as a Data Analyst, have been given the task to figure out if we can drop a particular number of tests, so that the institution can save money, at the same time not losing any information about the merit of a student.

Following is the data of the marks of the tests conducted last year. You need to tell the institution how many tests are going in vain, so that it can remove those many tests this year; however, it is not your task to find which tests we can safely drop but solutions are welcome.

Dataset reference: Marks Data.
</div>

<div class="project-card" id="project-8-index">
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
