<section class="opener" id="ch-1">
<span class="chapter-num">1</span>

# Introduction to Python
<span class="accent-rule"></span>
</section>

## Lesson 1.1 — Python Shell, Output, Literals and Data Types {: #ch-1-lesson-1 }

### Python shell | Replit Console

This lesson works with the Python interpreter in *Interactive Mode*, often called the Python shell. It executes individual lines of code and shows the output immediately. Throughout the lessons it is referred to simply as "the interpreter." In Replit this corresponds to the console screen on the right of the repl.

### Prompts

The orange symbol displayed is called a *prompt*. Its role is similar to a blinking cursor while editing documents — it is "an invitation to type code." Code typed at the prompt is executed by the interpreter, represented by `>>>`.

```repl
>>> print('Hello World!')
Hello World!
```

### Output

`print()` is a built-in function. A function accepts inputs and returns outputs, and "built-in" means Python readily provides it.

```repl
>>> print('Hello World!')
Hello World!
>>> print("Hello World!")
Hello World!
```

The text enclosed in parentheses is a **string** — "a sequence of characters enclosed in quotes." Strings use single or double quotes, but a single quote cannot be matched with a double quote. This is useful for apostrophes:

```repl
>>> print("India's capital is New Delhi.")
```

`print()` can also print numbers:

```repl
>>> print(1)
1
>>> print(2.0)
2.0
```

Multiple items can appear on one line:

```repl
>>> print(1, 2)
1 2
>>> print('online', 'degree', 'program')
online degree program
```

`print` separates multiple values with a delimiter, which is a space by default. Calling `print` with no input prints a blank line:

```repl
>>> print()

>>>
```

Using `print` without parentheses:

```repl
>>> print
<built-in function print>
```

But this raises an error:

```repl
>>> print 'Hello World!'
  File "<stdin>", line 1
    print 'Hello World!'
          ^
SyntaxError: Missing parentheses in call to 'print'. Did you mean print('Hello World!')?
```

Programming languages have strict syntaxes that must be followed exactly. Parentheses execute the function and pass values (arguments) to it.

### Emojis

```repl
>>> print('\N{smiling face with smiling eyes}')
😊
>>> print('\N{grinning face}')
😀
>>> print('\N{smiling face with halo}')
😇
>>> print('\N{thinking face}')
🤔
```

A full list of emojis is available in the Unicode emoji charts.

### Literals and Variables

Strings like `'Hello World!'` and numbers like `1` and `2.0` are *literals* — "a literal is something that describes a constant value." Variables are containers for storing values:

```repl
>>> x = 1
>>> print(x)
1
>>> y = 'a string'
>>> print(y)
a string
>>> foo_bar = 123.456
>>> print(foo_bar)
123.456
```

`=` is the assignment operator, used to define a new variable or to update an existing one:

```repl
>>> x = 1         # define a new variable
>>> x = x + 1     # update an existing variable
>>> print(x)
2
```

The assignment operator "is evaluated from right to left" — the right-side expression evaluates first, then the result is assigned to the left variable.

### Basic Data Types | type()

The basic data types covered are Integer, Float, String, and Boolean.

#### Integer

The `int` type represents integers. `type` determines an object's type:

```repl
>>> print(1)
1
>>> type(1)
<class 'int'>
```

#### Float

The `float` type represents real numbers:

```repl
>>> print(1.0)
1.0
>>> type(1.0)
<class 'float'>
```

A valid float literal:

```repl
>>> print(1.)
1.0
```

`1.` and `1.0` are the same literal.

#### String

The `str` type represents strings:

```repl
>>> print('one')
one
>>> type("one")
<class 'str'>
```

#### Boolean

The `bool` type represents boolean values:

```repl
>>> print(True)
True
>>> type(False)
<class 'bool'>
```

!!! note "Note"

    `bool` values are case sensitive — `true` and `false` are not `bool` values.

### Comments

A comment is "a line of text that is not executed by the interpreter." Comments begin with `#`:

```repl
>>> # This is a comment
>>> # print(1)
>>>
```

Comments can also appear at the end of a line of code:

```repl
>>> print(1) # This line is printing the value 1
1
```

Adding comments is one way to make code more readable.

## Lesson 1.2 — Operators and Expressions {: #ch-1-lesson-2 }

### Operators

#### Arithmetic Operators

Python's arithmetic operators are all binary (they take two operands):

| Operator | Operation |
|----------|-----------|
| `+` | Addition |
| `-` | Subtraction |
| `*` | Multiplication |
| `/` | Division |
| `//` | Floor division |
| `%` | Modulus |
| `**` | Exponentiation |

Interactive examples show `10 + 5` gives `15`, `10 / 5` gives `2.0`, `10 // 5` gives `2`, `10 % 5` gives `0`, and `10 ** 5` gives `100000`.

Key notes: `//` gives the quotient (`8 // 3` is `2`), `%` gives the remainder (`10 % 3` is `1`), and `**` returns x to the power y. `/` and `//` differ — `5 / 2` gives `2.5` while `5 // 2` gives `2`.

There are also **unary** `+` and `-` (one operand): `- 2` gives `-2`, `+ 2` gives `2`. Context decides the meaning; for example `1 - - 1` gives `2` (subtraction on the left, unary minus on the right). Operands can also be variables.

#### Relational Operators

Binary comparison operators return boolean values:

| Operator | Operation |
|----------|-----------|
| `>` | greater than |
| `<` | less than |
| `>=` | greater than or equal to |
| `<=` | less than or equal to |
| `==` | double equal to |
| `!=` | not equal to |

Results are `True`/`False` and can be assigned to variables.

!!! warning "Warning"

    Do not confuse `==` (equality) with `=` (assignment).

#### Logical Operators

| Operator | Operation |
|----------|-----------|
| `not` | negation |
| `and` | logical conjunction |
| `or` | logical disjunction |

`and` and `or` are binary; `not` is unary. Parentheses after `not` are optional (`not x` or `not(x)`).

!!! note "Convention"

    Both `1 + 2` and `1+2` give `3`. The course uses spaces around operators, including `=` (`x = 2`, not `x=2`), though both forms are valid.

#### Operator Chaining

Python allows chaining, so `10 < 11 <= 12` is `True`, equivalent to `10 < 11 and 11 <= 12`.

### Expressions

An expression is "some combination of literals, variables and operators." Examples include `1 + 4 / 4 ** 0` and `not True and False`. Each evaluates to a typed value. Two types are studied:

- **Arithmetic:** type `int` or `float`
- **Boolean:** type `bool`

### Types of Expressions

#### Arithmetic Expressions

```repl
>>> type(1 + 2)
<class 'int'>
>>> type(1.0 + 2)
<class 'float'>
```

The conclusion is that `float` is more dominant than `int` irrespective of the operator involved — all operations mixing a float yield a float.

#### Boolean Expressions

Relational and logical expressions yield `bool`:

```repl
>>> type(2 > 1)
<class 'bool'>
>>> type(True and False)
<class 'bool'>
```

Truth table for `X or Y`:

| X | Y | X or Y |
|-------|-------|--------|
| True | True | True |
| True | False | True |
| False | True | True |
| False | False | False |

## Lesson 1.3 — Arithmetic and Boolean Expressions {: #ch-1-lesson-3 }

### Arithmetic Expressions

#### Precedence

Consider an arithmetic expression that uses multiple operators:

```repl
>>> 4 // 2 - 1
1
```

This can be interpreted two ways: `(4 // 2) - 1 = 2 - 1 = 1` or `4 // (2 - 1) = 4 // 1 = 4`. Python follows the first. When an expression mixes operators, the interpreter must decide how to parenthesize it — that is, which operator takes **precedence**. From this example, floor division (`//`) has greater precedence than subtraction (`-`).

