<section class="opener" id="ch-8">
<span class="chapter-num">8</span>

# Object Oriented Programming
<span class="accent-rule"></span>
</section>

## Lesson 8.1 — Objects and Classes {: #ch-8-lesson-1 }

### Objects and Classes

This lesson introduces the fundamentals of object-oriented programming (OOP), aiming to explain the concept with minimal jargon. It uses the phrase "Unity in diversity" as a way to grasp the idea of objects.

The core intuition: humanity is united (we are all humans sharing this planet), yet each individual is unique — differing in properties like height and weight. This can be framed as two forces: a global force uniting everyone and a local force giving each person a distinct identity. In OOP terms, each human is an **object**, while all humans belong to the **class** "Humanity."

The same logic extends to cars. No two cars are identical — brand and speed are points of difference — yet a car is clearly distinct from a train because of shared global features. Each car is an object, and all cars belong to the class "Car."

Moving from concrete to abstract, here are the key definitions:

> "Objects are entities that have certain attributes along with operations associated with them."

For cars, attributes could include speed and fuel level; operations could include start, stop, accelerate, decelerate, and fill fuel tank.

> "A class is a blueprint or a template that is used to create objects."

The specification of a car lives in a class like `Car` (note the capital "C"), while a human's specification lives in a class like `Human`. A class is like a Google form: a template created once and distributed, with each person filling it in differently to create different objects.

> "Object Oriented Programming (OOP) is a paradigm that looks at the world as a collection of objects and the interactions among them."

### OOP in Python: an example

Consider a simple student template with two pieces of information: Name and Marks. The desired operations are to update the student's marks and to print the student's details.

```python
class Student:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks

    def update_marks(self, marks):
        self.marks = marks

    def print_details(self):
        print(f'{self.name}')
```

`class` is the Python keyword for defining classes, similar to how `def` defines functions. `Student` is the class name being created. The class contains three functions — `__init__`, `update_marks`, and `print_details`. Functions defined inside a class are called **methods**. Among them, `__init__` has a special role and is called the **constructor**.

To create an object of type `Student`:

```python
anish = Student('Anish', 95)
```

Now `anish` is an object of type `Student`. To verify this, run:

```python
print(type(anish)) # output should be: <class '__main__.Student'>
```

This example will be revisited in the next lesson to explore various features of a class.

## Lesson 8.2 — Classes, Objects, self, Class vs Object Attributes {: #ch-8-lesson-2 }

### Classes and Objects

The lesson continues with the `Student` class — do not worry about `self` yet. The class definition:

```python
class Student:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks
    def update_marks(self, marks):
        self.marks = marks
    def print_details(self):
        print(f'{self.name}:{self.marks}')
```

An object is created with `anish = Student('Anish', 80)`. Using the class name on the right-hand side invokes the **constructor** (`__init__()`). Its arguments become **attributes** accessed via the `.` operator:

```python
print(anish.name)
print(anish.marks)
```

`__init__()`, `update_marks()`, and `print_details()` are **methods** — functions defined in a class. To update marks: `anish.update_marks(95)`. In short, attributes define an object's state, while methods "capture the behaviour of the object."

### self

`self` "is used to point to the current object." Given two objects, calling `lakshmi.print_details()` is really executed as `Student.print_details(lakshmi)` — the object is passed as an argument. Likewise `anish.update_marks(95)` equals `Student.update_marks(anish, 95)`. This is why the first parameter of every method is `self`. So `self.name = name` assigns the argument to the current object's attribute.

### Class Attributes vs Object Attributes

Object attributes differ per object. To track a student count, use a **class attribute**, shared by all objects:

```python
class Student:
    counter = 0
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks
        Student.counter += 1
    def update_marks(self, marks):
        self.marks = marks
    def print_details(self):
        print(f'{self.name}:{self.marks}')
```

Creating three students and printing `Student.counter` each time:

```output
Number of students in the program = 1
Number of students in the program = 2
Number of students in the program = 3
```

