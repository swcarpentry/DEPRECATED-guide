Basic Programming With Python
=============================

A cochlear implant is a small device placed in the inner ear to give the
hearing impaired a sense of sound. To test how effective they are,
Aurora Audio wants to measure three things: the range of tones people
can hear, how well they can discriminate between similar tones. and the
softest volume they can notice. Each test is supposed to be scored from
0 to 5, but after her volunteers submitted their data, she found that
some had scored from -5 to 5 instead. She needs to clean up the data
before using it.

If Aurora had only one data set, the fastest solution might be to use a
spreadsheet. However, she actually has over a hundred data sets, with
more coming in each week. Since she doesn't want to spend hours doing
the same things over and over again, she wants to write a small program
to clean up her data for her. To do that, she's going to have to learn
how to program, and that's what the next couple of chapters are about.

We will use a programming language called Python for our examples.
Python is free, reasonably well documented, and widely used in science
and engineering. Our main reason for choosing it, though, is that
newcomers find it easier to read than most other languages. It also
allows people to do useful things without having to master advanced
concepts like object-oriented programming.

Our first few programs will show you how to manipulate data stored in
text files. This is a bit old fashioned, but it's still a common task in
every branch of science. It's also simple: flashier approaches, like
manipulating images and doing 3D graphics, require extra software that
can be painful to install.

Basic Operations
----------------

### Learning Objectives:

-   Run the Python interpreter interactively.
-   Correctly enter basic arithmetic expressions.
-   Explain what variables are used for.
-   Assign numbers and strings to variables.
-   Explain what happens when one variable is assigned to another.
-   Trace the effect of several consecutive assignment statements.

The best way to learn how to program is to start programming, so let's
run the Python interpreter and type in the following:

    >>> print 1 + 1
    2

The `>>>` [prompt](glossary.html#prompt) is the interpreter's way of
telling us that it's waiting for input, like the `$` prompt in [the
shell](shell.html). When we enter 1+1, Python does the calculation we've
asked for and prints the result.

Now type this:

    >>> x = 1+1

