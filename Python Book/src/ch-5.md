<section class="opener" id="ch-5">
<span class="chapter-num">5</span>

# Lists and Tuples
<span class="accent-rule"></span>
</section>

## Lesson 5.1 — Lists: Introduction, Iterating, Growing, Operations {: #ch-5-lesson-1 }

### Introduction

A list in Python is a data structure used to store a sequence of objects. Some examples:

```python
numbers = [1, 2, 3, 4, 5]
letters = ['a', 'b', 'c', 'd']
words = ['this', 'is', 'a', 'list']
```

Lists can be printed like other types. `print(numbers)` gives this output:

```output
[1, 2, 3, 4, 5]
```

Lists may hold objects of different data types:

```python
mixture = [1, 1.0, '1', True]
```

Lists have their own data type — `list` — and you can check whether a variable holds one:

```python
numbers = [1, 2, 3]
print(type(numbers))
print(isinstance(numbers, list))
```

The `len` function counts the elements:

```python
numbers = [1, 2, 3]
print(f'This list has {len(numbers)} elements in it')
```

Lists support indexing and slicing, which behave just as they did for strings:

```python
numbers = [1, 2, 3, 4]
print(numbers[0], numbers[1], numbers[2], numbers[3])
print(numbers[1 : 3])
print(numbers[-2])
```

### Iterating through lists

Since a list is a sequence, you can loop through it with `for` — one of the main uses of the `for` loop:

```python
# Method-1
numbers = [1, 2, 3, 4]
for num in numbers:
    print(num)
```

Here the loop variable `num` picks one item at a time; the body simply prints it. The same result can be achieved with a `while` loop:

```python
# Method-2
numbers = [1, 2, 3, 4]
index = 0
while index < len(numbers):
    print(numbers[index])
    index += 1
```

You can also iterate over the indices using `range`:

```python
# Method-3
numbers = [1, 2, 3, 4]
for index in range(len(numbers)):
    print(numbers[index])
```

Since `len(numbers)` equals `4`, the range sequence is `0, 1, 2, 3`, and `index` iterates through it. Methods 2 and 3 are alike — both walk through the indices and use indexing to reach each element — the difference being `while` versus `for`. Method-1 differs by pulling elements directly from the sequence.

### Growing a list

Lists are commonly used to gather a collection of items, often starting from an empty list. Python offers two ways to make one:

```python
list1 = []
list2 = list()
```

Both are empty. The interpreter ignores spaces between the braces, so `list1 = [ ]` works too. To add items, there are two approaches:

```python
list1 = list1 + [1]
print(list1)
list2 = list2.append(1)
print(list2)
```

Both lists end up with one element. The first approach is **list concatenation** — joining two lists together, much like coupling two train compartments, and similar to string concatenation. The second uses the `append` method (a function defined for the `list` type), which adds elements at the end.

Consider this problem:

> Generate the list of positive integers less than 100 that are divisible by 3.

At least two solutions exist. First, with `while`:

```python
# Method-1
num = 3
nums_div = []
while num < 100:
    nums_div.append(num)
    num += 3
```

And with `for`:

```python
# Method-2
nums_div = []
for num in range(3, 100, 3):
    nums_div.append(num)
```

### Operations on Lists

We have seen the `+` operator with lists:

```python
list1 = [1, 2, 3]
list2 = [4, 5, 6]
list12 = list1 + list2
print(list12)
list21 = list2 + list1
print(list21)
```

```output
[1, 2, 3, 4, 5, 6]
[4, 5, 6, 1, 2, 3]
```

Order matters during concatenation. Next, the `*` operator:

```python
list1 = [0] * 5
print(list1)
list2 = [1, 2, 3] * 3
print(list2)
```

```output
[0, 0, 0, 0, 0]
[1, 2, 3, 1, 2, 3, 1, 2, 3]
```

Two lists are equal when they hold the same sequence of elements:

```python
l1 = [1, 2, 3]
l2 = [1, 2, 3]
l3 = [3, 2, 1]
print(l1 == l2)
print(l2 == l3)
```

```output
True
False
```

Lists can also be compared with `>` or `<`, using lexicographic ordering — much like string comparison, which was covered in the first chapter.

