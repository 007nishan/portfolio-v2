<section class="opener" id="ch-4">
<span class="chapter-num">4</span>

# Functions
<span class="accent-rule"></span>
</section>

## Lesson 4.1 — Functions: Introduction and Examples {: #ch-4-lesson-1 }

### Introduction

In math, a function takes inputs and produces outputs — for example, f(x) = x² squares a number. Python functions serve a similar role but are far richer. Here is the mathematical function converted to Python:

```python
def f(x):
    y = x ** 2
    return y
```

This is the **definition** of function `f`. The `def` keyword defines functions, `f` is the name, and `x` is a parameter. The indented lines form the body — a set of statements describing what the function does. The last line returns the value in `y` using the `return` keyword.

Running this produces no output, because functions only run when called. A **function call** looks like this:

```python
def square(x):
    y = x ** 2
    return y
print(square(2))
```

```output
4
```

Here `square(2)` is a function call. The `x` in the definition is the **parameter**; the value passed in the call (here, 2) is the **argument**. This convention holds throughout the lesson.

A mental model for understanding functions:

- Parameters are the function's inputs.
- The body is the sequence of steps transforming input into output.
- The return statement communicates the output to the rest of the code.

### Examples

The following examples focus on syntactical aspects of function definitions.

Functions could have multiple parameters:

```python
# This function computes the area of a rectangle.
# Length and breadth are the parameters
def area(l, b):
    return l * b
```

Functions could have no parameters:

```python
def foo():
    return "I don't like arguments visiting me!"
```

Functions could have no return value:

```python
def foo():
    print("I don't like talking to the outside world!")
foo()
```

```output
I don't like talking to the outside world!
```

Note that you did not need `print(foo())` — just calling `foo()` works since the print statement is already inside. But what if you type `print(foo())`?

```output
I don't like talking to the outside world!
None
```

If no explicit return statement is present, `None` is the default return value. The interpreter first evaluates `foo()` (producing the first output line), and since it has no explicit return, it returns `None` (the second output line).

A minimal Python function looks like:

```python
def foo():
    pass
```

`pass` is a keyword; when the interpreter reaches it, it performs no computation and moves on. This is minimal because it has only the essentials for a syntactically valid definition: a name and at least one body statement. Such functions have their place. While writing complex code, a coder may realize they need a function for a task but not know the implementation details. They add a minimal named function as a to-do item, implementing it when the need arises.

Functions could have multiple return statements, but the first executed return exits the function:

```python
def foo():
    return 1
    return 2
```

`foo()` always returns 1; the last line is redundant. A non-redundant example:

```python
def evenOrOdd(n):
    if n % 2 == 0:
        return 'even'
    else:
        return 'odd'
print(evenOrOdd(10))
print(evenOrOdd(11))
```

```output
even
odd
```

With an even argument, the first return runs; with an odd argument, the else return runs.

Functions could return multiple values:

```python
# Accept only positive floating point numbers
def bound(x):
    lower = int(x)
    upper = lower + 1
    return lower, upper
y = 7.3
l, u = bound(y)
print(f'{l} < {y} < {u}')
```

The exact mechanism will become clear in the lesson on tuples. Here the first returned value goes into `l` and the second into `u`.

Functions must be defined before being called; the call cannot precede the definition:

```python
##### Alarm! Wrong code snippet! #####
print(f(5))
def f(x):
    return x ** 2
##### Alarm! Wrong code snippet! #####
```

This throws a `NameError`. The interpreter executes top to bottom; at the call line, `f` is a name never seen before, so it raises a `NameError` — which occurs when referencing a name the interpreter has not seen.

Function calls could be used in expressions:

```python
def square(a):
    return a ** 2
x, y, z = int(input()), int(input()), int(input())
if square(x) + square(y) == square(z):
    print(f'{x}, {y} and {z} form the sides of a right triangle with {z} as the hypotenuse')
```