Python doesn't display anything this time (except another prompt).
Instead, as [Figure 1](#f:first_variable) shows, it creates a
[variable](glossary.html#variable) called `x` and assigns it the value
2. We can then get that variable's value simply by entering its name:

    >>> print x
    2

![Our First Variable](img/python/first_variable.png)

### Statements vs. Expressions

Python is a fairly relaxed language, but there are still some things it
won't let us do. For example, this doesn't work:

    print x = 1 + 2
    SyntaxError: invalid syntax

The problem is that printing and assignment are both
[statements](glossary.html#statement), and statements cannot be mixed
together. 1+2, on the other hand, is an
[expression](glossary.html#expression)—something that produces a new
value—and expressions can be combined in many ways. Except for
assignment, every statement in Python begins with a keyword like
`print`, so it's usually easy to tell them apart.

We can now use that variable's value in calculations:

    >>> print x * 2
    4

including ones that create more variables:

    >>> y = x * 2
    >>> print y
    4

We can change a variable's value by assigning something new to it:

    >>> x = 10
    >>> print x
    10

As [Figure XXX](#f:assign_new_value) shows, assigning something to `x`
changes what it points to, but does not change anything else. In
particular, `y` still has the value 4 after this assignment: it is not
automatically updated when `x`'s value changes, as it would in a
spreadsheet.

![Assigning a New Value](img/python/assign_new_value.png)

Here's a more complex calculation:

~~~~ {src="src/python/fahrenheit_to_kelvin_unreadable.py"}
>>> x = 98.6
>>> y = (x - 32.0) * (5.0 / 9.0) + 273.15
>>> print y
310.15
~~~~

Its meaning becomes clearer if we rewrite it as:

~~~~ {src="src/python/fahrenheit_to_kelvin.py"}
>>> temp_fahr = 98.6
>>> temp_kelvin = (temp_fahr - 32.0) * (5.0 / 9.0) + 273.15
>>> print "body temperature in Kelvin:", temp_kelvin
body temperature in Kelvin: 310.15
~~~~

The first line creates a new variable called `temp_fahr` (short for
"temperature in Fahrenheit") and gives it the value 98.6 ([Figure
XXX](#f:first_memory_model)). The second line creates another variable
to hold the temperature in Kelvin (hence its name). It calculates a
value for this variable that depends on the value of `temp_fahr`. The
last line prints the result. The [character
string](glossary.html#string) (or just "string" for short) inside double
quotes is printed as-is, followed by the value of `temp_kelvin`.

![First Memory Model](img/python/first_memory_model.png)

Like every program, this one stores data and does calculations. We use
variables to do the first, and write instructions that use those
variables to do the second. And like every *good* program, this one is
written with human beings in mind. Computers get faster every year, but
our brains don't. As a result, the real bottleneck in scientific
computing is usually not how fast the program runs, but how long it
takes us to write it. This is why we use variable names like `temp_fahr`
and `temp_kelvin` instead of `x` and `y`.

### Creating Variables

Python creates a variable whenever a value is assigned to a name, but
won't let us get the value of a variable that hasn't been assigned one.
For example, if we try to do this:

    >>> double_temp = temp_celsius * 2

then Python prints an error message:

    Traceback (most recent call last):
      File "<undefined-variable.py>", line 1, in <module>
    NameError: name 'temp_celsius' is not defined

We'll explain what "module" means [later](funclib.html). What's
important now is that this strictness helps catch a lot of typing
mistakes: if we mistakenly type `temp_far` instead of `temp_fahr`:

    >>> temp_kelvin = (temp_far - 32.0) * (5.0 / 9.0) + 273.15

then Python will tell us something's gone wrong. It can't help us if we
type 3.20 instead of 32.0, though; if we want to catch that mistake,
we'll actually have to [test our program](quality.html).

Readability is also why we put the temperature in Fahrenheit in a
variable, then use that variable in line 2, rather than just putting
98.6 directly in the calculation. If we ever want to convert another
temperature, it's easier to see and change the value on line 1 than it
would be to find it buried in the middle of a line of arithmetic.

Finally, this first program also shows how arithmetic is done. '+' means
addition, '\*' means multiplication, and parentheses group things
together, just as they do in pen-and-paper arithmetic. We have to use
parentheses here because (also as in arithmetic) multiplication takes
precedence over addition: the expression `2*3+5` means, "Multiply two by
three, then add five," rather than, "Add three and five, then multiple
by two." If we want the latter, we have to write `2*(3+5)`.

### Repeating Commands

Just as we could repeat previous commands in the shell by using the [up
arrow](shell.html#a:repeat), so too can we repeat commands in the Python
interpreter. And while the standard interpreter doesn't have an
equivalent of the shell's `history` command, more advanced shells like
IPython do (along with much more).

### Summary

-   Use '=' to assign a value to a variable.
-   Assigning to one variable does not change the values associated with
    other variables.
-   Use `print` to display values.
-   Variables are created when values are assigned to them.
-   Variables cannot be used until they have been created.
-   Addition ('+'), subtraction ('-'), and multiplication ('\*') work as
    usual in Python.
-   Use meaningful, descriptive names for variables.

### Challenges

1.  What is the output of:

        >>> inner = 13.0
        >>> outer = 2 * inner
        >>> inner = 2 * inner
        >>> print outer

    1.  `13.0`{.out}
    2.  `26.0`{.out}
    3.  `52.0`{.out}
    4.  None of the above.

2.  Fill in the blank so that these lines of code produce the output
    shown.

        >>> female = 'GGT'
        >>> male = 'CAC'
        >>> ________
        >>> print female
        GGTGGTCAC

    1.  `female = female + female + male`{.in}
    2.  `female = (female + female) + male`{.in}
    3.  `female = 2 * female + male`{.in}
    4.  Any of the above.

3.  What single change can be made to the first three lines below to get
    the output shown?

        >>> scaling = 10 # line 1
        >>> original = 7 # line 2
        >>> adjusted = primary / scaling # line 3
        >>> print original + adjusted # line 4
        7.7

    1.  On line 1, change 10 to 0.1
    2.  On line 2, change 7 to 7.7
    3.  On line 3, change `adjusted` to `original`
    4.  None of the above.

Creating Programs
-----------------

### Learning Objectives:

-   Store Python commands in a file.
-   Use the interpreter to run a file containing Python commands.

Typing in commands over and over again is tedious and error-prone. Just
as we saved shell commands in [shell scripts](shell.html#s:scripts), we
can save Python commands in files and then have the Python interpreter
run those. Using your favorite text editor, put the following three
lines into a plain text file:

~~~~ {src="src/python/greeting.py"}
left = "hello"
right = "there"
print left, right
~~~~

and then save it as `greeting.py`. (By convention, Python files end in
'.py' rather than '.txt'.) To run it from the shell, type:

    $ python greeting.py
    hello there

When the Python interpreter executes a file, it runs the commands in
that file just as if they had been typed in interactively. It doesn't
wait until the whole file has been read to start executing; instead, as
the example below shows, it runs each command as soon as it can:

~~~~ {src="src/python/executing_file.py"}
print "before"
1/0
print "after"
before
Traceback (most recent call last):
  File "a.py", line 2, in <module>
    1/0
ZeroDivisionError: integer division or modulo by zero
~~~~

Note that this can lead to some confusing output. For example, if we
change the example above to:

    print "before", 1/0, "after"

then the output is:

    before
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ZeroDivisionError: integer division or modulo by zero

### Summary

-   Store programs in files whose names end in `.py` and run them with
    `python name.py`.

### Challenges

Nelle has created a file called `example.py` that contains the following
lines:

    tolerance = 5.0e3
    diameter = 2 * (tolerance/1000) ** 2 note the double '*'

What happens when she runs this file from the shell using the command:

    $ python -i example.py

1.  The statements are run in reverse order ('i' for 'inverted').
2.  The interpreter runs the program, then waits for interactive
    commands ('i' for 'interactive').
3.  The interpreter prints a list of the variables defined in the
    program ('i' for 'inspect').
4.  None of the above.

Nelle has created two programs called `prepare.py` and `analyze.py`.
What happens when she runs the command:

    $ python prepare.py analyze.py

1.  Python runs the two programs in the order shown.
2.  Python runs `prepare.py` but not `analyze.py`.
3.  Python runs `analyze.py` but not `first.py`.
4.  Python reports an error.

Types
-----

### Learning Objectives:

-   Explain what a data type is, and give examples of three different
    data types.
-   Correctly identify the types of integer, floating-point, and string
    values.
-   Call a built-in function.
-   Explain what "type conversion" is, and give an example.
-   Explain (with an example) why programs shouldn't guess what people
    want to do.

Let's take another look at our program:

~~~~ {src="src/python/fahrenheit_to_kelvin.py"}
temp_fahr = 98.6
temp_kelvin = (temp_fahr - 32.0) * (5.0 / 9.0) + 273.15
print "body temperature in Kelvin:", temp_kelvin
body temperature in Kelvin: 310.15
~~~~

Why have we written 5.0/9.0 instead of 5/9? Let's see what happens if we
take out the .0's:

~~~~ {src="src/python/fahrenheit_to_kelvin_int.py"}
>>> temp_fahr = 98.6
temp_kelvin = (temp_fahr - 32) * (5 / 9) + 273.15
>>> print "body temperature in Kelvin:", temp_kelvin
body temperature in Kelvin: 273.15
~~~~

That's not right. To understand what's gone wrong, let's look at 5/9:

    >>> 5/9
    0

The problem is that integers and floating point numbers (or
[floats](glossary.html#float)) are different things to a computer. If a
number doesn't have a decimal point, then Python stores its value as an
integer (with no fractional part). When it divides one integer by
another, it throws away the remainder. If a number contains a decimal
point, though, Python stores it as a float. When it does division (or
any other kind of arithmetic), the result is a float if either of the
values involved is a float:

    >>> 10 / 3
    3
    >>> 10.0 / 3
    3.3333333333333335

This makes sense, but only if you understand how the chips inside
computers work. Version 3 of Python changed the rules for division so
that it returns fractional numbers whenever it needs to. However, we're
using Python 2.7 in this course, so 10/3 is 3 until further notice.

Every value in a program has a specific [type](glossary.html#type) which
determines how it behaves and what can be done to it. We can find out
what type something is using a built-in
[function](glossary.html#function) called `type`:

    >>> type(12)
    <type 'int'>
    >>> type(12.0)
    <type 'float'>

Integers and floating-point numbers are two common types; another is the
character string. We can create one by putting characters inside either
single or double quotes (as long as they match at the beginning and
end):

~~~~ {src="src/python/simple_string.py"}
>>> name = "Alan Turing"
>>> born = 'June 23, 1912'
>>> print name, born
Alan Turing June 23, 1912
~~~~

We can also "add" strings:

~~~~ {src="src/python/simple_string.py"}
>>> full = name + " (" + born + ")"
>>> print full
Alan Turing (June 23, 1912)
~~~~

What we *can't* do is add numbers and strings:

~~~~ {src="src/python/add_numbers_strings.py"}
>>> print 2 + "three"
Traceback (most recent call last):
  File "add-numbers-strings.py", line 1, in <module>
    print 2 + "three"
TypeError: unsupported operand type(s) for +: 'int' and 'str'
~~~~

The string "2three" would be a reasonable result in this case, but it's
not so clear what `2+"3"` should do: should it produce the integer 5 or
the string `"23"`? Rather than guessing at the programmer's intentions,
Python expects some guidance:

    >>> print 2 + int("3")
    5
    >>> print str(2) + "3"
    23

`int` and `str` are two more built-in functions which convert values to
particular types. We'll look at functions in much more detail in [the
next chapter](funclib.html).

### Summary

-   The most commonly used data types in Python are integers (`int`),
    floating-point numbers (`float`), and strings (`str`).
-   Strings can start and end with either single quote (') or double
    quote (").
-   Division ('/') produces an `int` result when given `int` values: one
    or both arguments must be `float` to get a `float` result.
-   "Adding" strings concatenates them, multiplying strings by numbers
    repeats them.
-   Strings and numbers cannot be added because the behavior is
    ambiguous: convert one to the other type first.
-   Variables do not have types, but values do.

### Challenges

1.  If the variable `x` holds a number, is the value of `int(str(x))`
    always the same as the value of `x`?
    1.  Yes.
    2.  No, because functions cannot be put inside functions.
    3.  No, because the expression should be `int('str(x)')` (with
        quotes).
    4.  No, because `x` might be a floating-point number.

2.  What is value of `molecule` after the following code is run?

        >>> oxygen = 'O'
        >>> carbon = 'C
        >>> molecule = carbon + oxygen * 2

    1.  `'COO'`
    2.  `'CO2'`
    3.  `'COCO'`
    4.  None of the above: an error occurs on the last line.

3.  Fill in the blanks so that these lines of code produce the output
    shown.

        >>> pi = 3.14
        >>> x = ____(pi)
        >>> y = ____(x)
        >>> print y
        3.14

    1.  `float` and `str`
    2.  `str` and `str`
    3.  `str` and `float`
    4.  `int` and `float`

Reading Files
-------------

### Learning Objectives:

-   Draw a diagram to explain where computers store data.
-   Write programs that open, read, and close files.
-   Explain how "lines" of text are actually stored in files.
-   Call a pre-defined method of a built-in type.
-   Write programs that write data to files.

Broadly speaking, modern computers store data in one of six places
([Figure XXX](#f:memory_architecture)):

1.  Inside the processor itself.
2.  Inside a short-term memory called cache.
3.  In main memory.
4.  On a local disk.
5.  On disk somewhere else on a network.
6.  In an offline archive, such as a DVD jukebox.

![Where Data is Stored](img/python/memory_architecture.png)

Each level is tens to thousands of times faster than the one below it,
but tens to thousands of times more expensive per byte. Computer systems
have therefore been designed to expose some of these layers to users,
but not others: for example, it's actually hard to figure out exactly
when data is in the CPU, in cache, or in main memory.

In practice, this six-level hierarchy can be divided into three layers:

1.  The data is in memory. The program can manipulate it directly, but
    changes will not be saved when the program ends.
2.  The data is on disk. The program has to read it into memory to work
    with it, and write changes back out, but those changes will persist
    after the program ends.
3.  The data is far away, and may not be available when we want it.

We'll deal with the third issue in a [later chapter](web.html). For now,
let's look at how to get data out of a file on our computer's hard
drive. Suppose our hearing test data files are formatted like this:

~~~~ {src="src/python/cochlear01.txt"}
Subject: 1782
Date:    2012-05-21
Test     Run  Score
----     ---  -----
range    1    3
range    2    5
discrim  1    1
discrim  2    1
discrim  4    1.5
volume   1    3.5
volume   2    4.0
~~~~

It's easy to see where the tester decided that half-point scores were
OK. We can also see that the tester either forgot to record the result
of the third discrimination test, or decided to leave it out. Before
worrying about that, let's write a small program that extracts the
subject ID from a data file:

~~~~ {src="src/python/get_subject_date.py"}
reader = file('cochlear01.txt', 'r')
first_line = reader.readline()
print first_line
reader.close()
~~~~

The first line uses a built-in function called `file` to open our file.
Its first argument is the name of the file being opened. Its second is
the string `'r'`, which signals that we want to read from this file
(rather than write to it).

`file` creates a connection (or [handle](glossary.html#handle)) between
the program and the data on disk ([Figure XXX](#f:file_object)), which
is assigned to the variable `reader`. There's nothing special about that
name—we could call it `newton`—but whatever we call it, we can ask it to
read a line from the file for us and assign that string to `first_line`
by calling its [method](glossary.html#method) `readline`. The program
then prints that line and tells the file to close itself. This last step
isn't strictly necessary in a small program—Python automatically closes
any files that are open when the program finishes—but it's a good habit
to get into, since the operating system limits the number of files any
one program can have open at a time.

![File Objects](img/python/file_object.png)

### Methods

`readline` is a special kind of function called a
[method](glossary.html#method). It's attached to a particular object—in
this case, to the file handle `reader`. You can think of objects and
methods as nouns and verbs, so when we write `reader.readline()`, we're
asking whatever the variable `reader` points at to do `readline` for us.
As [Figure XXX](#f:methods) shows, the methods are associated with the
thing the variable points at, not with the variable itself.

![Where Methods are Stored](img/python/methods.png)

Here's what happens when we run our program:

    $ python get-subject-date.py
    Subject: 1782

It's not easy to see, but there's actually an extra blank line in the
output. Where does it come from?

The answer depends on the fact that text files aren't stored in lines:
that's just how things like text editors and shell commands display
them. A text file is actually stored as a sequence of bytes ([Figure
XXX](#f:text_file_storage)). Some of those happen to be newline
characters, and most tools interpret them as meaning "end of line". In
particular, when asked to read the next line from a file, Python's
file-reading functions read up to and including the end-of-line marker
and return that.

![Text File Storage](img/python/text_file_storage.png)

Nothing says files have to be stored this way, though. On Windows, text
files use two characters—a carriage return and a newline—to mark the end
of line. If we are using Python on Windows, it automatically translates
those two characters into a single newline when reading, and translates
newlines back into those two characters when writing, so that our
programs don't have to worry about it.

Coming back to our program, the `print` command automatically adds an
end-of-line marker to its output. We can tell it not to do that by
putting a comma at the end of the line. This usually makes things
confusing:

    >>> print 5
    5
    >>> print 5,
    5>>>

but it's useful when we want to prevent newlines doubling up:

~~~~ {src="src/python/get_subject_date_newline.py"}
reader = file('cochlear01.txt', 'r')
first_line = reader.readline()
print first_line,
reader.close()
Subject: 1782
~~~~

A better way to solve the problem is to get rid of the line ending on
the string:

~~~~ {src="src/python/get_subject_date_newline.py"}
reader = file('cochlear01.txt', 'r')
first_line = reader.readline()
first_line = first_line.strip()
print first_line
reader.close()
Subject: 1782
~~~~

`first_line` is a string, and, like files, strings have methods. One of
them, `strip`, creates a new string by removing any leading or trailing
spaces, tabs, or line-ending characters from the original string
([Figure XXX](#f:string_strip)). It does *not* modify the original
string: in Python, any string has a fixed value, just as the integer
`5`'s value is always fixed at 5.

![Stripping Strings](img/python/string_strip.png)

### Writing Files

Writing to a file is as easy as reading from one:

~~~~ {src="src/python/writing.py"}
writer = file('mydata.txt', 'w')
print >> writer, 'largest value:', 20
print >> writer, 'smallest value:', -2
writer.close()
~~~~

We begin by opening the file in `'w'` (write) mode. This gives us a
handle that we can use in subsequent operations, which we assign to a
variable. (We've called it `writer` here, but we could call it
anything.) After that, we can print to the file exactly as we have been
printing to the screen; as always, we close the file when we're done
(which is when the last few things we've written to the file are
actually stored on disk).

Opening a file for writing erases its previous content, or creates the
file if it didn't already exist. If we don't want to erase any previous
content, we can open the file for appending using `'a'` instead of
`'w'`.

### Summary

-   Data is either in memory, on disk, or far away.
-   Most things in Python are objects, and have attached functions
    called methods.
-   When lines are read from files, Python keeps their end-of-line
    characters.
-   Use `str.strip` to remove leading and trailing whitespace (including
    end-of-line characters).
-   Use `file(name, mode)` to open a file for reading ('r'), writing
    ('w'), or appending ('a').
-   Opening a file for writing erases any existing content.
-   Use `file.readline` to read a line from a file.
-   Use `file.close` to close an open file.
-   Use `print >> file` to print to a file.

### Challenges

1.  If `species.txt` is a text file, what do the following lines print?

        info = open('species.txt', 'r')
        print info.readline().strip()

    1.  The first character of the file.
    2.  Any blanks at the start or end of the first line of the file.
    3.  The first line of the file with leading and trailing blanks
        removed.
    4.  Nothing: the statement is an error.

2.  What does the following program leave in the file `output.txt`?

        results = open('output.txt', 'w')
        results.write('first')
        results.close()
        results = open('output.txt', 'a')
        results.write('second')
        results.close()

    1.

    2.

    3.

    4.

        firstsecond

        first
        second

        second

    Nothing.

3.  If the file `square.txt` contains:

        abcde
        fghij
        klmno

    what does the following program print?

        handle = open('square.txt', 'r')
        result = len(handle)
        handle.close()
        print result

    1.  3
    2.  15
    3.  18
    4.  The program produces an error message.

4.  If `square.txt` contains the three lines shown above, and the file
    `final.txt` does not exist, what is the effect of the following
    program?

        reader = open('square.txt', 'r')
        writer = open('final.txt', 'w')
        writer = reader
        reader.close()
        writer.close()

    1.  It creates an empty file called `final.txt`.
    2.  It copies the first line of `square.txt` to `final.txt`.
    3.  It copies all three lines from `square.txt` to `final.txt`.
    4.  It copies all three lines from `square.txt` to `final.txt`, but
        leaves `square.txt` empty.

Standard Input and Output
-------------------------

### Learning Objectives:

-   Explain what "importing a module" means and does.
-   Write programs that import standard library modules.
-   Explain what standard input and output are, and how they relate to
    the [pipe-and-filter](shell.html#b:pipefilter) model.
-   Write programs that read from standard input.
-   Write programs that write to standard output.

Our program currently reads the header from `cochlear01.txt` every time
we run it. There's not much point in that: what we really want is to
read from any file, or from several files in turn. Doing that requires a
bit of machinery we haven't seen yet, so let's solve a simpler problem:
reading from standard input instead of from a file. Once we can do that,
we can run our program as:

    $ python get-subject-date.py < somefile.txt

or read from several files using:

    $ for inputfile in cochlear*.txt
    do
        python get-subject-date.py < $inputfile
    done

Here's the modified program:

~~~~ {src="src/python/get_subject_date_stdin.py"}
import sys
reader = sys.stdin
first_line = reader.readline()
first_line = first_line.strip()
print first_line
reader.close()
~~~~

The two lines that have changed are highlighted at the top of the
program. The first loads a library called `sys`, which connects Python
to the system it is running on. The second line sets `reader` to be
`sys.stdin`, which is just the standard input stream we met in [our
discussion of pipes](shell.html#s:pipefilter:pipes). Nothing else
changes, since standard input tries really hard to behave like an open
file ([Figure XXX](#f:replacing_with_stdin)). In particular, the object
that `sys.stdin` (and hence `reader`) points at has a method with the
same name and behavior as a file's `readline` method, and another with
the same name and behavior as a file's `close`, so we can swap one for
the other without having to modify anything else.

![Replacing a File with Standard
Input](img/python/replacing_with_stdin.png)

### Interactive Testing

One other benefit of reading from standard input when no files are
supplied is that it allows interactive testing: we can run our program
and then just type in things we want it to read. If we do this, we must
type control-D to signal the end of input (or control-Z in a Windows
shell).

### Writing to Standard Output

Just as we can write to an open file using `print >> handle`, we can
write to standard output using `print >> sys.stdout`. This is redundant,
though, since `print` sends things to standard output by default.

### Summary

-   The operating system automatically gives every program three open
    "files" called standard input, standard output, and standard error.
-   Standard input gets data from the keyboard, from a file when
    redirected with '\<', or from the previous stage in a pipeline with
    '|'.
-   Standard output writes data to the screen, to a file when redirected
    with '\>', or to the next stage in a pipeline with '|'.
-   Standard error also writes data to the screen, and is not redirected
    by '\>' or '|'.
-   Use `import library` to import a library.
-   Use `library.thing` to refer to something imported from a library.
-   The `sys` library provides open "files" called `sys.stdin` and
    `sys.stdout` for standard input and output.

### Challenges

1.  What is the difference between:

        import sys
        reader = sys.stdin
        print len(reader.readline())

    and:

        import sys
        print len(sys.stdin.readline())

    1.  Nothing: they do exactly the same thing.
    2.  The second is not legal Python.
    3.  The first waits until there is actually input before running;
        the second does not.
    4.  None of the above (i.e., they are different in some other way).

2.  What does this program do?

        import sys                                # line 1
        sys.stdin = open('temporary.txt', 'w')    # line 2
        sys.stdin.write(123)                      # line 3
        sys.stdin.close()                         # line 4

    1.  It produces an error message on line 2 because `sys.stdin`
        cannot be opened for writing.
    2.  It produces an error message on line 3 because the number 123
        cannot be written written using `file.write`.
    3.  It sends the number 123 to the previous stage in the
        command-line pipeline.
    4.  It saves the number 123 to the file `temporary.txt`.

3.  Nelle wants to copy the first line of `patients.txt` to the file
    `subjects.txt` using the shell command:

        $ python copier.py > subjects.txt

    Fill in the blanks in the program below so that it does this.

        import sys
        source = ________
        line = ________
        source.close()
        ________.________(line)

      --------------------- --------------------- ------------------------ ----
      1.                    2.                    3.                       4.
      `open(sys.stdin)`     `sys.stdin`           `sys.stdin`
      `source.readline()`   `source.readline()`   `sys.stdin.readline()`
      `stdout`              `sys.stdout`          `sys`
      `write`               `write`               `stdout`
      --------------------- --------------------- ------------------------ ----

Repeating Things
----------------

### Learning Objectives:

-   Write a loop that processes the lines of a file.
-   Trace the values taken on by a loop variable during execution of the
    loop.
-   Explain what the "body" of a loop is, and correctly identify the
    bodies of loops.

Computers are useful because they can do lots of calculations on lots of
data, which means we need a concise way to represent multiple steps.
(After all, writing out a million additions would take longer than doing
them.) Let's start by finding out how many lines we have in our data
file:

~~~~ {src="src/python/count_line_in_file.py"}
reader = file('cochlear01.txt', 'r')
number = 0
for line in reader:
    number = number + 1
reader.close()
print number, 'lines in file'
11 lines in file
~~~~

Once again, we create a connection to the file using `file`. We then use
a [for loop](glossary.html#for-loop) to get one line from the file at a
time. We don't do anything with the lines; instead, we add 1 to the
value of `number` each time we see a new one. Once we're done, we close
the file (so that other people and programs can access it safely) and
report our findings ([Figure XXX](#f:for_loop)).

![For Loop](img/python/for_loop.png)

The indented line is called the [body](glossary.html#loop-body) of the
loop. It's the command that Python executes repeatedly. When Python is
expecting us to type in the body of a loop interactively, it changes its
prompt from `>>>` to `...` as a reminder.

The variable `line` is sometimes called the [loop
variable](glossary.html#loop-variable). There's nothing special about
its name: we could equally well have called it `something`. What's
important is that the `for` loop repeatedly assigns a value to it, then
executes the loop body one more time.

Python always uses indentation to show what's in the body of a loop (or
anything else—we'll see other things that have bodies soon). This means
that:

~~~~ {src="src/python/incorrectly_nested.py"}
for line in reader:
    print line.strip()
    print "done"
~~~~

and:

~~~~ {src="src/python/correctly_nested.py"}
for line in reader:
    print line.strip()
print "done"
~~~~

are different programs. The first one prints:

    Subject: 1782
    done
    Date:    2012-05-21
    done
    Test     Run  Score
    done
    ...

because the statement `print "done"` is inside the loop body. The second
prints:

    Subject: 1782
    Date:    2012-05-21
    Test     Run  Score
    ...
    volume   2    4.0
    done

because it is not.

### Why Indentation?

Most other languages use visible markers to show the beginnings and ends
of loop bodies, such as:

    for value in data {
        print value
    }

or:

    for value in data
    begin
        print value
    end

Python uses indentation because studies done in the 1980s showed that's
what people actually pay attention to. If we write something as:

    for value in data {
        print value
    }
        print "done"

then most people reading the code in a hurry will "see" the second
`print` statement as part of the loop.

### Summary

-   Use `for variable in something:` to loop over the parts of
    something.
-   The body of a loop must be indented consistently.
-   The parts of a string are its characters; the parts of a file are
    its lines.

### Challenges

1.  Suppose that the file `counts.txt` contains:

        1
        2
        3

    What does the following program print?

        source = open('counts.txt', 'r')
        result = 'result:'
        for data in source:
            result = result + data.strip()
        source.close()
        print result

    1.  An error message, because you cannot add numbers to strings.
    2.  `result:123`{.out}
    3.  `result:6`{.out}
    4.  None of the above.

2.  If `counts.txt` contains the same data, what does the following
    program print?

        source = open('counts.txt', 'r')
        first = source.readline()
        second = source.readline()
        for next in source:
            first = second
            second = next
        source.close()
        print first, second, next

    1.

    2.

    3.

    4.

        1 2 3

        1
        2
        3

        1
        3
        3

        2
        3
        3

3.  What does the following program print?

        odds = '135'
        evens = '246'
        total = 0
        for first in odds:
            total = total + int(first)
        for second in evens:
            total = total + int(first)
        print total

    1.  12
    2.  21
    3.  24
    4.  An error message.

4.  What does the following program print?

        text = 'abc'
        for char in text:
            text = text + char
        print text

    1.  `abca`{.out}
    2.  `abcabc`{.out}
    3.  `abcc`{.out}
    4.  An error message (the program eventually crashes when it runs
        out of memory).

Making Choices
--------------

### Learning Objectives:

-   Trace the execution of conditional statements.
-   Write conditional statements to perform selected statements only
    under specific conditions.
-   Use logical operators to combine tests in conditional statements.
-   Explain what "in-place operators" are, and correctly write
    statements using them.

Let's make one more change to our program. If you recall, our data files
look like this:

~~~~ {src="src/python/cochlear01.txt"}
Subject: 1782
Date:    2012-05-21
Test     Run  Score
----     ---  -----
range    1    3
range    2    5
discrim  1    1
discrim  2    1
discrim  4    1.5
volume   1    3.5
volume   2    4.0
~~~~

The first four lines aren't actually data, so we really shouldn't
include them in our count:

~~~~ {src="src/python/count_line_in_file_corrected.py"}
reader = file('cochlear01.txt', 'r')
number = 0
for line in reader:
    number = number + 1
reader.close()
print number - 4, 'lines in file'
7 lines in file
~~~~

Of course, if anyone ever puts more (or less) than four descriptive
lines at the top of a data file, our count will be wrong again. What we
*really* want to do is skip everything up to the dashed lines. We also
want to check that all the scores are between 0 and 5.

Let's step back and build up the machinery we need. Suppose that our
data files contained nothing but a single number on each line:

~~~~ {src="src/python/simple_cochlear02.txt"}
3
5
-1
1
1.5
7
4.0
~~~~

(We have deliberately added two out-of-range values for our program to
find.) Here's a program that reads the data and counts the number that
fall outside the allowed range:

~~~~ {src="src/python/counting_outliers_wrong.py"}
import sys
num_outliers = 0
for value in sys.stdin:
    if value < 0:
        num_outliers = num_outliers + 1
    if value > 5:
        num_outliers = num_outliers + 1
print num_outliers, "values out of range"
~~~~

The command `if` means exactly what it does in English: if a particular
condition is true, then do the statement or statements that are in the
`if` statement's body (i.e., indented underneath it). Here, we are using
one `if` to see if the current value is less than 0, and another to see
if it is greater than 5. In either case, we add one to the count of
outliers. If neither condition is satisfied, the value is clean, and
`num_outliers` won't be changed in that loop ([Figure
XXX](#f:loop_cond_flow)).

![Conditional Execution](img/python/loop_cond_flow.png)

When we run this program, though, we don't get a count of outliers.
Instead, we get an error message:

    $ python count-outliers.py < cochlear01.txt
    fixme: error message

The problem is once again one of types: the loop variable `line` holds a
string like `'3'`, not the number 3. The fix is straightforward:

~~~~ {src="src/python/counting_outliers_wrong.py"}
import sys
num_outliers = 0
for line in sys.stdin:
    value = float(line)
    if value < 0:
        num_outliers = num_outliers + 1
    if value > 5:
        num_outliers = num_outliers + 1
print num_outliers, "values out of range"
2 values out of range
~~~~

We can combine our two tests using `and` and `or`:

~~~~ {src="src/python/simple_and_or.py"}
import sys
num_outliers = 0
for line in sys.stdin:
    value = float(line)
    if (value < 0) or (value > 5):
        num_outliers = num_outliers + 1
print num_outliers, "values out of range"
2 values out of range
~~~~

Alternatively, we could count how many values are in range by reversing
the test:

~~~~ {src="src/python/simple_in_range.py"}
import sys
num_valid = 0
for line in sys.stdin:
    value = float(line)
    if (0 <= value) and (n <= value):
        num_valid = num_valid + 1
print num_valid, "values in range"
5 values in range
~~~~

or even:

~~~~ {src="src/python/single_range_test.py"}
import sys
num_valid = 0
for line in data:
    value = float(line)
    if 0 <= value <= 5:
        num_valid = num_valid + 1
print num_valid, "values in range"
5 values in range
~~~~

And if we want to count both at once, we can use `else`. The code it
controls is executed when the code in the `if` *isn't*:

~~~~ {src="src/python/simple_else.py"}
import sys
num_outliers = 0
num_valid = 0
for line in sys.stdin:
    value = float(line)
    if 0 <= value <= 5:
        num_valid = num_valid + 1
    else:
        num_outliers = num_outliers + 1
print num_valid, "in range and", num_outliers, "outliers"
5 in range and 2 outliers
~~~~

### In-Place Operators

We have seen expressions like:

    num_valid = num_valid + 1

several times now. In Python and many other languages, we can simplify
this by writing:

    num_valid += 1

which means, "Update the value on the left using addition with the value
on the right." Similarly, we can also double values using `*=` like
this:

    something *= 2

and so on for other binary (two-valued) operators. It may seem like a
small saving, but it actually prevents a lot of bugs by eliminating
duplicated code.

### Summary

-   Use `if test` to do something only when a condition is true.
-   Use `else` to do something when a preceding `if` test is not true.
-   The body of an `if` or `else` must be indented consistently.
-   Combine tests using `and` and `or`.
-   Use '\<', '\<=', '\>=', and '\>' to compare numbers or strings.
-   Use '==' to test for equality and '!=' to test for inequality.
-   Use `variable += expression` as a shorthand for
    `variable = variable + expression` (and similarly for other
    arithmetic operations).

### Challenges

1.  What is the value of `x` after executing the code shown below?

        x = 1
        x += x + 1

    1.  Undefined (an error occurs).
    2.  1
    3.  2
    4.  3

2.  What change must be made to the following code so that it produces
    the output shown?

        major = 5 > 0
        minor = 0.5 <= 0
        if major and minor:
            print 'both'
        elif major or minor:
            print 'one'
        else:
            print 'neither'
        one

    1.  The `if` test must be `if (major == True) and (minor == True)`,
        and the `elif` test must be
        `if (major == True) or (minor == True)`.
    2.  The `if` test must be `if major or minor`, and the `elif` test
        must be `if major`.
    3.  The `if` test must be `if major`, and the `elif` test must be
        `if minor`.
    4.  No change is required.

3.  A program initially executes these two lines:

        color = 'green'
        shape = 'triangle'

    Match each snippet of code to the final values of `color` and
    `shape`.

    A

    B

    C

        if color == 'green':
            shape = 'square'
        elif shape == 'square':
            color = 'red'

        if color == 'green':
            shape = 'square'
        if shape == 'square':
            color = 'red'

        if color == 'green' or shape == 'square':
            shape = 'circle'
        if shape == 'square':
            color = 'red'

        if color == 'green':
            if shape != 'triangle':
                shape = 'circle'
        else:
            shape = 'square'

      --------- ---------- ---------- ---------- ------------
                1          2          3
      `color`   `red`      `green`    `green`    `green`
      `shape`   `square`   `circle`   `square`   `triangle`
      --------- ---------- ---------- ---------- ------------

4.  What does the following code print?

        for char in 'CGT' * 0:
            print char
        else:
            print 'not found'

    A

    B

    C

    D

        C
        G
        T

        0

        not found

    An "invalid syntax" error message.

5.  Fill in the blanks so that the program below prints out the sum of
    the values in the list *after* the last negative number.

        data = [5, -2, 3, 1, -6, 2, 4]
        total = 0
        for value in data:
            if ________ < 0:
                ________ = 0
            else:
                ________ += ________
        print total

    A

    B

    C

    D

        total
        total
        value
        value

        value
        total
        value
        total

        total
        value
        total
        value

        value
        total
        total
        value

Flags
-----

### Learning Objectives:

-   Explain what Boolean values are.
-   Write statements that create and store Boolean values, and use them
    correctly in conditional statements.
-   Write examples showing how to keep track of events using flag
    variables.

An expression like `value < 0` produces one of two values called
(unsurprisingly) `True` and `False`. These values can be assigned to
variables like anything else:

    x = 5
    is_less_than = x < 0
    print is_less_than
    False

It's very common to assign `True` and `False` to variables to keep track
of whether some event has happened. For example, we could create a
variable called `have_seen_dashed_line` to keep track of whether or not
we have seen the dashed line that separates the header in a data file
from the actual data. Its initial value will be `False`, because we
obviously haven't seen the dashed line before we've read any input. As
soon as we do see the dashed line, we set it to `True`:

    import sys
    have_seen_dashed_line = False
    for line in data:
        if line.startswith('---'):
            have_seen_dashed_line = True
    print 'Did we ever see the dashed line?', have_seen_dashed_line
    True

A variable that is used this way is often called a
[flag](glossary.html#flag). We can use the `have_seen_dashed_line`
flag's value to decide whether or not to count a line as data:

    import sys
    have_seen_dashed_line = False
    number = 0
    for line in data:
        if line.startswith('---'):
            have_seen_dashed_line = True
        if have_seen_dashed_line:
            number = number + 1
    print 'Number of data lines:', number
    Number of data lines: 8

![Flagging and Incrementing](img/python/set_and_increment.png)

Whoops—that's almost right, but not quite. There are only 7 data lines
in our file: why are we reporting 8? The reason is that when we see the
dashed line, we set `have_seen_dashed_line` to `True`, then immediately
check its value, see that it's true, and increment `number` ([Figure
XXX](#f:set_and_increment)). What we want to do is *either* set the flag
(so that we'll start incrementing on the next iteration), *or* add one
to `number`. Here's the fixed program:

    import sys
    have_seen_dashed_line = False
    number = 0
    for line in data:
        if line.startswith('---'):
            have_seen_dashed_line = True
        else:
            if have_seen_dashed_line:
                number = number + 1
    print 'Number of data lines:', number
    Number of data lines: 7

And here's a version that combines the second `if` with the `else`:

    import sys
    have_seen_dashed_line = False
    number = 0
    for line in data:
        if line.startswith('---'):
            have_seen_dashed_line = True
        elif have_seen_dashed_line:
            number = number + 1
    print 'Number of data lines:', number
    Number of data lines: 7

Organizing the [branches](glossary.html#branch) of the `if` this way
makes it clearer that exactly one will be executed.

### Summary

-   The two Boolean values `True` and `False` can be assigned to
    variables like any other values.
-   Programs often use Boolean values as flags to indicate whether
    something has happened yet or not.

### Challenges

1.  What does the following program print?

        pressure = 55.3
        regions = [0 <= pressure < 50, 50 <= pressure < 80]
        print regions

    1.  `[0, 50]`
    2.  `[0, 1]`
    3.  `[False, True]`
    4.  A syntax error message.

2.  What does the following program print?

        data = [10, 50, 30, 20, 40]
        capped = False
        total = 0
        for value in data:
            if capped:
                total = value
            elif value > total:
                capped = True
            else:
                total += value
        print total

    1.  `1500`
    2.  `40`
    3.  `60`
    4.  `True`

3.  The `break` statement tells Python to exit a loop immediately. For
    example:

        for value in [1, 2, 3, 4, 5]:
            print value
            if value == 3:
                break

    prints:

        1
        2
        3

    Which of the following programs prints the same thing *without*
    using `break`?

    A

    B

    C

    D

        for value in [1, 2, 3, 4, 5]:
            if value <= 3:
                print value

        seen = False
        for value in [1, 2, 3, 4, 5]:
            print value
            if value > 2:
                seen = True

        printing = True
        for value in [1, 2, 3, 4, 5]:
            if printing:
                print value
            printing = value < 2

    All of the above.

4.  What does the program below print?

        deviated = True
        for value in [1, 2, 3, 4, 5]:
            if deviated:
                print value
                if value > 2 and deviated:
                    deviated = False

    A

    B

    C

    D

        1
        2

        1
        2
        3

        1
        2
        3
        4
        5

    None of the above.

Reading Data Files
------------------

### Learning Objectives:

-   Read a simple columnar data file and operate on its values.

It's finally time to clean up Aurora's actual cochlear implant data
files. Once again, these files typically look like this:

~~~~ {src="src/python/cochlear01.txt"}
Subject: 1782
Date:    2012-05-21
Test     Run  Score
----     ---  -----
range    1    3
range    2    5
discrim  1    1
discrim  2    1
discrim  4    1.5
volume   1    3.5
volume   2    4.0
~~~~

We already have a program that ignores everything up to and including
the dashed lines:

    import sys
    have_seen_dashed_line = False
    number = 0
    for line in data:
        if line.startswith('---'):
            have_seen_dashed_line = True
        elif have_seen_dashed_line:
            number = number + 1
    print 'Number of data lines:', number

Let's modify it to report scores that are outside the range 0–5. First,
we need a way to break each line into columns. Luckily for us, strings
know how to split themselves into fields:

    >>> typical_line = 'volume   2    4.0'
    >>> name, number, score = typical_line.split()
    >>> name
    'volume'
    >>> number
    '2'
    >>> score
    '4.0'

The `string.split` returns as many new strings as there are
whitespace-separated fields in the original string. In our case, there
are three fields, so we can assign them result of `split` to three
separate variables simultaneously. The third field, which we have put in
the variable `score`, is a string; if we want its value as a
floating-point number, we'll have to convert it using the `float`
function. Combining this code with the program we already had, we get:

    import sys
    have_seen_dashed_line = False
    for line in data:
        if line.startswith('---'):
            have_seen_dashed_line = True
        elif have_seen_dashed_line:
            name, number, score = line.split()
            score = float(score)

A simple `if` statement is the last piece of the puzzle:

    import sys
    have_seen_dashed_line = False
    for line in data:
        if line.startswith('---'):
            have_seen_dashed_line = True
        elif have_seen_dashed_line:
            name, number, score = line.split()
            score = float(score)
            if (score < 0.0) or (score > 5.0):
                print 'Out of range:', name, number, score

If we run this on our sample data file, it produces no output, because
all the scores in the file are valid:

    $ python check.py < cochlear01.txt
    $

But if we make some of the scores invalid, like this:

~~~~ {src="src/python/cochlear01.txt"}
Subject: 1782
Date:    2012-05-21
Test     Run  Score
----     ---  -----
range    1    3
range    2    7.5
discrim  1    1
discrim  2    1
discrim  4    1.5
volume   1    -3
volume   2    4.0
~~~~

then the output changes to:

    Out of range: range 2 7.5
    Out of range: volume 1 -3.0

which is what we wanted.

### Summary

-   Use `str.split()` to split a string into pieces on whitespace.
-   Values can be assigned to any number of variables at once.

### Challenges

1.  What does this program do?

        for line in open('columns.txt', 'r'):
            first, second = line.strip().split()
            print int(first) + int(second)

    1.  Nothing: the first line contains a syntax error.
    2.  Adds pairs of numbers from a file containing two columns of
        data.
    3.  Totals the values in the first column of data and (separately)
        the values in the second column.
    4.  Nothing: the program fails because it doesn't close the file it
        opens.

2.  What does this program do?

        source = open('masses.txt', 'r')
        total = 0.0
        for line in source:
            if line.startswith('#'):
                print total
                total = 0.0
            else:
                total += float(line)
        source.close()

    1.  Add up groups of numbers (one per line) separated by lines
        starting with '\#', printing the totals.
    2.  As in \#1, except the program does not print the first
        sub-total.
    3.  As in \#1, except the program does not print the last sub-total.
    4.  As in \#1, except the program does not include the first number
        in each group in its sub-total.

3.  What does this program do?

        reader = open('patients.txt', 'r')
        largest = 0
        for line in reader:
            if '#' in line:
                line, rest = line.split('#')
            largest = max(largest, len(line.strip()))
        reader.close()
        print largest

    1.  Print the length of the longest line in the file.
    2.  As in \#1, except it ignores everything after the first '\#' in
        each line.
    3.  As in \#2, except it does not include trailing whitespace in the
        length of the line.
    4.  As in \#2, except it does not include leading or trailing
        whitespace in the length of the line.

4.  What does this program do?

        reader = open('patients.txt', 'r')
        writer = open('filtered.txt', 'w')
        for line in reader:
            line = line.strip()
            if len(line) > 0:
                writer.write(line)
        reader.close()
        writer.close()

    1.  Copy the first non-blank line from `patients.txt` to
        `filtered.txt`.
    2.  Copy the longest non-blank line from `patients.txt` to
        `filtered.txt`.
    3.  Copy all lines from `patients.txt` to `filtered.txt`.
    4.  Copy all non-blank lines from `patients.txt` to `filtered.txt`.

Provenance Revisited
--------------------

### Learning Objectives:

-   Demonstrate how to embed provenance information in a program.
-   Write programs that carry simple provenance information forward.
-   Explain how automatically tracking provenance helps computational
    research.

As we said near the end of [the previous chapter](svn.html#provenance),
if we put a string like:

    $Revision: ...$

in a file, Subversion can automatically update it each time we commit a
change to that file. Let's add put `$Revision:$` in our program:

    import sys
    my_version = '$Revision: 143$'
    'Processed by check.py:', my_version
    have_seen_dashed_line = False
    for line in data:
        if line.startswith('---'):
            have_seen_dashed_line = True
        elif have_seen_dashed_line:
            name, number, score = line.split()
            score = float(score)
            if (score < 0.0) or (score > 5.0):
                print 'Out of range:', name, number, score
    Processed by check.py: $Revision: 143$
    Out of range: range 2 7.5
    Out of range: volume 1 -3.0

This is kind of handy: our output now automatically includes a
description of who produced it—*exactly* who, i.e., not just the name of
the program, but also which version. To see why this is useful, let's
rewrite the program so that it clips scores to lie inside 0–5 instead of
just reporting outlying values:

    import sys
    my_version = '$Revision: 143$'
    'Processed by clip.py:', my_version
    have_seen_dashed_line = False
    for line in data:

        if have_seen_dashed_line:
            name, number, score = line.split()
            score = float(score)
            if score < 0.0:
                print 0.0
            elif score > 5.0:
                print 5.0
            else:
                print score

        else:
            print line.rstrip()
            if line.startswith('---'):
                have_seen_dashed_line = True

### Ordering

Note that this version checked the `have_seen_dashed_line` flag first,
then handles the case where the flag isn't yet true. Some people find
this ordering easier to understand, because the "main" case that handles
actual data comes first. Others prefer the original, arguing that the
cases should appear in the order in which we expect the data to occur.
It doesn't matter which we use, as long as we're consistent with our
other loops.

When we run this program on the data that has invalid scores, it prints:

    Processed by clip.py: $Revision: 143$
    Subject: 1782
    Date:    2012-05-21
    Test     Run  Score
    ----     ---  -----
    range    1    3
    range    2    5.0
    discrim  1    1
    discrim  2    1
    discrim  4    1.5
    volume   1    0.0
    volume   2    4.0

The three most important lines are highlighted. Two of them—the data
lines—have been cleaned up; the line at the very top tells us who did
the cleaning up. This is another step in our march toward having a real
data provenance system: now, if we discover a bug in a program, we can
look at our files and see which ones had been processed by that program.
As we'll see in the [next chapter](funclib.html), we can extend this
further to carry provenance information forward through an entire
pipeline.

### Summary

-   Put version numbers in programs' output to establish provenance for
    data.

### Challenges

1.  Fill in the blanks so that this program prints a line like:

        # Version: 123

    in its output instead of just copying the raw provenance forward.

        my_version = '$Revision: 123$'
        cleaned = my_version.________('$')
        front, back = cleaned.split(________)
        print '# Version:', ________.strip()

      ---- --------- --------- -------- ---------
           A         B         C        D
      1.   `split`   `strip`   `find`   `strip`
      2.   `' '`     `':'`     `'$'`    `'$'`
      3.   `front`   `back`    `back`   `back`
      ---- --------- --------- -------- ---------

2.  Suppose our data files are also under version control, and also
    include revision numbers:

        Version: $Revision: 227$
        Subject: 1782
        Date:    2012-05-21
        Test     Run  Score
        ----     ---  -----
        range    1    3
        range    2    5
        discrim  1    1
        discrim  2    1
        discrim  4    1.5
        volume   1    3.5
        volume   2    4.0

    Which block of code must we add to:

        source = open('data.txt', 'r')
        largest = None
        for line in source:
            if ':' in line:
                ________
            else:
                name, number, score = line.strip().split()
                if largest is None:
                    largest = score
                else:
                    largest = max(largest, score)
        source.close()
        print 'Version:', version_number
        print 'Largest:', largest

    to copy the data file's version into the output?

    A

    B

    C

    D

        name, keyword, version_number = line.strip('$').split(':')
        version_number = version_number.strip()

        name, keyword, version_number = line.strip('$').split(':').strip()

        name, keyword, version_number = line.strip('$').split(':')
        version_number = version_number.strip()

    None of the above.

Lists
-----

### Learning Objectives:

-   Explain why it is useful to store many values together.
-   Write programs that create and manipulate lists of numbers and
    strings.
-   Write programs that use loops to operate independently on each value
    in a list.
-   Explain why programs should be tested on short, simple inputs first.

To start our exploration of lists, let's run an interpreter and try
this:

~~~~ {src="src/python/sum_values.py"}
>>> data = [1, 3, 5]
>>> for value in data:
...     print value
...
1
3
5
~~~~

`[1, 3, 5]` is a [list](glossary.html#list): a single object that stores
multiple values ([Figure XXX](#f:simple_list)). Just as a `for` loop
over an open file reads lines from that file one by one and assigns them
to the loop variable, a `for` loop over a list assigns each value in the
list to the loop variable in turn.

![A Simple List](img/python/simple_list.png)

Let's do something a bit more useful:

~~~~ {src="src/python/first_mean.py"}
data = [1, 4, 2, 3, 3, 4, 3, 4, 1]
total = 0
for n in data:
    total += n
mean = total / len(data)
print "mean is", mean
mean is 2
~~~~

This loop adds each value in the list to `total`. Once the loop is over,
we divide `total` by the length of the list, which we find using the
built-in function `len`.

Unfortunately, the result in the example above is wrong: The total of
the numbers in the list is 25, but we're printing 2 instead of 25/9
(which is 2.7777…). The problem once again is that we're dividing one
integer by another, which throws away the remainder. We can fix this by
initializing `total` to 0.0 (so that all the additions involve a
floating-point number and an integer, which produces a floating-point
number), or by using the `float` function to do the conversion
explicitly:

~~~~ {src="src/python/second_mean.py"}
data = [1, 4, 2, 3, 3, 4, 3, 4, 1]
total = 0
for n in data:
    total += n
mean = float(total) / len(data)
print "mean is", mean
mean is 2.77777777778
~~~~

The *real* problem isn't a matter of integers versus floats, though. The
real problem with this program is that we didn't know whether the answer
was right or wrong, so we couldn't tell if the program was correct or
not. After all, the average of these nine numbers might well have been
2.

The fact that a program runs without crashing doesn't mean it's correct.
One way to make programs easier to check is to run them on smaller or
more regular data. For example, If we ran the program on `[1, 4]`, we'd
probably notice that we were getting 2 instead of 2.5. Writing programs
so that they're checkable is another idea that we'll explore in detail
[later](quality.html).

### Even Simpler

Python actually has a built-in function called `sum`, so we can get rid
of the loop entirely:

~~~~ {src="src/python/loopless.py"}
total = sum(data)
print "mean is", float(total) / len(data)
~~~~

and shorten this even further by calling `float` directly on the result
of `sum`:

~~~~ {src="src/python/one_liner.py"}
print "mean is", float(sum(data)) / len(data)
~~~~

`float(sum(data))` is like *sin(log(x))*: the inner function is
evaluated first, and its result is used as the input to the outer
function. It's important to get the parentheses in the right place,
since the expressions:

~~~~ {src="src/python/one_liner.py"}
float(sum(data)) / len(data)
~~~~

and

~~~~ {src="src/python/incorrect_one_liner.py"}
float(sum(data) / len(data))
~~~~

calculate different things. In the first, `float` is applied to
`sum(data)`, i.e., Python adds up all the numbers, then converts the
result to a floating-point value before dividing by `len(data)` to get
the mean.

In the second, Python adds up the numbers, divides by `len(data)` to get
an integer result, and then converts that integer to a floating point
number. This is just our original bug in a more compact form. Once
again, the only way to guard against it is to test the program.

### Summary

-   Use `[value, value, ...]` to create a list of values.
-   `for` loops process the elements of a list, in order.
-   `len(list)` returns the length of a list.
-   `[]` is an empty list with no values.

### Challenges

1.  What does the following program print?

        total = 0
        for v in []:
            total += v
        print total

    1.  Nothing
    2.  0
    3.  The program doesn't run because of a syntax error.
    4.  None of the above.

2.  The expression `list('abc')` produces the list `['a', 'b', 'c']`.
    What does the expression `str(['a', 'b', 'c'])` produce?
    1.  `'abc'`
    2.  `['abc']`
    3.  `['a', 'b', 'c']`
    4.  An error message.

3.  What is the value of the expression `len(['abc', 'def'])`?
    1.  6
    2.  `[3, 3]`
    3.  2
    4.  3

4.  What does this program print?

        for i in 4:
            print i

    A

    B

    C

    D

        0
        1
        2
        3

        1
        2
        3
        4

    Nothing

    A syntax error message

More About Lists
----------------

### Learning Objectives:

-   Explain the difference between mutable and immutable values.
-   Index a list to retrieve values at specific locations.
-   Show how to alter the values in a list.
-   Trace changes to a list's values as a result of assignment.
-   Explain what an "out-of-bounds error" is, and give an example
    showing when one would occur.
-   Show how to generate all the valid indices for a list's elements.
-   Explain when it is appropriate to use short or long variable names,
    and why.

Lists (and their equivalents in other languages) are used more than any
other data structure, so let's have a closer look at them. First, lists
are [mutable](glossary.html#mutable), i.e., they can be changed after
they are created:

~~~~ {src="src/python/appending.py"}
data = [1, 4, 2, 3]
result = []
current = 0
for n in data:
    current = current + n
    result.append(current)
print "running total:", result
[1, 5, 7, 10]
~~~~

`result` starts off as an [empty list](glossary.html#empty-list), and
`current` starts off as zero ([Figure XXX](#f:running_total)). Each time
the loop executes—i.e., for each number in `values`—Python adds the next
value in the list to `current` to calculate the running total. It then
append this value to `result`, so that when the program finishes, we
have a complete list of partial sums.

![Running Total](img/python/running_total.png)

What if we want to double the values in `data` in place? We could try
this:

~~~~ {src="src/python/incorrect_doubling_in_place.py"}
data = [1, 4, 2, 3]
for n in data:
    n = 2 * n
print "doubled data is:", data
doubled data is [1, 4, 2, 3]
~~~~

but as we can see, it doesn't work. When Python calculates `2*n`, it
creates a new value in memory ([Figure XXX](#f:doubling_list)). It then
makes the variable `n` point at the value for a few microseconds before
going around the loop again and pointing `n` at the next value from the
list instead. Since nothing is pointing to the temporary value we just
created any longer, Python throws it away.

![Failed Attempt to Double Values in a
List](img/python/doubling_list.png)

The solution to our problem is to [index](glossary.html#list-indexing)
the list, which is just like subscripting a vector in mathematics. Here
are some examples:

~~~~ {src="src/python/modify_list.py"}
scientists = ["Newton", "Darwing", "Turing"]
print "length:", len(scientists)
length: 3
print "first element:", scientists[0]
first element: Newton
print "second element:", scientists[1]
second element: Darwing
print "third element:", scientists[2]
third element: Turing
~~~~

### It Seemed Like a Good Idea at the Time

For reasons that made sense in 1970, when the C programming language was
invented, Python lists are indexed from 0 to N-1 rather than 1 to N.
C++, C\#, Java, and other languages that imitate C also use 0 to N-1,
while Fortran, Pascal, MATLAB, and other languages that imitate human
beings use 1 to N.

How does indexing help us? Well, after noticing that we have misspelled
Darwin's name as "Darwing", we can fix it by assigning a new value to
that location in the list:

~~~~ {src="src/python/modify_list_continued.py"}
scientists[1] = "Darwin"
print scientists
["Newton", "Darwin", "Turing"]
~~~~

[Figure XXX](#f:update_list) shows the list before and after the change.
Again, once we've made the update, nothing is pointing to the string
"Darwing" with a "g" on the end, so the memory it's using is recycled.

![Successfully Doubling Values in a List](img/python/update_list.png)

In order for Python to give us a sensible value, the index we provide
for a list must be in range, i.e., between 0 and one less than the
length of the list. If it's too large, we get an error message:

~~~~ {src="src/python/list_out_of_range.py"}
scientists = ["Newton", "Darwin", "Turing"]
print scientists[55]
Traceback (most recent call last):
  File "list-04.py", line 2, in <module>
    print "out of range:", scientists[55]
IndexError: list index out of range
~~~~

The error message doesn't appear until Python actually tries to fetch
the out-of-bounds value. If this is in the middle of some other
operation, we may see some partial output before our error message:

~~~~ {src="src/python/list_out_of_range_partial.py"}
scientists = ["Newton", "Darwin", "Turing"]
print "out of range:", scientists[55]
out of range:
Traceback (most recent call last):
  File "list-04.py", line 2, in <module>
    print "out of range:", scientists[55]
IndexError: list index out of range
~~~~

And here's something else that's useful. In Python (but *not* in most
other languages), negative indices count backward from the end of a
list:

~~~~ {src="src/python/list_negative_indexing.py"}
scientists = ["Newton", "Darwin", "Turing"]
print "last:", scientists[-1]
print "penultimate:", scientists[-2]
last: Turing
penultimate: Darwin
~~~~

It's a lot easier to type `scientists[-1]` than
`scientists[len(scientists)-1]` to get the last item in a list, but it
does take some getting used to.

Now, back to our original problem of doubling values in place. We now
know that we can do this:

~~~~ {src="src/python/explicit_doubling.py"}
data = [1, 4, 2]
data[0] = 2 * data[0]
data[1] = 2 * data[1]
data[2] = 2 * data[2]
print "doubled data is:", data
doubled data is [2, 8, 4]
~~~~

but it clearly doesn't scale: we're not going to write a million
statements to update a list of a million values. We need to use a loop,
but instead of looping over the values in the list, we want to loop over
the allowed indices of the list. To do this, we will rely on a function
called `range` which creates a list of the first N integers:

~~~~ {src="src/python/range_5.py"}
print range(5)
[0, 1, 2, 3, 4]
~~~~

Once again, the values go from 0 to one less than the number given to
`range`, which just happens to be exactly the indices of a list of that
length. Let's try it out:

~~~~ {src="src/python/range_loop.py"}
data = [1, 4, 2]
indices = range(3)
for i in indices:
    print i, data[i]
0 1
1 4
2 2
~~~~

then fold the call to `range` into the loop:

~~~~ {src="src/python/range_loop_2.py"}
data = [1, 4, 2]
for i in range(3):
    print i, data[i]
0 1
1 4
2 2
~~~~

This program is correct, but fragile: if we add more values to the list,
Python will still only execute the loop three times, so we'll still only
print the first three values in the list:

~~~~ {src="src/python/incorrect_range_loop.py"}
data = [1, 4, 2, 5, 1, 3]
for i in range(3):
    print i, data[i]
0 1
1 4
2 2
~~~~

What we want is for the loop to automatically adjust itself based on the
length of the list:

~~~~ {src="src/python/data_length_loop.py"}
data = [1, 4, 2, 5, 1, 3]
data_length = len(data)
for i in range(data_length):
    print i, data[i]
0 1
1 4
2 2
3 5
4 1
5 3
~~~~

We can get rid of the variable `data_length` by putting the call to
`len(data)` inside the call to `range`:

~~~~ {src="src/python/idiomatic_range_loop.py"}
data = [1, 4, 2, 5, 1, 3]
for i in range(len(data)):
    print i, data[i]
0 1
1 4
2 2
3 5
4 1
5 3
~~~~

Again, `range(len(data))` is like *sin(log(x))*: the inner function is
evaluated first, and its result becomes the input to the outer function.
Put together like this, they are a common [idiom](glossary.html#idiom)
in Python, i.e., a way of saying something that everyone recognizes and
uses. When an experienced programmer sees:

    for i in range(len(something)):

what she "hears" is:

    for each legal index of something:

The reason this idiom is better than what we started with is that there
is no duplicated information. Instead of having a list of length 3, and
looping from 0 up to 3, we have a list of any length whatever, and loop
from 0 up to that length. In general, anything that is repeated two or
more times in a program will eventually be wrong in at least one.
Putting it another way, any piece of information should appear exactly
once in a program, so that if it needs to change, it only needs to be
changed in one place.

### Short and Long Variable Names

We have said several times that programs should use meaningful variable
names. Are we not violating our own rule by using `i` as a variable in
this program? The short answer is "yes", but it's a defensible
violation. Suppose we re-write our loop as:

    data = [1, 4, 2, 5, 1, 3]
    for location in range(len(data)):
        print location, data[location]

The longer name are more meaningful, but it also takes longer to read.
Since the original `i` is only used for a few lines, users will easily
be able to keep its meaning in short-term memory as long as they need
to. On balance, therefore, the short name are better in this case.

This is actually a general principle in program design. A variable that
holds a simple value, and is only used in a few adjacent lines of code,
can (and usually should) have a short name. A variable that holds a
complex value, or one which is used over more than a few lines of code,
should have a longer name in order to optimize the tradeoff between
reading speed and the limitations of human short-term memory.

Let's finally go back and double the values in place:

~~~~ {src="src/python/doubling_in_place.py"}
data = [1, 4, 2, 5, 3, 4, 5]
for i in range(len(data)):
    data[i] = 2 * data[i]
print data
[2, 8, 4, 10, 6, 8, 10]
~~~~

### Left and Right

Seeing the expression *x = 2x*, most mathematicians would say, "Right—so
*x* is zero." Seeing the same expression, most programmers would say,
"Right—you're doubling the value of *x*." [Figure
XXX](#f:double_in_place) shows how that actually works:

1.  Python reads the current value of `x` from memory.
2.  It multiplies that value by 2, storing the result in a temporary
    location…
3.  …and then modifies `x` to point at the new value.

![Doubling in Place](img/python/double_in_place.png)

Now look at what happens when Python execute the statements:

    x = 5
    y = x
    x = 2 * x

1.  The variable `x` is created, and set to point at the value 5
    ([Figure XXX](#f:new_values_for_variables)).
2.  The variable `y` is created, and set to point at the same value.
3.  The value 10 (i.e., 2×5) is created and stored in a temporary
    location.
4.  `x` is altered to point at that value.

![New Values for Variables](img/python/new_values_for_variables.png)

After these operations are complete, `y` is left pointing at the
original value, 5. It does *not* point at the same thing `x` does any
longer, and its value is *not* automatically recalculated to keep it
twice the value of `x`.

### Summary

-   Lists are mutable: they can be changed in place.
-   Use `list.append(value)` to append something to the end of a list.
-   Use `list[index]` to access a list element by location.
-   The index of the first element of a list is 0; the index of the last
    element is `len(list)-1`.
-   Negative indices count backward from the end of the list, so
    `list[-1]` is the last element.
-   Trying to access an element with an out-of-bounds index is an error.
-   `range(number)` produces the list of numbers
    `[0, 1, ..., number-1]`.
-   `range(len(list))` produces the list of legal indices for `list`.

### Challenges

1.  What does this program print?

        sizes = [0, 1, 1, 2, 2]
        total = 0
        for s in sizes:
            total += sizes[s]
        print total

    1.  0
    2.  2
    3.  4
    4.  6

2.  What does this program print?

        pop = [20, 40, 30]
        loc = [1, 2, 1]
        print pop[loc[0]], pop[loc[2]]

    1.  Nothing: there is a syntax error.
    2.  Nothing: the program is syntactically correct, but fails when
        run.
    3.  `1 1`
    4.  `20 30`

3.  What does this program print?

        genders = list('FMFFMFM')
        print [genders[0] + genders[-1]]

    1.  `'FM'`
    2.  `['FM']`
    3.  `['F', 'M']`
    4.  `['M', 'F']`

4.  What does this program print?

        result = ''
        for i in range(5):
            result += str(i/2)
        print result

    1.  An error message.
    2.  01122
    3.  00112
    4.  range(5)

5.  What does this program print?

        values = list('abcd')
        for i in range(len(values)):
            values[i] = values[-i]
        print values

    1.  ['a', 'b', 'c', 'd']
    2.  ['d', 'c', 'b', 'a']
    3.  ['a', 'c', 'c', 'a']
    4.  ['a', 'd', 'c', 'd']

6.  What does this program print?

        values = list('abcd')
        for char in values:
            values.append(char)
        print values

    1.  ['a', 'b', 'c', 'd']
    2.  ['a', 'b', 'c', 'd', 'a']
    3.  ['a', 'b', 'c', 'd', 'a', 'b', 'c', 'd']
    4.  It never finishes running.

Nesting Loops
-------------

### Learning Objectives:

-   Trace the execution of a nested loop.
-   Give examples of the kinds of problems that nested loops should be
    used to solve.
-   Construct nested loops with independent ranges.
-   Construct nested loops in which the range of the inner loop depends
    on the state of the outer loop, and give an example showing when
    this is useful.

Going back to Aurora's data cleanup problem, suppose that the scores in
each data set are always supposed to ramp upward: if we ever see a value
that's less than the value before it, something's gong wrong. Here's a
program that tries to check that (again, using inline data instead of
reading from a file to make the sample code clearer):

~~~~ {src="src/python/incorrect_upward_check.py"}
data = [1, 2, 2, 3, 4, 4, 5, 6, 5, 6, 7, 7, 8]
for i in range(len(data)):
    if data[i] < data[i-1]:
        print "failure at index:", i
    i = i + 1
failure at index: 0
failure at index: 8
~~~~

Whoops—why is it telling us that there's a failure at index 0? Take a
close look at the third line: when `i` is 0, it compares `data[0]` to
`data[-1]`, but as we said earlier, index -1 means the last element of
the list. We need to make sure that we only compare the *second* and
higher elements to the ones before them:

~~~~ {src="src/python/correct_upward_check.py"}
data = [1, 2, 2, 3, 4, 4, 5, 6, 5, 6, 7, 7, 8]
for i in range(1, len(data)):
    if data[i] < data[i-1]:
        print "failure at index:", i
    i = i + 1
failure at index: 8
~~~~

This program uses the fact that `range(low, high)` generates the values
from `low` to `high-1`. We can also use `range(low, high, stride)` to
generate values that are spaced `stride` apart, so that
`range(5, 20, 3)` produces `[5, 8, 11, 14, 17]`. (Remember, `range` goes
up to but not including the top value.)

Now suppose that we need to add up successive triples of our data to
smooth out the scores. Our first try steps through the indices three at
a time:

~~~~ {src="src/python/a_step_too_far.py"}
data = [1, 2, 2, 3, 4, 4, 5, 6, 5, 6, 7, 7, 8]
result = []
for i in range(0, len(data), 3):
    sum = data[i] + data[i+1] + data[i+2]
    result.append(sum)
print "grouped data:", result
Traceback (most recent call last):
  File "group-by-threes-fails.py", line 6, in <module>
    sum = data[i] + data[i+1] + data[i+2]
IndexError: list index out of range
~~~~

It's not immediately obvious what's wrong, but a bit of experimenting
with shorter lists turns up the problem. If the number of elements in
the list isn't exactly divisible by 3, our program is going to try to
reach past the end of the list. For example, if we have a 4-element
list, we will add up the values at locations 0, 1, and 2, then try to
add up the values at locations 3, 4, and 5, but locations 4 and 5 aren't
valid ([Figure XXX](#f:a_step_too_far)).

![A Step Too Far](img/python/a_step_too_far.png)

How we should fix this is a question for a scientist (or at least a
statistician). Should we throw away the top few values if there aren't
enough to make another triple, or add up as many as there are and hope
for the best? Let's assume the latter for now:

~~~~ {src="src/python/awkward_smoothing.py"}
data = [1, 2, 2, 3, 4, 4, 5, 6, 5, 6, 7, 7, 8]
result = []
for i in range(0, len(data), 3):
    sum = data[i]
    if (i+1) < len(data):
        sum += data[i+1]
    if (i+2) < len(data):
        sum += data[i+2]
    result.append(sum)
print "grouped data:", result
grouped data: [5, 11, 16, 20, 8]
~~~~

This works, but it feels clumsy: if we were adding up in groups of ten,
we'd have a lot of `if` statements. We need a better way.

Our first step toward that better way looks like this:

~~~~ {src="src/python/simple_nested_loop.py"}
vowels = "ae"
consonants = "dnx"
for v in vowels:
    for c in consonants:
        print v + c
ad
an
ax
ed
en
ex
~~~~

[Figure XXX](#f:nested_flowchart) shows what's going on in this [nested
loop](glossary.html#nested-loop). Each time the [outer
loop](glossary.html#outer-loop) executes, Python runs the entire [inner
loop](glossary.html#inner-loop). The innermost `print` statement
therefore executes six times, because the outer loop runs twice, and the
inner loop runs three times for each of those iterations.

![Nested Loops](img/python/nested_flowchart.png)

In this case, both loops execute a fixed number of times, but that
doesn't have to be the case. It's common, for example, to set the number
of times an inner loop runs based on the current value of the outer
loop's counter:

~~~~ {src="src/python/triangle_nested_loop.py"}
for i in range(4):
    for j in range(i):
        print i, j
1 0
2 0
2 1
3 0
3 1
3 2
~~~~

![Nested Loop Execution](img/python/triangle_nested_loop.png)

[Figure XXX](#f:triangle_nested_loop) traces this little program's
execution. The first time through, `i` is 0. Since `range(0)` is the
empty list `[]`, the inner loop is effectively:

        for j in []:
            print i, j

so it doesn't execute at all. The next time, though, when `i` is 1, the
inner loop is effectively:

        for j in [0]:
            print i, j

so the innermost `print` statement is executed once with `i` equal to 1
and `j` equal to 0. The third time around the outer loop, `i` is 2, so
`range(i)` is `[0, 1]`. This makes the inner loop execute twice, and so
on.

Now let's go back to Aurora's data smoothing. We can step through the
data in threes like this:

    for i in range(0, len(data), 3):
        ...body of loop...

If we know that the length of a list is an exact multiple of three, we
can always loop from index `i` up to (but not including) `i+3`:

    for i in range(0, len(data), 3):
        for j in range(i, i+3):
            ...body of loop...

If the list isn't long enough for us to do this, we want to go as high
as the least of `i+3` and `len(data)`. Using Python's built-in `min`
function, this is:

    min(i+3, len(data))

so we can write our inner loop as:

    for i in range(0, len(data), 3):
        upper_bound = min(i+3, len(data))
        for j in range(i, upper_bound):
            ...smooth data...

Here's the completed data smoothing program:

~~~~ {src="src/python/data_smoothing.py"}
data = [1, 2, 2, 3, 4, 4, 5, 6, 5, 6, 7, 7, 8]
result = []
for i in range(0, len(data), 3):
    upper_bound = min(i+3, len(data))
    sum = 0
    for j in range(i, upper_bound):
        sum += data[j]
    result.append(sum)
print "grouped data:", result
grouped data: [5, 11, 16, 20, 8]
~~~~

This program works, but there's room for improvement. If we ever want to
change the smoothing interval, we have to replace the number 3 in two
places. If we put that value in a variable `width`, we'll only need to
change it once:

~~~~ {src="src/python/data_smoothing_generalized.py"}
data = [1, 2, 2, 3, 4, 4, 5, 6, 5, 6, 7, 7, 8]
width = 3
result = []
for i in range(0, len(data), width):
    upper_bound = min(i+width, len(data))
    sum = 0
    for j in range(i, upper_bound):
        sum += data[j]
    result.append(sum)
print "grouped data:", result
grouped data: [5, 11, 16, 20, 8]
~~~~

This change also tells readers (including our future selves) that the
stride in the outer loop, and the offset used to calculate
`upper_bound`, are always supposed to be the same. That's yet another
reason to use variables with meaningful names: it tells people when
values are intentionally the same, as opposed to accidentally the same.

### Summary

-   `range(start, end)` creates the list of numbers from `start` up to,
    but not including, `end`.
-   `range(start, end, stride)` creates the list of numbers from `start`
    up to `end` in steps of `stride`.
-   Use nested loops to do things for combinations of things.
-   Make the range of the inner loop depend on the state of the outer
    loop to automatically adjust how much data is processed.
-   Use `min(...)` and `max(...)` to find the minimum and maximum of any
    number of values.

### Challenges

1.  What does this program print?

        total = 0
        for i in range(2):
            for j in range(-i):
                total += j
        print total

    1.  -2
    2.  -1
    3.  0
    4.  1

2.  How many different numbers can be put in the blank below so that the
    value of the expression is 12?

        sum(range(1, ____, 3))

    1.  Only 1
    2.  2 different values
    3.  3 different values
    4.  The expression's value can never be 12

3.  How many different numbers can be put in the blank below so that the
    value of the expression is 12?

        sum(range(1, 3, ____))

    1.  Only 1
    2.  2 different values
    3.  3 different values
    4.  The expression's value can never be 12

4.  Fill in the blanks in:

    > `final_mass` starts at 0, which is less than any of the values in
    > \_\_\_\_\_\_\_\_, so `________(final_mass, inner)` is always 0, so
    > `max(outer, min(...))` is always just \_\_\_\_\_\_\_\_, so the
    > final value is just the last value of `outer_masses`.

    so that it is an accurate description of the behavior of this
    program:

        outer_masses = [10, 20, 30]
        inner_masses = [1, 2, 3]
        final = 0
        for outer in outer_masses:
            for inner in inner_masses:
                final = max(outer, min(final, inner))
        print final

      --- ---------------- ------- --------------------
      A   `inner_masses`   `min`   `outer`
      B   `outer_masses`   `min`   `0`
      C   `inner_masses`   `max`   `inner_masses[-1]`
      --- ---------------- ------- --------------------

Nesting Lists
-------------

### Learning Objectives:

-   Explain what is meant by "nested lists", and what their relationship
    is to nested loops.
-   Draw data structure diagrams corresponding to nested lists, and
    write nested lists that correspond to given diagrams.
-   Explain what happens when an expression like "`table[3][2]`" is
    evaluated.

One of the hearing tests Aurora uses asks people to point out where a
sound is coming from. The data files contain lists of XY coordinates:

    4.2 1.7
    3.1 5.0
    0.8 6.1
    ... ...

She has roughly 100 such files, and one more file (in the same format)
that holds the actual location of each sound. She wants to calculate the
average distance between each actual and reported location.

The first step is to read a file and extract the XY values on each line:

~~~~ {src="src/python/read_separate_xy.py"}
x_values = []
y_values = []
reader = file('data.txt', 'r')
for line in reader:
    x, y = line.split()
    x = float(x)
    x_values.append(x)
    y = float(y)
    y_values.append(y)
reader.close()
~~~~

We can make this a bit more readable by combining the calls to `float`
and `append`:

~~~~ {src="src/python/read_separate_xy_combined.py"}
x_values = []
y_values = []
reader = file('data.txt', 'r')
for line in reader:
    x, y = line.split()
    x_values.append(float(x))
    y_values.append(float(y))
reader.close()
~~~~

but the basic approach is still unwieldy. What we really want is a list
of XY coordinates, not two parallel lists of X and Y coordinates. We can
easily create what we want using [nested
list](glossary.html#nested-list). [Figure XXX](#f:simple_nested_list)
shows what we're going to do, and the code below shows how we would
create a nested list by hand for specific XY values:

~~~~ {src="src/python/nested_list_explicit.py"}
>>> coordinates = [ [4.2, 1.7], [3.1, 5.0], [0.8, 6.1] ]
>>> print coordinates[0]
[4.2, 1.7]
>>> print coordinates[0][1]
1.7
~~~~

![A Simple Nested List](img/python/simple_nested_list.py)

This isn't as complicated as it first looks. Just as a variable can
point at any object, so too can any entry in a list. And since a list is
just an object in memory, one list can contain a reference to another.
This is why `coordinates[0]` is `[4.2, 1.7]`: the first entry of the
outer list is a reference to an entire sublist. We could just as easily
write:

    >>> temp = coordinates[0]
    >>> print temp
    [4.2, 1.7]

And since `x[1]` is 4.2, so too is `coordinates[0][1]`: the first
subscript select the sublist, while the second selects an element from
that sublist ([Figure XXX](#f:indexing_nested_lists)).

![Indexing Nested Lists](img/python/indexing_nested_lists.png)

It's important to understand that the inner list isn't "in" the outer
list: what the outer list contains is a reference to the inner one.
We'll return to this [later](#s:alias).

With nested lists in hand, it's straightforward to create a list of
coordinate pairs:

~~~~ {src="src/python/nested_vector.py"}
values = []
reader = file('data.txt', 'r')
for line in reader:
    x, y = line.split()
    coord = [float(x), float(y)]
    values.append(coord)
reader.close()
~~~~

Each time the loop executes, this program splits the line into two
strings, creates a new two-element list containing the corresponding
numbers, and then appends that list to `values`.

Now suppose that we have two such lists, and we want to find the average
distance between corresponding coordinates.

~~~~ {src="src/python/vector_diff.py"}
expected = [ [4.0, 2.0], [3.0, 5.0], [1.0, 6.0] ]
actual   = [ [4.2, 1.7], [3.1, 5.0], [0.8, 6.1] ]
x_diff, y_diff = 0.0,  0.0
for i in range(len(actual)):
    e = expected[i]
    a = actual[i]
    x_diff += abs(e[0] - a[0])
    y_diff += abs(e[1] - a[1])
print "average errors:", x_diff / len(actual), y_diff / len(actual)
average errors: 0.166666666667 0.133333333333
~~~~

The first two lines set up our data: in a real program, we'd read values
from files. The next line initializes `x_diff` and `y_diff`, which will
hold the errors in X and Y respectively. Each iteration of the loop sets
`a` and `e` to point at corresponding elements of the vectors. `a[0]` is
then the X coordinate of an actual point, while `e[0]` is the X
coordinate of the corresponding expected point, so `abs(e[0] - a[0])` is
the difference, which we add to `x_diff` using `+=`.

### Summary

-   Use nested lists to store multi-dimensional data or values that have
    regular internal structure (such as XYZ coordinates).
-   Use `list_of_lists[first]` to access an entire sub-list.
-   Use `list_of_lists[first][second]` to access a particular element of
    a sub-list.
-   Use nested loops to process nested lists.

### Challenges

1.  A colleague has defined a 3×3 matrix like this:

        tensor = [ [0, 1, 2],
                   [3, 4, 5],
                   [6, 7, 8] ]

    They then try to transpose it like this:

        transpose = []
        for i in [-1, -2, -3]:
            transpose.append(tensor[i])

    What is the actual result?

    1.  `transpose` contains the transpose of `tensor` as desired.
    2.  `transpose` contains the rows of `tensor` in reverse order.
    3.  `transpose` contains the columns of `tensor` in reverse order.
    4.  An error occurs.

2.  What is the output of this program?

        final = []
        for i in range(3):
            final.append(range(i))
        print final

    1.  `[0, 1, 2]`
    2.  `[[0], [1, [2]]`
    3.  `[[], [0], [0, 1]]`
    4.  `[[0, 1, 2]]`

3.  What does this program do?

        alpha = [ [1, 2], [3, 4] ]
        beta = [ [10, 20], [30, 40] ]
        result = [ [0, 0], [0, 0] ]
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    result[i][j] += alpha[i][k] * beta[k][j]

    1.  Calculate the sums of the rows and columns of `alpha` and
        `beta`.
    2.  Calculate the products of the elements the rows and columns of
        `alpha` and `beta`.
    3.  Calculate the matrix product `alpha`×`beta`
    4.  Calculate the matrix product `beta`×`alpha`

4.  What is:

        len([ [0], [0, 1], [0, 1, 2] ])

    1.  0
    2.  3
    3.  6
    4.  undefined (the lists have different lengths)

Aliasing
--------

### Learning Objectives:

-   Explain what an "alias" for a value is.
-   Explain why aliases can make programs harder to understand.
-   Identify examples in which aliasing does and does not occur.
-   Construct programs which create aliases for data.
-   Trace changes to data in programs that contain aliases.

At this point, we need to take a small side trip to explore something
which is very useful, but which can also be the source of some
hard-to-find bugs. Consider the following snippet of Python:

~~~~ {src="src/python/aliasing.py"}
>>> outer = [ [10, 20, 30], [40, 50, 60] ]
>>> inner = outer[0]
~~~~

After these two lines have been executed, the program's memory is as
shown in [Figure XXX](#f:aliasing_a): `outer` refers to a two-element
list containing references to a couple of three-element lists, while
`inner` refers to the first of those three-element lists.

![First Step of Aliasing Example](src/python/aliasing_a.png)

Now let's change the last value of the list that `inner` refers to:

    >>> inner[2] = 99

This changes memory as shown in [Figure XXX](#f:aliasing_b), which means
that the values of both `inner` *and* `outer` have changed:

    >>> print inner
    [10, 20, 99]
    >>> print outer
    [[10, 20, 99], [40, 50, 60]]

![Second Step of Aliasing Example](src/python/aliasing_b.png)

This is called [aliasing](glossary.html#alias), and it is not a bug: the
program is supposed to work this way. It doesn't have to, though;
Python's creator could have decided that:

    >>> inner = outer[0]

would create a copy of `outer[0]` and assign that to `inner` rather than
aliasing the first element of `outer` ([Figure XXX](#f:aliasing_copy)).
That would be easier to understand—there would be no chance that
assigning to one variable would cause another variable's value to
change—but it would also be less efficient. If our sublists contain a
million elements each, and we're assigning them to temporary variables
simply to make our program more readable, copying would cause
unnecessary slow-down.

![Copying Instead of Aliasing](src/python/aliasing_copy.png)

When a programming language copies data, and when it creates aliases
instead, is one of the most important things a programmer must know
about it. As we'll see when we start doing [web programming](web.html),
it's also one of the most important things to know about large systems
of any kind. If we query a database, is the result a copy of the data as
it was when we made the query, or a reference to the master copy? In the
first case, we can now change the data however we want without affecting
other people, but we won't see any updates they make ([Figure
XXX](#f:aliasing_data)). In the second case, we will automatically see
updates to the data, but that means our program has to cope with changes
at unpredictable times (and also has to re-fetch the data each time it
needs it, which will reduce performance). Neither approach is right or
wrong: there are simply engineering tradeoffs that we have to be aware
of.

![Aliasing Data](src/python/aliasing_data.png)

### Summary

-   Several variables can alias the same data.
-   If that data is mutable (e.g., a list), a change made through one
    variable is visible through all other aliases.

### Challenges

1.  Which diagram most accurately shows the state of memory after this
    code has executed?

        base = [1]
        base.append(base)

      ------------------------------- ------------------------------- ------------------------------- -------------------------------
      A                               B                               C                               D
      ![](img/python/challenge.png)   ![](img/python/challenge.png)   ![](img/python/challenge.png)   ![](img/python/challenge.png)
      ------------------------------- ------------------------------- ------------------------------- -------------------------------

2.  Which program creates the memory layout shown below?

    A

    B

    C

    D

        alpha = [beta]
        beta = [alpha]

        alpha = []
        beta = []
        alpha[0] = beta
        beta[0] = alpha

        alpha = [beta] + alpha

        alpha = []
        beta = []
        alpha.append(beta)
        beta.append(alpha)

3.  What does this program print?

        vector = [100, 200]
        matrix = []
        matrix.append(vector)
        vector[0] = 300
        vector[1] = 400
        matrix.append(vector)
        print matrix

    1.  `[[100, 200], [300, 400]]`
    2.  `[[300, 400], [300, 400]]`
    3.  `[[100, 200], [100, 200]]`
    4.  None of the above

4.  What does this program print?

        readings = [0] * 5
        readings[1] = 12
        readings[3] = 34
        print readings

    1.  `[0, 12, 2, 34, 4]`
    2.  `[0, 12, 0, 34, 0]`
    3.  `[0, 34, 0, 34, 0]`
    4.  None of the above

Summing Up
----------

Novices (and people looking for an argument) often ask, "What's the best
programming language?" The answer depends on what we want to do. If we
want to write small programs quickly, and be able to manage the
complexity of larger ones, then dynamic languages like Python, Ruby, R,
and MATLAB are good choices: they optimize programming time over
execution time. If we want to squeeze the last ounce of performance out
of our hardware, then compiled languages like C++, C\#, and modern
dialects of Fortran are currently better options. And if we want a user
interface that runs (almost) everywhere, Javascript has become a
surprisingly strong contender.