!!! note "Lexicographic ordering"

    First element from both lists are compared. If they differ this determines the outcome of the comparison. If they are equal, then the second element of both the lists are compared. This process continues until either list is exhausted.

Some example comparisons:

```python
print([1, 2] < [2, 1])
print([1] < [1, 2, 3])
print([2, 3, 4] < [3])
print([] < [1])
```

All four give `True`.

### Useful Functions

Some built-in functions that work on lists:

`sum` adds up the elements of a list of numbers:

```python
a = [1, 2, 3]
print(sum(a))
```

`max` and `min` find the maximum and minimum values respectively:

```python
a = [1, 2, 3]
print(min(a), max(a))
```

What happens if `a` is a list of strings? What would `max(a)` and `min(a)` produce?

`sorted` returns a sorted list:

```python
a = [2, 1, 3]
print(sorted(a))
```

We have met the `range` object and seen its usefulness for iterating over a sequence, so far tied to the `for` loop. Now it steps outside that role:

```python
numbers = range(10)
print(numbers)
```

This outputs `range(0, 10)` — a sequence you can iterate over. Python lets you turn it into a list:

```python
numbers = list(range(10))
print(numbers)
```

This gives `[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]`.

## Lesson 5.2 — Lists: Mutability and Call by Reference {: #ch-5-lesson-2 }

### Mutability

Consider a scenario: you work at a company analyzing cricket matches, and a colleague recording IPL runs has a broken "0" key. He uses the letter "O" instead, and you must write a program to replace every "O" with the number 0.

```python
runs = [1, 4, 2, 'O', 4, 'O'] # the data for one over is given here
print(runs)
for i in range(len(runs)):
    if runs[i] == 'O':
        runs[i] = 0
print(runs)
```

The key line is `runs[i] = 0`. This updates a list "in-place," which Python allows because lists are mutable — unlike strings, which are immutable. But "reckless exercise of power always results in instability," shown by this example:

```python
list1 = [1, 2, 3]
list2 = list1
list2[0] = 100
print(list1)
print(list2)
```

Both produce identical results even though only `list2` was modified:

```output
[100, 2, 3]
[100, 2, 3]
```

To understand this, consider the built-in `id` function. Every Python object has a unique identity, and `id(x)` returns it. The docs describe it as "guaranteed to be unique among simultaneously existing objects." In this implementation, the id is the object's memory address.

The assignment `list2 = list1` does not create a new object but instead creates another name (an alias) for the same object — comparable to a nickname. To check whether two names point to the same object, use the `is` keyword:

```python
list1 = [1, 2, 3]
list2 = list1
list2[0] = 100
print(list1 is list2)
```

This prints `True`. Another scenario:

```python
list1 = [1, 2, 3]
list2 = [1, 2, 3]
print(list1 == list2)
print(list1 is list2)
```

```output
True
False
```

Equality and identity differ: the first line checks equality, the second checks identity. Here the two lists point to different objects (different identities) but hold the same sequence, so they are equal.

To create a genuine copy so that updating one does not affect the other, Python offers three ways:

```python
list1 = [1, 2,  3]
list2 = list(list1)
list3 = list1[:]
list4 = list1.copy()

list2[0] = 100
list3[0] = 200
list4[0] = 300

print(list1, list2, list3, list4)
print(list1 is not list2, list1 is not list3, list1 is not list4)
```

```output
[1, 2, 3] [100, 2, 3] [200, 2, 3] [300, 2, 3]
True True True
```

Explanations:

- **`list(list1)`:** passing `list1` to the `list` function returns a new list with the same elements.
- **`list1[:]`:** slicing the list produces a new list object; with no `start` or `stop`, they default to `0` and `len(list1)`, so the whole list is returned as a brand new object.
- **`list1.copy()`:** the `copy` method defined for list objects is used.

The last two lines confirm all three copying methods work.

### Call by reference

Mutability affects how lists behave in functions. Two snippets are compared:

```python
# Snippet-1
def foo():
    L.append(1)

L = [0]
print(f'L before: {L}')
foo()
print(f'L after: {L}')
```

Snippet-1 has no parameters. Since `L` is never assigned a new value inside `foo`, its scope stays global.

```python
# Snippet-2
def foo(L_foo):
    L_foo.append(1)
    print(L is L_foo)

L = [0]
print(f'L before: {L}')
foo(L)
print(f'L after: {L}')
```

