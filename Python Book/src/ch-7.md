<section class="opener" id="ch-7">
<span class="chapter-num">7</span>

# File Handling
<span class="accent-rule"></span>
</section>

## Lesson 7.1 — Why Files {: #ch-7-lesson-1 }

### Why files

This lesson motivates the concept of files by comparing computer memory to human memory. Just as humans can only hold a limited number of "chunks" of information in short-term memory (often cited as around seven), computers also have finite short-term memory despite being powerful. The solution for both is external storage. Files serve computers the way books serve humans, providing a permanent place to record information that can be retrieved whenever needed.

### File handling

We typically open files by double-clicking an icon. Consider an example file containing income-expenditure data for a family over five months:

```output
Income      Expenditure
12,000      10,000
50,000      45,000
75,000      35,000
14,000      12,000
60,000      40,000
```

The goal is to create a new file that adds a third column for savings, producing the following output:

```output
Income      Expenditure     Savings
12,000      10,000          2,000
50,000      45,000          5,000
75,000      35,000          40,000
14,000      12,000          2,000
60,000      40,000          20,000
```

The task appears simple — open the file, calculate the values, and paste them in a new column. But there is a problem of scale: what if the number of entries grows dramatically? For instance, processing data for every family in a neighborhood. With 10 years of data for 1000 families, we would be dealing with $1000 * 10 * 12 = 120{,}000$ entries, which would overwhelm both a calculator and a person.

This is where Python helps. We can write just a few lines of code to automate the entire process. Upcoming lessons will cover file processing, teaching these operations:

- opening a file and closing it
- reading from a file
- writing to a file

"File handling is an umbrella term that denotes all these operations."

## Lesson 7.2 — Creating, Opening, Reading and Writing a File {: #ch-7-lesson-2 }

### Creating a file in Replit

This lesson uses Replit and the `Add File` button to create a file. Each file needs a name — here it is called `examples.txt`. The following lines are added to the file:

```output
one
two
three
four
five
```

After creating the file, it appears in Replit when you click on `examples.txt`.

A `.txt` file is a text file, identifiable by the extension at the end of the file name. Different files use different extensions. For example, `main.py` is a file with the `py` extension, which is why it appears alongside `examples.txt` under the Files tab in Replit.

### Opening and reading from a file

To open the file and print its contents to the console, head to `main.py` and type:

```python
f = open('examples.txt', 'r')
for line in f:
    print(line)
f.close()
```

`open()` is a built-in function accepting two arguments:

- file name
- mode

The first argument is the file name (`'examples.txt'`). The second is the mode — here `'r'` for read mode. Both arguments are strings. The `open()` function returns a file object, called `f` in the code. The loop goes through each line and prints it. Finally, `close()` closes the file. "It is a good practice to close the file once we are done with processing it."

```output
one

two

three

four

five

```

There is an extra blank line between successive lines. To suppress these, modify the print function:

```python
f = open('examples.txt', 'r')
for line in f:
    print(line, end = '')   # there is NO SPACE between the quotes
f.close()
```

By default, `print()` appends a newline character (`'\n'`). Using `end = ''` appends the empty string instead, removing the extra line.

```output
one
two
three
four
five
```

### Opening and writing to a file

Consider this code:

```python
f = open('writing.txt', 'w')
f.write('one ')
f.write('two ')
f.write('three ')
f.write('four ')
f.write('five')
f.close()
```

Here the file is opened in write mode. When executed, it creates a file in Replit called `writing.txt`. The `write()` method writes to the file, taking the content as a string argument. Even though five words are written across five lines of code, all of them get written to the same line in the file. To move to a new line, use the `'\n'` character. Try this code:

```python
f = open('writing.txt', 'w')
f.write('one')
f.write('\n')
f.write('two')
f.write('\n')
f.write('three')
f.write('\n')
f.write('four')
f.write('\n')
f.write('five')
f.close()
```

A better way, in fewer lines, is to append `\n` to every line you wish to write:

```python
f = open('writing.txt', 'w')
f.write('one\n')
f.write('two\n')
f.write('three\n')
f.write('four\n')
f.write('five')
f.close()
```

This produces the same file with fewer lines of code. The next lesson takes a closer look at the idea of a file object.

!!! note "Note"

    Notice that no `'\n'` was added after `five`. Consider why that is — and try running the code with `'\n'` after `five`.

## Lesson 7.3 — File Object and Mode {: #ch-7-lesson-3 }

### File Object

The `open()` function returns a file object. To understand a file object, consider an analogy: imagine you are the CEO of a tech company who is great at multitasking, but overwhelmed by responsibilities. You hire a personal assistant (PA) to manage the workload. If you have a meeting scheduled with delegates from another company at 5:00 PM the following Tuesday, you would instruct your PA to "make a note of this meeting", and they would record it in a file.

Later, when you suddenly remember the meeting, you would ask your PA to fetch the details. In both scenarios, it is the PA who directly interacts with the file — first recording information, then retrieving it.