The lesson references a precedence table where higher-precedence operators appear at the top, and operators sharing a cell have equal precedence (for instance, `+` and `-`).

```repl
>>> 3 ** 2 * 4 - 4
32
```

The parenthesization proceeds as `(3 ** 2) * 4 - 4`, then `((3 ** 2) * 4) - 4`, evaluating to `((3 ** 2) * 4) - 4 = (9 * 4) - 4 = 36 - 4 = 32`.

#### Order

```repl
>>> 3 - 2 + 1
2
```

This could mean `(3 - 2) + 1 = 1 + 1 = 2` or `3 - (2 + 1) = 3 - 3 = 0`. Python uses the first. But this does not mean subtraction outranks addition — they share precedence. Python evaluates expressions from **left to right**. The two exceptions are `**` and `=`, which evaluate right to left.

```repl
>>> 4 - 3 - 1
0
```

The options are `(4 - 3) - 1 = 1 - 1 = 0` or `4 - (3 - 1) = 4 - 2 = 2`. The first (left-to-right) is used.

```repl
>>> 8 % 4 % 2
0
```

Readers are asked to test which parenthesization matches — this is left as an exercise:

```repl
>>> (8 % 4) % 2
>>> 8 % (4 % 2)
```

Finally, `**` behaves uniquely:

```repl
>>> 2 ** 3 ** 0
2
```

The options are `(2 ** 3) ** 0` or `2 ** (3 ** 0)`. Python follows the second (right to left). This right-to-left behavior applies only to exponentiation and assignment.

### Boolean expressions

The simplest boolean-producing expression:

```repl
>>> 1 > 0
True
>>> type(1 > 0)
<class 'bool'>
```

Expressing that 3.14 lies between 3 and 4:

```repl
>>> 3 < 3.14 and 4 > 3.14
True
```

This can also be written as:

```repl
>>> 3 < 3.14 < 4
True
```

Adding boolean literals:

```repl
>>> 10 > 20 or True
True
```

As an exercise:

```repl
>>> False or False or False or False or True
```

#### Precedence and Order

Logical operators also have precedence and evaluate left to right.

```repl
>>> not True and False
False
```

The two parenthesizations are `not(True) and False = False and False = False` or `not(True and False) = not(False) = True`. Python follows the first, consistent with logical precedence rules.

```repl
>>> True or False and False
True
```

The options are `(True or False) and False = True and False = False` or `True or (False and False) = True or False = True`. Since `and` outranks `or`, Python uses the second.

#### Beware of `float`!

```repl
>>> 10.00000000000000000000001 > 10
False
```

This seems surprising, because it is a valid mathematical statement that should be `True`. The reason relates to how floating point numbers are represented — programming languages generally "do not support arbitrary precision for representing real numbers." When a number cannot be represented exactly, an approximation is returned, so caution is needed with `float` comparisons.

```repl
>>> 0.1 ** 100 == 0.0
False
>>> 0.1 ** 1000 == 0.0
True
```

Because `0.1 ** 1000` is extremely small, the interpreter represents it as 0.

```repl
>>> 0.1 * 3 == 0.3
False
```

Examining the left side:

```repl
>>> 0.1 * 3
0.30000000000000004
```

!!! note "Note (may be skipped)"

    The issue is how `0.1` is represented in binary — "it has a non-terminating, recurring sequence of bits after the decimal point." Since computers use finite bits, the sequence gets truncated, producing an approximate representation of `0.1`. The lesson links to an external resource for more detail (exploringbinary.com).

#### Short Circuit Evaluation

```repl
>>> 1 / 0
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ZeroDivisionError: division by zero
```

Division by zero produces an error, as expected. But the next result is surprising:

```repl
>>> True or (1 / 0)
True
```

No error appears. The explanation: evaluation runs left to right with `or`. Since the left operand is `True`, the whole expression is `True` regardless of the right operand, so the interpreter skips evaluating it. "This behaviour is called short circuit evaluation."

A more complex example:

```repl
>>> (not((3 > 2) or (5 / 0))) and (10 / 0)
False
```

The lesson references a flow chart with arrows showing evaluation order. Following them reveals that the two problematic expressions — `5 / 0` and `10 / 0` — are never evaluated.

## Lesson 1.4 — The Replit Editor, Errors and Debugging {: #ch-1-lesson-4 }

### Replit Editor

This section explains moving from Replit's console to the editor. The key advantage is that code is automatically saved — described as being like "Google Docs for code." The editor is to the left of the console. After typing code, you click the green `Run` button at the top, and output appears in the console. From this point on, the book drops the prompt symbol before each line.

### Errors

#### Introduction

Enter and run this code:

```python
print('123)
```

```output
  File "main.py", line 1
    print('123)
              ^
SyntaxError: EOL while scanning string literal
```

The first lines are an error message — the interpreter's warning that something is wrong. Here it is a `SyntaxError`. The details explain:

- **EOL** stands for **E**nd **O**f **L**ine
- scanning a string literal

The `^` sign points to where the error occurred, acting as a visual aid. The problem is the missing ending quote `'`. The fix:

```python
print('123')
```

#### Debugging

Errors in code are also called bugs, and fixing them is called **debugging**. The process works as follows:

1. **Run**: run the code
2. **Detect**: the interpreter intimates the coder of the error
3. **Understand**: the coder has to understand the error message and go back to the code to see what went wrong
4. **Update**: fix the error by modifying or updating one or more lines of the code

Afterward the coder runs the code again, closing the loop. If another error appears, the process repeats. With large codebases, fixing bugs "might take several hours or even days."

#### Exceptions

These are not syntax errors. First example:

```python
1 / 0
```

```output
Traceback (most recent call last):
  File "main.py", line 1, in <module>
    1 / 0
ZeroDivisionError: division by zero
```

This is a `ZeroDivisionError`. There is no syntax problem here. Errors detected during a program's execution are called **exceptions**. Another example:

```python
1 + 'one'
```

```output
Traceback (most recent call last):
  File "main.py", line 1, in <module>
    1 + 'one'
TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

This is a `TypeError` — an integer and a string cannot be added with the `+` operator.

Next is `NameError`:

```python
print('There is no problem with this line')
print(x ** 2)
```

```output
There is no problem with this line
Traceback (most recent call last):
  File "main.py", line 2, in <module>
    print(x ** 2)
NameError: name 'x' is not defined
```

The first line prints correctly because the interpreter executes code top to bottom. A `NameError` occurs when referencing a variable that has not been defined. Referencing variables is covered in the next chapter.

#### Wrong Code Snippets

Incorrect code examples are demonstrated this way:

```python
##### Alarm! Wrong code snippet! #####

# Incorrect code will go here #

