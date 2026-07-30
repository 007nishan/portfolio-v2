<section class="opener" id="ch-0">
<span class="chapter-num">0</span>

# Warm-up
<span class="accent-rule"></span>
</section>

## Lesson 0 — Getting Started with Python {: #ch-0-lesson-0 }

### What is Python?

A programming language is, in essence, a language you use to tell your computer what to do. Python is a general-purpose language that is useful for data science, automation, machine learning, and software and web development.

Consider a program that sums the first 100 numbers:

```python
sum = 0
for number in range(1, 101):
    sum += number
print(sum)
```

Don't worry about how this works yet. Contrast using a calculator to add the numbers 1 through 100 with simply running this code — the program is *blazingly fast*. Coding lets you build solutions and applications; even the calculators used by non-coders are themselves built with code. The example programs in these lessons live in `main.py` files, which you can view via a "Show files" button.

### Why learn Python?

The main reasons are **utility** and **popularity**. Python powers applications at companies like Google, Netflix, Dropbox, and Quora. A 2022 StackOverflow survey rated Python "the second most wanted language," with around 66% of roughly 65,000 respondents developing with it and wanting to continue.

Python also lets you create beautiful things like animations — coders are like musicians and painters using their tools. Python is human-readable, easy, and powerful, which makes it an ideal first language.

!!! tip "How easy is Python?"

    Python's vast collection of libraries eases complex tasks. This is illustrated by the xkcd comic that appears when you enter `import antigravity` in IDLE.

### Lessons

#### Organization

Lessons are numbered `<chapter>.<lesson>`, with about four lessons per chapter, and are best read in sequence from chapter 1 onward. Readers who are already familiar can jump ahead via the Table of Contents. Each chapter introduces one main concept (its title), though other topics also appear — for example, chapter 2 covers conditionals plus built-in functions and standard libraries. The book outline is:

- Chapter-1: Introduction to Python
- Chapter-2: Conditionals
- Chapter-3: Loops
- Chapter-4: Functions
- Chapter-5: Lists and Tuples
- Chapter-6: Sets and dictionaries
- Chapter-7: File handling
- Chapter-8: Object Oriented Programming

#### How to read these lessons?

- Do not trust any piece of code blindly.
- Execute the code and observe the output.
- Think about the output.
- Verify if the explanation given in the text matches your observations.

*Code does not lie.* Learners should run every snippet.

#### Python Version

Lessons use Python 3.8 or higher. Python 2 users are strongly encouraged to switch, since Python 2 has reached end of life.

### Setting up Replit

Replit is an online coding environment, ideal for learning, and it is used extensively in the course. Sign up at replit.com using your Online Degree account and use Replit's tutorial to get started.

### Installing Python on your System

For a local installation, see python.org/downloads and follow a step-by-step guide. Having Python installed is useful for Diploma-level subjects.

### History

Python first appeared in February 1991, created as a hobby project by Dutch programmer Guido van Rossum, who served as *benevolent dictator for life* until stepping down in 2018. On the naming, the official documentation notes that van Rossum was reading scripts from "Monty Python's Flying Circus," a 1970s BBC comedy, and wanted a name that was "short, unique, and slightly mysterious." Python is now over 30 years old, built by people and used by thousands worldwide — jump in with an open mind.

!!! note "Note"

    An image caption in the source reads: "Guido Van Rossum at the Dropbox Headquarters in 2014."

### Explore

1. Check out the Python Software Foundation website to learn about the organization behind Python.
2. Read a Dropbox blog interview with Guido van Rossum (trivia: he worked at Dropbox for six and a half years).
3. Watch documentaries and interviews where Guido discusses Python's origins, for a humanistic view of technology.
4. StackOverflow, a question-and-answer forum for programming, will likely become heavily used — but use it wisely, and avoid using it for assignment answers.
5. Look into the official documentation on the Python website.
