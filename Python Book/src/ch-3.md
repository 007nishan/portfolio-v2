<section class="opener" id="ch-3">
<span class="chapter-num">3</span>

# Loops
<span class="accent-rule"></span>
</section>

## Lesson 3.1 — The while Loop; break and continue {: #ch-3-lesson-1 }

### Introduction

How do we sum the first five positive integers? A simple direct approach:

```python
print(1 + 2 + 3 + 4 + 5)
```

Now consider summing the first 1,000,000 integers — the manual approach is impractical. An estimate of how long it would take by hand comes to about 58 days. This motivates loops.

### `while`

`while` is a Python keyword followed by a boolean **condition**. The "loopy" solution to the summation problem:

```python
total = 0
num = 0
while num < 1_000_000:
    num = num + 1
    total = total + num
print(total)
# Rest of code will follow below this comment
```

The indented lines form the loop body. If the condition is `True`, control enters the body and executes lines sequentially, then loops back to re-check the condition. When the condition becomes `False`, the body is skipped and execution continues after the loop. The body must be indented to separate it from surrounding code. Note that the underscore in `1_000_000` improves readability for large numbers.

Two further problems are described:

1. Read integers until a negative is entered; print the sum of positives (or 0 if none).
2. Read integers until a negative is entered; print the maximum positive (or 0 if none).

Solution to the maximum problem:

```python
# Initialize
num = int(input())
max_num = 0
# Loop
while num >= 0:
    if num > max_num:
        max_num = num
    num = int(input())
# Print output
print(max_num)
```

The indented lines make up the loop body; the comments help explain the code.

### Loop Control Statements

`break` and `continue` are keywords tied to loops. `break` exits a loop entirely, skipping any code below it. This example finds the LCM of 2, 3, 4:

```python
num = 1
while True:
    if (num % 2 == 0) and (num % 3 == 0) and (num % 4 == 0):
        break
    num = num + 1
print(num)
```

`continue` skips to the next iteration, bypassing the remaining code in the current pass. This example prints multiples of 3 up to 50:

```python
x = 0
while x < 50:
    x = x + 1
    if x % 3 != 0:
        continue
    print(x)
```

Both statements skip the code that follows them within the loop, but "break exits the loop whereas continue moves to the next iteration." Both examples could be rewritten without `break` or `continue`, which is left as an exercise.

## Lesson 3.2 — The for Loop, range() and Iterating Strings {: #ch-3-lesson-2 }

### `for` loop

The `for` loop is an alternative to a while loop. Consider printing the first 5 non-negative integers:

```python
for i in range(5):
    print(i) # A dummy line
```

```output
0
1
2
3
4
```

Both `for` and `in` are Python keywords, while `range` is an object representing a sequence of numbers. The second line forms the body of the loop. The loop behaves as follows:

- Each iteration picks up an element from the sequence and prints it to the console.
- Reading left to right, the leftmost element is picked first.
- Processing goes left to right through the sequence.
- After the rightmost element prints, control returns to the first line one final time; with no elements left, control exits the loop.

As with `while` loops and `if`-`else` blocks, the body of a `for` loop must be indented.

### range()

The `range()` function returns a sequence of numbers. `range(5)` produces the sequence 0, 1, 2, 3, 4. More generally, `range(n)` creates the sequence 0, 1, ..., n − 1. The following prints all two-digit numbers greater than zero:

```python
for i in range(10, 100):
    print(i)
```

Here `range(10, 100)` represents 10, 11, ..., 99. In general, `range(start, stop)` gives `start, start + 1, ..., stop - 1`. The next example prints all even two-digit natural numbers:

```python
for i in range(10, 100, 2):
    print(i)
```

`range(10, 100, 2)` represents 10, 12, ..., 98. In general, `range(start, stop, step)` gives `start, start + step, start + 2 * step, ..., last`, where `last` is the largest element less than `stop`. This holds when `step` is positive.

The following three forms are equivalent:

- `range(n)`
- `range(0, n)`
- `range(0, n, 1)`

Using a negative step size, you can create decreasing sequences. This prints all two-digit even numbers greater than zero in descending order:

```python
for i in range(98, 9, -2):
    print(i)
```

For a negative `step`, the sequence runs `start, start + step, ...`, with `last` being the smallest element greater than `stop`.

Next, consider:

```python
for i in range(5, 5):
    print(i)
```

`range(5, 5)` is an empty sequence, so nothing prints. Another empty-sequence example:

```python
for i in range(10, 5):
    print(i)
```

