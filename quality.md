Software Quality
================

Laura Landscape is studying the impact of climate change on agriculture.
She has several thousand aerial photographs of farms taken in the early
1980s, and she wants to compare those with photographs of the same
fields taken since 2007 to see what has changed.

The first step is to find regions where fields overlap. Luckily, the
area she is studying is in Saskatchewan, where fields actually are
rectangular. A student intern has written a function that finds the
regions of overlap between the fields in different photographs. Having
used student code before, she wants to test it before putting it into
production. She also thinks she might have to make the function faster,
to handle larger data sets, and she wants to have tests in place so that
her optimizations don't break anything. What should she do?

Nobody actually enjoys testing software: we'd all rather be writing new
programs, or better yet, using the ones we have to do some new science.
If you'd like to skip this lecture, you can, provided that:

1.  your programs always work correctly the first time you run them;
2.  you don't actually care whether they're doing the right thing or
    not, as long as their output *looks* plausible; or
3.  you enjoy wasting time, because experience and research both show
    that improving quality is the best way to improve productivity.

We said "improving quality" rather than testing because as Steve
McConnell once said, trying to improve the quality of software by doing
more testing is like trying to lose weight by weighing yourself more
often. Testing just tells us what the quality *is*; if we want to
improve it, so that we don't have to throw away a week's worth of
analysis because of a missing semi-colon, we have to change our
programs, and change the way we go about writing programs. That's what
this chapter is really about.

Defensive Programming
---------------------

### Understand:

-   That programs should detect errors as early as possible.
-   How to use assertions to establish that something is true in a
    program.
-   That functions should define and obey contracts with their users.

