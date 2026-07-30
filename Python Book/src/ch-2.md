<section class="opener" id="ch-2">
<span class="chapter-num">2</span>

# Conditionals
<span class="accent-rule"></span>
</section>

## Lesson 2.1 — Variables, Assignment and Dynamic Typing {: #ch-2-lesson-1 }

### Introduction

Variables are containers used to store values. In Python, they are defined using the assignment operator `=`.

```python
x = 1
y = 100.
z = "good"
```

Variables can also be updated with the assignment operator:

```python
x = 1
print('The initial value of x is', x)
x = 2
print('The value after updating x is', x)
```

```output
The initial value of x is 1
The value after updating x is 2
```

### Assignment Operator

The syntax of an assignment statement is:

```python
variable_name = expression
```

The operator works right to left — the right-hand expression is evaluated first, then its value is assigned to the left-hand variable.

```python
x = 1 + 2 * 3 / 2
print(x)
```

```output
4.0
```

Placing a literal on the left of the operator causes an error:

```python
##### Alarm! Wrong code snippet! #####
3 = x
##### Alarm! Wrong code snippet! #####
```

```output
SyntaxError: cannot assign to literal
```

The assignment statement binds the name on the left to an object on the right. Consider a sequence where, after line 1, `x` binds to the `int` `8`; a trailing period on line 2 makes `10` a `float`, so `x` holds `18.0`. On the next line `y = x` makes both names bind to the same object. When `x` is later reassigned, it binds to a new object, but `y` remains bound to `18.0`.

Do not confuse assignment with equality:

```python
x = 2   # this is the assignment operator
x == 2  # this is the equality operator
```

Assignment creates or updates variables; equality compares two expressions. They are not interchangeable.

!!! note "Dynamic Typing"

    Python is dynamically typed. A variable is "a value bound to a name" where the value has a type but the variable itself does not.

```python
a = 1
print(type(a))
a = 1 / 2
print(type(a))
a = "IIT Madras"
print(type(a))
```

```output
<class 'int'>
<class 'float'>
<class 'str'>
```

Here `a` starts as an `int`, becomes a `float`, and then a `str`.

### Referencing versus Defining

Using an already-defined variable in an expression is called referencing.

```python
x = 2
print(x * x, 'is the square of', x)
```

The second line references `x` from the first. Referencing a variable before assigning it raises a `NameError`:

```python
print(someVar)
```

```output
NameError: name 'someVar' is not defined
```

### Keywords and Naming Rules

Keywords are reserved words with special meaning. Some of them are:

```python
not, and, or, if, for, while, in, is, def, class
```

We have already seen `not`, `and`, `or`; the rest appear in later chapters. Keywords cannot be variable names:

```python
##### Alarm! Wrong code snippet! #####
and = 2
##### Alarm! Wrong code snippet! #####
```

Other naming rules:

- A variable name may only contain alphanumeric characters and underscores:
    - a – z
    - A – Z
    - 0 – 9
    - `_`
- A name must start with a letter or underscore.

Observations that follow:

- A name cannot start with a number.
- Names are case-sensitive (`age`, `Age`, `AGE` are three different variables).

These are rules, not conventions — violating them raises a `SyntaxError`.

```python
##### Alarm! Wrong code snippet! #####
3a = 1
##### Alarm! Wrong code snippet! #####
```

```output
SyntaxError: invalid decimal literal
```

### Reusing Variables

Variables can help compute other variables — common in programming and data science. Given the equations y = x² and z = (x+1)(y+1), evaluated at x = 10:

```python
x = 10
y = x ** 2
z = (x + 1) * (y + 1)
```

### Multiple Assignment

Consider defining two variables:

```python
x = 1
y = 2
```

Python allows a compact single-line form. This assigns 1 to `x` and 2 to `y`:

```python
x, y = 1, 2
```

Order matters — this assigns 2 to `x` and 1 to `y`:

```python
x, y = 2, 1
```

This works through tuple packing and unpacking (covered in Chapter 5). You can also initialize several variables to the same value:

```python
x = y = z = 10
print(x, y, z)
```

```output
10 10 10
```

The equality breaks as soon as any one is updated:

```python
x = x * 1
y = y * 2
z = z * 3
print(x, y, z)
```

```output
10 20 30
```

### Assignment Shortcuts

Run this and observe the output:

```python
x = 1
x += 1
print(x)
```

`+=` is new: `x += a` increments `x` by `a` — it adds `a` to `x` and stores the result in `x`. It is equivalent to `x = x + a`. This applies to other operators too:

| Shortcut | Meaning |
|----------|---------|
| `x += a` | `x = x + a` |
| `x -= a` | `x = x - a` |
| `x *= a` | `x = x * a` |
| `x /= a` | `x = x / a` |
| `x %= a` | `x = x % a` |
| `x **= a` | `x = x ** a` |

The arithmetic operator must come before the assignment operator. Swapping will not work:

```python
x = 1
x =+ 1
print(x)
```

This outputs `1` because `+` is treated as a unary operator. Statements like `x =* 1` or `x =/ 2` cause errors.

### Deleting Variables

Variables can be removed with the `del` keyword:

```python
x = 100
print('x is a variable whose value is', x)
print('we are now going to delete x')
del x
print(x)
```

The last line raises a `NameError` because `x` was deleted, so accessing it afterward fails.

!!! note "Note"

    Python is both dynamically typed and strongly typed.

## Lesson 2.2 — Input, Type Conversion and Built-in Functions {: #ch-2-lesson-2 }

### Input

This lesson covers accepting user input, which is a routine part of programming. Any software given to a customer needs a functional interface for user interaction. Apps like Facebook, Instagram, and Twitter regularly accept input, even though we rarely view it through a programming lens. For instance, when commenting on a Facebook post, the comment text is the input, and backend code processes it and displays it attractively.

Python's built-in `input()` function accepts user input — "a simple yet powerful function":

```python
x = input()
print('The input entered by the user is', x)
```

When run, the interpreter waits for text in the console. Pressing Enter signals that input is complete, and the text is stored in `x`.

```repl
1
The input entered by the user is 1
```

You can prompt the user by passing an instruction as an argument:

```python
x = input('Enter an integer between 0 and 10: ')
print('The number entered by the user is', x)
```

To inspect the variable's type:

```python
x = input()
print('The input entered by the user is of type', type(x))
```

Try `int`, `float`, `str`, and `bool` inputs. The key point: `input()` always returns a string. Even entering `123` is processed as the string `'123'`. To accept an integer, we use type conversion.

### Type Conversion

To convert a string into an integer, Python provides `int()`:

```python
x = '123'
print('The type of x is', type(x))
y = int(x)
print('The type of y is', type(y))
```

The third line converts an object of type `str` into type `int`. The reverse works too, using `str()`:

```python
x = 123
print('The type of x is', type(x))
y = str(x)
print('The type of y is', type(y))
```

To accept an integer, take a string first and convert it:

```python
x = input('Enter an integer: ')
x = int(x)
print('The integer entered by the user is', x)
```

This can be shortened to a single line:

```python
x = int(input())
print('The integer entered by the user is', x)
```

The first line composes two functions — passing the output of the inner `input()` as input to the outer `int()`. If a float value is entered:

```python
x = int(input())    # user enters a float value here
```

This throws a `ValueError`. For example, `int('1.23')` fails because the value in quotes is a float, not an int, so it cannot be converted.

### Built-in Functions

The term **built-in functions** refers to functions that are already defined. Loosely, a function in Python is an object that takes inputs and produces outputs — for example, `print()` accepts input and prints it to the console.

A few more useful functions:

- `round()` takes a number and returns the nearest integer. `round(1.2)` returns `1`, `round(1.9)` returns `2`.
- `abs()` returns the absolute value. `abs(-1.2)` returns `1.2`.
- `int()` is more involved. An integer in a string returns that integer: `int('123')` is `123`. A float has its decimal part discarded: `int(1.2)` returns `1` and `int(-2.5)` returns `-2`. A float passed as a string throws a `ValueError`. `int('2.5')` gives:

```output
ValueError: invalid literal for int() with base 10: '2.5'
```

- `pow()`: `pow(x, y)` returns x raised to the power y, the same as the `**` operator. Generally `**` is faster, but the difference is negligible for small numbers, and `pow()` improves readability. With a third argument, `pow(x, y, z)` returns x^y mod z — the remainder when x^y is divided by z.
- `isinstance()` checks whether an object is of a specified type. `isinstance(3, int)` returns `True` since `3` is an `int`. The first argument can be any object; if `x` is a `str`, then `isinstance(x, str)` returns `True`.

The Python documentation (docs.python.org, Built-in Functions) provides an exhaustive list of built-in functions.

## Lesson 2.3 — Conditional Statements {: #ch-2-lesson-3 }

This lesson introduces conditional statements using a motivating problem: accept an integer, then print `positive` if it is greater than zero, `negative` if less than zero, or `zero` otherwise. Conditional statements are a fundamental building block in computer science that allow code to execute conditionally.

### if statement

A simpler version first: accept an integer and print `non-negative` if it is greater than zero. The `if` keyword is followed by a boolean expression called the **condition**. If the condition is `True`, the indented body runs; otherwise it is skipped.

```python
x = int(input())
if x >= 0:
    print('non-negative')
```

Indentation matters and must be consistent — the first level uses four spaces. Consider two examples of the **if-block**.

Positive `x`:

```python
# Left
x = 1
if x >= 0:
    print('non-negative')
    print('inside if')
print('outside if')
```

Since the condition is `True`, the indented lines run:

```output
non-negative
inside if
outside if
```

Negative `x`:

```python
# Right
x = -1
if x >= 0:
    print('non-negative')
    print('inside if')
print('outside if')
```

Here the condition is `False`, so the body is skipped:

```output
outside if
```

### if-else

Next problem: print `non-negative` if the number is ≥ zero, else print `negative`. The `else` keyword runs its body when the if-condition is `False`.

```python
x = int(input())
if x >= 0:
    print('non-negative')
else:
    print('negative')
```

Points to remember:

- `if` and `else` are at the same indentation level.
- `else` can never occur independently of an `if`.
- `else` cannot have a new condition attached.

Example of **wrong code** demonstrating the last two points:

```python
##### Alarm! Wrong code snippet! #####
else:
    print(1)
##### Alarm! Wrong code snippet! #####

##### Alarm! Wrong code snippet! #####
x, y = 1, 2
if x >= y:
    print(1)
else x < y:
    print(1)
##### Alarm! Wrong code snippet! #####
```

### if-elif-else

The `elif` keyword is shorthand for else-if, solving the original problem:

```python
x = int(input())
if x > 0:
    print('positive')
elif x == 0:
    print('zero')
else:
    print('negative')
# End of code
```

Table of inputs and outputs:

| Input | Output |
|--------|----------|
| x = 1 | positive |
| x = 0 | zero |
| x = -1 | negative |

The block has three sub-blocks: the if-block, the elif-block, and the else-block. The interpreter checks the if-condition first; if `True`, its body runs, then control jumps past the block. If `False`, it checks the elif; if that is `True`, its body runs then jumps past the block. If the elif is `False`, the else runs.

General syntax:

```python
if <condition_1>:
    <statement_1>
elif <condition_2>:
    <statement_2>
else:
    <statement_3>
```

Features to note:

- Exactly one of the three statements runs.
- Once an `if` or `elif` condition is `True`, its body runs and flow exits the whole block.
- There can be multiple `elif` conditions after the `if`.
- An `else` cannot come before an `elif`; the final `else` is optional but must come last if present.

