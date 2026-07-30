<section class="opener" id="ch-6">
<span class="chapter-num">6</span>

# Dictionaries and Sets
<span class="accent-rule"></span>
</section>

## Lesson 6.1 — Dictionaries: Introduction, Iterating, Growing, Mutability {: #ch-6-lesson-1 }

### Introduction

Suppose we want to store information mapping countries to their capitals in Python:

| Country | Capital |
|---|---|
| Brazil | Brasilia |
| Russia | Moscow |
| India | New Delhi |
| China | Beijing |
| South Africa | Cape Town |

South Africa has three capitals but only the legislative capital is listed here for convenience, and these five nations form part of the BRICS block.

A dictionary is one of the most interesting data structures in Python — essentially a look-up table. Here is how the BRICS data would be stored:

```python
brics = {
            'Brazil': 'Brasilia',
            'Russia': 'Moscow',
            'India': 'New Delhi',
            'China': 'Beijing',
            'South Africa': 'Cape Town'
}
```

A dictionary is a collection of key-value pairs. In this example, each country is a key mapped to its capital (the value) — so `'India'` is the key and `'New Delhi'` is the value. A dictionary object is of type `dict`.

```python
print(type(brics))
print(isinstance(brics, dict))
```

To access the value for a given key:

```python
print(brics['India'], 'is the capital of', 'India')
print(brics['China'], 'is the capital of', 'China')
```

The value for a key can be updated:

```python
# Moving to a different capital for South Africa
brics['South Africa'] = 'Pretoria'
# Or we could also store all three capitals
brics['South Africa'] = ('Pretoria', 'Cape Town', 'Bloemfontein')
```

New key-value pairs can also be added. The lesson expands beyond BRICS by creating a new dictionary named `globe` starting as a copy of `brics`, using the `copy()` method (similar to the one for lists):

```python
brics = {
            'Brazil': 'Brasilia',
            'Russia': 'Moscow',
            'India': 'New Delhi',
            'China': 'Beijing',
            'South Africa': 'Cape Town'
        }
globe = brics.copy()
globe['Spain'] = 'Madrid'
```

Adding a new pair is as simple as the last line above. Keys of a dictionary are unique — the same key cannot map to two different values — but two different keys can share the same value:

```python
some_dict = {'key_1': 0, 'key_2': 0}
```

Accessing a key that is not present raises a `KeyError`:

```python
##### Alarm! Wrong code snippet! ######
some_dict = {'0': 'zero', '1': 'one'}
print(some_dict[0])
##### Alarm! Wrong code snippet! ######
```

### More Examples

A dictionary key can be any immutable object (with a catch discussed later). Examples with basic types `int`, `str`, `float`, `bool`:

```python
# int <> int
squares = {0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
# str <> int
months = {'Jan': 31, 'March': 31, 'May': 31, 'Nov': 30}
# int <> str
roll_numbers = {1: 'CS001', 2: 'CS002', 3: 'CS003'}
# str <> str
names = {'Rohit': 'Sharma', 'Saina': 'Nehwal'}
# str <> float
constants = {'pi': 3.14, 'e': 2.71}
# float <> str
fractions = {0.5: 'half', 0.25: 'quarter', 0.3: 'one-third'}
# int <> bool
binary = {0: True, 1: False}
```

Dictionaries with `list` and `tuple` values:

```python
# str <> list
outcomes = {'IND VS AUS': ['IND', 'AUS', 'IND', 'IND'], 'IND VS ENG': ['IND', 'ENG']}
# float <> tuple
bounds = {1.7: (1, 2), 4.3: (4, 5), -1.2: (-2, -1)}
```

Tuples can be keys as long as they contain no mutable objects:

```python
# tuple <> list
T1, T2 = (0, 1), (1, 2)
random_numbers = {T1: [0.1, 0.4, 0.9], T2: [1.1, 1.9]}
```

A richer mixed example:

```python
# mixed
report_card = {
                'name': 'Ramanujan',
                'age': 18,
                'school': 'KV',
                'marks': (75, 80, 60, 95, 100)
              }
```

### More on Keys

Saying keys must be immutable is not entirely accurate. Using a list as a key:

```python
##### Alarm! Wrong code snippet #####
some_list = [0, 1]
bad_dict = {some_list: 0}
##### Alarm! Wrong code snippet #####
```

This raises a `TypeError` with the message `unhashable type: 'list'`. The error refers to hashability rather than immutability. The more accurate rule:

> "The keys of a dictionary must be hashable."

#### Hash Tables

Python dictionaries are implemented using a hash table. Think of a book-rack with numbered rows, where key-value pairs are books. To find a book you need its row number, which is provided by a *hash function*, denoted $h$, that converts the key to the row number.

The hash function takes a key $k$ and returns $h(k)$, the *hash value* — analogous to the rack number. Once the rack number is known, the stored item can be retrieved.

An object is hashable if it has a hash value that never changes during its lifetime and can be compared to other objects. Most immutable objects seen so far (`int`, `float`, `str`, `bool`) are hashable, while mutable containers like lists are not. But not every immutable object works as a key:

```python
##### Alarm! Wrong code snippet #####
some_tuple = ([0, 1], [2, 3])
bad_dict = {some_tuple: 0}
##### Alarm! Wrong code snippet #####
```

Although `some_tuple` is immutable, it contains lists which are mutable. Per the Python docs, immutable containers are hashable only if their elements are also hashable — so this tuple is unhashable and cannot be a key.

### Iterating over Dictionaries

Iterating over keys:

```python
squares = {0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25}    # key is a number, value is its square
for key in squares.keys():
    print(f'The square of {key} is {squares[key]}')
```

`squares.keys()` returns a sequence of keys. Python lets us drop the `keys` method:

```python
squares = {0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25}    # key is a number, value is its square
for key in squares:
    print(f'The square of {key} is {squares[key]}')
```

We can also iterate over key-value pairs:

```python
squares = {0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25}    # key is a number, value is its square
for key, value in squares.items():
    print(f'The square of {key} is {value}')
```

### Growing a Dictionary

An empty dictionary can be defined in two ways:

```python
D1 = dict()
D1[0] = 1
D2 = { }
D2[0] = 1
```

**Problem:** Create a dictionary from a list of words that maps words to their lengths.

```python
words = ['interstellar', 'dunkirk', 'inception', 'tenet']
lengths = dict()
for word in words:
    lengths[word] = len(word)
print(lengths)
```

A piece of trivia is posed: what do the words in the list have in common?

### Mutability

Like lists, dictionaries are mutable. This code demonstrates aliasing:

```python
dict_1 = {'one': 1, 'two': 2, 'three': 3}
dict_2 = dict_1
dict_2['four'] = 4
print(dict_1, dict_2)
print(dict_1 is dict_2)
```

Here `dict_2` is an alias of `dict_1`, both pointing to the same object. To make a new dict with the same contents, use `copy()` or the `dict` built-in:

```python
dict_1 = {'one': 1, 'two': 2, 'three': 3}
dict_2 = dict_1.copy()      # dict(dict_1) also works
dict_2['four'] = 4
print(dict_1, dict_2)
print(dict_1 is not dict_2)
```

The last line prints `True`, confirming two different objects, so modifying one does not affect the other. But `copy()` only makes a shallow copy — fine for immutable values, but problematic with mutable ones:

```python
dict_1 = {'one': [1], 'two': [1, 1], 'three': [1, 1, 1]}
dict_2 = dict_1.copy()
dict_2['one'].append(100)
print(dict_1, dict_2)
print(dict_1 is not dict_2)
print(dict_1['one'] is dict_2['one'])
```

Here the value for `'one'` in both dictionaries is affected because `dict_1['one']` and `dict_2['one']` are still the same object. To fix this, use a deep copy:

```python
from copy import deepcopy
dict_1 = {'one': [1], 'two': [1, 1], 'three': [1, 1, 1]}
dict_2 = deepcopy(dict_1)
dict_2['one'].append(100)
print(dict_1, dict_2)
print(dict_1 is not dict_2)
print(dict_1['one'] is not dict_2['one'])
```

## Lesson 6.2 — Text Processing {: #ch-6-lesson-2 }

This lesson explores text processing using an excerpt from a talk given by Guido. The excerpt discusses how programming languages are how programmers "express and communicate *ideas*" — with the audience being other programmers rather than computers.