Here `L_foo` is a parameter with local scope, yet modifying it changes `L` outside the function because both point to the same object. The function call resembles an assignment `L_foo = L`, making `L_foo` another name bound to the same object. This is termed **call by reference**: whenever a mutable variable is passed to a function, references to the object are passed.

The takeaway: modifying mutable objects inside a function produces side effects outside it. To avoid these, create a new list object:

```python
def foo(L_foo):
    L_foo.append(1)
    print(L is L_foo)

L = [0]
print(f'L before: {L}')
foo(list(L))
print(f'L after: {L}')
```

Now `foo` produces no side effects. The call could instead use `foo(L[:])` or `foo(L.copy())`.

## Lesson 5.3 — Lists: Simulating an IPL Innings {: #ch-5-lesson-3 }

### Simulating an IPL Innings

This lesson revisits the challenge of recording runs scored on every ball of an IPL match. A T20 innings has 20 overs of 6 balls each. Assuming all deliveries are fair with no extras, that leaves exactly 120 numbers to record, each between 0 and 6. A list is a good way to store this data for further processing.

To simulate an innings, the `random` library is used:

```python
import random
runs = random.choices([0, 1, 2, 3, 4, 5, 6], k = 120)
print(type(runs))
print(len(runs))
```

The `choices` function samples uniformly (with replacement) from the seven input numbers. In summary, it:

- Picks a number at random from `[0, 1, 2, 3, 4, 5, 6]`, each equally likely.
- Copies it to the output list, leaving the original list undisturbed.
- Repeats this process 120 times.

To verify the counts are roughly equal:

```python
for run in [0, 1, 2, 3, 4, 5, 6]:
    print('{} appears {} times'.format(run, runs.count(run)))
```

Here, `runs.count(run)` returns how many times `run` appears in the list; `count` is a list method.

```output
0 appears 19 times
1 appears 20 times
2 appears 19 times
3 appears 16 times
4 appears 18 times
5 appears 11 times
6 appears 17 times
```

The counts are close, but not realistic: 5 runs are rarely seen in cricket, and 0, 1, 2 are far more common than 3, 4, 6. Preferences can be expressed using a `weights` keyword argument:

```python
import random
# choices is distributed over multiple lines
# this is done to improve readability
runs = random.choices([0, 1, 2, 3, 4, 5, 6], 
                      weights = [30, 30, 20, 5, 10, 0, 5], 
                      k = 120)
for run in [0, 1, 2, 3, 4, 5, 6]:
    print('{} appears {} times'.format(run, runs.count(run)))
print(f'Total number of runs scored = {sum(runs)}')
```

```output
0 appears 32 times
1 appears 34 times
2 appears 32 times
3 appears 7 times
4 appears 12 times
5 appears 0 times
6 appears 3 times
Total number of runs scored = 185
```

Here `sum(runs)` (a built-in function) totals the list elements. The `weights` argument can be understood with this table:

| Run | Weight |
|-----|--------|
| 0 | 30 |
| 1 | 30 |
| 2 | 20 |
| 3 | 5 |
| 4 | 10 |
| 5 | 0 |
| 6 | 5 |
| Total | 100 |

The weight reflects the importance given to a run. From the table, 0 and 1 each occur 30% of the time, 6 occurs 5% of the time, and so on. The `choices` function respects this distribution while selecting items.

To find when the first six was scored:

```python
first_six_ball = runs.index(6) + 1
print(first_six_ball)
```

The `index` method takes an element and returns its first occurrence in the list. Since the ball number is one more than the index, `1` is added. What if the input is not present in the list?

```python
first_five_ball = runs.index(5)
print(first_five_ball)
```

Since `5` never occurs, this raises a `ValueError` with the message `5 is not in list`. Care is needed when using `index`. The same task could be done differently:

```python
for ball, run in enumerate(runs):
    if run == 6:
        print(f'The first six was hit at ball number {ball + 1}')
        break
```

The `enumerate` object is useful for accessing both an element and its index while iterating. It yields pairs of `(index, list[index])`, effectively giving two loop variables — the index and the element.

To find how many balls it took to score the last 50 runs, reversing the list makes iteration easier:

```python
balls = 0
last_runs = 0
for run in reversed(runs):
    last_runs += run
    balls += 1
    if last_runs >= 50:
        print(f'It took {balls} balls to score the last 50 runs.')
        break
```

The `reversed` object lets you iterate in reverse order without changing the original list. Finally, to check whether the batsmen ran three runs at any point (regardless of when):

```python
three_existence = 3 in runs
print(three_existence)
```

Just as the `in` keyword was earlier used to check for one string inside another, here it checks list membership. This prints `True` if 3 is an element in `runs` and `False` otherwise.

## Lesson 5.4 — List Methods; Stack and Queue; split and join {: #ch-5-lesson-4 }

### List Methods

#### `insert`

So far we have covered list methods such as `append`, `count`, and `index`. There are additional useful methods to explore. The `insert` method places an element at a specified position in a list:

```python
L = [1, 1, 2, 3, 8]
L.insert(4, 5)
print(L)
```

The signature `list.insert(index, object)` puts `object` before `index` in the list. Here, `5` is inserted before index `4`. A few more examples:

```python
L = [10, 20, 30]
L.insert(0, 5)          # L becomes [5, 10, 20, 30]
L.insert(2, 15)         # L becomes [5, 10, 15, 20, 30]
L.insert(4, 25)         # L becomes [5, 10, 15, 20, 25, 30]
L.insert(len(L), 35)    # L becomes [5, 10, 15, 20, 25, 30, 35]
L.insert(20, 40)        # L becomes [5, 10, 15, 20, 25, 30, 35, 40]
```

When the index exceeds the list's length, the element is appended to the end. `insert` shines when adding to the front of a list, whereas `append` handles additions at the end.

#### `pop`

Consider this code:

```python
L = ['a', 'b', 'c', 'd', 'e', 'f']
index = 1
x = L.pop(index)
print(f'The element {x} at index {index} was removed from the list')
print(f'The current list is {L}')
```

`L.pop(index)` deletes and returns the element at `index`. When no argument is given, `index` defaults to -1, making it a default argument for `pop`. A value of -1 removes the last element:

```python
L = ['a', 'b', 'c', 'd', 'e', 'f']
x = L.pop()
print(f'The current list is {L}')
```

What happens if you supply an index that is out of range?

#### `reverse`

You can reverse a list in-place:

```python
L = [1, 2, 3, 4, 5]
print('Before:', L, id(L))
L.reverse()
print('After:', L, id(L))
```

It is "in-place" because the list keeps the same `id` before and after — it is the same object. Care is needed with in-place operations. A frequent mistake looks like:

```python
L = [1, 2, 3, 4, 5]
L = L.reverse()
print(L)
```

This prints `None`, since `reverse` returns nothing. If you want both the original and its reversed version, do this:

```python
L = [1, 2, 3, 4, 5]
L_reversed = L.copy()
L_reversed.reverse()
print('Original list:', L)
print('Reversed list:', L_reversed)
```

Why was the copy needed?

#### `sort`

Another handy in-place method is `sort`:

```python
L = [2, 1, 5, 6, 4, 3]
print('Before', L)
L.sort()
print('After', L)
```

Although the call looks simple, sorting is a non-trivial algorithm. Sorting algorithms will be covered in the next course on data structures and algorithms.

#### `remove`

Now for some destructive functions:

```python
L = [1, 2, 3, 4, 5] * 2
print('Before', L)
L.remove(1)
print('After', L)
```

`L.remove(x)` deletes the leftmost occurrence of `x`. Attempting to remove a missing element raises a `ValueError` reading `list.remove(x): x not in list`. A safe removal approach:

```python
# x is the item to be removed; L is the list
if x in L:
    L.remove(x)
```

How does `remove` differ from `pop`?

### Stack

Combining a list with `append` and `pop` mimics a data structure called a **stack**, where the last item added is the first removed — like a pile of books, where the topmost (most recent) book comes off first. The mnemonic is LIFO: Last In First Out.

```python
# Start with an empty stack
stack = [ ]
# Append items to end of the stack; also called a push operation
stack.append('Harry Potter and the Philosopher\'s Stone')
stack.append('Harry Potter and the Chamber of Secrets')
# State of the stack 
print(stack)
# Remove items from the end of the stack; also called a pop operation
stack.pop()
# State of the stack
print(stack)
```