### Nested conditional statements

Problem: accept three distinct integers; print `in ascending order` if entered in ascending order, else `not in ascending order`.

An **incomplete** solution:

```python
# Incomplete solution
x = int(input())
y = int(input())
z = int(input())
if x < y:
    print('in ascending order')
else:
    print('not in ascending order')
```

This fails to check whether `y < z`, so an input like `x, y, z = 1, 3, 2` wrongly prints `in ascending order`. The complete solution:

```python
x = int(input())
y = int(input())
z = int(input())
if x < y:
    if y < z:
        print('in ascending order')
    else:
        print('not in ascending order')
else:
    print('not in ascending order')
```

Each new if block's body must be indented one level relative to its condition. Placing one conditional inside another is called **nesting**: the outer block contains the inner block. Each `else` pairs with the `if` at the same indentation level.

### Defining variables inside if

Consider this code:

```python
x = int(input())
if x % 5 == 0:
    output = 'the number is divisible by 5'
print(output)
```

Running it with different inputs reveals: when the input is a multiple of 5, it runs fine; otherwise it raises a `NameError`. This happens because the variable `output` is only created if the assignment line executes at run-time — its presence in the source code alone is not enough to define it.

## Lesson 2.4 — System Libraries: calendar, time, this {: #ch-2-lesson-4 }

### Library

A library is a collection of functions sharing a common theme. This is a loose definition that becomes clearer once you begin working with a library directly.

### `calendar`

Consider this problem: in the year 3000, on which day of the week will the 15th of August fall? Python solves it easily:

```python
import calendar
calendar.prmonth(3000, 8)
```

```output
    August 3000
Mo Tu We Th Fr Sa Su
             1  2  3
 4  5  6  7  8  9 10
11 12 13 14 15 16 17
18 19 20 21 22 23 24
25 26 27 28 29 30 31
```

The 15th falls on a Friday — accomplished in just two lines. `calendar` is one of many libraries in Python's standard library. Here, `calendar` names the library and `import` is the keyword used to bring it into the code.

`calendar` groups together functions related to calendars, and `prmonth()` is one of them. It takes `<year>` and `<month>` and displays that month's calendar. You must import the library before using its functions. Here is what happens if you skip that step:

```python
# import calendar
calendar.prmonth(3000, 8)
```

```output
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
NameError: name 'calendar' is not defined
```

To reach a function inside a library, use this syntax:

```python
<calendar>.<function>(<arguments>)
```

Another approach uses the `weekday` function:

```python
import calendar
print(calendar.weekday(3000, 8, 15))
```

The output is `4`. Days map to numbers as follows:

| Day | Number |
|-----|--------|
| Monday | 0 |
| Tuesday | 1 |
| Wednesday | 2 |
| Thursday | 3 |
| Friday | 4 |
| Saturday | 5 |
| Sunday | 6 |

### `time`

Now a hypothetical scenario: you are stranded on an island in the Indian Ocean with a device running only a Python interpreter, and you want the current date and time.

```python
from time import ctime
print('The current time is:', ctime())
```

```output
The current time is: Fri Apr  2 12:24:43 2021
```

The import statement on the first line looks different because `from` is a new keyword. That line essentially says: from the `time` library, import the `ctime` function. This style is handy when you need only one or two functions from a library.

```python
from time import ctime, sleep
print('Current time is:', ctime())
print('I am going to sleep for 10 seconds')
sleep(10)
print('Current time is:', ctime())
```

`sleep(x)` is a `time` function that pauses program execution for `x` seconds. If you plan to use many functions from a library, it is a poor idea to import each one separately — better to import the whole library instead.

### `this`

As a fun exercise, try:

```python
import this
```

```output
The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
```

These are nuggets of wisdom from Tim Peters, a major contributor to the Python programming language. Some points, like "readability counts," make immediate sense.