Text processing helps analyze text data. Given a piece of text, some basic questions include:

- How many sentences are there in the text?
- How many words are there in the text?
- How many of them are unique?
- Which word appears the most number of times?

These questions are meaningful for tasks like classifying articles into categories such as lifestyle, science and technology, literature, or films. Rather than reading hundreds of articles manually, you can computationally process each one to find the top common words and infer the topic.

We begin by storing the text in a variable:

```python
text = "In reality, programming languages are how programmers express and communicate ideas — and the audience for those ideas is other programmers, not computers. The reason: the computer can take care of itself, but programmers are always working with other programmers, and poorly communicated ideas can cause expensive flops. In fact, ideas expressed in a programming language also often reach the end users of the program — people who will never read or even know about the program, but who nevertheless are affected by it."
```

### Number of sentences

Sentences may end with a full stop, exclamation mark, or question mark. For simplicity, assume all sentences end with a full stop, so we split on that delimiter:

```python
sentences = text.split('.')
```

To inspect the list, temporary printing code is used — understanding what your code does by printing variable contents is important:

```python
# Prints one sentence in each line
for sentence in sentences:
    print(sentence)
print(f'There are {len(sentences)} sentences in this text.')
```

```output
In reality, programming languages are how programmers express and communicate ideas — and the audience for those ideas is other programmers, not computers
 The reason: the computer can take care of itself, but programmers are always working with other programmers, and poorly communicated ideas can cause expensive flops
 In fact, ideas expressed in a programming language also often reach the end users of the program — people who will never read or even know about the program, but who nevertheless are affected by it
There are 4 sentences in this text.
```

Although there are only three sentences, the output reports four. The issue is that `sentences[-1]` is an empty string. When splitting on a delimiter present in the string, substrings are generated on either side; since the full stop is the last character, the substring to its right is empty. The fix removes empty strings:

```python
while '' in sentences:
    sentences.remove('')
print(f'There are {len(sentences)} sentences in this text.')
```

```output
There are 3 sentences in this text.
```

One problem solved!

### Number of words

To count words, we split each sentence by space:

```python
words = [ ]
for sentence in sentences:
    words_ = sentence.split(' ')    # words_ contains words in sentence
    words.extend(words_)            # words is the collection of all words
```

Printing `len(words)` gives 86, but wordcounter.net reports 82. To investigate, each word and its index are printed:

```python
for index, word in enumerate(words):
    print(index, word)
```

The problematic entries found were:

```output
11 —
23
49
67 —
```

Indices 11 and 67 are em dashes (—), while 23 and 49 are empty strings. Since there are two characters to remove, the list is cleaned:

```python
proc_words = [ ]
for word in words:
    if not(word == '' or word == '—'):
        proc_words.append(word)
print(f'There are {len(proc_words)} words in this text')
```

This yields 82 words as expected. One more problem solved!

### Number of Unique Words

This section introduces a dictionary to track unique words along with their frequency:

```python
uniq_words = dict()
for word in proc_words:
    if word not in uniq_words:
        uniq_words[word] = 0
    uniq_words[word] += 1
print(f'There are {len(uniq_words)} unique words in this text')
```

The result is 62 unique words. But manual inspection shows "programmers" occurs four times. Checking the dict:

```python
print(uniq_words['programmers'])
```

The output is `2` — another wrong answer. Making mistakes is the norm, not the exception, and "An error in the code is hidden knowledge." To investigate, we search `proc_words` for entries containing "programmers":

```python
for word in proc_words:
    if 'programmers' in word:
        print(word)
```

```output
programmers
programmers,
programmers
programmers,
```

The problem is the comma special character. Another issue is capitalization at the beginning of sentences. The code is revised to handle both:

```python
proc_words = [ ]
for word_ in words:
    word = word_.lower()
    if not(word == '' or word == '—'):
        if not word_.isalnum():
            word = word_[:-1]
        proc_words.append(word)
print(f'There are {len(proc_words)} words in this text')
```

Here, each word is converted to lowercase, em dashes and empty strings are ignored, and if a word contains a special character it is stripped of the trailing character (assuming special characters appear at the end). Examples in the text: "programmers," and "reason:". Then `uniq_words` is regenerated:

```python
uniq_words = dict()
for word in proc_words:
    if word not in uniq_words:
        uniq_words[word] = 0
    uniq_words[word] += 1
print(f'There are {len(uniq_words)} unique words in this text')
```

Now there are 58 unique words. This can be verified by printing all words and counts:

```python
for word, freq in uniq_words.items():
    print(word, freq)
```

As a test, the sum of counts should equal the total number of words:

```python
total = 0
for word in uniq_words:
    total += uniq_words[word]
assert total == len(proc_words)
```

Since no `AssertionError` is raised, the result is correct.

### Frequent Words

The final task is finding the top three most frequently occurring words:

```python
first_word = second_word = third_word = ''
first_val = second_val = third_val = 0
for word, freq in uniq_words.items():
    if freq > first_val:
        first_val, second_val, third_val = freq, first_val, second_val
        first_word, second_word, third_word = word, first_word, second_word
    elif freq > second_val and freq < first_val:
        second_val, third_val = freq, second_val
        second_word, third_word = word, second_word
    elif freq > third_val and freq < second_val:
        third_val = freq
        third_word = word
print(first_word, first_val)
print(second_word, second_val)
print(third_word, third_val)
```

```output
the 6
programmers 4
in 3
```

"Programmers" is the second most frequent word, while "the" and "in" are first and third. These common words are called stop-words; removing them makes "programmers" the most frequent non-trivial word. So without reading the text, one could guess it is about programmers — thanks to Python.

### Summary

The main lesson takeaway is the kinds of mistakes made and how each was fixed. In nearly every problem, we started with a solution, tested it, discovered something was wrong, and went back to fix the problem.

## Lesson 6.3 — Pangrams and Dictionary Methods {: #ch-6-lesson-3 }

### Pangrams and Dictionaries

This lesson explores building a mapping between the 26 letters of the English alphabet and the numbers 1 through 26, where each letter maps to a unique number (a→1, b→2, ... z→26) in a simple linear fashion.

The most tedious approach is to type out the entire dictionary by hand:

```python
mapping = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5,
           'f': 6 , 'g': 7, 'h': 8, 'i': 9, 'j': 10, 
           'k': 11, 'l': 12, 'm': 13, 'n': 14, 'o': 15,
           'p': 16, 'q': 17, 'r': 18, 's': 19, 't': 20,
           'u': 21, 'v': 22, 'w': 23, 'x': 24, 'y': 25,
           'z': 26
          }
for letter, count in mapping.items():
    print(letter, count)
```

Typing this out is dull and mechanical, and copy-pasting is impractical if you do not want to open the textbook every time you need this mapping. A more interesting method uses a **pangram** — a sentence that uses every letter of the alphabet:

> the quick brown fox jumps over the lazy dog

```python
pangram = 'the quick brown fox jumps over the lazy dog'
words = pangram.split(' ')          # get list of words in the sentence
letters = ''.join(words)            # join the words back; eliminates spaces
sorted_letters = sorted(letters)    # sort letters
mapping, count = dict(), 0
for letter in sorted_letters:
    # check if letter is not present in dict
    # to avoid counting same letter multiple times
    if letter not in mapping:
        count += 1
        mapping[letter] = count     # map the letter to count
for letter, count in mapping.items():
    print(letter, count)
```

There is much to learn from these 14 lines. With this dictionary in place, the lesson moves into dictionary methods bundled with `dict`.

### Dictionary Methods

`keys` and `items` were seen earlier. Both are methods returning a view object that can be iterated over. Quoting the Python documentation, view objects provide a dynamic view on the dictionary's entries, so when the dictionary changes, the view reflects those changes.

```python
keys = mapping.keys()
print(keys)
```

```output
dict_keys(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])
```

Using `list()`, both the `keys` and `items` views can be turned into lists:

```python
keys_list = list(mapping.keys())
print(keys)
items_list = list(mapping.items())
print(items)
```

```output
['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
[('a', 1), ('b', 2), ('c', 3), ('d', 4), ('e', 5), ('f', 6), ('g', 7), ('h', 8), ('i', 9), ('j', 10), ('k', 11), ('l', 12), ('m', 13), ('n', 14), ('o', 15), ('p', 16), ('q', 17), ('r', 18), ('s', 19), ('t', 20), ('u', 21), ('v', 22), ('w', 23), ('x', 24), ('y', 25), ('z', 26)]
```