### Queue

A list paired with `insert` and `pop` simulates a **queue**, where the first item added is the first removed — like a real-life line at a billing counter, where the first person served is the first to leave. The mnemonic is FIFO: First In First Out.

```python
# Start with an empty queue
queue = [ ]
# Insert elements at the beginning of the queue
queue.insert(0, 'Customer-1')
queue.insert(0, 'Customer-2')
# State of the queue
print(queue)
# Remove items from the queue
queue.pop()
# State of the queue
print(queue)
```

### Strings and Lists

#### `split`

Lists come up often when processing strings. Consider this problem:

> Accept a sentence as input and find the number of words in it. Assume that it is a simple sentence with a single space separating consecutive words. There are no other punctuation marks in the sentence.

First, a solution without lists:

```python
sentence = 'this sentence is false' # a simple sentence
count = 1
for char in sentence:
    if char == ' ':
        count += 1
print(count)
```

We scanned character by character, counting spaces; the word count is one more than the number of spaces. As an aside, this sentence is a paradoxical statement — it cannot be true or false, since assuming either leads to the other. Now the list-based approach:

```python
sentence = 'this sentence is false' # a simple sentence
words = sentence.split(' ')         # space is the delimiter used
count = len(words)
print(count)
```

`split` is a string method that divides a string along a delimiter — one or more characters marking where to split. It returns a list of the split substrings. Printing `words` gives:

```output
['this', 'sentence', 'is', 'false']
```

Another example:

```python
comma_words = 'one,two,three,four'
numbers = comma_words.split(',')
print(numbers)
```

```output
['one', 'two', 'three', 'four']
```

Here `','` is the delimiter. Delimiters are not limited to single characters — they can be any string:

```python
some_string = 'allISwell'
words = some_string.split('IS')
print(words)
```

```output
['all', 'well']
```

#### `join`

Just as we went from a string to a list, we can go from a list of strings back to a string. Consider:

> Accept a sequence of words as input and construct a sentence out of it.

A solution without lists:

```python
words = ['this', 'sentence', 'is', 'false']
sentence = ''
for word in words:
    sentence += word + ' '
print(sentence)
```

This looks correct but is off by one character. Print the last character:

```python
print(sentence[-1])
```

Instead of `e`, it is a space — an extra trailing space. This seems trivial, but programming demands precision. A better version:

```python
words = ['this', 'sentence', 'is', 'false']
sentence = words[0]
for word in words[1 : ]:
    sentence += ' ' + word
print(sentence)
```

This is more accurate but clumsy, iterating from the second word. The cleanest solution uses a simple, sophisticated method:

```python
words = ['this', 'sentence', 'is', 'false']
sentence = ' '.join(words)
print(sentence)
```

"Isn't that a thing of beauty!" Where `split` chops a string along a delimiter, `join` stitches list strings together using a chosen "thread" — a space here. We could use another string, like a comma:

```python
words = ['one', 'two', 'three']
sentence = ','.join(words)
print(sentence)
```

```output
one,two,three
```

That stitching is too tight — let's add some space:

```python
words = ['one', 'two', 'three']
sentence = ', '.join(words)
print(sentence)
```

Note the space after the comma.

```output
one, two, three
```

## Lesson 5.5 — Nested Lists, Matrices, Shallow and Deep Copy {: #ch-5-lesson-5 }

### Nested Lists

This lesson revisits the `runs` list created earlier using the `random` library:

```python
import random
runs = random.choices([0, 1, 2, 3, 4, 5, 6],
                      weights = [30, 30, 20, 5, 10, 0, 5],
                      k = 120)
assert len(runs) == 120
```

An `assert` statement lets you check whether part of your code behaves as expected. Here, it verifies the list length is `120`, which matters because later computations rely on it. When the expression after `assert` evaluates to `True`, execution moves to the next line; if it is `False`, an `AssertionError` is raised.

Here is an alternate way to organize the same information:

```python
overs = list()
new_over = list()
for ball, run in enumerate(runs):
    new_over.append(run)
    if (ball + 1) % 6 == 0:
        overs.append(new_over)
        new_over = list()
```

`overs` is a nested list — a list of lists. Each entry in `overs` stands for an over in the match, holding the runs from that over. The following snippet checks that the outer and inner lists have sizes 20 and 6:

```python
assert len(overs) == 20
for over in overs:
    assert len(over) == 6
```

To find the runs on the fourth ball of the third over:

```python
answer = overs[2][3]    # zero-indexing
print(answer)
```

The first index refers to the outer list, the second to the inner list. To make this clearer, try:

```python
third_over = overs[2]
print(third_over)
fourth_ball = third_over[3]
print(fourth_ball)
assert fourth_ball == overs[2][3]
```

### Matrices

Matrices are 2D objects that can be represented as nested lists. First, build a 3 × 3 matrix filled with zeros:

```python
mat = [ ]
for i in range(3):
    mat.append([ ])     # we are appending an empty list
    for _ in range(3):
        mat[i].append(0)
print(mat)
```

```output
[[0, 0, 0], [0, 0, 0], [0, 0, 0]]
```

Notice the inner loop variable `_`. Since it is never actually used, the convention is to name such placeholder variables `_`, existing only to satisfy the language's syntax. Now build another matrix:

```python
mat = [ ]
num = 1
for i in range(3):
    mat.append([ ])
    for _ in range(3):
        mat[i].append(num)
        num += 1
print(mat)
```

```output
[[1, 2, 3], [4, 5, 6], [7, 8, 9]]
```

The same matrix can also be constructed like this:

```python
mat = [ ]
num = 1
for _ in range(3):
    row = [ ]
    for _ in range(3):
        row.append(num)
        num += 1
    mat.append(row)
print(mat)
```

### Shallow and Deep Copy

Look at this code:

```python
mat1 = [[1, 2], [3, 4]]
mat2 = mat1
mat2.append([5, 6])
print(mat1)
print(mat2)
print(mat1 is mat2)
```

Since lists are mutable, `mat2` is merely another name for `mat1`; both refer to the same object, so changing one changes both. Earlier, three techniques for copying lists were shown so edits stay independent. Trying one:

```python
mat2 = mat1.copy()
mat2.append([5, 6])
print(mat1)
print(mat2)
print(mat1 is mat2)
```

That works fine. But now try:

```python
mat1 = [[1, 2], [3, 4]]
mat2 = mat1.copy()
mat2[0][0] = 100
print(mat1)
print(mat2)
```

```output
[[100, 2], [3, 4]]
[[100, 2], [3, 4]]
```

Here `mat1` changed too! Were we not relying on `copy` to prevent this? The issue is a mutable object nested inside another mutable object. In that scenario `copy` performs only a shallow copy — just a fresh outer list is made, while the inner lists remain shared between `mat1` and `mat2`:

```python
print(mat1[0] is mat2[0])
print(mat1[1] is mat2[1])
```

Both print `True`. To copy so that both outer and inner lists become brand-new objects, use `deepcopy`:

```python
from copy import deepcopy
mat1 = [[1, 2], [3, 4]]
mat2 = deepcopy(mat1)
mat2[0][0] = 100
print(mat1)
print(mat2)
```

```output
[[1, 2], [3, 4]]
[[100, 2], [3, 4]]
```

Now the two are entirely separate objects:

```python
from copy import deepcopy
mat1 = [[1, 2], [3, 4]]
mat2 = deepcopy(mat1)
print(mat1 is not mat2)
print(mat1[0] is not mat2[0])
print(mat1[1] is not mat2[1])
```

All three print `True`. `deepcopy` comes from the `copy` library. Without getting into its inner workings, the takeaway is: when working with nested lists or any collection of mutable objects, reach for `deepcopy` to get a clean, independent copy.

## Lesson 5.6 — Tuples: Introduction, Packing and Unpacking {: #ch-5-lesson-6 }

### Introduction

A tuple is an immutable sequence of values:

```python
family = ('father', 'mother', 'child')
print(type(family))
print(isinstance(family, tuple))
```

Tuples closely resemble lists and support indexing and slicing:

```python
print(family[0])
print(family[:2])
```

The key difference is that tuples are immutable and cannot be updated in-place. The following raises an error:

```python
##### Alarm! Wrong code snippet! #####
numbers = ('one', 'two', 'four')
numbers[2] = 'three'
##### Alarm! Wrong code snippet! #####
```