The first and most important step in creating quality programs is to
follow the rules outlined in [previous](python.html)
[chapters](funclib.html) for writing readable code. The second is to
realize that since nobody is perfect, programs should be designed to
detect both their own errors, and errors in the way they are used. This
is called [defensive programming](glossary.html#defensive-programming),
and is akin to adding a self-test function to a piece of lab equipment.

In most modern languages, we do this by adding
[assertions](glossary.html#assertion) to our programs. An assertion is
simply a statement that something is supposed to be true at a certain
point in the program. For example, here's the `combine_values` function
from the section on [functional programming](funclib.html#s:funcobj):

~~~~ {src="src/quality/combine.py"}
def combine_values(func, values):
    current = values[0]
    for i in range(1, len(values)):
        current = func(current, values[i])
    return current
~~~~

If we want to add up the values in a list, we call it like this:

    def add(a, b):
        return a + b

    numbers = [1, 3, 6, 7, 9]
    print combine_values(add, numbers)
    26

If we call it with an empty list, though, it fails, because the first
statement tries to get the list's first element:

    print combine_values(add, [])
    IndexError: list index out of range

Let's add an assertion to test for this case explicitly:

~~~~ {src="src/quality/combine2.py"}
def combine_values(func, values):
    assert len(values) > 0, 'Cannot combine values from empty list'
    current = values[0]
    for i in range(1, len(values)):
        current = func(current, values[i])
    return current

print combine_values(add, [])
AssertionError: Cannot combine values from empty list
~~~~

This assertion documents the [contract](glossary.html#contract) between
the function and its caller: the function will only produce a value if
the caller provides a list containing some data. We could use a comment
or docstring to do the same thing, but the assertion has the advantage
of being executable: the program actually does the check every time the
function is called.

Good programs are littered with assertions—in fact, 10-20% of the
statements in many widely-used programs are there to check that the
other 80-90% are working correctly. Broadly speaking, assertions fall
into three categories:

-   A [precondition](glossary.html#precondition) is something that has
    to be true in order for a piece of code to work correctly.
-   A [postcondition](glossary.html#postcondition) is something that has
    to be true at the end of a piece of code if it worked correctly.
-   An [invariant](glossary.html#invariant) is something that is always
    true at a particular point inside a piece of code.

![Representing Rectangles](img/python/rectangle_rep.png)

For example, suppose we are representing rectangles using a pair of
pairs `[[x0, y0], [x1, y1]]` ([Figure XXX](#f:rectangle_rep)). In order
to normalize some calculations, we need to resize the rectangle so that
it is 1.0 units long on its longest axis. Here's a function that does
that:

~~~~ {src="src/quality/rectangle_resize.py"}
def normalize_rectangle(rect):
    [[x0, y0], [x1, y1]] = rect
    assert x0 < x1, 'Invalid X coordinates'
    assert y0 < y1, 'Invalid Y coordinates'
    dx = x1 - x0
    dy = y1 - y0
    if dx > dy:
        scaled = float(dy) / dx
        upper = [1.0, scaled]
    else:
        scaled = float(dx) / dy
        upper = [scaled, 1.0]

    assert 0 < upper[0] <= 1.0, 'Calculated upper X coordinate invalid'
    assert 0 < upper[1] <= 1.0, 'Calculated upper Y coordinate invalid'

    return [[0, 0], upper]
~~~~

The first two assertions test that the inputs are valid, i.e., that the
upper X and Y coordinates are greater than their lower counterparts.
Notice that the test is greater than, not greater than or equal to; this
tells us (and the computer) that rectangles aren't allowed to have zero
width or height. The last two assertions check that the upper
coordinates of the scaled rectangle are valid: neither can be zero
(because that would mean the rectangle had zero width or height), and
neither can be greater than 1.

If the inputs are correct, and our calculation is correct, then these
two conditions should always hold, so strictly speaking, these two
assertions are redundant. However, programmers aren't perfect, and if
there *is* a bug in our calculations, we want the program to complain
about it as early as possible.

This principle is sometimes stated as, "Fail early, fail often." The
longer the gap between when something goes wrong and when we realize it,
the more lines of code and program execution history we have to wade
through in order to track the problem down.

### Assertions and Bugs

Another rule that good programmers follow is, "Bugs become assertions."
Whenever we fix a bug in a program, we should add some assertions to the
program at that point to catch the bug if it reappears. After all, if we
made the mistake once, we (or someone else) might well make it again,
and few things are as frustrating as having someone delete several
carefully-crafted lines of code that fixed a subtle problem because they
didn't realize what problem those lines were there to fix.

### Assertions and Types

It's common to see code like this from people who have just learned
about assertions:

~~~~ {src="src/quality/rectangle_resize.py"}
def normalize_rectangle(rect):
    assert type(rect) == list, 'Input is not a list'
    assert len(rect) == 2, 'Input rectangle does not have two elements'
    assert len(rect[0]) == 2, 'Low coordinate of rectangle does not have two elements'
    assert type(rect[0][0]) in (int, float), 'Low X coordinate is not a number'
    ...
~~~~

In essence, these assertions are emulating the checks that are built
into statically-typed languages like Java and C++, which require
programmers to declare what kind of data every variable can store. For
the most part, they aren't very useful in dynamically-typed languages
like Python:

1.  The statement that unpacks the values in `rect` and assigns them to
    `x0`, `y0`, `x1`, and `y1` will fail if `rect` doesn't have the
    right structure, so the assertion doesn't do any checking that the
    program isn't doing already.
2.  These checks are overly restrictive. There's no reason we shouldn't
    be able to pass in tuples of coordinates instead of lists, or use
    rational (fractional) numbers instead of integers or floats, but if
    we do either of those things, the assertions given above will fail.
    Rather than checking how something is implemented (i.e., what types
    are used), assertions should check what those things can do (i.e.,
    what operations we can perform on them). We will talk about this
    more when we talk about the difference between [interface and
    implementation](#s:testable).

### Summary

-   Design programs to catch both internal errors and usage errors.
-   Use assertions to check whether things that ought to be true in a
    program actually are.
-   Assertions help people understand how programs work.
-   Fail early, fail often.
-   When bugs are fixed, add assertions to the program to prevent their
    reappearance.

Handling Errors
---------------

### Understand:

-   Why functions shouldn't use status code to indicate whether they ran
    correctly or not.
-   What exceptions are and when they can occur.
-   How to handle exceptions.
-   That there are different kinds of exceptions, which can be handled
    separately.
-   That exceptions can and should be handled a long way from where they
    occur.
-   How to raise an exception.

It's a sad fact, but things sometimes go wrong in programs. Some of
these errors have external causes, like missing or badly-formatted
files. Others are internal, like bugs in code. Either way, there's no
need for panic: it's actually pretty easy to handle errors in sensible
ways.

First, though, let's have a look at how programmers used to do error
handling. Back in the Dark Ages, programmers would have functions return
some sort of status to indicate whether they had run correctly or not.
This led to code like this:

    params, status = read_params(param_file)
    if status != OK:
      log.error('Failed to read', param_file)
      sys.exit(ERROR)

    grid, status = read_grid(grid_file)
    if status != OK:
      log.error('Failed to read', grid_file)
      sys.exit(ERROR)

The unhighlighted code is what we really want; the highlighted lines are
there to check that files were opened and read properly, and to report
errors and exit if not.

A lot of code is still written this way, but this coding style makes it
hard to see the forest for the trees. When we're reading a program, we
want to understand what's supposed to happen when everything works, and
only then think about what might happen if something goes wrong. When
the two are interleaved, both are harder to understand. The net result
is that most programmers don't bother to check the status codes their
functions return. Which means that when errors *do* occur, they're even
harder to track down.

Luckily, there's a better way. Modern languages like Python allow us to
use [exceptions](glossary.html#exception) to handle errors. More
specifically, using exceptions allows us to separate the "normal" flow
of control from the "exceptional" cases that arise when something goes
wrong, which makes both easier to understand:

    try:
      params = read_params(param_file)
      grid = read_grid(grid_file)
    except:
      log.error('Failed to read', filename)
      sys.exit(ERROR)

As a fringe benefit, this often allows us to eliminate redundancy in our
error handling.

To join the two parts together, we use the keywords `try` and `except`.
These work together like `if` and `else`: the statements under the `try`
are what should happen if everything works, while the statements under
`except` are what the program should do if something goes wrong.

We have actually seen exceptions before without knowing it, since by
default, when an exception occurs, Python prints it out and halts our
program. For example, trying to open a nonexistent file triggers a type
of exception called an `IOError`, while an out-of-bounds index to a list
triggers an `IndexError`:

    >>> open('nonexistent.txt', 'r')
    IOError: No such file or directory: 'nonexistent.txt'
    >>> values = [0, 1, 2]
    >>> values[99]
    IndexError: list index out of range

We can use `try` and `except` to deal with these errors ourselves if we
don't want the program simply to fall over. Here, for example, we put
our attempt to open a nonexistent file inside a `try`, and in the
`except`, we print a not-very-helpful error message:

try: reader = open('nonexistent.txt', 'r') except IOError: print
'Whoops! Whoops!

Notice that the output is blue, signalling that it was printed normally,
rather than red, which is shown for errors. When Python executes this
code, it runs the statement inside the `try`. If that works, it skips
over the `except` block without running it. If an exception occurs
inside the `try` block, though, Python compares the type of the
exception to the type specified by the `except`. If they match, it
executes the code in the `except` block.

![Flow of Control with Exceptions](img/quality/exception_flowchart.png)

Note, by the way, that `IOError` is Python's way of reporting several
kinds of problems related to input and output: not just files that don't
exist, but also things like not having permission to read files, and so
on.

We can put as many lines of code in a `try` block as we want, just as we
can put many statements under an `if`. We can also handle several
different kinds of errors afterward. For example, here's some code to
calculate the entropy at each point in a grid:

    try:
        params = read_params(param_file)
        grid = read_grid(grid_file)
        entropy = lee_entropy(params, grid)
        write_entropy(entropy_file, entropy)
    except IOError:
        log_error_and_exit('IO error')
    except ArithmeticError:
        log_error_and_exit('Arithmetic error')

Python tries to run the four statements inside the `try` as normal. If
an error occurs in any of them, Python immediately jumps down and tries
to find an `except` whose type matches the type of the error that
occurred. If it's an `IOError`, Python jumps into the first error
handler. If it's an `ArithmeticError`, Python jumps into the second
handler instead. It will only execute one of these, just as it will only
execute one branch of a series of `if`/`elif`/`else` statements.

This layout has made the code easier to read, but we've lost something
important: the message printed out by the `IOError` branch doesn't tell
us which file caused the problem. We can do better if we capture and
hang on to the object that Python creates to record information about
the error:

    try:
        params = read_params(param_file)
        grid = read_grid(grid_file)
        entropy = lee_entropy(params, grid)
        write_entropy(entropy_file, entropy)
    except IOError as err:
        log_error_and_exit('Cannot read/write' + err.filename)
    except ArithmeticError as err:
        log_error_and_exit(err.message)

If something goes wrong in the `try`, Python creates an exception
object, fills it with information, and assigns it to the variable `err`.
(There's nothing special about this variable name—we can use anything we
want.) Exactly what information is recorded depends on what kind of
error occurred; Python's documentation describes the properties of each
type of error in detail, but we can always just print the exception
object. In the case of an I/O error, we print out the name of the file
that caused the problem. And in the case of an arithmetic error,
printing out the message embedded in the exception object is what Python
would have done anyway.

So much for how exceptions work: how should they be used? Some
programmers use `try` and `except` to give their programs default
behaviors. For example, if this code can't read the grid file that the
user has asked for, it creates a default grid instead:

    try:
        grid = read_grid(grid_file)
    except IOError:
        grid = default_grid()

Other programmers would explicitly test for the grid file, and use `if`
and `else` for control flow:

    if file_exists(grid_file):
        grid = read_grid(grid_file)
    else:
        grid = default_grid()

It's mostly a matter of taste, but we prefer the second style. As a
rule, exceptions should only be used to handle exceptional cases. If the
program knows how to fall back to a default grid, that's not an
unexpected event. Using `if` and `else` instead of `try` and `except`
sends different signals to anyone reading our code, even if they do the
same thing.

Novices often ask another question about exception handling style as
well, but before we address it, there's something in our example that
you might not have noticed. Exceptions can actually be thrown a long
way: they don't have to be handled immediately. Take another look at
this code:

    try:
        params = read_params(param_file)
        grid = read_grid(grid_file)
        entropy = lee_entropy(params, grid)
        write_entropy(entropy_file, entropy)
    except IOError as err:
        log_error_and_exit('Cannot read/write' + err.filename)
    except ArithmeticError as err:
        log_error_and_exit(err.message)

The four lines in the `try` block are all function calls. They might
catch and handle exceptions themselves, but if an exception occurs in
one of them that *isn't* handled internally, Python looks in the calling
code for a matching `except`. If it doesn't find one there, it looks in
that function's caller, and so on. If we get all the way back to the
main program without finding an exception handler, Python's default
behavior is to print an error message like the ones we've been seeing
all along.

This rule is the origin of the saying, "Throw low, catch high." There
are many places in our program where an error might occur. There are
only a few, though, where errors can sensibly be handled. For example, a
linear algebra library doesn't know whether it's being called directly
from the Python interpreter, or whether it's being used as a component
in a larger program. In the latter case, the library doesn't know if the
program that's calling it is being run from the command line or from a
GUI. The library therefore shouldn't try to handle or report errors
itself, because it has no way of knowing what the right way to do this
is. It should instead just raise an exception, and let its caller figure
out how best to handle it.

Finally, we can raise exceptions ourselves if we want to. In fact, we
*should* do this, since it's the standard way in Python to signal that
something has gone wrong. Here, for example, is a function that reads a
grid and checks its consistency:

    def read_grid(grid_file):
        '''Read grid, checking consistency.'''

        data = read_raw_data(grid_file)
        if not grid_consistent(data):
            raise Exception('Inconsistent grid: ' + grid_file)
        result = normalize_grid(data)

        return result

The `raise` statement creates a new exception with a meaningful error
message. Since `read_grid` itself doesn't contain a `try`/`except`
block, this exception will always be thrown up and out of the function,
to be caught and handled by whoever is calling `read_grid`. We can
define new types of exceptions if we want to. And we should, so that
errors in our code can be distinguished from errors in other people's
code. However, this involves classes and objects, which is outside the
scope of these lessons.

### Summary

-   Use `raise` to raise exceptions.
-   Raise exceptions to report errors rather than trying to handle them
    inline.
-   Use `try` and `except` to handle exceptions.
-   Catch exceptions where something useful can be done about the
    underlying problem.
-   An exception raised in a function may be caught anywhere in the
    active call stack.

Unit Testing
------------

### Understand:

-   That testing can't catch all mistakes, but is still worth doing.
-   What a unit test is.
-   That unit tests should be independent of each other.
-   Why we want to ensure that all unit tests are always run.
-   How to write unit tests using a standard library.
-   That testing effort should focus on boundary cases.
-   That tests help us specify what code should do.

Now that we know how to defend against errors, and how to handle them,
we can look at how to test our programs. First, though, it's important
to understand that testing can only do so much. Suppose we are testing a
function that compares two 7-digit phone numbers. There are 10^7^ such
numbers, which means that there are 10^14^ possible test cases for our
function. At a million tests per second, it would take us 155 days to
run them all. And that's only one simple function: exhaustively testing
a real program with hundreds or thousands of functions, each taking half
a dozen arguments, would take many times longer than the expected
lifetime of the universe.

And how would we actually write 10^14^ tests? More importantly, how
would we check that the tests themselves were all correct?

In reality, all that testing can do is show that there *might* be a
problem in a piece of code. If testing doesn't find a failure, there
could still be bugs lurking there that we just didn't find. And if
testing says there *is* a problem, it could well be a problem with the
test rather than the program.

So why test? Because it's one of those things that shouldn't work in
theory, but is surprisingly effective in practice. It's just like
mathematics: any theorem proof might contain a flaw that just hasn't
been noticed yet, but somehow we manage to make progress.

The obstacle to testing isn't actually whether or not it's useful, but
whether or not it's easy to do. If it isn't, people will always find
excuses to do something else. It's therefore important to make things as
painless as possible. In particular, it has to be easy for people to:

-   add or change tests,
-   understand the tests that have already been written,
-   run those tests, and
-   understand those tests' results.

Test results must also be reliable to be useful. If a testing tool says
that code is working when it's not, or reports problems when there
actually aren't any, people will lose faith in it and stop using it.

Let's start with the simplest kind of testing. A [unit
test](glossary.html#unit-test) is a test that exercises one component,
or unit, in a program. Every unit test has five parts. The first is the
[fixture](glossary.html#fixture), which is the thing the test is run on:
the inputs to a function, or the data files to be processed.

The second part is the [action](glossary.html#test-action), which is
what we do to the fixture. Ideally, this just involves calling a
function, but some tests may involve more.

The third part of every unit test is its [expected
result](glossary.html#expected-result), which is what we expect the
piece of code we're testing to do or return. If we don't know the
expected result, we can't tell whether the test passed or failed. As
we'll see [later](#s:unit), defining fixtures and expected results can
be a good way to design software.

The first three parts of the unit test are used over and over again. The
fourth part is the [actual result](glossary.html#test-result), which is
what happens when we run the test on a particular day, with a particular
version of our software.

The fifth and final part of our test is a
[report](glossary.html#test-report) that tells us whether the test
passed, or whether there's a failure of some kind that needs human
attention. As with the actual result, this could be different each time
we run the test.

So much for terminology: what does this all look like in practice?
Suppose we're testing a function called `dna_starts_with`. It returns
`True` if its second argument is a prefix of the first (i.e., if one
sequence starts with another), and `False` otherwise:

    >>> dna_starts_with('actggt', 'act')
    True
    >>> dna_starts_with('actggt', 'ctg')
    False

We'll build a simple set of tests for this function from scratch to
introduce some key ideas, then introduce a Python library that can take
care of the repetitive details.

Let's start by testing our code directly using `assert`. Here, we call
the function four times with different arguments, checking that the
right value is returned each time.

    assert dna_starts_with('a', 'a')
    assert dna_starts_with('at', 'a')
    assert dna_starts_with('at', 'at')
    assert not dna_starts_with('at', 't')

This is better than nothing, but it has several shortcomings. First,
there's a lot of repeated code: only a fraction of what's on each line
is unique and interesting. That repetition makes it easy to overlook
things, like the `not` used to check that the last test returns `False`
instead of `True`.

This code also only tests up to the first failure. If any of the tests
doesn't produce the expected result, the `assert` statement will halt
the program. It would be more helpful if we could get data from all of
our tests every time they're run, since the more information we have,
the faster we're likely to be able to track down bugs.

Here's a different approach. First, let's put each test in a function
with a meaningful name:

    def single_base_starts_with_itself():
        assert dna_starts_with('a', 'a')

    def longer_genome_starts_with_base():
        assert dna_starts_with('at', 'a')

    def longer_genome_starts_with_itself():
        assert dna_starts_with('at', 'at')

    def longer_genome_doesnt_start_with():
        assert not dna_starts_with('at', 't')

Of course, those tests won't run themselves, so we'll add one more
function at the bottom of the program that calls each test in turn:

    def run():
        single_base_starts_with_itself()
        longer_genome_starts_with_base()
        longer_genome_starts_with_itself()
        longer_genome_doesnt_start_with()

So far, this isn't much of an improvement—in fact, it's made things
worst. But what if we put all our tests in a list, and then loop over
that list, calling each function in turn?

    def run():
        tests = [single_base_starts_with_itself,
                 longer_genome_starts_with_base,
                 longer_genome_starts_with_itself,
                 longer_genome_doesnt_start_with]
        for t in tests:
            t()

This will still crash the first time a test fails, though, so let's add
some error handling:

    def run():
        tests = [single_base_starts_with_itself,
                 longer_genome_starts_with_base,
                 longer_genome_starts_with_itself,
                 longer_genome_doesnt_start_with]
        pass = fail = error = 0
        for t in tests:
            try:
                t()
                pass += 1
            except AssertionError:
                fail += 1
            except:
                error += 1
        return pass, fail, error

This version makes the pattern in our testing clear (well, clear-ish).
Each function is called exactly once; if it runs without an assertion,
we count the test as a success. If an assertion fails, we count the test
as a failure, and if any other exception occurs, we add one to our count
of errors (i.e., of tests that are themselves broken).

This pattern is so common that libraries have been written to support it
in [dozens of different programming
languages](http://en.wikipedia.org/wiki/XUnit). We'll use a Python
library called Nose to illustrate the ideas. In Nose, each test is a
function whose name begins with the letters `test_`. We can group tests
together in files, whose names also begin with the letters `test_`. To
execute our tests, we run the command `nosetests`. This automatically
searches the current directory and its sub-directories for test files
and runs the tests they contain.

To see how this works, let's use it to test the `dna_starts_with`
function. All we have to do is delete the `run` function (which we no
longer need) and change the names of the individual tests:

    def test_single_base_starts_with_itself():
        assert dna_starts_with('a', 'a')

    def test_longer_genome_starts_with_base():
        assert dna_starts_with('at', 'a')

    def test_longer_genome_starts_with_itself():
        assert dna_starts_with('at', 'at')

    def test_longer_genome_doesnt_start_with():
        assert not dna_starts_with('at', 't')

To run these tests, we simply type:

    $ nosetests
    ....
    ----------------------------------------------------------------------
    Ran 4 tests in 0.004s

    OK

Each '.' represents a successful test. To see what happens if a test
fails, let's add two more functions to the file that are deliberately
broken:

    def test_deliberate_failure():
        assert dna_starts_with('at', 'xxx')

    def test_deliberate_error():
        infinity = 1/0
        assert dna_starts_with('at', 'a')

    ~/foo $ nosetests
    ....FE
    ======================================================================
    ERROR: test_dna.test_deliberate_error
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/python2.7/site-packages/nose-1.0.0-py2.7.egg/nose/case.py", line 187, in runTest
        self.test(*self.arg)
      File "/home/scb/testing/test_dna.py", line 20, in test_deliberate_error
        infinity = 1/0
    ZeroDivisionError: integer division or modulo by zero

    ======================================================================
    FAIL: test_dna.test_deliberate_failure
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/python2.7/site-packages/nose-1.0.0-py2.7.egg/nose/case.py", line 187, in runTest
        self.test(*self.arg)
      File "/home/scb/testing/test_dna.py", line 17, in test_deliberate_failure
        assert dna_starts_with('at', 'xxx')
    AssertionError

    ----------------------------------------------------------------------
    Ran 6 tests in 0.055s

    FAILED (errors=1, failures=1)

Of course, the Nose library can't think of test cases for us. We still
have to decide what to test, and how many tests to run. How should we go
about deciding which tests to write? The answer comes from economics: we
want the tests that are most likely to give us useful information that
we don't already have. For example, if `dna_starts_with('atc', 'a')`
works, there's probably not much point testing
`dna_starts_with('ttc', 't')`: it's hard to think of a bug that would
show up in one case, but not in the other.

We should therefore try to choose tests that are as different from each
other as possible, so that we force the code we're testing to execute in
all the different ways it can. Another way of thinking about this is
that we should try to find [boundary
cases](glossary.html#boundary-case). If a function works for zero, one,
and a million values, it will probably work for eighteen values.

Let's apply this idea to the overlapping rectangles problem from the
introduction. A "normal" case is two rectangles that overlap by half in
each direction:

![A Simple Test Case](img/quality/simple_rectangle_test_case.png)

What other tests would be useful? One would be two rectangles that
overlap by half in each direction.. Another is the case where the
rectangle on the left extends above and below the one on the right, so
none of the corners of the left rectangle are involved. And in a third
the two rectangles are exactly the same width, but have different
vertical extents. This will tell us whether the overlap function behaves
correctly when rectangles intersect along entire lines, rather than just
crossing at points. And then there's the case where the second rectangle
is contained entirely within the first, so their edges don't actually
cross at all.

![More Test Cases](img/quality/more_rectangle_test_cases.png)

But what do we expect if the two rectangles share an edge, but their
areas don't overlap? And what if they only share a corner? Should the
function we're testing tell us that these rectangles don't overlap?
Should it return a point, rather than a rectangle? Or should it return a
rectangle with zero area?

![Boundary Cases](img/quality/boundary_cases.png)

Thinking about tests in terms of boundary cases helps us find examples
like this, where it isn't immediately obvious what the right answer is.
Writing those tests forces us to define how the function we're testing
is supposed to behave—i.e., what correct behavior actually is.

Let's turn all of this into working code. Here's a test for the case
where rectangles only touch at a corner:

    def test_touch_at_corner():
        assert overlap([[0, 0], [2, 2]], [[2, 2], [4, 4]]) == None

As you can see, we've decided that this doesn't count as overlap. Our
test is an unambiguous, runnable answer to our question about how the
function is supposed to behave.

Here's our second test: two rectangles that have exactly the same
extent, so their overlap is the same again.

    def test_touch_at_corner():
        r = [[0, 0], [2, 2]]
        assert overlap(r, r) == r

This wasn't actually in the set of test cases we came up with earlier,
but it's still a good test. And here's a third test, where one rectangle
is skinnier than another:

    def test_partial_overlap():
        red = [[0, 3], [2, 5]]
        blue = [[1, 0], [2, 4]]
        assert overlap(red, blue) == [[1, 3], [2, 4]]

This test case actually turned up a bug in the first version of the
overlap function that we wrote. Here's the function:

    def overlap(red, blue):
        '''Return overlap between two rectangles, or None.'''

        [[red_lo_x, red_lo_y], [red_hi_x, red_hi_y]] = red
        [[blue_lo_x, blue_lo_y], [blue_hi_x, blue_hi_y]] = blue

        if (red_lo_x >= blue_hi_x) or (red_hi_x <= blue_lo_x) or \
           (red_lo_y >= blue_hi_x) or (red_hi_y <= blue_lo_y):
            return None

        lo_x = max(red_lo_x, blue_lo_x)
        lo_y = max(red_lo_y, blue_lo_y)
        hi_x = min(red_hi_x, blue_hi_x)
        hi_y = min(red_hi_y, blue_hi_y)

        return [[lo_x, lo_y], [hi_x, hi_y]]

It takes the coordinates of each rectangle as input, unpacks them to get
the high and low X and Y coordinates of each rectangle, checks to make
sure that the rectangles actually overlap, then calculates the
coordinates of the overlap and returns the result as a new rectangle. By
looking at which test cases pass and fail, it's pretty easy to discover
that we are comparing the low Y coordinate of one rectangle with the
high X coordinate of the other (probably as a result of copying and
pasting):

    def overlap(red, blue):
        '''Return overlap between two rectangles, or None.'''

        [[red_lo_x, red_lo_y], [red_hi_x, red_hi_y]] = red
        [[blue_lo_x, blue_lo_y], [blue_hi_x, blue_hi_y]] = blue

        if (red_lo_x >= blue_hi_x) or (red_hi_x <= blue_lo_x) or \
           (red_lo_y >= blue_hi_x) or (red_hi_y <= blue_lo_y):
            return None

        lo_x = max(red_lo_x, blue_lo_x)
        lo_y = max(red_lo_y, blue_lo_y)
        hi_x = min(red_hi_x, blue_hi_x)
        hi_y = min(red_hi_y, blue_hi_y)

        return [[lo_x, lo_y], [hi_x, hi_y]]

Stepping back, the most important lesson in this episode isn't the
details of the Nose library. It's that our time is more valuable than
the computer's, so we should spend it doing the things the computer
can't, like thinking of interesting test cases and what our code is
actually supposed to do. Nose and other libraries like it are there to
handle all the things that we *shouldn't* have to re-think each time.
They will also help guide we toward good practices, to make our testing
and programming more productive.

Testing tells us whether our program is doing what it's supposed to do.
But if it's done right, it will also tell us *what* our program actually
*is* supposed to be doing. As we saw earlier, we can think of tests as
runnable specifications of a program's behavior. Unlike design documents
or comments in the code, we can actually run our tests, so it's harder
for them to fall out of sync with the program's actual behavior. In
well-run projects, tests also act as examples to show newcomers how the
code should be used, and how it's supposed to behave under different
circumstances.

### Assertions and Tests

Some people believe that every time a bug is fixed, the programmer
should add assertions to the program to catch it if it ever reappears.
Other people believe that tests should be used for this, i.e., that when
a bug is found, the programmer should write a test that fails if the bug
is present, but passes if the bug is fixed. Both are good practices, and
over time, individual programmers and projects usually settle on a mix
of the two.

### Summary

-   Testing cannot prove that a program is correct, but is still worth
    doing.
-   Use a unit testing library like Nose to test short pieces of code.
-   Write each test as a function that creates a fixture, executes an
    operation, and checks the result using assertions.
-   Every test should be able to run independently: tests should *not*
    depend on one another.
-   Focus testing on boundary cases.
-   Writing tests helps us design better code by clarifying our
    intentions.

Numbers
-------

### Understand:

-   How computers represent numbers.
-   That floating point numbers are inexact, uneven approximations of
    real numbers.
-   The difference between absolute error and relative error.
-   That tests of numerical code should be written in terms of relative
    error.
-   Three strategies for testing numerical programs.

Let's start by looking at how numbers are stored. If we only have the
two digits 0 and 1, the natural way to store a positive integer is to
use base 2, so 1001~2~ is (1×2^3^)+(0×2^2^)+(0×2^1^)+(1×2^0^) = 9~10~.
It's equally natural to extend this scheme to negative numbers by
reserving one bit for the sign. If, for example, we use 0 for positive
numbers and 1 for those that are negative, +9~10~ would be 01001~2~ and
-9~10~ would be 11001~10~.

There are two problems with this. The first is that this scheme gives us
two representations for zero (00000~2~ and 10000~2~). This isn't
necessarily fatal, but any claims this scheme has to being "natural"
disappear when we have to write code like:

    if (length != +0) and (length != -0):

As for the other problem, it turns out that the circuits needed to do
addition and other arithmetic on this [sign and magnitude
representation](glossary.html#sign-and-magnitude) are more complicated
than the hardware needed for another called [two's
complement](glossary.html#twos-complement). Instead of mirroring
positive values, two's complement rolls over when going below zero, just
like a car's odometer. If we're using four bits per number, so that
0~10~ is 0000~2~, then -1~10~ is 1111~2~. -2~10~ is 1110~2~, -3~10~ is
1101~2~, and so on until we reach the most negative number we can
represent, 1000~2~, which is -8. Our representation then wraps around
again, so that 0111~2~ is 7~10~.

This scheme isn't intuitive, but it solves sign and magnitude's "double
zero" problem, and the hardware to handle it is faster and cheaper. As a
bonus, we can still tell whether a number is positive or negative by
looking at the first bit: negative numbers have a 1, positives have a 0.
The only odd thing is its asymmetry: because 0 counts as a positive
number, numbers go from -8 to 7, or -16 to 15, and so on. As a result,
even if `x` is a valid number, `-x` may not be.

Finding a good representation for real numbers (called [floating point
numbers](#glossary.html#floating-point), since the decimal point can
move around) is a much harder problem. The root of the problem is that
we cannot represent an infinite number of real values with a finite set
of bit patterns. And unlike integers, no matter what values we *do*
represent, there will be an infinite number of values between each of
them that we can't.

Floating point numbers are usually represented using sign, magnitude,
and an exponent. In a 32-bit word, the IEEE 754 standard calls for 1 bit
of sign, 23 bits for the magnitude (or *mantissa*), and 8 bits for the
exponent. To illustrate the problems with floating point, we'll use a
much dumber representation: we'll only worry about positive values
without fractional parts, and we'll only use 3 for the magnitude and 2
for the exponent.

[Figure XXX](#f:simple_float) shows the values that we can represent
this way. Each one is the mantissa times two to the exponent. For
example, the decimal values 48 is binary 110 times 2 to the binary 11
power, which is 6 times 2 to the third, or 6 times 8. (Note that real
floating point representations like the IEEE 754 standard don't have the
redundancy shown in this table, but that doesn't affect our argument.)

![Simple Representation of Floating Point
Numbers](img/numpy/simple_float.png)

The first thing you should notice is that there are a lot of values we
*can't* store. We can do 8 and 10, for example, but not 9. This is
exactly like the problems hand calculators have with fractions like 1/3:
in decimal, we have to round that to 0.3333 or 0.3334.

But if this scheme has no representation for 9, then 8+1 must be stored
as either 8 or 10. This raises an interesting question: if 8+1 is 8,
what is 8+1+1? If we add from the left, 8+1 is 8, plus another 1 is 8
again. If we add from the right, though, 1+1 is 2, and 2+8 is 10.
Changing the order of operations can make the difference between right
and wrong. There's no randomness involved—a particular order of
operations will always produce the same result—but as the number of
steps increases, so too does the difficulty of figuring out what the
best order is.

This is the sort of problem that numerical analysts spend their time on.
In this case, if we sort the values we're adding, then add from smallest
to largest, it gives us a better chance of getting the best possible
answer. In other situations, like inverting a matrix, the rules are much
more complicated.

Here's another observation about our uneven number line: the spacing
between the values we can represent is uneven, but the relative spacing
between each set of values stays the same, i.e., the first group is
separated by 1, then the separation becomes 2, then 4, then 8, so that
the ratio of the spacing to the values stays roughly constant. This
happens because we're multiplying the same fixed set of mantissas by
ever-larger exponents, and it points us at a couple of useful
definitions.

The [absolute error](glossary.html#absolute-error) in some approximation
is simply the absolute value of the difference between the actual value
and the approximation. The [relative
error](glossary.html#relative-error), on the other hand, is the ratio of
the absolute error to the value we're approximating. For example, if
we're off by 1 in approximating 8+1 and 56+1, the absolute error is the
same in both cases, but the relative error in the first case is 1/9 =
11%, while the relative error in the second case is only 1/57 = 1.7%.
When we're thinking about floating point numbers, relative error is
almost always more useful than absolute error. After all, it makes
little sense to say that we're off by a hundredth when the value in
question is a billionth.

To see why this matters, let's have a look at a little program:

~~~~ {src="src/numpy/nines.py"}
nines = []
sums = []
current = 0.0
for i in range(1, 10):
    num = 9.0 / (10.0 ** i)
    nines.append(num)
    current += num
    sums.append(current)
for i in range(len(nines)):
    print '%.18f %.18f' % (nines[i], sums[i])
~~~~

The loop runs over the integers from 1 to 9 inclusive. Using those
values, we create the numbers 0.9, 0.09, 0.009, and so on, and put them
in the list `vals`. We then calculate the sum of those numbers. Clearly,
this should be 0.9, 0.99, 0.999, and so on. But is it?

  --- ---------------------- ----------------------
  1   0.900000000000000022   0.900000000000000022
  2   0.089999999999999997   0.989999999999999991
  3   0.008999999999999999   0.998999999999999999
  4   0.000900000000000000   0.999900000000000011
  5   0.000090000000000000   0.999990000000000046
  6   0.000009000000000000   0.999999000000000082
  7   0.000000900000000000   0.999999900000000053
  8   0.000000090000000000   0.999999990000000061
  9   0.000000009000000000   0.999999999000000028
  --- ---------------------- ----------------------

Here are our answers. The first column is the loop index; the second,
what we actually got when we tried to calculate 0.9, 0.09, and so on,
and the third is the cumulative sum.

The first thing you should notice is that the very first value
contributing to our sum is already slightly off. Even with 23 bits for a
mantissa, we cannot exactly represent 0.9 in base 2, any more than we
can exactly represent 1/3 in base 10. Doubling the size of the mantissa
would reduce the error, but we can't ever eliminate it.

The second thing to notice is that our approximation to 0.0009 actually
appears accurate, as do all of the approximations after that. This may
be misleading, though: after all, we've only printed things out to 18
decimal places. As for the errors in the last few digits of the sums,
there doesn't appear to be any regular pattern in the way they increase
and decrease.

This phenomenon is one of the things that makes testing scientific
programs hard. If a function uses floating point numbers, what do we
compare its result to if we want to check that it's working correctly?
If we compared the sum of the first few numbers in `vals` to what it's
supposed to be, the answer could be `False`, even if we're initializing
the list with the right values, and calculating the sum correctly. This
is a genuinely hard problem, and no one has a good generic answer. The
root of our problem is that we're using approximations, and each
approximation has to be judged on its own merits.

There are things you can do, though. The first rule is, compare what you
get to analytic solutions whenever you can. For example, if you're
looking at the behavior of drops of liquid helium, start by checking
your program's output on a stationary spherical drop in zero gravity.
You should be able to calculate the right answer in that case, and if
your program doesn't work for it, it probably won't work for anything
else.

The second rule is to compare more complex versions of your code to
simpler ones. If you're about to replace a simple algorithm for
calculating heat transfer with one that's more complex, but hopefully
faster, don't throw the old code away. Instead, use its output as a
check on the correctness of the new code. And if you bump into someone
at a conference who has a program that can calculate some of the same
results as yours, swap data sets: it'll help you both.

The third rule is, never use `==` (or `!=`) on floating point numbers,
because two numbers calculated in different ways will probably not have
exactly the same bits. Instead, check to see whether two values are
within some tolerance, and if they are, treat them as equal. Doing this
forces you to make your tolerances explicit, which is useful in its own
right (just as putting error bars on experimental results is useful).

Finally, and most importantly, if you're doing any calculation on a
computer at all, take half an hour to read Goldberg's excellent paper,
"[What Every Computer Scientist Should Know About Floating-Point
Arithmetic](bib.html#goldberg-floating-point)".

### Summary

-   Floating point numbers are approximations to actual values.
-   Use tolerances rather than exact equality when comparing floating
    point values.
-   Use integers to count and floating point numbers to measure.
-   Most tests should be written in terms of relative error rather than
    absolute error.
-   When testing scientific software, compare results to exact analytic
    solutions, experimental data, or results from simpler or
    previously-tested programs.

Coverage
--------

### Understand:

-   What code coverage is.
-   How to use tools to calculate code coverage.
-   Why complete code coverage doesn't guarantee that code has been
    fully tested.
-   How to use coverage to guide testing effort.

The [code coverage](glossary.html#code-coverage) of a set of tests is
the percentage of the application code those tests exercise. For
example, suppose our function is:

    def sign(num):
        if num < 0:
            return -1
        if num == 0:
            return 0
        return 1

If our entire test suite consists of:

    def test_positive_number():
        assert sign(-1) == -1

then only three of the six lines in the function are actually being
tested:

    def sign(num):
        if num < 0:
            return -1
        if num == 0:
            return 0
        return 1

so the coverage is only 50%. If we add a second test:

    def test_zero():
        assert sign(0.0) == 0

the coverage goes to 83%, and if we add a third:

    def test_positive():
        assert sign(172891) > 0

the coverage reaches 100%.

Code coverage is often used as a rough indication of how well tested a
piece of software is—after all, if the coverage of a set of tests is
less than 100%, then some lines of code aren't being tested at all.
However, even 100% coverage doesn't guarantee that code has been
completely tested. To see why, consider the following code (adapted from
[this
example](http://nedbatchelder.com/blog/200710/flaws_in_coverage_measurement.html)):

~~~~ {src="src/quality/sensitivity.py"}
def sensitivity(alpha, beta):
    if alpha:
        factor = 0
    else:
        factor = 2

    if beta:
        result = 2.0/factor
    else:
        result = factor/2.0

    return result
~~~~

These three tests achieve 100% code coverage:

    def test_neither():
        assert sensitivity(False, False) == 1

    def test_alpha_only():
        assert sensitivity(True, False) == 0

    def test_beta_only():
        assert sensitivity(False, True) == 1

but `sensitivity(True, True)` still fails with a `ZeroDivisionError`.
The problem is that the tests don't achieve 100% [path
coverage](glossary.html#path-coverage): even though every line is
exercised at least once, there are paths through the code that aren't
ever taken ([Figure XXX](#f:path_coverage)).

![Line Coverage vs. Path Coverage](img/quality/path_coverage.png)

While code coverage isn't sufficient to show that everything has been
tested, it is still useful. In particular, looking at which lines have
and have not been exercised in a newly-written or modified piece of code
can help developers think of tests they should write. The simplest tool
to use for calculating coverage in Python is `coverage.py`. To see how
it works, suppose `sensitivity.py` contains the following:

~~~~ {src="src/quality/sensitivity.py"}
def sensitivity(alpha, beta):
    if alpha:
        factor = 0
    else:
        factor = 2

    if beta:
        result = 2.0/factor
    else:
        result = factor/2.0

    return result

assert sensitivity(False, False) == 1
assert sensitivity(True, False) == 0
~~~~

If we run the coverage tool from the shell using:

    $ coverage sensitivity.py

it creates a file called `.coverage` that records which lines were
executed. This file isn't text, so opening it in an editor isn't useful;
instead, to see what we did and didn't exercise, we run:

    $ coverage html

which creates a directory called `htmlcov`, inside which is a page
called `index.html`. When we open this in a browser, we see a summary of
the coverage statistics:

Module

statements

missing

excluded

coverage

Total

10

1

0

90%

sensitivity

10

1

0

90%

If we follow the link to `sensitivity.py`, we see:

> **Coverage for sensitivity : 90%**
>
> 10 statements 9 run 1 missing 0 excluded
>
>      1  def sensitivity(alpha, beta):
>      2      if alpha:
>      3          factor = 0
>      4      else:
>      5          factor = 2
>      6
>      7      if beta:
>      8          result = 2.0/factor
>      9      else:
>     10          result = factor/2.0
>     11
>     12      return result
>     13
>     14  assert sensitivity(False, False) == 1
>     15  assert sensitivity(True, False) == 0

which tells us that line 8 hasn't been run. It's up to us to figure out
why not, and what to do about it, but at least we now know what our
problem is.

### Summary

-   Use a coverage analyzer to see which parts of a program have been
    tested and which have not.

Debugging
---------

### Understand:

-   Why using `print` statements to debug is inefficient.
-   What a symbolic debugger is.
-   How to set a breakpoint in a debugger.
-   How to inspect values using a debugger.
-   How to debug programs systematically.

Programmers spend a lot of time debugging, so it's worth learning how to
do it systematically. We'll talk about tools first, since they'll make
everything else less painful. We'll then talk about some techniques.
Throughout, we'll assume that we built the right thing the wrong way;
requirements errors are actually a major cause of software project
failure, but they're out of scope for now.

When something goes wrong in a program like this:

~~~~ {src="src/quality/to_debug.py"}
import sys

def insert_or_increment(counts, species, number):
    # Look for species in list.
    for (s, n) in counts:
        # If we have seen it before, add to its count and exit.
        if s == species:
            n += number
            return
    # Haven't seen it before, so add it.
    counts.append([species, number])

source = open(sys.argv[1], 'r')
counts = []
for line in source:
    species, number = line.strip().split(',')
    insert_or_increment(counts, species, int(number))
counts.sort()
for (s, n) in counts:
    print '%s: %d' % (s, n)
~~~~

most people start debugging by adding `print` statements:

~~~~ {src="src/quality/debug_print.py"}
def insert_or_increment(counts, species, number):
    # Look for species in list.
    print 'insert_or_increment(', counts, ',', species, ',', number, ')'
    for (s, n) in counts:
        print '...checking against', s, n
        # If we have seen it before, add to its count and exit.
        if s == species:
            n += number
            print '...species matched, so returning with', counts
            return
    # Haven't seen it before, so add it.
    counts.append([species, number])
    print 'new species, so returning with', counts
~~~~

and then paging through output like this:

~~~~ {src="src/quality/debug_print.txt"}
insert_or_increment( [] , marlin , 5 )
new species, so returning with [['marlin', 5]]
insert_or_increment( [['marlin', 5]] , shark , 2 )
...checking against marlin 5
new species, so returning with [['marlin', 5], ['shark', 2]]
insert_or_increment( [['marlin', 5], ['shark', 2]] , marlin , 1 )
...checking against marlin 5
...species matched, so returning with [['marlin', 5], ['shark', 2]]
insert_or_increment( [['marlin', 5], ['shark', 2]] , turtle , 5 )
...checking against marlin 5
...checking against shark 2
new species, so returning with [['marlin', 5], ['shark', 2], ['turtle', 5]]
insert_or_increment( [['marlin', 5], ['shark', 2], ['turtle', 5]] , herring , 3 )
...checking against marlin 5
...checking against shark 2
...checking against turtle 5
new species, so returning with [['marlin', 5], ['shark', 2], ['turtle', 5], ['herring', 3]]
insert_or_increment( [['marlin', 5], ['shark', 2], ['turtle', 5], ['herring', 3]] , herring , 4 )
...checking against marlin 5
...checking against shark 2
...checking against turtle 5
...checking against herring 3
...species matched, so returning with [['marlin', 5], ['shark', 2], ['turtle', 5], ['herring', 3]]
insert_or_increment( [['marlin', 5], ['shark', 2], ['turtle', 5], ['herring', 3]] , marlin , 1 )
...checking against marlin 5
...species matched, so returning with [['marlin', 5], ['shark', 2], ['turtle', 5], ['herring', 3]]
herring: 3
marlin: 5
shark: 2
turtle: 5
~~~~

This works for small problems—i.e., it gives the programmer enough
insight into the problem to fix it—but it doesn't scale to larger
programs or harder problems. First, adding print statements is a good
way to add typos, particularly when we have to modify the block
structure of the program to fit them in. It's also time-consuming to
type things, delete them, type more in, and so on. It's especially
tedious if we're working in a language like C++, Fortran, or Java that
requires compilation. Finally, if we're printing lots of information,
it's all too easy to miss the crucial bit as it flies by on the screen.

A [debugger](glossary.html#debugger) is a program that controls the
execution of some [target
program](glossary.html#target-program)—typically, one that has a bug in
it that we're trying to track down. Debuggers are more properly called
*symbolic* debuggers because they show us the source code we wrote,
rather than raw machine instructions (although debuggers exists to do
that too). While the target program is running, the debugger can:

-   pause, resume, or restart it;
-   display or change values in it; and
-   watch for calls to particular functions or changes to particular
    variables.

Here's what a typical debugger looks like in action:

![A Debugger in Action](img/quality/debugger_screenshot.png)

The most important parts of this display are the source code window and
the call stack display. The former shows us where we are in the program;
the latter, what variables are in scope and what their values are. Most
debuggers also display whatever the target program has printed to
standard output recently.

We typically start a debugging session by setting a
[breakpoints](glossary.html#breakpoint) in the target program. This
tells the debugger to suspend the target program whenever it reaches
that line so that we can inspect the program's state. For example,
[Figure XXX](#f:debugger_screenshot) shows the state of the program when
adding four herrings to the list of species' counts. The program is
paused while it processes the first entry in the list to let us explore
our data and call stack, without having to modify the code in any way.
We can also use the debugger to:

-   [single-step](glossary.html#single-step), i.e., execute one
    statement at a time;
-   [step into](glossary.html#step-into) function calls;
-   [step over](glossary.html#step-over) them; or
-   run to the end of the current function.

This allows us to see how values are changing, which branches the
program is actually taking, which functions are actually being called,
and most importantly, why.

But debuggers can do much more than this. For example, most debuggers
let us move up and down the call stack, so that when our program is
halted, we can see the current values of variables in *any* active
function call, not just the one we're in.

Most debuggers also support [conditional
breakpoints](glossary.html#conditional-breakpoint), which only takes
effect if some condition is met. For example, we can set a breakpoint
inside a loop so that the target program only halts when the loop index
is greater than 100. This saves us having to step through 100
uninteresting iterations of the loop.

We can also use the debugger to modify values while the program is
running. For example, suppose we have a theory about why a bug is
occurring. We can run the target program to that point, change the value
of a particular variable, then resume the target program. This trick is
sometimes used to test out error-handling code, since it's easier to
change `time_spent_waiting` to 600 seconds in debugger than to pull out
the network cable and wait ten minutes…

### Post Mortem

Debuggers for compiled languages often support [post mortem
debugging](glossary.html#post-mortem-debugging). When a program fails
badly, it creates a [core dump](glossary.html#core-dump): a large file
containing a bitwise copy of everything that was in the program's
memory. A post-mortem debugger loads that memory image into the debugger
to see where it was and what state it was in when it failed. This isn't
as useful as watching it run, but sometimes the best you can do

Many people recommend using the scientific method to debug programs
(e.g., David Agans' book [Debugging](bib.html#agans-debugging)). In
practice, though, most programmers don't do this. Instead, what
[Lawrance and colleagues](bib.html#lawrance-debug-foraging) found is
that they forage for information by reading the code and (re-)running
the program to build up a mental model of what it's doing until they see
where the bug is, then make a change and see if it has the desired
effect.

No matter how we think of it, systematic (i.e., productive) debugging
follows a few simple rules. First, *try to get it right the first time*,
since the simplest bugs to fix are the ones that don't exist. Most of
the techniques we have discussed in this chapter, such as defensive
programming and test-driven development, are meant to accomplish this.

Second, make sure that we *know what the program is supposed to do*. If
we don't know that the output or behavior is supposed to be, we can't
even be sure there *is* a bug, much less whether we've fixed it.

### Extrapolation is the Root of Many Evils

If the case is covered by a test case, then we're in good shape; if it
isn't, we need to ask whether we actually know enough to create that
test case. In particular, if this situation isn't covered by the
formulas we're trying to implement, or whatever other specification
we've been given, we need to ask whether we have the right to
extrapolate and fill in the blank.

Third, *make sure it's plugged in*, i.e., make sure we're actually
exercising the problem that we think we are. Are we giving it the right
test data? Is it configured the way we think it is? Is it the version we
think it is? Has the feature that's "failing" actually been implemented
yet? It's very easy—particularly when we're tired or frustrated—to spend
hours trying to debug a failure that doesn't actually exist.

The next rule of debugging is *make it fail reliably*. We can only debug
things when they go wrong; if we can't find a test case that fails every
time, we're going to waste a lot of time watching the program *not*
fail.

What if we can't make it fail reliably? What if the problem involves
timing, random numbers, network load, or something we just haven't
figured out yet? In that case, we should apply rule number four: *divide
and conquer*. The smaller the gap between cause and effect, the easier
the relationship is to see, so once we have a case that fails, we should
try to simplify it so that we have less of the program to worry about.

If we can simplify the failure by using smaller or simpler input,
without modifying our program, we should do so. If we have to modify the
program, the best way is to start adding assertions. Does the failure
first show up in function X? If so, add an assertion at the start of the
function to make sure its inputs are valid. If they aren't, add
assertions at the start of the functions that call X, and so on. This is
a good way to stop ourselves from introducing new bugs as you fix old
ones, since we can leave those assertions in the code forever if we
want.

The corollary to rule number 4 is rule number 5: *change one thing at a
time*. The more things we change at once, the harder it is to keep track
of what we've done and what effect it had. Every time we make a change,
even a small one, we should re-run all of our tests immediately.

Finally, the most important rule is *be humble*. Don't keep telling
yourself why it *should* work: if it doesn't, it doesn't. And don't be
too proud to ask for help: if you can't find the problem in 15 minutes,
ask someone rather than spending another hour banging your head against
a wall.

### Summary

-   Use an interactive symbolic debugger instead of `print` statements
    to diagnose problems.
-   Set breakpoints to halt the program at interesting points instead of
    stepping through execution.
-   Try to get things right the first time.
-   Make sure you know what the program is supposed to do before trying
    to debug it.
-   Make sure the program is actually running the test case you think it
    is.
-   Make the program fail reliably.
-   Simplify the test case or the program in order to localize the
    problem.
-   Change one thing at a time.
-   Be humble.

Designing Testable Code
-----------------------

### Understand:

-   The difference between interface and implementation.
-   Why testing should focus on interfaces rather than implementations.
-   Why and how to replace software components with simplified versions
    of themselves during testing.

One of the most important ideas in computing is the difference between
*interface* and *implementation*. Something's
[interface](glossary.html#interface) specifies how it interacts with the
world: what it will accept as input, and what output it produces. Again,
it's like a contract in business: if Party A does X, then Party B
guarantees Y.

Something's [implementation](glossary.html#implementation) is how it
accomplishes whatever it does. This might involve calculation, database
lookups, or anything else. The key is, it's hidden inside the thing: how
it does what it does is nobody else's business. For example, here's an
outline for a Python function that integrates a function of one variable
over a certain interval:

    def integrate(func, x1, x2):
        ...math goes here...
        return result

Its interface is simple: given a function and the low and high bounds on
the interval, it returns the appropriate integral. A fuller definition
of its interface would also specify how it behaves when it's given bad
parameters, error bounds on the result, and so on.

Its implementation could use any of a dozen algorithms. In fact, its
implementation could change over time as new algorithms are developed.
As long as its contract with the outside world stays the same, none of
the programs that use it should need to change. This allows users to
concentrate on their tasks, while giving whoever wrote this function the
freedom to tweak it without making work for other people.

We often use this idea—the separation between interface and
implementation—to simplify unit testing. The goal of unit testing is to
test the components of a program one by one—that's why it's called
"unit" testing. But the components in real programs almost always depend
on each other: this function calls that one, this data structure refers
to the one over there, and so on. How can we isolate the component under
test from the rest of the program so that we can test it on its own?

One technique is to replace the components we're *not* currently testing
with simplified versions that have the same interfaces, but much simpler
implementations, just as a director would use a stand-in rather than a
star when fiddling with the lighting for a show. Doing this for programs
that have already been written sometimes requires some reorganization,
or [refactoring](glossary.html#refactor). But once we understand the
technique, we can build programs with it in mind to make testing easier.

Let's go back to our photographs of fields in Saskatchewan. We want to
test a function that reads a photo from a file. (Remember that a photo
is just a set of rectangles.) Here's a plausible outline of the
function:

    def read_photo(filename):
        result = set()
        reader = open(filename, 'r')
        ...fill result with rectangles in file...
        reader.close()
        return result

It creates a set to hold the rectangles making up the photo, opens a
file, and then reads rectangles from the file and puts them in the set.
When the input is exhausted, the function closes the file and returns
the set.

Here is a unit test for that function that reads data from a file called
`unit.pht`, then checks that the result is a set containing exactly one
rectangle:

    def test_photo_containing_only_unit():
        assert read_photo('unit.pht') == { ((0, 0), (1, 1)) }

This is pretty straightforward, but experience teaches us that it's a
bad way to organize things. First, this test depends on an external
file, and on that file being in exactly the right place. Over time,
files can be lost, or moved around, which makes tests that depend on
them break.

Second, it's hard to understand a test if the fixture it depends on
isn't right there with it. Yes, it's easy to open the file and read it,
but every bit of extra effort is a bit less testing people will actually
do.

Third, file I/O is slower than doing things in memory—tens or hundreds
of thousands of times slower. If your program has hundreds of tests, and
each one takes a second to run, developers will have to wait several
minutes to find out whether their latest change has broken anything that
used to work. The most likely result is that they'll run the tests much
less frequently, which means they'll waste more time backtracking to
find and fix bugs that could have been caught when they were fresh if
the tests only took seconds to run.

Here's how to fix this. Imagine for a moment that instead of reading
rectangles, we're just counting them:

    def count_rect(filename):
        reader = open(filename, 'r')
        count = 0
        for line in reader:
            count += 1
        reader.close()
        return count

This simple function assumes the file contains one rectangle per line,
with no blank lines or comments. (Of course, a real rectangle counting
function would probably be more sophisticated, but this is enough to
illustrate our point.) Here's the function after refactoring:

    def count_rect_in(reader):
        count = 0
        for line in reader:
            count += 1
        return count

    def count_rect(filename):
        reader = open(filename, 'r')
        result = count_rect_in(reader)
        reader.close()
        return result

We've taken the inner core of the original function and made it a
function in its own right. This new function does the actual work—i.e.,
it counts rectangles—but it does *not* open the file that the rectangles
are read from. That's still done by the original function. It opens the
input file, calls the new function that we extracted, then closes the
file and returns the result. Notice that this function keeps the name of
the original function, so that any program that used to call
`count_rect` can still do so.

Now let's write some tests:

    from StringIO import StringIO

    Data = '''0 0 1 1
    1 0 2 1
    2 0 3 1'''

    def test_num_rect():
        reader = StringIO(Data)
        assert count_rect_in(reader) == 3

This piece of code checks that `count_rect_in`—the function that
actually does the hard work—handles the three-rectangle case properly.
But instead of an external file, we're using a string in the test
program as a fixture.

To make this string look like a file, we're relying on a Python class
called `StringIO`. As the name suggests, this acts like a file, but uses
a string instead of the disk for storing data. `StringIO` has all the
same methods as a file, like `readline`, so `count_rect_in` doesn't know
that it isn't reading from a real file on disk.

We can use this same trick to test functions that are supposed to write
to files as well. For example, here's a unit test to check that another
function, `photo_write_to`, can correctly write out a photo containing
only the unit square:

    def test_write_unit_only():
        fixture = { ((0, 0), (1, 1)) }
        writer = StringIO()
        photo_write_to(fixture, writer)
        result = writer.getvalue()
        assert result == '0 0 1 1\n'

Once again, we create a `StringIO` and pass that to the function instead
of an actual open file. If `photo_write_to` only writes to the file
using the methods that real files provide, it won't know that it's been
passed something else. And once we're finished writing, we can call
`getvalue` to get the text that we wrote, and check it to make sure it's
what it's supposed to be.

In order to make output testable, though, there's one more thing we have
to do. Here's a possible implementation of `photo_write_to`:

    def photo_write_to(photo, writer):
        contents = list(photo)
        contents.sort()
        for rect in contents:
            print >> writer, rect[0][0], rect[0][1],
                             rect[1][0], rect[1][1]

It puts the rectangles in the photo into a list, sorts that list, then
writes the rectangles one by one. Why do the extra work of sorting? Why
not just loop over the set and write the rectangles out directly?

Let's work backwards to the answer. This version of `photo_write_to` is
shorter and faster than the previous one:

    def photo_write_to(photo, writer):
        contents = list(photo)
        for rect in contents:
            print >> writer, rect[0][0], rect[0][1],
                             rect[1][0], rect[1][1]

However, there is no way to predict its output for any photo that
contains two or more rectangles. For example, here are two fields of
corn ready for harvest:

![Corn Fields](img/quality/cornfields.png)

And here are two lines of Python that we might put in a unit test to
represent the photo, and write it to a file or a `StringIO`:

    two_fields = { ((0, 0), (1, 1)), ((1, 0), (2, 1)) }
    photo_write(two_fields, ...)

The function's output might look like this:

    0 0 1 1
    1 0 2 1

but it could equally well look like this, with the rectangles in reverse
order:

    1 0 2 1
    0 0 1 1

because sets are stored in an arbitrary order that is under the
computer's control. Since we don't know what that order is, we can't
predict the output if we loop over the set directly, which means we
don't know what to compare the output to. If we sort the rectangles, on
the other hand, they'll always be in the same order, and to sort them,
we have to put them in a list first.

One final lesson for this section: you probably haven't noticed, but the
tests we've written in this episode are inconsistent. Here's the fake
"file" we created for testing the photo-reading function:

    Data = '''0 0 1 1
    1 0 2 1
    2 0 3 1'''

And here's the string we used to check the output of our photo-writing
function:

    def test_write_unit_only():
        fixture = { ((0, 0), (1, 1)) }
        ...
        assert result == '0 0 1 1\n'

Notice that one string has a newline at the end and the other doesn't.
It doesn't matter whether we require this or not—either convention is
better than saying "maybe", because if we allow both, our code becomes
more complicated, and more testing will be required.

Stepping back, the most important lesson in this section isn't how to
test functions that do I/O. The most important idea is that we should
design our programs so that their components can be tested. To do this,
we should depend on interfaces, not implementations: on the contracts
that functions provide, not on the details of how they accomplish
whatever they do.

Following this rule will make it easy for us to replace components that
you're *not* currently testing with simplified versions to make it
easier to test the ones you *are* interested in. It will also save us
from writing your tests over and over as the internals of the functions
you are testing are changed. Interfaces are longer-lived than
implementations: if you rely on the former rather than the latter,
you'll spend less time rewriting tests, and more time figuring out what
effect climate change is having on fields in Saskatchewan.

Another rule when you're designing programs to be testable is to isolate
interactions with the outside world. For example, code that opens file
should be separated from code that reads data, so that you can test the
latter without needing to do the former. Finally, you should make the
things you are going to examine to check the result of a test
deterministic, i.e., the result of a particular function call should
always be exactly the same value, so that you can compare it directly to
the expected result. Unfortunately, this last rule can sometimes be hard
to follow in scientific programs because of floating-point
approximations.

### Summary

-   Separating interface from implementation makes code easier to test
    and re-use.
-   Replace some components with simplified versions of themselves in
    order to simplify testing of other components.
-   Do not create arbitrary, variable, or random results, as they are
    extremely hard to test.
-   Isolate interactions with the outside world when writing tests.

Summing Up
----------

It's pretty obvious that if we want to be sure our programs are right,
we need to put in some effort. What isn't so obvious is that focusing on
quality is also the best way—in fact, the *only* way—to improve
productivity as well. Getting something wrong and then fixing it almost
always takes longer than getting it right in the first place. (As some
people are fond of saying, a week of hard work can sometimes save you an
hour of thought.) Designing testable code, practicing defensive
programming, writing and running tests, and thinking about what the
right answer is supposed to be all help get us answers faster, as well
as ones that are more likely to be correct.