Importantly, neither snippet produces an error. Finally, run and observe the following (flagged as incorrect):

```python
##### Alarm! Wrong code snippet! #####
for i in range(0.0, 10.0):
    print(i)
##### Alarm! Wrong code snippet! #####
```

### Iterating through Strings

Because a string is a sequence of characters, a `for` loop can iterate through it. This prints each character of the string on its own line:

```python
word = 'good'
for char in word:
    print(char)
```

```output
g
o
o
d
```

The output can be enriched with additional code:

```python
word = 'good'
count = 1
for char in word:
    print(char, 'occurs at position', count, 'in the string', word)
    count = count + 1
```

```output
g occurs at position 1 in the string good
o occurs at position 2 in the string good
o occurs at position 3 in the string good
d occurs at position 4 in the string good
```

## Lesson 3.3 — Nested Loops; while vs for; print end and sep {: #ch-3-lesson-3 }

### Nested loops

Here is a problem to consider: count the ordered pairs of positive integers that multiply to 100, where order matters so that (2, 50) and (50, 2) are treated as distinct.

```python
count = 0
for a in range(1, 101):
    for b in range(1, 101):
        if a * b == 100:
            count = count + 1
print(count)
```

This is a nested loop. The outer loop steps through values of `a`, and the inner loop steps through values of `b`, with multiple indentation levels. This problem "could have been solved without using a nested loop" and the nested approach is not efficient — a better solution is left as an exercise.

Next problem: count the primes below a positive integer *n*.

```python
n = int(input())
count = 0
for i in range(2, n + 1):
    flag = True
    for j in range(2, i):
        if i % j == 0:
            flag = False
            break
    if flag:
        count = count + 1
print(count)
```

The idea:

- The outer loop steps through 2, 3, ..., n using loop variable `i`.
- Initially assume `i` is prime by setting `flag` to `True`.
- The inner loop tests potential divisors 2, 3, ..., i−1 using `j`; note the inner sequence depends on the outer variable `i`.
- If `j` divides `i`, then `i` is not prime, so `flag` becomes `False` and we break out of the inner loop.
- If no `j` divides `i`, the assumption holds and `flag` stays `True`.
- After the inner loop, if `flag` is `True`, we increment `count` for the prime found.

Important points about nesting:

- Nesting is not limited to `for` loops. Valid combinations include: `for` inside `for`, `for` inside `while`, `while` inside `while`, and `while` inside `for`.
- Multiple levels of nesting are allowed.

### while versus for

Generally, `for` loops suit cases where the iteration count can be quantified, while `while` loops fit cases where it cannot be known exactly beforehand. That does not mean a `for` loop's iteration count is always constant, as this example shows:

```python
n = int(input())
for i in range(n):
    print(i ** 2)
```

The iteration count varies with each different input, but once the input is known, the count is fixed. By contrast:

```python
x = int(input())
while x > 0:
    x = int(input())
```

Here the iteration count is only knowable after termination; there is no way to express it as an explicit function of the user input.

### print: end, sep

#### end

Problem: accept a positive integer `n` and print numbers 1 to n on one line separated by commas. For `n = 9`, the desired output is:

```output
1,2,3,4,5,6,7,8,9
```

This attempt will not work:

```python
n = int(input())
for i in range(1, n + 1):
    print(i, ',')
```

For `n = 9`, it produces:

```output
1 ,
2 ,
3 ,
4 ,
5 ,
6 ,
7 ,
8 ,
9 ,
```

The `print` function offers a fix:

```python
n = int(input())
for i in range(1, n):
    print(i, end = ',')
print(n)
```

For `n = 9`, this gives the required output:

```output
1,2,3,4,5,6,7,8,9
```

By default, `print()` outputs the expression and then a newline. That behavior is controlled by the `end` argument, whose default is the newline character. Setting `end` to a comma forces `print()` to append a comma rather than a newline. It is named `end` because it is added at the end. Consider this code:

```python
print()
print(end = ',')
print(1)
print(1, end = ',')
print(2, end = ',')
print(3, end = ',')
```

```output
,1
1,2,3,
```

The first output line is a newline because the default `end` is `'\n'`, even though nothing is passed. The second `print` passes no expression but sets `end` to `,`, so only a comma appears.

#### sep

When multiple expressions are passed to `print()`, they appear on the same line separated by a space by default:

```python
print('this', 'is', 'cool')
```

```output
this is cool
```

To change or remove that separator, use `sep`:

```python
print('this', 'is', 'cool', sep = ',')
```

```output
this,is,cool
```

An empty string works as a separator too:

```python
print('this', 'is', 'cool', sep = '')
```

```output
thisiscool
```

#### end and sep

A final example uses both `end` and `sep`. Accept a positive integer `n` (a multiple of 3) and print this pattern:

```output
|1,2,3|4,5,6|7,8,9|...|n - 2,n - 1,n|
```

For `n = 9`, print:

```output
|1,2,3|4,5,6|7,8,9|
```

Solution:

```python
n = int(input())
print('|', end = '')
for i in range(1, n + 1, 3):
    print(i, i + 1, i + 2, sep = ',', end = '|')
print()
```

The `for` loop steps by 3 starting at 1. Setting `sep` to `,` prints the comma-separated triplet `i, i + 1, i + 2`, while setting `end` to `|` prints the bar after each triplet. The second line ensures a leading `|`. The final `print()` outside the loop moves the console prompt to the next line after the pattern finishes — you can remove it to observe the difference.

## Lesson 3.4 — Formatted Printing: f-strings, format(), Specifiers {: #ch-3-lesson-4 }

### Formatted printing

Consider a program that reads a name and prints a greeting:

```python
name = input()
print('Hi,', name, '!')
```

With `Sachin` as input, the output is:

```output
Hi, Sachin !
```

The problem: there is an unwanted space after the name — a formatting issue that Python's tools can solve.

### f-strings

The first method is the **formatted string literal**, or f-string. The corrected version:

```python
name = input()
print(f'Hi, {name}!')
```

```output
Hi, Sachin!
```

The key string here is the f-string `f'Hi, {name}'`. The `f` prefix distinguishes it from a normal string, and when evaluated it produces a string with the variable's value inserted where `{name}` appears. Two elements are essential: the `f` prefix and the curly braces around the variable.

Omitting either one produces different behavior:

```python
name = 'Sachin'
print('Hi, {name}!')
print(f'Hi, name!')
```

```output
Hi, {name}!
Hi, name!
```

A rectangle example demonstrates using expressions inside braces:

```python
l, b = int(input()), int(input())
print(f'The length of the rectangle is {l} units')
print(f'The breadth of the rectangle is {b} units')
print(f'The area of the rectangle is {l * b} square units')
```

For `l = 4, b = 5`, the output is:

```output
The length of the rectangle is 4 units
The breadth of the rectangle is 5 units
The area of the rectangle is 20 square units
```

Note that the last line contains an expression (`l * b`) rather than just a variable. Any valid Python expression is allowed inside the braces, and the interpreter substitutes its value.

A multiplication table example:

```python
x = int(input())
print(f'Multiplication table for {x}')
for i in range(1, 11):
    print(f'{x} X {i} \t=\t {x * i}')
```

For input `3`, the output is:

```output
Multiplication table for 3
3 X 1   =    3
3 X 2   =    6
3 X 3   =    9
3 X 4   =    12
3 X 5   =    15
3 X 6   =    18
3 X 7   =    21
3 X 8   =    24
3 X 9   =    27
3 X 10  =    30
```

The `\t` is a tab character placed before and after the `=`. Try removing both tabs and re-running to observe the change.

f-strings can also define string variables, not just be passed to `print()`:

```python
name = input()
qual = input()
gender = input()
if qual == 'phd':
    name_respect = f'Dr. {name}'
elif gender == 'male':
    name_respect = f'Mr. {name}'
elif gender == 'female':
    name_respect = f'Ms. {name}'
print(f'Hello, {name_respect}')
```

Guess what this code does.

### format()

Another approach uses the string method `format()`:

```python
name = input()
print('Hi, {}!'.format(name))
```

The curly braces get replaced by the value of `name`. The rectangle example again:

```python
l, b = int(input()), int(input())
print('The length of the rectangle is {} units'.format(l))
print('The breadth of the rectangle is {} units'.format(b))
print('The area of the rectangle is {} square units'.format(l * b))
```

The multiplication table with `format()`:

```python
x = int(input())
for i in range(1, 11):
    print('{} X {} \t=\t {}'.format(x, i, x * i))
```

The output matches the f-string version. The three pairs of braces are filled left-to-right by the three arguments given to `format()`.

An example with implicit mapping:

```python
fruit1 = 'apple'
fruit2 = 'banana'
print('{} and {} are fruits'.format(fruit1, fruit2))
```

The mapping can be made explicit using indices:

```python
fruit1 = 'apple'
fruit2 = 'banana'
print('{0} and {1} are fruits'.format(fruit1, fruit2))
```