This produces a `TypeError` reading `TypeError: 'tuple' object does not support item assignment`. Because of immutability, you cannot append, insert, or delete elements. Only two methods exist for tuples — `count` and `index` — with their usual meanings:

```python
numbers = (1, 2, 3, 1, 1)
print(numbers.count(1))
print(numbers.index(2))
```

You can iterate over a tuple with `for`:

```python
for num in (1, 2, 3):
    print(num)
```

Since tuples are immutable, they are passed by value like other immutable types (strings, numbers). Useful functions that operate on tuples include `sum`, `max`, and `min`.

### More on Tuples

A few additional points.

A singleton tuple needs a trailing comma:

```python
i_am_single = (1, )
print(len(i_am_single))
print(isinstance(i_am_single, tuple))
```

Removing the comma changes the result — it becomes an integer:

```python
i_am_single = (1)
print(isinstance(i_am_single, int))
```

A list can be converted to a tuple and back:

```python
a_list = [1, 2, 3]
a_tuple = tuple(a_list)
b_tuple = (1, 2, 3)
b_list = list(b_tuple)
```

A tuple can hold a non-homogeneous sequence:

```python
a_tuple = (1, 'cool', True)
```

Membership is checked with `in`:

```python
1 in (1, 2, 3)
'hello' not in ('some', 'random', 'sequence')
```

Tuples can be nested:

```python
a = ((1, 2, 3), (4, 5, 6))
print(a[0][2])
```

A tuple can hold mutable objects:

```python
a_tuple = ([0, 1, 2], [4, 5, 6])
a_tuple[0][0] = 100
```

This runs without error. Although the tuple itself is immutable, the element inside is mutable. The sequence of objects is not being changed — `a_tuple[0]` still points to the same object. This can be verified:

```python
a_tuple = ([0, 1, 2], [4, 5, 6])
print(id(a_tuple[0]))
a_tuple[0][0] = 100
print(id(a_tuple[0]))
```

The `id` of the element remains unchanged. The identities of the objects making up a tuple can never change, but if those objects are mutable (like lists), their internal values may change while retaining their identities.

### Lists and Tuples

A summary comparing the two:

| List | Tuple |
|------|-------|
| Mutable | Immutable |
| `L = [1, 2, 3]` | `T = (1, 2, 3)` |
| Supports indexing and slicing | Supports indexing and slicing |
| Supports item assignment | Doesn't support item assignment |
| Methods: `count, index, append, insert, remove, pop` and others | Methods: `count, index` |
| To get a list: `list(obj)` | To get a tuple: `tuple(obj)` |

An example task explores their partnership:

> "Populate a list that contains all ordered pairs of positive integers whose product is 100."

Note that order matters — (2, 50) and (50, 2) are treated as different pairs.

```python
pairs = [ ]
for a in range(1, 101):
    for b in range(1, 101):
        if a * b == 100:
            pairs.append((a, b))
print(pairs)
```

Here `pairs` is a list of tuples. A tuple is the better choice for each pair because the two elements have a well-defined relationship that should not be accidentally modified.

### Packing and Unpacking

Tuples occupy a significant place in Python. Consider:

```python
T = 1, 2, 3
print(T)
print(isinstance(T, tuple))
```

Though the first line might look like an error, it works: `T` becomes the tuple `(1, 2, 3)`. This is called **tuple packing**. The reverse is **sequence unpacking**:

```python
x, y, z = T
print(x, y, z)
```

Here `T` is unpacked into `x`, `y`, and `z` — the principle behind multiple assignment. The Python documentation states:

> "Multiple assignment is a combination of tuple packing and sequence unpacking."

```python
x, y, z = 1, 2, 3
```

Above, the RHS is first packed into a tuple, then unpacked into the variables. The "sequence" qualifier exists because any sequence can be unpacked:

```python
l1, l2, l3, l4 = 'good'         # string
num1, num2, num3 = [1, 2, 3]    # list
b1, b2 = (True, False)          # tuple
x, y, z = range(3)              # range
```

The same operations apply when functions return multiple values:

```python
def max_min(a, b):
    if a > b:
        return a, b
    return b, a

x = max_min(1, 2)
print(x)
print(isinstance(x, tuple))
```

Here `x` is a tuple. In the return statements, multiple values are packed into a tuple, so the function essentially returns a tuple.