Function calls cannot be assigned values:

```python
##### Alarm! Wrong code snippet! #####
def foo():
    return True
foo() = 1
##### Alarm! Wrong code snippet! #####
```

This throws a `SyntaxError`.

Functions can be called from within other functions:

```python
def foo():
    print('I am inside foo')
def bar():
    print('I am inside bar')
    print('I am going to call foo')
    foo()
print('I am outside both foo and bar')
bar()
print('I am outside both foo and bar')
```

Functions can be defined inside other functions:

```python
def foo():
    def bar():
        print('bar is inside foo')
    bar()
foo()
```

Try calling `bar()` outside `foo()`. What do you observe?

### Docstrings

Consider this function:

```python
def square(x):
    """Return the square of x."""
    return x ** 2
```

The string just below the function definition is a docstring. From the Python docs:

> "A docstring is a string literal that occurs as the first statement in a module, function, class, or method definition."

Such a docstring becomes the `__doc__` special attribute of that object. Ignore unfamiliar terms like "module" and "class" for now and focus on functions. Adding docstrings is good practice. It may not be needed for simple, obvious functions, but as function complexity grows, docstrings can be a lifesaver for other programmers reading your code.

The docstring can be accessed via the `__doc__` attribute:

```python
print(square.__doc__)
```

This gives `Return the square of x.` as output.

## Lesson 4.2 — Arguments and Call by Value {: #ch-4-lesson-2 }

### Arguments

Python provides several ways for passing arguments to functions.

#### Positional arguments

Every function shown so far has relied on positional arguments, where an argument's position in the call determines which parameter receives it. Consider this problem: write a function taking three positive integers `x`, `y`, and `z`, returning `True` when they form a right triangle with legs `x` and `y` and hypotenuse `z`, else `False`.

```python
def isRight(x, y, z):
    if x ** 2 + y ** 2 == z ** 2:
        return True
    return False
print(isRight(3, 4, 5)) # 3 is passed to x, 4 is passed to y, 5 is passed to z
print(isRight(5, 4, 3)) # 5 is passed to x, 4 is passed to y, 3 is passed to z
```

```output
True
False
```

Arguments bind to parameters based on their position in the call. Positional arguments are also known as required arguments — they cannot be omitted, and supplying too many raises an error. There must be exactly as many arguments as parameters. Run this and note the error:

```python
##### Alarm! Wrong code snippet!
isRight(3, 4)
isRight(3, 4, 5, 6)
##### Alarm! Wrong code snippet!
```

#### Keyword arguments

Keyword arguments add flexibility. Reusing the same problem with modified calls:

```python
# The following is just a function call.
# We are not printing anything here.
isRight(x = 3, y = 4, z = 5)
```

Here the parameter names are stated explicitly and values assigned with `=`. A benefit is that it lowers the chance of ordering arguments incorrectly:

```python
isRight(3, 4, 5)    # intended call
isRight(5, 4, 3)    # actuall call
isRight(x = 3, y = 4, z = 5) # same as intended call
isRight(z = 5, y = 4, x = 3) # same as intended call
```

Keyword and positional arguments can be mixed in one call:

```python
isRight(3, y = 4, z = 5)
```

Now try this:

```python
#### Alarm! Wrong code snippet! ####
isRight(x = 3, 4, 5)
#### Alarm! Wrong code snippet! ####
```

The interpreter raises a `TypeError` reading `positional argument follows keyword arguments`. The positional arguments `4` and `5` appear after the keyword argument `x = 3`. Whenever both types are present, keyword arguments must come last — sensible, since positional arguments depend heavily on position and belong at the front.

What about this call?

```python
#### Alarm! Wrong code snippet! ####
isRight(3, x = 3, y = 4, z = 5)
#### Alarm! Wrong code snippet! ####
```

This raises a `TypeError`: `isRight() got multiple values for argument x`. Each parameter needs exactly one argument — no more, no less — supplied either positionally or as a default, but not both.