##### Alarm! Wrong code snippet! #####
```

## Lesson 1.5 — Strings: Quotes, Length, Operations, Escapes {: #ch-1-lesson-5 }

### Quotes: single, double and triple

A string is any sequence of characters wrapped in single or double quotes. Example strings include:

```python
"this is a string"
'this is also a string'
'1 + 1 = 2'
"!, ?, _, @ are special characters"
"if you need to use apostrophe ('), you can use double quotes"
```

Be consistent in choosing single or double quotes. Python also supports triple quotes (`'''`), which are especially useful for multi-line strings. To capture these three lines in one string:

```output
first line
second line
third line
```

This code produces a `SyntaxError`:

```python
x = 'first line
second line
third line'
print(x)
```

Triple quotes solve this:

```python
x = '''first line
second line
third line'''
print(x)
```

Typing `x` in the console after running gives:

```output
'first line\nsecond line\nthird line'
```

The `\n` is a newline character (see the escape characters section).

### Length

Length is the number of characters in a string, found with the built-in `len` function:

```python
x = 'good'
print(len(x))
```

This outputs `4`. Unlike C, Python has no separate character type — "A character in Python is represented by a string of length 1." Examples of length-1 strings:

```python
x = 'a'
y = 'b'
```

Empty strings are also allowed:

```python
x = ''
print(len(x))
```

The empty string has length 0.

### Operations on strings

#### Concatenation

Concatenation joins strings using the `+` operator — "just a fancy term for joining two strings together":

```python
string1 = 'first'
string2 = ','
string3 = 'second'
string4 = string1 + string2 + string3
print(string4)
```

```output
first,second
```

#### Replication

The `*` operator makes and joins multiple copies of a string:

```python
s = 'good'
five_s = s * 5
print(five_s)
```

```output
goodgoodgoodgoodgood
```

This demonstrates the adage "multiplication is repeated addition":

```python
s = 'good'
s * 5 == s + s + s + s + s  # This expression evaluates to True
```

#### Comparison

Strings can be compared, starting with the `==` operator:

```python
x = 'python'
print(x == 'python', x == 'nohtyp')
```

```output
True False
```

Two strings are equal "if and only if both of them represent exactly the same sequence of characters." Next:

```python
print('good' > 'bad')
print('nine' < 'one' )
print('a' < 'ab' < 'abc' < 'b')
```

```output
True
True
True
```

These examples show that length is not the comparison metric; instead Python uses alphabetical ordering, more precisely **lexicographic ordering**.

!!! note "Lexicographic ordering"

    "The first characters from the two strings are compared. If they differ this determines the outcome of the comparison. If they are equal, then the second character of both the strings are compared. This process continues until either string is exhausted."

For comparing characters, "Python's string type uses the Unicode standard for representing characters." Unicode is a specification listing every character used by human languages, giving each a unique code. Characters are represented by **code points**, and a code point value is an integer used for ordering.

The built-in `ord` function returns a character's code point:

```python
print(ord('a'), ord('b'))
print(ord('a'), ord('A'))
```

```output
97 98
97 65
```

This shows why `'a' < 'b'` is `True` (97 < 98), and lets us infer `'A' < 'a'` returns `True`.

### Escape characters

The backslash `\` is the escape character, used partly to represent whitespace like tabs and newlines:

```python
print('This is the first sentence.\nThis is the second sentence.')
```

```output
This is the first sentence.
This is the second sentence.
```

`\n` is a newline character. Though it looks like two characters, "`\n` is still regarded as a single character." Verify with:

```python
x = '\n'
print(len(x))
```

This outputs `1`. The tab character is `\t`:

```python
print('a\tb')
```

```output
a	b
```

Quotes can be escaped with `\'`, useful for apostrophes in single-quoted strings:

```python
print('India\'s capital is New Delhi')
```

```output
India's capital is New Delhi
```

Remove the backslash and predict why an error occurs.

### Substrings

A substring is a string contained within another — for example `'good'` is a substring of `'very good'`, but `'very good'` is not a substring of `'verygood'`. The `in` keyword checks for substrings:

```python
a = 'good'
b = 'very good'
present = a in b
print(present)
not_present = b in a
print(not_present)
```

```output
True
False
```

`in` is "a powerful keyword which has several other uses" and can combine with `not`:

```python
a = 'abc'
b = 'ab'
print(a not in b)
```

```output
True
```

## Lesson 1.6 — Strings: Indexing, Slicing, Immutability, Methods {: #ch-1-lesson-6 }

This lesson recaps prior string operations and introduces the sequential nature of strings, serving as a lead-in to lists, along with string methods. The earlier operations covered include finding length with `len`, concatenation with `+`, replication with `*`, comparison using relational operators like `>`, `<`, `==`, and use of the `in` keyword.

### Indexing

A string is a sequence of characters, and sequences support indexing. Using "world" as an example, 'w' is the first letter, 'o' the second, and so on. The index formally denotes an element's position, and computer science widely uses zero-based numbering starting from 0.

```python
word = 'world'
print(word[0])
print(word[1])
print(word[2])
print(word[3])
print(word[4])
```

```output
w
o
r
l
d
```

`word[i]` gives the character at index `i`, informally the letter at position `i + 1`.

```python
word = 'world'
print(word[5])
```

```output
Traceback (most recent call last):
  File "main.py", line 2, in <module>
    print(word[5])
IndexError: string index out of range
```

The interpreter throws an `IndexError` because index 5 is out of range; the last character is at index 4.

```python
word = 'world'
print(word[-1])
```

```output
d
```

Python supports negative indexing. The lesson offers an analogy: descending a staircase where, upon reaching the last step, "some invisible hand magically transports you back to the top most step." This is likened to the Penrose stairs. An index of `-1` points to the last element, moving backward to `-5` for the first.

```python
word = 'world'
print(word[-1])
# ... please add the remaining lines!
print(word[-5])
```

Unlike the Penrose stairs, this cannot repeat forever — `print(word[-6])` throws an `IndexError`.

### Slicing

Slicing extracts a substring using the slice operator. The lesson uses an example of IIT-M email ids of the form:

> branch_year_number@iitm.ac.in

Each branch has a two-letter code (`CS` for Computer Science, `ME` for Mechanical Engineering), followed by a two-digit joining year, then a three-digit roll number. Sample email ids:

```output
CS_10_014@iitm.ac.in
ME_11_123@iitm.ac.in
BT_17_001@iitm.ac.in
```

```python
email = 'CS_10_014@iitm.ac.in'
roll = email[6 : 9]
print(roll)
```

The `start:stop` operator is "our knife in slicing sequences." To extract `014` at indices 6, 7, 8, you start at index 6 and stop before index 9 — the character at `stop` is excluded.

```python
email = 'CS_10_014@iitm.ac.in'
branch = email[0 : 2]
year = email[3 : 5]
roll = email[6 : 9]
college = email[10 : 14]
# Print each one of them and check the output
```

```python
email = 'CS_10_014@iitm.ac.in'
in_roll = email[ : 9]
print(in_roll)
```

This outputs `CS_10_014`. When no start is given, it defaults to 0; when no stop is given, it defaults to the end of the string, i.e. `len(email)`.

```python
email = 'CS_10_014@iitm.ac.in'
domain = email[-10 : ]
print(domain)
```

This outputs `iitm.ac.in`, combining negative indexing and slicing.

```python
word = 'world'
print(word[-4 : 3])
print(word[1 : -2])
```

### Immutability

```python
word = 'some string'
word[0] = 'S'
```

The interpreter throws a `TypeError` with the message `'str' object does not support item assignment`. An object is mutable if it can be changed, immutable if it cannot. Strings are **immutable**, so characters cannot be modified **in-place**.

This differs from reassignment:

```python
word = 'some string'
word = 'Some string'
```

Here, `word` is assigned an entirely new string literal rather than modified in place. There are two distinct literals — `'some string'` and `'Some string'` — and the former is not transformed into the latter. Mutable and immutable objects are explored further in chapter 5.

### Methods

The problem posed: accept a sentence and output it with the first letter capitalized. For input `'this is a chair.'`, the output should be `'This is a chair.'`.

```python
sentence = input()
cap_sentence = sentence.capitalize()
print(cap_sentence)
```

`capitalize` is a *method* — a function defined for a specific object (here, the `str` type) and called using that object. Calling it on an `int` produces an error:

```python
##### Alarm! Wrong code snippet!
a = 1
a.capitalize()
##### Alarm! Wrong code snippet!
```

`sentence.capitalize()` returns a string, which is assigned to `cap_sentence`. Another problem: check whether a string is a valid person's name. Assuming a name has only alphabets without special characters or numbers, the `isalpha` method checks this:

```python
# name is some pre-defined string
valid = name.isalpha()
print(valid)
```

`name.isalpha()` returns a boolean — `True` if every character is alphabetic and the string is non-empty, `False` otherwise. A comprehensive list of string methods is available in the Python documentation (docs.python.org, Standard Types — String Methods).