The file object acts as your PA, mediating between you (the coder) and the file stored on your computer's hard disk. You give instructions to the file object, which handles the actual reading and writing. All communication between you and the file passes through the file object.

### Mode

There are two modes for opening a file, covered more thoroughly in later lessons.

#### Read mode

The mode you choose for processing the file is an instruction that always comes from you and is directed at the file object. When reading, information flows from the file, through the file object, and to you. To read a file, you open it in read mode:

```python
f = open('<file_name>', 'r')
# ...
# code for reading something from file
# ...
f.close()
```

#### Write mode

When writing to a file, information flows from you, through the file object, and to the file. To write to a file, you open it in write mode:

```python
f = open('<file_name>', 'w')
# ...
# code for writing something into the file
# ...
f.close()
```

## Lesson 7.4 — File Methods {: #ch-7-lesson-4 }

### `read()`

Working with `examples.txt` (containing the lines one, two, three, four, five), the `read()` method returns the entire file as a single string.

```python
f = open('examples.txt', 'r')
content = f.read()
print(content)
f.close()
```

```output
one
two
three
four
five
```

The variable `content` is one string with newline characters between lines: `'one\ntwo\nthree\nfour\nfive'`. Every line except the last ends in `\n`, which is why printing produces separate lines, and why looping with `print(line)` earlier produced blank lines between entries.

### `readline()`

Reads one line at a time.

```python
f = open('examples.txt', 'r')
line1 = f.readline()
line2 = f.readline()
line3 = f.readline()
line4 = f.readline()
line5 = f.readline()
f.close()
```

| Variable | Value |
|----------|---------|
| `line1` | `'one\n'` |
| `line2` | `'two\n'` |
| `line3` | `'three\n'` |
| `line4` | `'four\n'` |
| `line5` | `'five'` |

Reading past the end returns an empty string, which gives a way to detect the file's end. A loop-based approach:

```python
f = open('examples.txt', 'r')
line = f.readline()
while line != '':
    print(line, end = '')
    line = f.readline()
f.close()
```

A more compact version uses truthiness and `strip()`:

```python
f = open('examples.txt', 'r')
line = f.readline()
while line:
    print(line.strip())
    line = f.readline()
f.close()
```

Python treats empty sequences as `False`, as this demonstrates:

```python
line = ''
if not line:
    print('It works!')
```

### `readlines()`

Reads the file into a list of line strings.

```python
f = open('examples.txt', 'r')
lines = f.readlines()
for line in lines:
    print(line.strip())
f.close()
```

The resulting list: `['one\n', 'two\n', 'three\n', 'four\n', 'five']`.

### `write()`

Writing in a loop, but naively adding `\n` to every line creates an extra empty line (six lines instead of five):

```python
f = open('writing.txt', 'w')
lines = ['one', 'two', 'three', 'four', 'five']
for line in lines:
    f.write(line + '\n')
f.close()
```

Fixing it by not appending `\n` after the last item:

```python
f = open('writing.txt', 'w')
lines = ['one', 'two', 'three', 'four', 'five']
for i in range(len(lines)):
    line = lines[i]
    if i != len(lines) - 1:
        f.write(line + '\n')
    else:
        f.write(line)
f.close()
```

`write()` only accepts strings. Passing an integer:

```python
f = open('writing.txt', 'w')
f.write(1)
f.close()
```

```output
Traceback (most recent call last):
  File "main.py", line 2, in <module>
    f.write(1)
TypeError: write() argument must be str, not int
```

Convert integers to strings first:

```python
f = open('writing.txt', 'w')
f.write(str(1))
f.close()
```

An exercise asks you to run the following (note `writeline` is not a real method) and consider why it fails:

```python
f = open('writing.txt', 'w')
f.writeline(str(1))
f.close()
```

### `writelines()`

Writes a list of strings to a file.

```python
f = open('writing.txt', 'w')
lines = ['1\n', '2\n', '3\n', '4\n', '5']
f.writelines(lines)
f.close()
```

Resulting file contents:

```output
1
2
3
4
5
```

## Lesson 7.5 — Reading CSV Files {: #ch-7-lesson-5 }

### CSV files

This section builds on earlier work with simple files by introducing CSV files, which are common in data science. In these files, values on each line are separated by commas. A sample CSV file might contain rows like `col0,col1,col2,col3` followed by data rows such as `row1,item11,item12,item13`.

These files work well for tabular data. The first line is the **header**, describing the columns; the remaining lines are the data rows. Represented as a table:

| | col0 | col1 | col2 | col3 |
|---|---|---|---|---|
| **row1** | item11 | item12 | item13 | |
| **row2** | item21 | item22 | item23 | |
| **row3** | item31 | item32 | item33 | |
| **row4** | item41 | item42 | item43 | |
| **row5** | item51 | item52 | item53 | |

### Reading a CSV file

The lesson creates a file named `table.csv` in Replit. Opening and reading it works just like a text file:

```python
f = open('table.csv', 'r')
for line in f:
    print(line.strip())
f.close()
```