Here `keys_list` is a list of the dictionary's keys, while `items_list` is a list of tuples, each being a key-value pair. Another useful method is `values`, which returns a **view** on the values:

```python
view = mapping.values()
view_list = list(view)
```

All three views — `keys`, `items`, and `values` — support membership tests:

```python
print('a' in mapping.keys())
print(1 in mapping.values())
print(('a', 1) in mapping.items())
```

All three of these return `True`. Membership tests for keys can be written more simply:

```python
print('a' in mapping)
print('x' in mapping)
print('ab' not in mapping)
```

Notice that dropping the `keys` method still works. To delete a key from a dictionary, use the familiar `pop` method:

```python
mapping['ab'] = 3           # some noise added to mapping
value = mapping.pop('ab')
print(value)
print('ab' not in mapping)
```

If `key` is a key in dictionary `D`, then `D.pop(key)` removes that key and returns its associated value. Removing a key also removes its value. Dictionaries are "aristocratic data structures": keys sit higher in the hierarchy, and values depend on keys for their existence.

## Lesson 6.4 — Dictionaries in Action: LMS {: #ch-6-lesson-4 }

This lesson explores how a Learning Management System (LMS) works — the software that powers an online degree portal. It aims to answer how assignment submissions get recorded and graded. At a high level, an LMS consists of two components: a frontend and a backend.

As a user, you interact with the frontend — the website displaying content. When you take an action (like clicking submit on a graded assignment), that action goes to the backend as input. The backend processes it and returns output to the frontend, which displays the result. Python plays a prominent role in the backend.

Grading requires two inputs — the assignment and the corresponding submission — and returns a result as output. The grader can be expressed as a function:

```python
def grader(assignment, submission):
    """Grading logic"""
    result = 0.0
    return result
```

This function is incomplete; we still need to model an assignment and its submission.

### Assignment Model

An assignment is essentially a list of problems, so modeling an assignment reduces to modeling a problem. A problem could have these attributes:

| Attribute | Type |
|-----------|------|
| id | string |
| question | string |
| type | string |
| options | list |
| answers | tuple |
| marks | float |

For grading, only two attributes are needed: the problem-id and the answers. The assignment becomes a list of dictionaries:

```python
# assume that the assignment has three problems
# the assignment will be a list of dictionaries
assignment = [
                {'id': '10001', 'answers': (0, 1), 'marks': 2.0},
                {'id': '10002', 'answers': (1, ), 'marks': 1.0 },
                {'id': '10003', 'answers': (2, ), 'marks': 2.0}
             ]
```

!!! note "Note"

    A singleton tuple is written as `(<item>, )` — the comma cannot be omitted.

Several attributes from the table do not appear in the dictionary because they are not relevant to grading; they were listed to give a fuller picture of how assignments can be modeled.

### Submission Model

The submission model is more involved. It has global attributes like the user's name, roll number, and submission time, plus local attributes such as the options selected per problem.

| Attribute | Type |
|-----------|------|
| name | string |
| roll_number | string |
| timestamp | string |
| problems | list |

A sample submission:

```python
submission = {
                'name': 'Kapil Dev',
                'roll_number': 'BSC1001',
                'time': 'Sunday 18 April 2021 10:23:30 PM IST',
                'problems': [
                                {'id': '10001', 'selected': (0, 1)},
                                {'id': '10002', 'selected': (1, )},
                                {'id': '10003', 'selected': (3, )}
                            ]
              }
```

The `submission` is a fairly complicated object. It is a dictionary; the first three keys are simple, but the value of `'problems'` is a list of dictionaries. Complexity could increase further since a user might make multiple submissions (a list of submissions), but that is left aside for now.

### Grader

Although representing the assignment as a list of dictionaries is not bad, the grader would have to search the list for each problem id when grading. Since problem ids are unique, a better representation is possible:

```python
assignment_ = [
                {'id': '10001', 'answers': (0, 1), 'marks': 2.0},
                {'id': '10002', 'answers': (1, ), 'marks': 1.0 },
                {'id': '10003', 'answers': (2, ), 'marks': 2.0}
             ]
assignment = dict()
for problem in assignment_:
    problem_id = problem['id']
    answers = problem['answers']
    marks = problem['marks']
    assignment[problem_id] = {'answers': answers, 'marks': marks}
```

The assignment now looks like this:

```python
assignment = {
                '10001': {
                            'answers': (0, 1),
                            'marks': 2.0
                         },
                '10002': {
                            'answers': (1, ),
                            'marks': 1.0
                         },
                '10003': {
                            'answers': (2, ),
                            'marks': 2.0
                         },
             }
```

We can now complete the grader using this new assignment model:

```python
def grader(assignment, submission):
    """Grading logic"""
    result = 0.0
    for problem in submission['problems']:
        problem_id = problem['id']
        selected = problem['selected']
        answers = assignment[problem_id]['answers']
        if answers == selected:
            result += assignment[problem_id]['marks']
    return result
```

## Lesson 6.5 — Sets {: #ch-6-lesson-5 }

### Introduction

A set is an unordered collection with no duplicate elements. Unlike lists and tuples, a set has no notion of order — that is why it is called an unordered collection rather than a sequence. You can define one like this:

```python
even_nums = {2, 4, 6, 8, 10}
print(type(even_nums))
print(isinstance(even_nums, set))
```

```output
<class 'set'>
True
```

Note the syntactic similarity between sets and dictionaries — both use curly braces. A dictionary holds key-value pairs while a set holds just values. Python sets closely mirror mathematical sets, so most familiar mathematical set properties carry over naturally.

```python
nums_1 = {2, 4, 6, 8, 10}
nums_2 = {2, 2, 4, 4, 6, 6, 8, 8, 10, 10}
print(nums_1, nums_2)
print(nums_1 == nums_2)
print(nums_1 is not nums_2)
```

```output
{2, 4, 6, 8, 10} {2, 4, 6, 8, 10}
True
True
```

Since sets do not support duplicates, `nums_1` and `nums_2` are equal, though they are not the same object. Sets support membership testing like other collections.

```python
nums = {1, 2, 3, 4, 5}
print(1 in nums)
print(6 not in nums)
```

The number of elements (its cardinality) is given by `len()`:

```python
nums = {1, 2, 3, 4, 5}
print(f'Cardinality of nums is {len(nums)}')
```

Sets cannot be indexed, which makes sense since they are not ordered. This code raises an error:

```python
##### Alarm! Wrong code snippet! #####
some_set = {'this', 'is', 'a', 'set'}
print(some_set[0])
##### Alarm! Wrong code snippet! #####
```

Any hashable object can be added to a set, including most immutable types like `int`, `float`, `str`, and `tuple`. Caveat: a tuple containing lists is unhashable and cannot be added.

```python
a_set = {1.0, 'one', 1, True, (1, )}    # valid set
not_a_set = {([1, 2], [3, 4])}          # not a valid set
```

`not_a_set` raises a `TypeError` as expected.

### Iterating through Sets

Although a set is not a sequence, you can still iterate over its elements.

```python
nums = {1, 2, 3, 4, 5}
for num in nums:
    print(num)
```

### Growing Sets

How do we define an empty set?

```python
##### Alarm! Be careful about the variable name! #####
empty_set = { }
print(isinstance(empty_set, set))
print(isinstance(empty_set, dict))
##### Alarm! Be careful about the variable name! #####
```

As it turns out, `empty_set` is actually an empty dictionary — `{ }` still denotes an empty dictionary as it did in earlier lessons. So the correct way to make an empty set is:

```python
empty_set = set()
print(isinstance(empty_set, set))
```

With empty sets and iteration available, we can build sets from scratch.

> Consider the first 100 powers of 7: 7¹, 7², ⋯, 7¹⁰⁰. Note the last digit of each. How many are unique? What are they?

There is a simple mathematical answer, but let's pursue a computational one:

```python
num = 1
digits = set()
for i in range(100):
    num *= 7
    last = num % 10
    digits.add(last)
print(digits)
```

`add` inserts elements into a set. Sets are ideal when duplicates crop up often and you do not care about them. The same task can be done with lists:

```python
num = 1
digits = [ ]
for i in range(100):
    num *= 7
    last = num % 10
    if last not in digits:
        digits.append(last)
print(digits)
```

### Set Operations

Mathematical sets interact through operations, and Python sets aim to match them:

- Subset
- Superset
- Union
- Intersection
- Difference

**Subset:** *A* is a subset of *B* (A ⊆ B) if every element of *A* is in *B*.

```python
A = {1, 3, 5}
B = {1, 2, 3, 4, 5}
print(A.issubset(B))    # method-1
print(A <= B)           # method-2
```

Both lines return `True`. A *proper* subset (A ⊂ B) requires every element of *A* to be in *B* with *A* ≠ *B*:

```python
A = {1, 2, 3}
B = {1, 2, 3}
print(A <= B)   # method-1
print(A < B)    # method-2
```

The `A < B` operator checks proper-subset status; here *A* is not a proper subset, so the second print gives `False`.

**Superset:** *A* is a superset of *B* (A ⊃ B) if every element of *B* is in *A*.

```python
A = {1, 3, 5}
B = {1, 2, 3, 4, 5}
B.issuperset(A)     # method-1
print(B >= A)       # method-2
```

**Union:** the union (A ∪ B) contains elements in either *A* or *B* or both.

```python
A = {1, 3, 5}
B = {2, 4, 6}
C1 = A.union(B)     # method-1
C2 = A | B          # method-2
print(C1, C2)
print(C1 == C2)
```

For multiple sets:

```python
A1, A2, A3, A4 = {1}, {2, 3}, {4, 5, 6}, {7, 8, 9, 10}
B1 = A1.union(A2, A3, A4)   # method-1
B2 = A1 | A2 | A3 | A4      # method-2
print(B1, B2)
print(B1 == B2)
```

**Intersection:** the intersection (A ∩ B) contains elements common to both.

```python
A = {2, 4, 6}
B = {2, 4}
C1 = A.intersection(B)  # method-1
C2 = A & B              # method-2
print(C1, C2)
print(C1 == C2)
```

With no common elements, we get the empty set:

```python
even, odd = {2, 4, 6}, {1, 3, 5}
common = even & odd
assert common == set()
```

The `assert` here adds variety; since no `AssertionError` is raised, the result is correct.

**Difference:** the difference of *A* and *B* (A − B or B − A) are not the same.

- A − B: elements in *A* not in *B*.
- B − A: elements in *B* not in *A*.

```python
A = {1, 2, 3, 4}
B = {2, 4, 5}
C1 = A.difference(B)    # method-1
C2 = A - B              # method-2
print(C1, C2)
print(C1 == C2)
D1 = B.difference(A)    # method-1
D2 = B - A              # method-2
print(D1, D2)
print(D1 == D2)
```

### Other Set Methods

Now for methods with a more computational character. To remove an element, use `remove`:

```python
A = {'this', 'is', 'a', 'set'}
print('Before', A)
A.remove('this')
print('After', A)
```

Removing an absent element raises a `KeyError`:

```python
A = {'this', 'is', 'a', 'set'}
A.remove('cool')    # error!
```

Consider this problem:

> Given a list `L`, extract all unique elements into another list `L_uniq`. Order does not matter.

A solution without sets:

```python
L = [1, 2, 3, 3, 4, 5, 6, 1, 2, 2]
L_uniq = [ ]
for elem in L:
    if elem not in L_uniq:
        L_uniq.append(elem)
print(L_uniq)
```

And with sets:

```python
L = [1, 2, 3, 3, 4, 5, 6, 1, 2, 2]
S = set(L)
L_uniq = list(S)
print(L_uniq)
```

Passing a list to `set` strips duplicates and yields the unique elements.

### Mutability

Sets are mutable.

```python
A = {1, 2, 3}
B = A
B.add(4)
print(A, B)
print(A is B)
```

Here `A` and `B` refer to the same object. As before, there are two ways to make a shallow copy:

```python
A = {1, 2, 3}
B1 = A.copy()
B2 = set(A)
B1.add(4)
B2.add(0)
print(A, B1, B2)
print(A is not B1)
print(A is not B2)
```