The integers give the argument index (starting from 0, left to right). Changing the argument order changes the output. A third form uses keyword arguments:

```python
fruit1 = 'apple'
fruit2 = 'banana'
print('{string1} and {string2} are fruits'.format(string1 = fruit1, string2 = fruit2))
```

This relies on keyword arguments, which are covered later in the functions chapter and set aside for now.

### Format specifiers

Consider:

```python
pi_approx = 22 / 7
print(f'The value of pi is approximately {pi_approx}')
```

```output
The value of pi is approximately 3.142857142857143
```

There are too many digits after the decimal. Format specifiers solve this:

```python
pi_approx = 22 / 7
print(f'The value of pi is approximately {pi_approx:.2f}')
```

```output
The value of pi is approximately 3.14
```

Inside `{pi_approx:.2f}`, the part before `:` is the variable and the part after is the format specifier `.2f`:

- `.` signifies the decimal point.
- `2` (after the decimal) means exactly two digits after the decimal point, i.e., the value is rounded to two decimal places.
- `f` signifies a `float` value.

A variant with `.3f`:

```python
pi_approx = 22 / 7
print(f'The value of pi is approximately {pi_approx:.3f}')
```

```output
The value of pi is approximately 3.143
```

Next, printing three students' marks:

```python
roll_1, marks_1 = 'BSC1001', 90.5
roll_2, marks_2 = 'BSC1002', 100
roll_3, marks_3 = 'BSC1003', 90.15
print(f'{roll_1}: {marks_1}')
print(f'{roll_2}: {marks_2}')
print(f'{roll_3}: {marks_3}')
```

```output
BSC1001: 90.5
BSC1002: 100
BSC1003: 90.15
```

To right-align the marks with uniform representation:

```python
roll_1, marks_1 = 'BSC1001', 90.5
roll_2, marks_2 = 'BSC1002', 100
roll_3, marks_3 = 'BSC1003', 90.15
print(f'{roll_1}: {marks_1:10.2f}')
print(f'{roll_2}: {marks_2:10.2f}')
print(f'{roll_3}: {marks_3:10.2f}')
```

```output
BSC1001:      90.50
BSC1002:     100.00
BSC1003:      90.15
```

In `{marks_1:10.2f}`, `.2f` rounds the float to two decimals, and the `10` sets the minimum column width. If the number has fewer than 10 characters (including the decimal point), spaces are added before the number to compensate.

Finally, printing integers with formatting via `format()`:

```python
print('{0:5d}'.format(1))
print('{0:5d}'.format(11))
print('{0:5d}'.format(111))
print('{:5d}'.format(1111))
print('{:5d}'.format(11111))
print('{:5d}'.format(111111))
```

```output
    1
   11
  111
 1111
11111
111111
```

Points to note:

- The `d` stands for integer.
- The first three statements include the argument index (`0`) before the `:`; the last three have nothing before the `:`. Both forms are valid.
- The `5d` sets a minimum column width of 5.
- The first four lines have leading spaces because those integers have fewer than five characters.

## Lesson 3.5 — System Libraries: math and random {: #ch-3-lesson-5 }

This lesson covers two more libraries — `math` and `random` — using them to solve interesting problems in mathematics.

### `math`

Consider a sequence of nested square roots: √2, √(2+√2), √(2+√(2+√2)), and so on. This sequence converges toward a specific value called its **limit**. Can we estimate this value using what we've learned?

```python
import math
x = 0
for n in range(1, 6):
    x = math.sqrt(2 + x)
    print(f'n = {n}, x_n = {x:.3f}')
```

```output
n = 1, x_n = 1.414
n = 2, x_n = 1.848
n = 3, x_n = 1.962
n = 4, x_n = 1.990
n = 5, x_n = 1.998
```

The `sqrt()` function returns the square root of its argument. The results as a table:

| $n$ | $x_n$ | Approximate value |
|-----|-------|-------------------|
| 1 | √2 | 1.414 |
| 2 | √(2+√2) | 1.848 |
| 3 | √(2+√(2+√2)) | 1.962 |
| 4 | √(2+√(2+√(2+√2))) | 1.990 |
| 5 | √(2+√(2+√(2+√(2+√2)))) | 1.998 |

The sequence appears to approach the value 2. Running the loop for more iterations:

```python
import math
x = 0
for n in range(1, 20):
    x = math.sqrt(2 + x)
print(x)
```

After 20 iterations the value is very close to two: `1.9999999999910236`. Since deciding when to stop by trial and error is not ideal, a better approach is to define a **tolerance** — terminate when the difference between successive values falls below a predefined value.