#### Default arguments

Imagine a neighborhood map where grid lines are roads for cars. To go from point *O* to point *P* on foot, the shortest path is straight along line *OP*, the **Euclidean distance**. In a car you must follow the grid, covering *OM + MP*, the **Manhattan distance**.

Suppose a self-driving car startup uses both metrics, calling Euclidean distance 10 times and Manhattan 1000 times. Representing them as functions makes sense:

```python
# Assume that O is the origin
# All distances are computed from the origin
def euclidean(x, y):
    return pow(x ** 2 + y ** 2, 0.5)

def manhattan(x, y):
    return abs(x) + abs(y)
```

This code works but ignores that Manhattan is used a hundred times more often. Default arguments help:

```python
def distance(x, y, metric = 'manhattan'):
    if metric == 'manhattan':
        return abs(x) + abs(y)
    elif metric == 'euclidean':
        return pow(x ** 2 + y ** 2, 0.5)
```

The `metric` parameter defaults to `'manhattan'`. Calling without passing `metric`:

```python
print(distance(3, 4))
```

This gives `7`. With no value provided, the default `'manhattan'` was used. Anywhere the Manhattan distance is needed, `distance(x, y)` can replace it.

Key points to remember:

- Parameters assigned a value in the definition are called default parameters.
- Default parameters always come at the end of the parameter list in a definition.
- The argument for a default parameter is optional in a call.
- Such an argument may be passed positionally or as a keyword argument.

Illustrating these:

```python
#### Alarm! Wrong code snippet! ####
def distance(metric = 'manhattan', x, y):
    if metric == 'manhattan':
        return abs(x) + abs(y)
    elif metric == 'euclidean':
        return pow(x ** 2 + y ** 2, 0.5)
#### Alarm! Wrong code snippet! ####
```

This raises a `SyntaxError`: `non-default argument follows default argument`. The default parameter must come last. Different valid ways of passing arguments with defaults:

```python
distance(3, 4)
distance(3, 4, 'manhattan')
distance(3, 4, metric = 'manhattan')
```

All three calls are equivalent: the first uses the default, the second passes `'manhattan'` positionally, and the third passes it as a keyword argument.

### Call by value

Consider this code:

```python
def double(x):
    x = x * 2
    return x
a = 4
print(f'before function call, a = {a}')
double(a)
print(f'after function call, a = {a}')
```

```output
before function call, a = 4
after function call, a = 4
```

The value of `a` is unaffected by the function. When `double(a)` runs, the value in `a` is assigned to parameter `x` — arguments are passed by assignment in Python, so effectively `x = a` occurs. Passing a variable's value like this is called **call by value**.

Consider the following code:

```python
def square(x):
    return x * x
x = 10
x_squared = square(x)
```

Using the same name for the function parameter and the passed argument is poor practice. It is better to differentiate their names to avoid confusion and improve readability. How the inner `x` relates to the outer `x` will be covered in the next lesson on scopes. The code can be rewritten as:

```python
def square(num):
    return num * num
x = 10
x_squared = square(x)
```

## Lesson 4.3 — Scope, Namespaces, locals and globals {: #ch-4-lesson-3 }

### Scope

Consider a function `foo()` that assigns `x = 1` internally and prints messages, then calls `foo()` and tries `print(x)` from outside. This produces a `NameError` because `x` exists only inside the function.

The key idea: the region of code where a name can be referenced is its **scope**. Referencing a variable outside its scope raises a `NameError`.

### Local vs Global

When `x` is assigned inside a function, its scope is **local** — it only exists inside that function. The textbook uses a memorable metaphor comparing functions to black holes that do not let variables escape.

By contrast, a variable `y = 10` defined in the main program is **global** and can be referenced from anywhere (including inside functions) after being defined. There is a caveat: if a same-named variable is defined inside the function, behavior changes.