`print(madhavan.counter)` gives `3` — a class attribute can be accessed by any object. But assigning `madhavan.counter = -1`:

```output
Student counter: 3
Madhavan counter: -1
```

This creates a new object attribute with the same name; Python "prioritizes the object attribute," delinking `madhavan.counter` from the class one. To reset: `Student.counter = 0` then print gives `Student counter: 0`.

The final exercise (adding `Rohan`) produces:

```output
Usha counter: 0
Madhavan counter: -1
Student counter: 1
Usha counter: 1
Madhavan counter: -1
```

Key point: "class attributes cannot be updated by an object" — only referenced or accessed.

Attributes can also be created dynamically at runtime, not only in the constructor:

```python
class Student:
    def __init__(self, name):
        self.name = name

anish = Student('Anish')
anish.maths = 100
anish.physics = 90
anish.chem = 70
```

Every `Student` gets `name` at creation, but `maths`, `physics`, and `chem` are unique to `anish`.

## Lesson 8.3 — Inheritance and Method Overriding {: #ch-8-lesson-3 }

### Inheritance

This lesson returns to the guiding philosophy of object-oriented programming: **"Unity in diversity."** The class embodies unity while objects embody diversity — but that diversity is organized into a hierarchy we observe everywhere.

Using a human roles example (students, working professionals, college students, software developers, full-stack developers), we see that hierarchies exist naturally. The core idea of **inheritance** is that classes lower in the hierarchy inherit features and attributes from their ancestors. For instance, since all working professionals draw a monthly salary, software developers and full-stack developers inherit that salary attribute from their ancestors.

### Concrete Example

Assignments are collections of questions, and questions come in different types (NAT, MCQ). Though a NAT differs from an MCQ, both are questions — forming a hierarchy. Since parents come first, the base `Question` class is defined:

```python
class Question:
    def __init__(self, statement, marks):
        self.statement = statement
        self.marks = marks

    def print_question(self):
        print(self.statement)

    def update_marks(self, marks):
        self.marks = marks
```

Only attributes common to all questions are retained: the statement and the marks. Next, child classes for MCQ and NAT are defined using the hierarchy relationship:

```python
class NAT(Question):
    def __init__(self, statement, marks, answer):
        super().__init__(statement, marks)
        self.answer = answer

    def update_answer(self, answer):
        self.answer = answer
```

A `NAT` is a specialized `Question` with an extra feature (`answer`) and a new method (`update_answer`), while inheriting everything else. `Question` becomes the "parent-class or base-class" and `NAT` the "child-class or derived-class."

The general syntax:

```python
class Derived(Base):
    def __init__(self, ...):
        pass

#### OR ####
class Child(Parent):
    def __init__(self, ...):
        ...
```

For this example specifically:

```python
class NAT(Question):
    def __init__(self, ...):
        pass
```

### Parent-child relationship

Something interesting happens in the derived class constructor:

```python
class NAT(Question):
    def __init__(self, statement, marks, answer):
        super().__init__(statement, marks)
        self.answer = answer

    def update_answer(self, answer):
        self.answer = answer
```

The `super()` function points to the parent class (`Question`), so the parent's constructor is effectively called. Inherited methods like `update_marks()` can be invoked directly:

```python
q_nat = NAT('What is 1 + 1?', 1, 2)
q_nat.update_marks(4)
print(q_nat.marks)
```

```output
4
```

### Method Overriding

The parent class again for reference:

```python
class Question:
    def __init__(self, statement, marks):
        self.statement = statement
        self.marks = marks

    def print_question(self):
        print(self.statement)

    def update_marks(self, marks):
        self.marks = marks
```

Sometimes you want to modify inherited method behavior. For an MCQ, printing only the statement is incomplete — options should also appear. You can **override** the inherited method:

```python
class MCQ(Question):
    def __init__(self, statement, marks, ops, c_ops):
        super().__init__(statement, marks)
        self.ops = ops      # list of all options
        self.c_ops = c_ops  # list of correct options

    def print_question(self):
        super().print_question()
        # Assume there are only four options
        op_index = ['(a)', '(b)', '(c)', '(d)']
        for i in range(4):
            print(op_index[i], self.ops[i])
```