```python
import math
x_prev, x_curr = 0, math.sqrt(2)
tol, count = 0.00001, 0
while abs(x_curr - x_prev) >= tol:
    x_prev = x_curr
    x_curr = math.sqrt(2 + x_prev)
    count += 1
print(f'Value of x at {tol} tolerance is {x_curr}')
print(f'It took {count} iterations')
```

### `random`

How can we toss a coin in Python?

```python
import random
print(random.choice('HT'))
```

`random` is a library and `choice()` is a function within it that accepts any sequence and returns a randomly chosen element. Here the input is a string, which is a sequence of characters.

The theoretical probability of heads on a coin toss is 0.5. To verify this computationally, we set up an experiment: toss a coin $n$ times, count the heads, and divide by $n$ to get the empirical probability. As $n$ grows large, this should approach 0.5.

```python
import random
n = int(input())
heads = 0
for i in range(n):
    toss = random.choice('HT')
    if toss == 'H':
        heads += 1
print(f'P(H) = {heads / n}')
```

Running this for different values of $n$:

| $n$ | $P(H)$ |
|-----|--------|
| 10 | 0.2 |
| 100 | 0.52 |
| 1,000 | 0.517 |
| 10,000 | 0.5033 |
| 100,000 | 0.49926 |
| 1,000,000 | 0.499983 |

As expected, the value approaches `0.5`. `random` is quite versatile.

!!! note "Exercise"

    Rolling a die: `randint(a, b)` returns a random integer $N$ where $a \leq N \leq b$.

    ```python
    import random
    print(random.randint(1, 6))
    ```

    Find the empirical probability for each face of a die using this function.

## Lesson 3.6 — Mathematics and Programming {: #ch-3-lesson-6 }

This lesson explores where mathematics and programming meet, offered as a closing topic for the chapter.

### Limits

The lesson begins with the number √2 − 1. Since it is known that 1 < √2 < 2, it follows that 0 < √2 − 1 < 1. Consider the sequence:

$$ a_n = \left( \sqrt{2} - 1 \right)^n $$

As *n* grows large, the terms shrink toward zero, because repeatedly multiplying a fraction by itself makes it progressively smaller. Mathematically, the limit as *n* approaches infinity is zero. This is verified with the following program:

```python
import math
n = int(input())                # sequence length
CONST = math.pow(2, 0.5) - 1    # basic term in the sequence
a_n = 1                         # zeroth term
for i in range(n):
    a_n = a_n * CONST           # computing the nth term
print(a_n)
```

Try several values of *n*. For *n* = 100, the result is 5.27 × 10⁻³⁹ — so tiny that it may as well be zero for practical purposes.

### Recurrence relation

Next comes another fact: for every number *n*, there exist unique integers *x* and *y* such that:

$$ (\sqrt{2} - 1)^n = x + y \cdot \sqrt{2} $$

For *n* = 1, this is clear: *x* = −1, *y* = 1. For larger values, the claim can be established by mathematical induction. A sketch of the proof: if $(\sqrt{2} - 1)^n = x_n + y_n \cdot \sqrt{2}$, then

$$ (\sqrt{2} - 1)^{n + 1} = (x_n + y_n \cdot \sqrt{2}) \cdot (\sqrt{2} - 1) = (2y_n - x_n) + (x_n - y_n) \cdot \sqrt{2} = x_{n + 1} + y_{n + 1} \cdot \sqrt{2} $$

This equation defines a *recurrence relation* — one where "each new term in the sequence is a function of the preceding terms." With starting values *x₁* = −1 and *y₁* = 1, for *n* > 0 the recurrence is:

$$ \begin{align} x_{n + 1} &= 2 y_n - x_n\\ y_{n + 1} &= x_n - y_n \end{align} $$

Loops are handy tools for computing such sequence terms:

```python
n = int(input())    # sequence length
x_n, y_n = -1, 1    # x_1 and y_1
for i in range(n - 1):
    x_n, y_n = 2 * y_n - x_n, x_n - y_n
```

### Rational Approximation

This recurrence provides a way to approximate √2 using rational numbers:

$$ \sqrt{2} \approx \frac{-x_n}{y_n} $$

As *n* grows, the approximation gets increasingly accurate. After 100 iterations, the result is accurate to several decimal places:

$$ \frac{228725309250740208744750893347264645481}{161733217200188571081311986634082331709} $$

The lesson closes with a reflection on usefulness: "We don't do things because they are useful. We do them because they are interesting." The point being that interesting things tend to eventually find a use.