The rules (adapted from the Python FAQ) state that assigning a value to a variable anywhere in a function makes it local, while a variable only *referenced* (never assigned) inside a function is treated as global.

Function parameters are also local — `double(x)` with `print(x)` outside will raise a `NameError`.

### Examples

**Variant-1** defines `y = 10` after the function definition but before calling `foo()` — this works fine. What matters is that `y` is defined before the call.

**Variant-2** defines `y = 10` *after* calling `foo()`, which raises a `NameError` since `y` is not defined yet at call time.

A trickier case uses `x = 10` inside `foo` and `x = 100` outside:

```output
x inside foo = 10
x outside foo = 100
```

These are different variables. The inside `x` is local (assigned in the function); the outside `x` is global and inaccessible from within `foo`.

### Namespaces

To understand name resolution, the lesson introduces namespaces. A namespace is a lookup table — specifically a dictionary — mapping names to objects.

#### globals()

Variables defined in the main program live in the `globals` namespace. Calling `print(globals())` shows names like `x`, `avar`, and `foo` mapped to their objects. Functions map to something like `<function foo at 0x7f8ecd2aa1f0>`, where the hex value is the memory location of the definition.

You can also check membership:

```python
print('x' in globals())
print('avar' in globals())
print('foo' in globals())
```

All three print `True`.

#### locals()

A variable `y` assigned inside a function is not in `globals`. `print('y' in globals())` returns `False`. The interpreter creates a separate **local namespace** each time a function is called:

```python
def foo():
    y = 2.0
    print('Is y in locals?', 'y' in locals())

foo()
print('Is y in globals?', 'y' in globals())
```

```output
Is y in locals? True
Is y in globals? False
```

### Scope and Namespaces

For every function call, a local namespace holds the names and objects defined in that function:

```python
def foo():
    print(y)
    print(locals())
    x = 1
    print(locals())

y = 10
foo()
```

```output
10
{}
{'x': 1}
```

Since `y` is only referenced, it stays global; `x` is assigned so it enters the local namespace. When control exits the function, its namespace is deleted.

**Name resolution protocol** (the interpreter checks in order):

- First the local namespace for that call; if present, use that value.
- Otherwise the global namespace; if present, use that value.
- Otherwise the `built-in` namespace (covered at the end).
- If found nowhere, raise a `NameError`.

Revisiting the earlier example: when `foo()` is called, a local namespace is created; `x` enters it at assignment; the reference uses the local value `10`; after exit, the namespace is deleted; and the final line uses the global `100`.

### `global` keyword

Consider:

```python
def foo():
    print(x)
    x = x + 1

x = 10
foo()
```

This raises `UnboundLocalError: local variable 'x' referenced before assignment`. Because `x` is assigned in the function, it is local, so referencing it before assignment fails. The outer `x = 10` does not count since it is global.

To reuse the global `x` inside the function, use the `global` keyword:

```python
def foo():
    global x
    print(f'x inside foo = {x}')
    x = x + 1
    print(f'x inside foo = {x}')

x = 10
print(f'x outside foo = {x}')
foo()
```

```output
x outside foo = 10
x inside foo = 10
x inside foo = 11
```

Declaring `x` as global means no new local variable is created despite the assignment.

### Built-ins

Built-in functions like `print`, `int`, and `input` are also names, resolved at runtime, defined in a separate `builtins` namespace.

This runs without error (but should not be done):

```python
##### Never do something like this! #####
print = 1
##### Never do something like this! #####
```

Syntactically it is valid. However:

```python
##### Alarm! Wrong code snippet! #####
print = 1
print(1)
##### Alarm! Wrong code snippet! #####
```

This throws a `TypeError` because the name `print` was reassigned to an `int`.

The built-in namespace is the final stage of name resolution.

!!! warning "Warning"

    Using a built-in name as a variable is "a very bad practice that should be avoided at any cost!"