Since `Question` already prints the statement, the override "piggy-backs" on that behavior via `super()`, then adds the options. Creating and calling an MCQ object:

```python
q_mcq = MCQ('What is the capital of India?',
           2,
           ['Chennai', 'Mumbai', 'Kolkota', 'New Delhi'],
           ['New Delhi'])
q_mcq.print_question()
```

```output
What is the capital of India?
(a) Chennai
(b) Mumbai
(c) Kolkota
(d) New Delhi
```

## Lesson 8.4 — Vector: A Complete OOP Example {: #ch-8-lesson-4 }

This lesson presents a final example of classes in action, demonstrating several important OOP concepts through the example of a vector.

### Vector: Mathematical Preliminaries

Every point P(x, y) in 2D space can be associated with a **vector** — geometrically, a directed arrow from the origin to point P. One tip is always at the origin, and the other tip (the *head*) is at point P. The lesson uses P₁ and P₂ as example vectors.

Key vector operations covered:

**Magnitude.** The magnitude of a vector P(x, y) is the length of segment OP:

$$|OP| = \sqrt{x^2 + y^2}$$

**Scale.** Scaling by value *s* changes the vector's length but not its direction:

$$s \cdot (x, y) \rightarrow (sx, sy)$$

**Add.** Two vectors combine component-wise:

$$(x_1, y_1) + (x_2, y_2) = (x_1 + x_2, y_1 + y_2)$$

**Reflect.** Reflection about an axis is a special case of rotation about the origin. Reflecting about the X-axis:

$$(x, y) \rightarrow (x, -y)$$

### Vector: Specification

The **specification** is the bridge to move from a mathematical vector to a programmatic one — a written description of the attributes and methods the class needs, derived from the mathematical vector.

**Attributes:**

- `x`: the x-coordinate
- `y`: the y-coordinate

These two attributes fully define any 2D vector.

**Methods:**

- `__init__()`: constructor; populates attributes from arguments
- `__str__()`: returns coordinates as `(x,y)` for `str()`/`print()`
- `magnitude()`: returns the magnitude
- `scale()`: scales the current vector by *s*
- `rotate_xaxis()`: reflects the current vector about the X-axis
- `rotate_yaxis()`: reflects the current vector about the Y-axis
- `add()`: accepts a vector argument; returns the sum with the current vector

### Vector: Definition

```python
class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def print(self):
        return f'({self.x},{self.y})'
    def magnitude(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5
    def scale(self, s):
        self.x, self.y = self.x * s, self.y * s
    def rotate_xaxis(self):
        self.y = -self.y
    def rotate_yaxis(self):
        self.x = -self.x
    def add(self, P):
        result = Vector(0, 0)
        result.x, result.y = self.x + P.x, self.y + P.y
        return result
```

All methods except `add()` and `__str__()` return no value — they transform the vector itself. The `add()` method is interesting: it accepts a vector `P`, creates a new zero-vector inside, stores the sum in `result`, and returns it.

### Collection of Vectors

The point of having a class is to create objects, since the class is merely a template. Example use case:

```python
triangle = [Vector(0, 1), Vector(3, 1), Vector(3, 0)]
```

Here `triangle` is a list of `Vector` objects representing a triangle. To compute the side lengths:

```python
def dist(P1, P2):
    return ((P1.x - P2.x) ** 2 + (P1.y - P2.y) ** 2) ** 0.5

def side_lengths(triangle):
    la = dist(triangle[0], triangle[1])
    lb = dist(triangle[1], triangle[2])
    lc = dist(triangle[2], triangle[0])
    return la, lb, lc
```

Similarly, a square could be defined as a list of four vectors. This closes the discussion on object-oriented programming in Python; these concepts will be covered in greater detail when studying Java.

!!! note "Note"

    The class specification references `__str__()`, but the code above defines a `print()` method instead — reproduced as it appears in the source.