```output
Name,Physics,Mathematics,Chemistry
Newton,100,98,90
Einstein,100,85,88
Ramanujan,70,100,70
Gauss,100,100,70
```

**Task:** Print each student's chemistry marks, one per line — meaning we extract the last column.

Consider one line. The newline appears on every line except the last, so we strip it:

```python
# The `\n` at the end will be present for all lines except the last one
line = 'Newton,100,98,90\n'
line = line.strip() # removes the \n character
```

Split the line on commas using `split()`:

```python
line = 'Newton,100,98,90\n'
line = line.strip()
columns = line.split(',')
print(columns)
```

This returns a list of strings:

```output
['Newton', '100', '98', '90']
```

Take the last element and convert it to an integer:

```python
line = 'Newton,100,98,90'
line = line.strip()
columns = line.split(',')
chem_marks = int(columns[-1])
print(chem_marks)
```

Now apply this to all rows using a loop:

```python
f = open('table.csv', 'r')
for line in f:
    line = line.strip()
    columns = line.split(',')
    chem_marks = int(columns[-1])
    print(chem_marks)
f.close()
```

But this produces an error:

```output
Traceback (most recent call last):
  File "main.py", line 5, in <module>
    chem_marks = int(columns[-1])
ValueError: invalid literal for int() with base 10: 'Chemistry'
```

The problem is that the code tried to convert the header's last column to an integer. When reading CSV files, "we need to find a way to deal with the header." Modified code:

```python
f = open('table.csv', 'r')
header = f.readline()
# The file object has finished reading the first line
# It is now ready to read from the second line onwards
for line in f:
    line = line.strip()
    columns = line.split(',')
    chem_marks = int(columns[-1])
    print(chem_marks)
f.close()
```

This works. After reading the header on the second line, the for loop begins from the file's second line onward.

An alternative using `readlines()` alone:

```python
f = open('table.csv', 'r')
lines = f.readlines()
# lines[1: ] is the rest of the list 
# after ignoring the header
for line in lines[1: ]:
    line = line.strip()             # strip the line of \n
    columns = line.split(',')       # split based on comma
    chem_marks = int(columns[-1])   # convert last column to int
    print(chem_marks)
f.close()
```

`readlines()` is reasonable for small files (under ~1000 lines): all lines come back in a list, so file processing becomes list processing. If `lines` is the list, then `lines[i]` corresponds to the (i + 1)th line in the file, and the ith file line corresponds to `lines[i - 1]`.

!!! warning "Processing large files"

    For large files, `readline()` is the best method, reading one line at a time. Using `readlines()` on large files is dangerous because it dumps the whole file into a list of strings, consuming large amounts of memory.

The same program written with `readline`:

```python
f = open('table.csv', 'r')
header = f.readline().strip()       # this is for the header
line = f.readline()                 # second line; actual rows begin
while line:
    line = line.strip()             # strip the line of \n
    columns = line.split(',')       # split based on comma
    chem_marks = int(columns[-1])   # convert last column to int
    print(chem_marks)
    line = f.readline()             # read the next line in the file
f.close()
```

### Files to Collections

It is often useful to convert a CSV file into a suitable collection. Here the goal is to build a list of dictionaries:

```python
data = [
{'Name': 'Newton', 'Physics': 100, 'Mathematics': 98, 'Chemistry': 90}, 
{'Name': 'Einstein', 'Physics': 100, 'Mathematics': 85, 'Chemistry': 88}, 
{'Name': 'Ramanujan', 'Physics': 70, 'Mathematics': 100, 'Chemistry': 70}, 
{'Name': 'Gauss', 'Physics': 100, 'Mathematics': 100, 'Chemistry': 70}]
```

Points to note:

- It is a list of dictionaries, one dictionary per file row.
- Header elements become the keys in each dictionary.
- Values have different data types — names are strings, marks are integers.

The full code is broken into parts. First, get the stripped list of lines:

```python
f = open('table.csv', 'r')
lines = [ ]
for line in f.readlines():
    line = line.strip()
    lines.append(line)
# Now, we have the list of lines
```

Next, extract header details:

```python
header = lines[0].split(',')    # lines[0] is the first row
num_cols = len(header)
# Now, we have the header information
# We also know the number of columns in the file
```

Finally, process the remaining lines:

```python
### Block-3 ###
data = [ ]                      # list to store the contents
for line in lines[1: ]:         # ignore the header
    cols = line.split(',')      # split the column based on comma
    row_dict = dict()           # create a dict to store this particular row
    for i in range(num_cols):   # go through each element (column) in this row
        key = header[i]         # key will be this column's name
        if key == 'Name':       # are we storing a name or a number?
            value = cols[i]     # since this is a name, don't convert to int
        else: 
            value = int(cols[i])    # since this is marks, convert to int
        row_dict[key] = value       # update dict
    data.append(row_dict)           # append this row to the list data
f.close()
```

!!! note "Note"

    CSV stands for comma-separated values.