## Lesson 4.4 — Recursion and Caution in Recursion {: #ch-4-lesson-4 }

### Function calling Function

This lesson explores how functions can call other functions, and introduces recursion. Here is a program demonstrating chained function calls:

```python
def first():
    second()
    print('first')

def second():
    third()
    print('second')

def third():
    print('third')

first()
```

```output
third
second
first
```

The lesson introduces a visualization approach called the **traffic-signal method**. A simple function (one that calls no other functions) can be in one of two states: *ongoing* (control is inside executing a line) or *completed* (all lines executed, control has exited — either via `return` or reaching the end, where `None` is returned by default).

A function that calls another function can be in three states: *ongoing*, *suspended*, or *completed* — color coded like a traffic signal. Since `third()` calls no other function, it never enters the suspended state. The print in `third` runs first, so `third` appears first in the output. Then control returns to the most recent suspended function (`second`), which prints and completes, then `first` prints and completes.

### Recursion

A recursive function calls itself within its own body. The classic example is factorial:

```python
def fact(n):
    if n == 0:
        return 1
    return n * fact(n - 1)
```

When the interpreter hits the recursive call, it suspends `fact(n)` and begins executing `fact(n - 1)`. When `fact(0)` is called, the condition is `True`, returning `1` — this is the **base-case**. Without a base-case, recursion never terminates. After the base case, control transfers back through the suspended calls: `fact(1)`, then `fact(2)`, and so on until `fact(4)` returns `24`.

### Caution in Recursion

#### Fibonacci series

The Fibonacci series: 1, 1, 2, 3, 5, 8, ... Each term is the sum of the two preceding terms. With x₁ = x₂ = 1, for all n > 2 (n ∈ ℕ): xₙ = xₙ₋₁ + xₙ₋₂

```python
def fibo(n):
    if n == 1 or n == 2:
        return 1
    return fibo(n - 1) + fibo(n - 2)
```

Calling `fibo(40)` takes a very long time due to wasteful repeated computation. The recursion tree shows how `fibo(3)` and `fibo(1)` are computed twice, and `fibo(2)` thrice. Larger values like `50` cause even more redundant work.

To measure runtime, the `time` library helps:

```python
import time

def fibo(n):
    if n == 1 or n == 2:
        return 1
    return fibo(n - 1) + fibo(n - 2)

start = time.time()
fibo(40)
end = time.time()
print(f'It took approximately {round(end - start)} seconds.')
```

This takes almost a minute in a standard Python repl. A more efficient iterative solution:

```python
import time

def fibo(n):
    if n == 1 or n == 2:
        return 1
    x_prev, x_curr = 1, 1
    while n > 2:
        x_prev, x_curr = x_curr, x_prev + x_curr
        n -= 1
    return x_curr

start = time.time()
fibo(40)
end = time.time()
print(f'It took approximately {round(end - start)} seconds.')
```

The line `x_prev, x_curr = x_curr, x_prev + x_curr` uses multiple simultaneous assignment: the right-hand side is evaluated first, then those values are simultaneously assigned to the containers on the left. A fuller explanation comes with tuples in the next chapter.

#### Counting Function Calls

You can count how many times a function is called using a global variable:

```python
def fact(n):
    global count
    count = count + 1
    if n == 0:
        return 1
    return n * fact(n - 1)

count = 0
fact(4)
print(count)
```

This is one of the legitimate uses of global variables.

#### Turtles all the way down

A recursive function without a base case is problematic. The simplest pathological example:

```python
##### Alarm! Bad code snippet! #####
def foo():
    foo()
##### Alarm! Bad code snippet! #####
```

Calling `foo()` produces a `RecursionError` with the message `maximum recursion depth exceeded`. The limit is usually 1000 in most systems — more than 1000 recursive calls triggers the error. To check the limit:

```python
import sys
print(sys.getrecursionlimit())
```
