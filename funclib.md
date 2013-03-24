Functions and Libraries in Python
=================================

On the first day of your post-doc at Euphoric State University, your
supervisor calls you into her office to ask a favor. One of her previous
students wrote a program to reformat and calibrate data produced by rock
drills in the 1970s and 1990s. It's a useful piece of code, but she is
now studying fossilized coral reefs, so she would like you to figure out
how that program works and add some new features to it.

The good news is, the program is only two hundred lines long. The bad
news is, it's one big block of code, and several sections seem to be
duplicated. Before you can start adding anything new, you need to clean
it up.

This chapter will show you how to do that, and along the way introduce
the single most powerful idea in programming: abstraction. No
programming language can possibly include everything that anyone might
ever want (though that hasn't stopped C++ and Perl from trying…).
Instead, languages should make it easy for people to create new tools to
solve their specific problems, and the most common way to do this is to
define [functions](glossary.html#function) that combine several
operations into one. In this chapter, we'll look at how functions work,
and how to divide tasks into comprehensible, reusable chunks.

How Functions Work
------------------

### Understand:

-   Why to break a program up into functions.
-   How to define a new function.
-   How to pass values into a function.
-   How to combine functions.
-   What a call stack is.
-   What a variable's scope is.

As we said above, a function's job is to bundle several steps together
so that they can be used as if they were a single command. The simplest
possible function is one that just produces the same value over and over
again:

~~~~ {src="src/funclib/zero.py"}
def zero():
    return 0

result = zero()
print "zero produces", result
zero produces 0
~~~~

This function is pretty pointless, but it does illustrate a few things.
First, we create functions in Python using the keyword `def`, followed
by the function's name. The empty parentheses signal that the function
doesn't take any inputs—we'll see functions that do in a moment—and the
colon signals the start of a new block of code. The body of the function
is then indented, just like the body of a loop. The keyword `return`
then specifies the value that the function produces.

We have seen lots of examples already of calling functions, so the third
line of code should look familiar: when Python sees the statement
`result = zero()` it sets aside whatever it was doing, goes and does
whatever the function `zero` tells it to do, and then continues with its
original calculation using the function's result. In this case, the
overall effect is to assign 0 to `result`, which is then printed.

Functions that always produce the same value aren't particularly useful,
so most functions take input values, or
[parameters](glossary.html#parameter), and use them in their
calculations. For example, the function `fahr_to_kelvin` takes a
temperature in Fahrenheit (as recorded by rock drills in the 1970s) and
returns the corresponding temperature in Kelvin:

~~~~ {src="src/funclib/f2k.py"}
def fahr_to_kelvin(temp):
    return ((temp - 32.0) * 5.0/9.0) + 273.15

print 'water freezes at', fahr_to_kelvin(32)
print 'water boils at', fahr_to_kelvin(212)
water freezes at 273.15
water boils at 373.15
~~~~

When we call `fahr_to_kelvin`, the value we pass in (such as `32` or
`212`) is assigned to the variable `temp`, which is the function's only
parameter. The function uses that value in its calculations, and returns
a result as before.

If one function is good, two must be better. Let's write a function to
convert Kelvin to Celsius:

~~~~ {src="src/funclib/k2c.py"}
def kelvin_to_celsius(temp):
    return temp - 273.15

print 'absolute zero is', kelvin_to_celsius(0)
absolute zero is -273.15
~~~~

Instead of writing a third equation to translate Fahrenheit into
Celsius, we can now combine the two functions we have to do the required
calculation:

~~~~ {src="src/funclib/f2c.py"}
def fahr_to_celsius(temp):
    degrees_k = fahr_to_kelvin(temp)
    return kelvin_to_celsius(degrees_k)

temp_f = 32.0
temp_c = fahr_to_celsius(temp_f)
print 'water freezes at', temp_c
water freezes at 0.0
~~~~

To really understand what happens when we combine functions this way, we
need to understand the [function call stack](glossary.html#call-stack),
or "stack" for short. Here are the function definitions once again:

~~~~ {src="src/funclib/f2c.py"}
def fahr_to_kelvin(temp):
    return ((temp - 32.0) * 5.0/9.0) + 273.15

def kelvin_to_celsius(temp):
    return temp - 273.15

def fahr_to_celsius(temp):
    degrees_k = fahr_to_kelvin(temp)
    return kelvin_to_celsius(degrees_k)
~~~~

All three functions have a parameter called `temp`. Let's try calling
one of the functions, and then printing `temp`'s value *after* the
function call:

~~~~ {src="src/funclib/print_temp.py"}
def kelvin_to_celsius(temp):
    return temp - 273.15

absolute_zero = 0.0
not_used = kelvin_to_celsius(absolute_zero)
print 'temp after function call is', temp
temp after function call is
Traceback (most recent call last):
  File "src/funclib/print-temp.py", line 5, in <module>
    print 'temp after function call is', temp
NameError: name 'temp' is not defined
~~~~

Why isn't `temp` defined? And if it isn't, why did we get an error for
the last line of our program, rather than when we used `temp` inside
`kelvin_to_celsius`?

The answer is that Python doesn't actually create a variable called
`temp` when the function is defined. Instead, it makes a note that it is
supposed to create such a variable when `kelvin_to_celsius` is called,
and then throw it away when the function finishes executing.

This is easier to explain with pictures. After executing line 4 of our
program, Python knows that `kelvin_to_celsius` refers to a function, and
that `absolute_zero` refers to the value 0.0:

![First Step of Function Call](img/funclib/func_call_step_1.png)

The first thing it does when it executes line 5 is call
`kelvin_to_celsius`. To do this, it creates a new storage area for
variables and puts it on top of the one that holds `kelvin_to_celsius`
and `absolute_zero`. Since the function has one parameter, `temp`,
Python creates a variable with that name in the new storage area, and
gives it the value 0.0 (since that's what we passed in when we called
the function):

![Second Step of Function Call](img/funclib/func_call_step_2.png)

This variable storage area is called a [stack
frame](glossary.html#stack-frame): stack, because it is stacked on top
of the previous area, and frame, because…well, just because. Every time
a function is called—any function—Python creates a new frame to holds
the function's variables and puts it on top of the stack. While it is
executing that function's code, Python looks in the top stack frame to
find variables; when the function returns, Python discards the top stack
frame and starts using the one underneath it again.

Since the rest of the statement on line 5 (the line containing the
function call) assigns the function's value to `not_used`, memory looks
something like this after line 5 is finished:

![Third Step of Function Call](img/funclib/func_call_step_3.png)

It should now be clear why we got the error we did, and why we got it
*where* we did. When Python executes line 6, the uppermost frame of the
stack doesn't contain a variable called `temp`. The frame that *did*
contain that variable was discarded when the call to `kelvin_to_celsius`
finished.

To understand why Python (and other languages) do all of this, let's go
back to `fahr_to_celsius` again. Its definition, and the definitions of
the functions it calls, are:

~~~~ {src="src/funclib/f2c.py"}
def fahr_to_kelvin(temp):
    return ((temp - 32.0) * 5.0/9.0) + 273.15

def kelvin_to_celsius(temp):
    return temp - 273.15

def fahr_to_celsius(temp):
    degrees_k = fahr_to_kelvin(temp)
    return kelvin_to_celsius(degrees_k)
~~~~

These nine lines of code define the variable `temp` three times—once in
each function—but those three `temp`s are *not* the same variable. The
first `temp`, defined on line 1, is created each time `fahr_to_kelvin`
is called, and only lasts as long as that call is in progress. In
computer science jargon, it is [local](glossary.html#local-scope) to the
function. Similarly, the second `temp` (on line 4) is local to
`kelvin_to_celsius`, and the third (on line 7) to `fahr_to_celsius`.
They only exist while the functions that own them are being executed,
and can only be "seen" inside those functions.

Again, some pictures will make this clearer (and it does need to be
clear, since everything else about functions depends on this idea).
Let's call `fahr_to_celsius` as before:

~~~~ {src="src/funclib/f2c.py"}
temp_f = 32.0
temp_c = fahr_to_celsius(temp_f)
print 'water freezes at', temp_c
~~~~

Just before line 9 runs, the stack consists of a single frame, which
contains the three functions and the variable `temp_f`:

![A Call Stack With a Single Frame](img/funclib/stack_single_frame.png)

When we call `fahr_to_celsius`, Python creates a new stack frame
containing the variable `temp`, and assigns it the value 32.0 (which it
got from `temp_f`):

![A New Stack Frame](img/funclib/stack_double_frame.png)

`fahr_to_celsius` immediately calls `fahr_to_kelvin`, so Python creates
another stack frame to hold `fahr_to_kelvin`'s local variables. This
frame also contains a variable called `temp`, but since it's in a
different frame, it's a different variable than `fahr_to_celsius`'s
`temp`:

![Yet Another Stack Frame](img/funclib/stack_triple_frame.png)

Using its `temp`, `fahr_to_kelvin` calculates a result of 273.15. When
it returns that value, Python discards `fahr_to_kelvin`'s stack frame:

![Back to a Double Frame](img/funclib/stack_back_to_double_frame.png)

and creates a new variable `degrees_k` to hold that value in what is now
the top frame—the one belonging to `fahr_to_celsius`:

![A New Variable in the Second
Frame](img/funclib/new_variable_in_double_frame.png)

Python then goes through the same steps for the call to
`kelvin_to_celsius`. It creates a stack frame with a variable `temp`,
which it assigns the value 273.15:

![Repeating the Process](img/funclib/repeat_stack_frame.png)

does its calculations, and then discards the stack frame when the
function is finished. Since `fahr_to_celsius` is also now done, Python
discards its stack frame, creates a variable called `temp_c` in the
original (bottom) frame, and assigns it the value 0.0:

![The Final State](img/funclib/final_state_of_frames.png)

Every modern programming language uses this model to manage
calculations. Each function call creates a new stack frame with its own
variables. While the function is running, it uses the variables in its
own frame, and when the function call is finished, the stack frame is
discarded.

The area of the program in which a particular variable is visible is
called its [scope](glossary.html#scope). As a rule, programming
languages do not let functions access variables in other functions'
scopes because doing so would make large programs almost impossible to
write. For example, imagine we used two functions to sum the squares of
the values in a list:

~~~~ {src="src/funclib/sum_squares.py"}
def sum(numbers):                       #  1
    result = 0                          #  2
    for x in numbers:                   #  3
        result = result + square(x)     #  4
    return result                       #  5
                                        #  6
def square(val):                        #  7
    result = val * val                  #  8
    return result                       #  9
                                        # 10
print sum([1, 2])                       # 11
~~~~

We expect to get 1^2^+2^2^ = 5 via the following steps:

`sum`

`sum`

`square`

`square`

Line

`result`

`x`

`val`

`result`

2

0

3

0

1

7

0

1

1

8

0

1

1

1

4

1

1

3

1

2

7

1

2

2

8

1

2

2

4

4

1

5

5

1

5

If `sum`'s `result` and `square`'s `result` were the same variable,
though, we would get 8 instead:

  Line   `result`   `x`   `val`
  ------ ---------- ----- -------
  2      0                
  3      0          1     
  7      0          1     1
  8      1          1     1
  4      2          1     
  3      2          2     
  7      2          2     2
  8      4          2     2
  4      8          2     
  5      8          2     

What's worse, if we changed the name of the variable in `square` from
`result` to `y`, the final answer would be 5 again. Changing the name of
a variable shouldn't matter: *f(x)=x^2^* and *f(y)=y^2^* ought to
calculate the same value, and if changing a variable name in one part of
our program can change the result calculated by another, we will have to
keep the entire program in our head in order to make any change safely.

The fundamental issue here is one of evolution rather than one of
technology. Human short-term memory can only hold a few items at a time;
the value is sometimes given as "seven plus or minus two", and while
that is an over-simplification, it's a good guideline. If we need to
remember more unrelated bits of information than that for more than a
few seconds, they become jumbled and we start making mistakes.

If we have to keep more than half a dozen things straight in our mind in
order to understand or change a piece of code, we will therefore start
making mistakes. Most programming languages therefore enforce a "local
scope only" rule so that programmers can ignore what's inside the
functions they are calling, or what's outside the functions they are
writing, and use their short-term memory for the task at hand instead.

### Summary

-   Define a function using `def name(...)`
-   The body of a function must be indented.
-   Use `name(...)` to call a function.
-   Use `return` to return a value from a function.
-   The values passed into a function are assigned to its parameters in
    left-to-right order.
-   Function calls are recorded on a call stack.
-   Every function call creates a new stack frame.
-   The variables in a stack frame are discarded when the function call
    completes.
-   Grouping operations in functions makes code easier to understand and
    re-use.

Global Variables
----------------

### Understand:

-   What global scope is.
-   Why functions shouldn't communicate via global variables.

There is one important pragmatic exception to the "local scope only"
rule. Every function also has access to the [global
scope](glossary.html#global-scope), which is all the top-level
definitions in the program (i.e., ones that aren't inside any particular
function). In our pictures, the global scope is the bottom-most frame on
the stack, which is there when the program starts and never goes away.

Functions need access to the global scope because that is where other
functions are defined. Going back to our temperature calculator, if
`fahr_to_celsius` could only see variables defined in its local scope,
it wouldn't be able to see either `fahr_to_kelvin` or
`kelvin_to_celsius`, and therefore wouldn't be able to call them.

Programmers also usually put constants at the top level of their program
(i.e., define them in the global scope) so that they don't need to pass
them into functions. For example, it's common to see code like this:

~~~~ {src="src/funclib/constant.py"}
SCALING = 2.5

def scale_up(x):
    return x * SCALING

def scale_down(x):
    return x / SCALING
~~~~

(Many programmers write constants' names in upper case as a cue to
readers, but Python doesn't enforce this.) When Python executes
`scale_up` (or `scale_down`), it looks inside that function's scope for
a variable called `SCALING`. Since there isn't one, it then checks the
global scope, where it finds what it needs:

![Searching Scopes](img/funclib/searching_scopes.png)

Defining `SCALING` once at the top of the program ensures that both
functions always use the same scaling factor; this code has the same
effect:

~~~~ {src="src/funclib/constant_duplicated.py"}
def scale_up(x):
    return x * 2.5

def scale_down(x):
    return x / 2.5
~~~~

but it would be very easy for a programmer to change the scaling factor
in one function and forget to change it in the other.

Putting constants in the global scope is good style, but the following
is definitely not:

~~~~ {src="src/funclib/badglobal.py"}
largest = 0

def fixup(values):
    global largest
    for i in range(len(values)):
        if values[i] < 0.0:
            values[i] = 0.0
        if values[i] > largest:
            largest = values[i]

def scale(values):
    for i in range(len(values)):
        values[i] = values[i] / largest
~~~~

Here, the function `fixup` puts the largest value it has seen in a
global variable called `largest`, which the function `scale` then uses.

### The `global` Statement

Since we actually assign a value to `largest` inside `fixup`, instead of
just reading its value, we have to tell Python that we want to use the
global variable `largest` rather than creating one inside the function
(which is what it would do by default); this is why we need the
statement:

        global largest

at the top of the function.

Using a global variable to move information from one function to another
works fine in simple cases:

~~~~ {src="src/funclib/badglobal.py"}
rows = [1.0, 4.0, -2.5, 3.5]
fixup(rows)
scale(rows)
print rows
[0.25, 1.0, 0.0, 0.875]
~~~~

but look what happens when we start working with multiple data sets:

~~~~ {src="src/funclib/badglobal.py"}
columns = [1.5, 1.5, -2.0, 3.0]
fixup(columns)
scale(columns)
print columns
[0.375, 0.375, 0.0, 0.75]
~~~~

If we actually want each data set fixed up and scaled separately, the
answer for `columns` should be `[0.5, 0.5, 0.0, 1.0]`. The problem is
that the values in `columns` are actually being scaled by the largest
value found in `rows`. Bugs like this, which are caused by [side
effects](glossary.html#side-effect) that aren't visible in either the
functions' definitions or calls, are notoriously difficult to track
down. In fact, one of the reasons Python requires us to use the `global`
statement in `fixup` is to make the use of global variables more
obvious, and to discourage us from doing so.

### Summary

-   Every function always has access to variables defined in the global
    scope.
-   Programmers often write constants' names in upper case to make their
    intention easier to recognize.
-   Functions should *not* communicate by modifying global variables.

Multiple Arguments
------------------

### Understand:

-   How to pass multiple values into a function.
-   How and why to specify default values for parameters.

The functions we have seen so far have had only one parameter. When we
define a function, however, we can give it any number of parameters.
When the function is called and a new stack frame is created, a new
variable is defined for each of those parameters, and the actual values
given by the caller are assigned to the parameters in order from left to
right. For example, if we define `average3` to calculate the average of
three numbers:

~~~~ {src="src/funclib/average_3.py"}
def average3(a, b, c):
    return (a + b + c) / 3.0
~~~~

and call it like this:

~~~~ {src="src/funclib/average_3.py"}
x = 2
y = 2
z = 5
print average3(x, y, z)
3.0
~~~~

then just before the function returns, the program's memory looks like
this:

![State of Memory Before Function
Return](img/funclib/memory_before_return.png)

Calling a function with the wrong number of values is an error:

~~~~ {src="src/funclib/average_3_wrong.py"}
print average3(1, 5)
Traceback (most recent call last):
  File "src/funclib/average-3-wrong.py", line 4, in <module>
    print 1, 5, '=>', average3(1, 5)
TypeError: average3() takes exactly 3 arguments (2 given)
~~~~

This is only sensible: if we pass two values to `average3`, Python has
no way of knowing what third value to use. We can tell it what we want
by specifying [default values](glossary.html#default-value) for
parameters:

~~~~ {src="src/funclib/average_3_default.py"}
def average3(a=0.0, b=0.0, c=0.0):
    return (a + b + c) / 3.0
~~~~

The meaning is straightforward: if the caller doesn't tell the function
what value to use for `a`, the function should use 0.0, and similarly
for the other parameters. We can now call our function in four different
ways:

~~~~ {src="src/funclib/average_3_default.py"}
print '()', average3()
print '(1.0)', average3(1.0)
print '(1.0, 2.0)', average3(1.0, 2.0)
print '(1.0, 2.0, 5.0)', average3(1.0, 2.0, 5.0)
() 0.0
(1.0) 0.333333333333
(1.0, 2.0) 1.0
(1.0, 2.0, 5.0) 2.66666666667
~~~~

We still can't call this function with more than three parameters,
though, since once again Python wouldn't know where to put the fourth
and higher.

Allowing people to call `average3` with fewer than three values isn't
actually very useful. What *is* useful is using sensible defaults to
save ourselves from writing several slightly-different versions of a
function. For example, suppose we need a function that averages a list
of numbers. The obvious solution is:

~~~~ {src="src/funclib/average_list_simple.py"}
def average_list(values):
    result = 0.0
    for v in values:
        result += v
    return result / len(values)

for test in [[1.0], [1.0, 2.0], [1.0, 2.0, 5.0]]:
    print test, '=>', average_list(test)
[1.0] => 1.0
[1.0, 2.0] => 1.5
[1.0, 2.0, 5.0] => 2.66666666667
~~~~

Before we go on, notice that there is a bug in this function: if it is
called for an empty list, the expression `result / len(values)` try to
divide by zero. We will look at how to handle this case
[below](#p:average-none).

Now suppose that we want to be able to calculate averages for parts of
our data instead of always calculating the average for the whole data
set. One way would be to require the caller to slice the list: has
slicing been introduced?

    a = average_list(values[20:90])

but another would be to allow them to tell `average_list` what range to
use. This is what most list and string methods do: if they are passed
one value, they work from that index to the end of the data, while if
they are passed two, they work on the range those indices delimit. For
example, the string method `str.count` can be called three ways:

  ---------------------------------------- --------
  Call                                     Result
  `'This is his DNA.'.count('is')`         3
  `'This is his DNA.'.count('is', 4)`      2
  `'This is his DNA.'.count('is', 4, 8)`   1
  ---------------------------------------- --------

Here's how to do this ourselves:

~~~~ {src="src/funclib/average_with_defaults.py"}
def average_list(values, start=0, end=None):
    if end is None:
        end = len(values)
    result = 0.0
    i = start
    while i < end:
        result += values[i]
        i += 1
    return result / (end - start)
~~~~

If `average_list` is called with three values, they will be assigned to
`values`, `start`, and `end`, which gives the caller complete control
over the function's behavior. If it is called with just two parameters,
then `end` will have the value `None`. The initial `if` statement will
spot this case and re-set `end` to the length of `values` so that the
loop that does the averaging will run correctly. And if `average_list`
is called with just one value, `start` will have the value 0, which is
what we want it to be to start the loop with the first element of the
list. (In this case, `end` will again be `None`, so it will be re-set as
before.) Here's what our function looks like in action:

~~~~ {src="src/funclib/average_with_defaults.py"}
numbers = [1.0, 2.0, 5.0]
print '(', numbers, ') =>', average_list(numbers)
print '(', numbers, 1, ') =>', average_list(numbers, 1)
print '(', numbers, 1, 2, ') =>', average_list(numbers, 1, 2)
( [1.0, 2.0, 5.0] ) => 2.66666666667
( [1.0, 2.0, 5.0] 1 ) => 3.5
( [1.0, 2.0, 5.0] 1 2 ) => 2.0
~~~~

![Calls With Defaults](img/funclib/calls_with_defaults.png)

### How Older Languages Do It

If the language we are using doesn't let us define default parameter
values, we could turn our function into three:

~~~~ {src="src/funclib/average_without_defaults.py"}
def average_list_range(values, start, end):
    result = 0.0
    i = start
    while i < end:
        result += values[i]
        i += 1
    return result / (end - start)

def average_list_from(values, start):
    return average_list_range(values, start, len(values))

def average_list_all(values):
    return average_list_range(values, 0, len(values))
~~~~

This is a very common [design pattern](glossary.html#design-pattern) in
many programming languages. We start by defining the most general
function we can think of—in this case, one that work on a
fully-specified range—and then write [wrapper
functions](glossary.html#wrapper-function) as easy-to-use shortcuts for
common cases. These wrapper functions do *not* duplicate what's in the
general function; instead, they call it, filling in some or all of the
parameters it requires with sensible defaults.

The problem with this approach is that we have to come up with names for
all those little functions. Default parameters were invented to solve
this problem: instead of writing lots of functions, we write one, and
provide default values for some or all of its parameters.

One restriction on functions with default values is that all of the
parameters that have default values must come *after* all of the
parameters that don't. To see why, imagine we were allowed to mix
defaulting and non-defaulting parameters like this:

~~~~ {src="src/funclib/average_with_defaults_wrong.py"}
def average_list(start=None, values, end=None):
    if start is None:
        start = 0
    if end is None:
        end = len(values)
    result = 0.0
    i = start
    while i < end:
        result += values[i]
        i += 1
    return result / (end - start)
~~~~

If we call the function with just one parameter, it's pretty clear that
its value has to be assigned to `values`. But what should Python do if
the function is called with two parameters, like
`average_list([1.0, 2.0, 5.0], 1)`? Should it use the provided values
for the first and second parameters, and the default for the third? Or
should it use the first parameter's default, and assign the given values
to the second and third? We know what we want, but Python doesn't:
remember, it can't infer anything from variables' names. We could define
some sort of rule to tell it what to do in this case, but it's simpler
and safer to disallow the problem in the first place. This is why
methods like `str.count` take parameters in [the order they
do](#a:string-count): the more likely a parameter is to be changed, the
closer to the front of the parameter list it should be.

Now let's go back and figure out what the average of an empty list
should be. Broadly speaking, there are three possibilities:

1.  Return 0.0 or some other number.
2.  Return some other value, such as `None`.
3.  Treat this as an error, i.e., let the divide-by-zero error happen.

Many people pick the first option (some even arguing that since zero is
the average of all possible numbers, it's the only sensible choice). The
danger of doing this is that it might mask errors in code. For example,
if a file-reading function has a bug in it, and returns an empty list
instead of a list of numbers, we'd really like our program to report an
error [as soon as possible](quality.html#s:defensive). If `average_list`
absorbs an error instead of failing, the user may not realize something
has gone wrong until millions of instructions later, which makes
debugging harder.

The second option—returning a non-numerical value—is almost always a
worse choice, because it complicates the calling code. People want to be
able to write:

    …    …    …
    scaling_factor = average_list(neighbors) / 3.0
    center_cell = scaling_factor * center_cell
    …    …    …

but if `average_list` might return `None`, their code will only be safe
if they write:

    …    …    …
    scaling_factor = average_list(neighbors) / 3.0
    if temp is not None:
        center_cell = scaling_factor * center_cell
    …    …    …

Given what we have seen so far, and allowing the divide-by-zero error to
occur, is actually the safest choice: if our program ever does try to
calculate the average of an empty list, it will fail right away. We will
see a better way to handle this situation
[later](quality.html#s:except).

### Summary

-   A function may take any number of arguments.
-   Define default values for parameters to make functions more
    convenient to use.
-   Defining default values only makes sense when there are sensible
    defaults.

Returning Values
----------------

### Understand:

-   How to return values from a function at any time.
-   Why functions shouldn't return values at arbitrary points.
-   What a function returns if it doesn't return anything explicitly.

All of our functions so far have ended with a `return` statement, and
that has been the only `return` statement they've contained. Once again,
this doesn't have to be the case: it is often easier to write functions
that return from several places, though this can also make them harder
to read.

Let's start with a function that calculates the sign of a number:

~~~~ {src="src/funclib/sign.py"}
def sign(num):
    if num < 0:
        return -1
    if num == 0:
        return 0
    return 1
~~~~

If we call it with a negative number, the first branch of the `if`
returns -1. If we call it with 0, the `return` in the second `if` is
executed, and if we call it with a positive number, neither of the `if`
branches is taken, so we [fall through](glossary.html#fall-through) to
the final `return`, which produces the value 1:

~~~~ {src="src/funclib/sign.py"}
print -5, '=>', sign(-5)
print 0, '=>', sign(0)
print 241, '=>', sign(241)
-5 => -1
0 => 0
241 => 1
~~~~

One common use of multiple return statements is to handle special cases
at the start of a function. For example, suppose we decide that we want
the average of an empty list to be zero after all. We could modify our
averaging function to check for this case before doing anything else:

~~~~ {src="src/funclib/average_empty.py"}
def average_list(values):

    # The average of no values is 0.0.
    if len(values) == 0:
        return 0.0

    # Handle actual values.
    result = 0.0
    for v in values:
        result += v
    return result / len(values)
~~~~

The early `return` statement (plus a comment) makes it very clear to
whoever is reading this code that we are handling an empty list in a
special way. Compare this to an implementation that uses `if` and `else`
to separate the two cases while keeping a single `return` statement at
the end of the function:

~~~~ {src="src/funclib/average_empty.py"}
def average_list(values):

    # The average of no values is 0.0.
    if len(values) == 0:
        result = 0.0

    # Handle actual values.
    else:
        result = 0.0
        for v in values:
            result += v
        result /= len(values)

    # Return final result.
    return result
~~~~

This version is easier to understand in one way, but harder in another.
What makes it harder is our limited short-term memory: the body of the
`else` is only four lines long, but reading and understanding those
lines may push the special handling of the empty list out of our mind.
In this case, the code is short enough that we will probably be able to
retain the special case, but if the calculation was more complex, we
would lose sight of the big picture.

What makes it easier is its regularity: each possible case of input
(empty or non-empty) is handled in a conditional branch, and each
branch's job is to assign a value to `result` for the function to
return. If there were six or seven special cases, this pattern would
help us keep track of what what going on—provided we knew (or
recognized) the pattern.

The psychological term for what's going on here is
[chunking](glossary.html#chunk), which refers to the way people group
items together in memory. For example, when you look at the five dots on
a dice:

![Five Spots](img/funclib/five_spots.png)

what you actually "see" is the X pattern, and what you remember is that
pattern rather than five individual dots. rather than remembering five
individual dots. Similarly, you remember common words such as "common"
as words, not as sequences of letters, and so on.

One of the key differences between experts and novices is that experts
are better at chunking: they don't actually have larger short-term
memories, but since they recognize a broader repertoire of patterns,
they are able to manage more information. Turning that over, the more
recognizable patterns are used in a program, the easier it is for people
to keep it in their heads. And as Chase and Simon discuss in their
classic paper "[Perception in chess](bib.html#chase-simon-chess)",
things that *don't* conform to patterns can actually be *harder* for
experts to recognize, since their brains will mis-match and "correct"
what's actually there.

Here's a third version of our function that doesn't use an early return.
and only has one conditional branch:

~~~~ {src="src/funclib/average_empty.py"}
def average_list(values):
    result = 0.0
    if len(values) > 0:
        for v in values:
            result += v
        result /= len(values)
    return result
~~~~

Many people find this version harder to understand than either of the
previous two, even though it is shorter. The reason is that the special
case isn't handled explicitly. Instead, this function returns 0 for the
empty list because of the code that *isn't* executed: if the list is
empty, the loop doesn't run, so the initial value of `result` becomes
the function's final value by default. Spotting this, and keeping track
of what the function isn't doing as well as what it is, is difficult
enough that many people won't realize there is a special case at all.

One last thing to note about functions in Python is that every function
returns something: if there isn't an explicit `return` statement, the
value returned is `None`. For example, let's comment out the last line
of our sign function:

~~~~ {src="src/funclib/sign_commented.py"}
def sign(num):
    if num < 0:
        return -1
    if num == 0:
        return 0
#    return 1

print -5, '=>', sign(-5)
print 0, '=>', sign(0)
print 241, '=>', sign(241)
-5 => -1
0 => 0
241 => None
~~~~

The sign of 241 is now `None` instead of 1, because when the function is
called with a positive value, neither of the `if` branches is taken, and
execution "falls off" the end of the function.

Other languages do this differently. In C, for example, trying to use
the "result" of a function that doesn't explicitly return something is a
compilation error—the program can't even be run. No matter what the
language, this is one reason why commenting out blocks of code is a bad
idea: it's all too easy to accidentally disable a `return` statement
buried inside the code that's no longer being executed.

### Summary

-   A function may return values at any point.
-   A function should have zero or more `return` statements at its start
    to handle special cases, and then one at the end to handle the
    general case.
-   "Accidentally" correct behavior is hard to understand.
-   If a function ends without an explicit `return`, it returns `None`.

Aliasing
--------

### Understand:

-   How and when aliasing will occur during function calls.

We said [earlier](#a:call-stack) that values are copied into parameters
whenever a function is called. But as we explained in the [previous
chapter](python.html#s:alias), variables don't actually store values:
they are actually just names that refer to values. To see what this
means for our programs, here's a function that takes a string and a list
as parameters, and appends something to both:

~~~~ {src="src/funclib/appender.py"}
def appender(a_string, a_list):
    a_string = a_string + 'turing'
    a_list.append('turing')
~~~~

And here is some code to set up a pair of variables and call that
function:

~~~~ {src="src/funclib/appender.py"}
string_val = 'alan'
list_val = ['alan']
appender(string_val, list_val)
print 'string', string_val
print 'list', list_val
string alan
list ['alan', 'turing']
~~~~

Why did the list change when the string didn't? To find out, let's trace
the function's execution. Just before the call, the global frame has two
variables that refer to a string and a list:

![Before Appending](img/funclib/append_before_call.png)

The call creates a new stack frame with aliases for those values:

![While Appending](img/funclib/append_during_call.png)

The `a_string + 'turing'` creates a new string `'alanturing'`; assigning
this to the variable `a_string` changes what that local variable refers
to, but doesn't change what the global variable `string_val` refers to:

![A New String](img/funclib/append_new_string.png)

The statement `a_list.append('turing')`, however, actually modifies the
list that `a_list` is pointing to:

![But the Same List](img/funclib/append_same_list.png)

But this is the same thing that the variable `list_val` in the caller is
pointing to. When the function returns and the call frame is thrown
away, the new string `'alanturing'` is therefore lost, because the only
reference to it was in the function call's stack frame. The change to
the list, on the other hand, is kept, because the function actually
modified the list in place:

![The Final State of Memory](img/funclib/append_final_state.png)

Let's change one line in the function:

~~~~ {src="src/funclib/appender_2.py"}
def appender(a_string, a_list):
    a_string = a_string + 'turing'
    a_list = a_list + ['turing']
~~~~

and see what happens when we run the same experiment:

~~~~ {src="src/funclib/appender_2.py"}
string_val = 'alan'
list_val = ['alan']
appender(string_val, list_val)
print 'string', string_val
print 'list', list_val
string alan
list ['alan']
~~~~

The answer is different because concatenating (adding) two lists creates
a new list, rather than modifying either of the lists being
concatenated. As a result, the local variable `a_list` is the only thing
that refers to the list `['alan', 'turing']`, so that value is discarded
when the function finishes and `list_val`'s value is undisturbed.

### Memory Models

Python's treatment of lists (and other mutable data that we'll see
[later](setdict.html)) isn't the only way to handle things. For example,
MATLAB functions use a rule called [copy on
write](glossary.html#copy-on-write). Initially, it creates aliases for
arrays that are passed into functions. The first time a function assigns
to an array, though, MATLAB clones the array and changes the clone
rather than the original ([Figure XXX](#f:copy_on_write)). This saves it
from copying data when it doesn't need to, while guaranteeing that
functions don't have side effects (which makes them easier to think
about).

![Copy on Write](img/funclib/copy_on_write.png)

Other languages have slightly different rules about scoping and
aliasing. Together, those rules make up the language's [memory
model](glossary.html#memory-model). Understanding that model is perhaps
the most important step in understanding how programs written in the
language actually work, and more importantly, how to debug them when
they don't.

### Summary

-   Values are actually passed into functions by reference, which means
    that they are aliased.
-   Aliasing means that changes made to a mutable object like a list
    inside a function are visible after the function call completes.

Libraries
---------

### Understand:

-   How to import code in one Python module for use in another.
-   That code is executed as it's imported.
-   That each module corresponds to a variable scope.

A function is a way to turn a bunch of related statements into a single
chunk that can be re-used. A [module](glossary.html#module) or
[library](glossary.html#library) (for our purposes, the terms mean the
same thing) does for functions what functions do for statements: group
them together to create more usable chunks. This hierarchical
organization is similar in spirit to that used in biology: instead of
family, genus, and species, we have module, function, and statement.

Every Python file can be used as a module by other programs. import has
already been introduced To load a module into a program, we use the
`import` statement. For example, suppose we have created a Python file
called `halman.py` that defines a single function called `threshold`:

~~~~ {src="src/funclib/halman.py"}
# halman.py
def threshold(signal):
  return 1.0 / sum(signal)
~~~~

If we want to call this function in a program stored in another file, we
use `import halman` to load the contents of `halman.py`, and then call
the function as `halman.threshold`:

~~~~ {src="src/funclib/use_halman.py"}
import halman
readings = [0.1, 0.4, 0.2]
print 'signal threshold is', halman.threshold(readings)
~~~~

We can then run the program that does the `import` and calls the
function:

    $ python use_halman.py
    signal threshold is 1.42857

When a module is imported, Python executes the statements it contains
(which are usually function definitions). It then creates an object to
store references to all the items defined in that module and assigns it
to a variable with the same name as the module. For example, let's
create a file called `noisy.py` that prints out a message and then
defines `NOISE_LEVEL` to be 1/3:

~~~~ {src="src/funclib/noisy.py"}
# noisy.py
print 'Is this module being loaded?'
NOISE_LEVEL = 1./3.
~~~~

When it imports `noisy` Python executes the first statement—the
`print`—and displays a message on the screen:

    >>> import noisy
    Is this module being loaded?

Importing the module also defines the variable `NOISE_LEVEL`. Inside the
main program, we can access as `noisy.NOISE_LEVEL`:

    >>> print noisy.NOISE_LEVEL
    0.33333333

Just like a function, each module is a separate scope, so that variable
names defined inside a module belong to that module and don't collide
with variable names defined elsewhere. When a function wants to a find a
variable, it actually looks in its own scope, then in its module. Our
earlier rule "function then global" is just a special case of this,
since the global scope is just the module scope of our main program.

![Name Resolution](img/funclib/name_resolution.png)

To see how this works, let's create a file called `module.py` that
defines both a variable called `NAME` and a function called `func` that
prints it out:

~~~~ {src="src/funclib/module.py"}
# module.py
NAME = 'Transylvania'

def func(arg):
  return NAME + ' ' + arg
~~~~

In our main program, we also define a variable called `NAME`, then
import our module. When we call `module.func` it sees the `NAME`
variable that was defined inside the module, not the one that was
defined globally:

~~~~ {src="src/funclib/use_module.py"}
>>> NAME = 'Hamunaptra'
>>> import module
>>> print module.func('!!!')
Transylvania !!!
~~~~

Once again, rules about where and how to look things up might seem
arcane, but it would be practically impossible to write large programs
without some kind of scoping them. Restricting lookup to the current
function, its module, and the top level of the program makes it easier
for people to understand code, since there are only three places where
the variables used on a particular line might be, two of which (the
containing function and the file it's in) are guaranteed to be nearby.

### How Other Languages Do It

When a dynamic language like Python (or MATLAB, R, Ruby, or Perl) loads
a program, it actually does two things:

1.  translate the statements into instructions the computer can execute,
    and
2.  execute those instructions.

Compiled languages like Fortran, C++, and Java do these things
separately: a [compiler](glossary.html#compiler) does the translation,
saving the instructions in a file on disk, which a separate
[loader](glossary.html#loader) copies into memory for execution some
time later ([Figure XXX](#f:compiling_vs_interpreting)). In general,
compiled languages therefore don't execute instructions while loading;
instead, they wait until everything is in memory before running any of
it.

![Compiling vs. Interpreting](img/funclib/compiling_vs_interpreting.png)

### Summary

-   Any Python file can be imported as a library.
-   The code in a file is executed when it is imported.
-   Every Python file is a scope, just like every function.

Standard Libraries
------------------

### Understand:

-   What is in the standard math library.
-   What is in the system library.
-   Several ways to import things from libraries.

The real power of a language is in its libraries: they are the distilled
wisdom and effort of all the programmers who have come before us.
Python's standard library contains over a hundred modules, and the
fastest way to become a more productive programmer is to become familiar
with them. One of the most useful is `math`, which defines `sqrt` for
square roots, `hypot` for calculating x^2^+y^2^, and values for *e* and
π that are as accurate as the machine can make them.

    >>> import math
    >>> print math.sqrt(2)
    1.4142135623730951
    >>> print math.hypot(2, 3)  # sqrt(x**2 + y**2)
    3.6055512754639891
    >>> print math.e, math.pi   # as accurate as possible
    2.7182818284590451 3.1415926535897931

Since `math.sqrt` is a handful to type, and `sqrt` is probably not
ambiguous, Python provides several ways to import things. For example,
we can import specific functions from a library and then call them
directly, rather than using the `modulename.functionname` syntax:

    >>> from math import sqrt
    >>> sqrt(3)
    1.7320508075688772

We can also import a function under a different name, so that if two
modules define functions with the same name, we can give one or the
other a different name when we want to use them together:

    >>> from math import hypot as euclid
    >>> euclid(3, 4)
    5.0

We can also use `import *` to bring everything in the module into the
current scope at once. This has the same effect as using
`from module import a`, `from module import b`, and so on for every name
in the module:

    >>> from math import *
    >>> sin(pi)
    1.2246063538223773e-16

`import *` is usually a bad idea: if someone adds a new function or
variable to the next version of the module, your `import *` could
silently overwrite something that you have written, or are importing
from somewhere else. Bugs like this can be extremely hard to find, since
nothing seemed to change in your program.

Another useful library is `sys` (short for "system"). It defines
constants to tell us what version of Python we're using, what operating
system we're running on, and how large integers are:

    >>> import sys
    >>> print sys.version
    2.7 (r27:82525, Jul  4 2010, 09:01:59) [MSC v.1500 32 bit (Intel)]
    >>> print sys.platform
    win32
    >>> print sys.maxint
    2147483647
    >>> print sys.path
    ['',
     'C:\\WINDOWS\\system32\\python27.zip',
     'C:\\Python27\\DLLs', 'C:\\Python27\\lib',
     'C:\\Python27\\lib\\plat-win',
     'C:\\Python27', 'C:\\Python27\\lib\\site-packages']

The most commonly-used element of `sys`, though, is `sys.argv`, which
holds a list of the [command-line
arguments](glossary.html#command-line-arguments) used to run the
program. The name of the script itself is in `sys.argv[0]`; all the
other arguments are put in `sys.argv[1]`, `sys.argv[2]`, and so on. For
example, here's a program that does nothing except print out its
command-line arguments:

~~~~ {src="src/funclib/echo.py"}
# echo.py
import sys
for i in range(len(sys.argv)):
  print i, '"' + sys.argv[i] + '"'
~~~~

If it is run without any arguments, it reports that `sys.argv[0]` is
`echo.py`:

    $ python echo.py
    0 echo.py

When it is run with arguments, though, it displays those as well:

    $ python echo.py first second
    0 echo.py
    1 first
    2 second

We can use this to write command-line tools like a simple calculator:

~~~~ {src="src/funclib/calculator.py"}
import sys

total = 0
for value in sys.argv[1:]:
    total += float(value)
print total
$ python calculator.py 1 2 3
6.0
~~~~

Notice that we loop over `sys.argv[1:]`, i.e., over everything except
the first element of `sys.argv`. That first element is always the name
of our program (in this case, `calculator.py`), which we definitely
don't want to try to add to our running total.

A more common use of `sys.argv` is to pass the names of a bunch of files
into our program. Suppose, for example, that we have a function called
`summarize` that opens a file, reads the values in it, and returns the
minimum, average, and maximum:

~~~~ {src="summarize.py"}
def summarize(filename):
    reader = open(filename, 'r')
    least, greatest, total, count = 0.0, 0.0, 0.0
    for line in reader:
        current = float(line)
        least = min(least, current)
        greatest = max(least, current)
        total += current
        count += 1
    reader.close()
    return least, total / count, greatest
~~~~

If we want to display summaries for several files at once, we can
require the user to give them as command-line arguments:

    $ python summarize.py july.dat august.dat september.dat

and connect the command line with the program's internals using
`sys.argv`:

~~~~ {src="summarize.py"}
all_filenames = sys.argv[1:]  # Again, don't include the program name
for filename in all_filenames:
    low, ave, high = summarize(filename)
    print filename, low, ave, high
~~~~

### Summary

-   Use `from library import something` to import something under its
    own name.
-   Use `from library import something as alias` to import something
    under the name `alias`.
-   `from library import *` imports everything in `library` under its
    own name, which is usually a bad idea.
-   The `math` library defines common mathematical constants and
    functions.
-   The system library `sys` defines constants and functions used in the
    interpreter itself.
-   `sys.argv` is a list of all the command-line arguments used to run
    the program.
-   `sys.argv[0]` is the program's name.
-   `sys.argv[1:]` is everything except the program's name.

Building Filters
----------------

### Understand:

-   How to build a program that behaves like a Unix filter.
-   How to decide what should be done in a function and what should be
    done by its caller.
-   How to get help interactively.
-   How to provide interactive help.
-   How a file can tell if it's being used as the main program or being
    loaded as a library.

As well as creating a list of a program's command-line arguments, `sys`
also connects the program to standard input, standard output, and
standard error (which were introduced in the chapter on [the Unix
shell](shell.html#s:pipefilter)). Here's a typical example of how these
variables are used together:

~~~~ {src="src/funclib/count.py"}
import sys

def count_lines(reader):
    result = 0
    for line in reader:
        result += 1
    return result

if len(sys.argv) == 1:
    count_lines(sys.stdin)
else:
    for filename in sys.argv[1:]:
        rd = open(filename, 'r')
        count_lines(rd)
        rd.close()
~~~~

This program looks at `sys.argv` to see if it was called with any
filenames as arguments or not. If there were no arguments, then
`sys.argv` will only hold the name of the program, and its length will
be 1. In that case, the program reads data from standard input:

    $ python count.py < a.txt
    48

Otherwise, the program assumes its command-line arguments are the names
of files. It opens each one in turn, counts how many lines are in it,
and then closes it:

    $ python count.py a.txt b.txt
    48
    227

### Who Opens?

There's a subtle but important difference between `count_lines` and the
`summarize` function we wrote earlier. `summarize` expects a filename as
its sole parameter, and opens and closes that file itself.
`count_lines`, on the other hand, expects to be given a handle to an
already-open file, i.e., it expects whoever is calling it to take care
of the opening and closing.

Why the difference? Because we want to use the same `count_lines`
function for both the files whose names we're given on the command line,
and for `sys.stdin`. Putting it another way, we can't call `open` with
`sys.stdin` as a parameter—it's already an open file, not a string—so we
have to do our opening before we call the function.

We *could* push responsibility for opening down into the function if we
really wanted to, so that our main program was just:

~~~~ {src="src/funclib/count_2.py"}
if len(sys.argv) == 1:
    count_lines(sys.stdin)
else:
    for filename in sys.argv[1:]:
        count(filename)
~~~~

If we do this, though, the function has to check whether its parameter
is a string (which we interpret to mean "the name of a file") or
something else (which we hope is an open file we can read from). We have
to do the same check at the end of the function as well to close the
file if we opened it:

~~~~ {src="src/funclib/count_2.py"}
def count_lines(source):
    if type(source) == str:
        reader = open(source, 'r')
    result = 0
    for line in reader:
        result += 1
    if type(source) == str:
        reader.close()
    return result
~~~~

Most people find the original easier to understand, since it does a
better job of separating the calculation from the file management.

Let's go back to our original program and write it a little more
politely:

~~~~ {src="src/polite_count.py"}
'''Count lines in files.  If no filename arguments given,
read from standard input.'''

import sys

def count_lines(reader):
  '''Return number of lines in text read from reader.'''
  return len(reader.readlines())

if __name__ == '__main__':
  if len(sys.argv) == 1:
    print count_lines(sys.stdin)
  else:
    r = open(sys.argv[1], 'r')
    print count_lines(r)
    r.close()
~~~~

The two significant changes are the strings at the start of the module
and of the function `count_lines`, and the funny-looking line that
compares `__name__` to `'__main__'`. Let's look at them in that order.

To help us find our way around libraries, Python provides a `help`
function. If `math` has been imported, the call `help(math)` prints out
the documentation embedded in the math library:

    >>> import math
    >>> help(math)
    Help on module math:
    NAME
        math
    FILE
        /usr/lib/python2.5/lib-dynload/math.so
    MODULE DOCS
        http://www.python.org/doc/current/lib/module-math.html
    DESCRIPTION
        This module is always available.  It provides access to the
        mathematical functions defined by the C standard.
    FUNCTIONS
        acos(...)
            acos(x)
            Return the arc cosine (measured in radians) of x.
        …        …        …

Here's how this works. If the first thing in a module or function other
than blank lines or comments is a string, and that string isn't assigned
to a variable, Python saves it as the documentation string, or
[docstring](glossary.html#docstring), for that module or function. These
docstrings are what online (and offline) help display. For example,
let's create a file `adder.py` with a single function `add`, and write
docstrings for both the module and the function:

~~~~ {src="src/funclib/adder.py"}
# adder.py
'''Addition utilities.'''

def add(a, b):
  '''Add arguments.'''
  return a+b
~~~~

If we import `adder`, `help(adder)` prints out all of its docstrings,
i.e., the documentation for the module itself and for all of its
functions:

    >>> import adder
    >>> help(adder)
    NAME
        adder - Addition utilities.
    FUNCTIONS
        add(a, b)
            Add arguments.

We can also be more selective, and only display the help for a
particular function instead:

    >>> help(adder.add)
    add(a, b)
           Add arguments.

The second part of our more polite program was that odd-looking `if`
statement. It depends on a trick to do something useful, and that trick
needs a bit of explaining. When Python reads in a file, it assigns a
value to a special variable called `__name__` (with two underscores
before and after). If the file is being run as the main program,
`__name__` is assigned the string `'__main__'` (again with two
underscores before and after). If the file is being loaded as a module
by some other program, though, Python assigns the module's name to
`__name__` instead. To show this in action, let's create a Python file
called `my_name.py` that does nothing but print out the value of
`__main__`:

~~~~ {src="my_name.py"}
print __name__
~~~~

If we run it directly from the command line, it tells us that `__name__`
has the value `'__main__'`:

    $ python my_name.py
    __name__

If we import this file into an interactive Python session, though,
what's printed out during the import is different:

    $ python
    >>> import my_name
    my_name

We get the same behavior if we import `my_name` into another program:

    $ cat test_import.py
    import my_name
    $ python test_import.py
    my_name

Now, suppose that a file contains the conditional statement
`if __name__ == '__main__'`. The code inside the `if` will only run if
the file is the main program, because that's the only situation in which
`__name__` will be `'__main__'`. Put another way, the statements inside
the conditional will *not* be run if the file is being loaded as a
library by some other program. This makes it easy to write modules that
can be used as both programs in their own right, and as libraries by
other pieces of code.

For example, the file `stats.py` defines a function `average`, and then
runs three simple tests—but only if `__name__` has the value
`'__main__'`:

~~~~ {src="src/stats.py"}
# stats.py
'''Useful statistical tools.'''

def average(values):
  '''Return average of values or None if no data.'''
  if values:
    return sum(values) / len(values)
  else:
    return None

if __name__ == '__main__':
  print 'test 1 should be None:', average([])
  print 'test 2 should be 1:', average([1])
  print 'test 3 should be 2:', average([1, 2, 3])
~~~~

If we import this file into an interactive session, it doesn't produce
any output, because `stats.__name__` has been assigned the value
`'stats'`:

    >>> import stats
    >>> print stats.__name__
    stats

If we run this file directly, though, that same `__name__` variable will
be assigned the value `'__main__'`, so the test *will* be run:

    $ python stats.py
    test 1 should be None: None
    test 2 should be 1: 1
    test 3 should be 2: 2

This is another common design pattern in Python: group related functions
into a module, then put some tests for those functions in the same
module under `if __name__ == '__main__'`, so that if the module is run
as the main program, it will check itself.

### How Other Languages Do It

The `__name__ == 'main'` idiom is one of the few things that Python got
wrong: it's economical, in that it doesn't introduce any special-purpose
machinery that doesn't have to be there anyway, but novices have to
master several difficult concepts before they can understand how it
works.

Other languages handle the "where do I start?" problem differently. C,
for example, expects programs to have a function called `main`, which is
automatically invoked to start the program running.

### Summary

-   If a program isn't told what files to process, it should process
    standard input.
-   Programs that explicitly test values' types are more brittle than
    ones that rely on those values' common properties.
-   The variable `__name__` is assigned the string `'__main__'` in a
    module when that module is the main program, and the module's name
    when it is imported by something else.
-   If the first thing in a module or function is a string that isn't
    assigned to a variable, that string is used as the module or
    function's documentation.
-   Use `help(name)` to display the documentation for something.

Functions as Objects
--------------------

### Understand:

-   That a function is just another kind of data.
-   How to create an alias for a function.
-   How to pass a function to another function.
-   How to store a reference to a function in a list.
-   How to use higher-level functions to eliminate redundancy in
    programs.

An integer is just 32 or 64 bits of data that a variable can refer to,
while a string is just a sequence of bytes that a variable can also
refer to. Functions are just more bytes in memory—ones that happen to
represent instructions. That means that variables can refer to them just
as they can refer to any other data.

This insight—the fact that code is just another kind of data, and can be
manipulated like integers or strings—is one of the most useful and
powerful in all computing. To understand why, let's have a closer look
at what actually happens when we define a function:

~~~~ {src="src/funclib/threshold.py"}
def threshold(signal):
    return 1.0 / sum(signal)
~~~~

These two lines tell Python that `threshold` is a function that returns
one over the sum of the values in `signal`. When we define it, Python
translates the statements in the function into a blob of bytes, then
creates a variable called `threshold` and makes it point at that blob:

![Defining a Function](img/funclib/defining_function.png)

This is not really any different from assigning the string
`'alan turing'` to the variable `name`. the only difference is what's in
the memory the variable points to.

If `threshold` is just a reference to something in memory, we should be
able to assign that reference to another variable. Sure enough, we can,
and when we call the function via that newly-created alias, the result
is exactly what we would get if we called the original function with the
same parameters, because there's really only one function—it just has
two names:

~~~~ {src="src/funclib/threshold.py"}
data = [0.1, 0.4, 0.2]
print threshold(data)
1.42857
t = threshold
print t(data)
1.42857
~~~~

![Aliasing a Function](img/funclib/aliasing_function.png)

### Aliasing and Importing

We have created aliases for functions before without realizing it. When
we execute `from math import sqrt as square_root`, we are loading the
`math` module, then creating an alias called `square_root` for its
function `sqrt`.

If a function is just another kind of data, and we can create an alias
for it, can we put it in a list? More precisely, can we put a reference
to a function in a list? Let's define two functions, `area` and
`circumference`, each of which takes a circle's radius as a parameter
and returns the appropriate value:

~~~~ {src="src/funclib/funclist.py"}
def area(r):
    return pi * r * r

def circumference(r):
    return 2 * pi * r
~~~~

Once those functions are defined, we can put them into a list (more
precisely, put references to them in a list):

~~~~ {src="src/funclib/funclist.py"}
funcs = [area, circumference]
~~~~

![A List of Functions](img/funclib/list_of_functions.png)

We can now loop through the functions in the list, calling each in turn.
Sure enough, the output is what we would get if we called `area` and
then `circumference`:

~~~~ {src="src/funclib/funclist.py"}
for f in funcs:
    print f(1.0)
3.14159
6.28318
~~~~

Let's go a little further. Instead of storing a reference to a function
in a list, let's pass that reference into another function, just as we
would pass a reference to an integer, a string, or a list. Here's a
function called `call_it` that takes two parameters: a reference to some
other function, and some other value.

~~~~ {src="src/funclib/passfunc.py"}
def call_it(func, value):
    return func(value)
~~~~

All `call_it` does is call that other function with the given value as a
parameter:

~~~~ {src="src/funclib/passfunc.py"}
print call_it(area, 1.0)
3.14159

print call_it(circumference, 1.0)
6.28318
~~~~

Now it's time for the payoff. Here's a function called `do_all` that
applies a function—anything at all that takes one argument—to each value
in a list, and returns a list of the results:

~~~~ {src="src/funclib/doall.py"}
def do_all(func, values):
    result = []
    for v in values:
        temp = func(v)
        result.append(temp)
    return result
~~~~

If we call `do_all` with `area` and a list of numbers, we get what we
would get if we called `area` directly on each number in turn:

~~~~ {src="src/funclib/doall.py"}
print do_all(area, [1.0, 2.0, 3.0])
[3.14159, 12.56636, 28.27431]
~~~~

And if we define a function to "slim down" strings of text by throwing
away their first and last characters, we can apply it to every string in
a list, without having to write another copy of the code that loops
through the list, calls the function, and concatenates the results:

~~~~ {src="src/funclib/doall.py"}
def slim(text):
    return text[1:-1]

print do_all(slim, ['abc', 'defgh'])
b efg
~~~~

Functions that operate on other functions are called [higher-order
functions](glossary.html#higher-order-functions). They're common in
mathematics: integration, for example, is a function that operates on
some other function. In programming, higher-order functions allow us to
mix and match pieces of code rather than duplicating them.

As another example, let's look at `combine_values`, which takes a
function and a list of values as parameters, and combines the values in
the list using the function provided:

~~~~ {src="src/funclib/combine.py"}
def combine_values(func, values):
    current = values[0]
    for i in range(1, len(values)):
        current = func(current, values[i])
    return current
~~~~

Now let's define `add` and `mul` to add and multiply values:

~~~~ {src="src/funclib/combine.py"}
def add(x, y):
    return x + y

def mul(x, y):
    return x * y
~~~~

If we combine 1, 3, and 5 with `add`, we get their sum, 9:

~~~~ {src="src/funclib/combine.py"}
print combine_values(add, [1, 3, 5])
9
~~~~

If we combine the same values with `mul`, we get their product, 15:

~~~~ {src="src/funclib/combine.py"}
print combine_values(mul, [1, 3, 5])
15
~~~~

This same higher-order function `combine_values` could concatenate lists
of strings, too, or multiply several matrices together, or whatever else
we wanted, without us having to write or test the loop ever again.
Without higher-order functions, we would have to write one function for
each combination of data structure and operation, i.e., one function to
add numbers, another to concatenate strings, a third to sum matrices,
and so on. *With* higher-order functions, on the other hand, we only
write one function for each basic operation, and one function for each
kind of data structure. Since A plus B is usually a lot smaller than A
times B, this saves us coding, testing, reading, and debugging.

Several higher-order functions are built in to Python. One is `filter`,
which constructs a new list containing all the values in an original
list for which some function is true:

~~~~ {src="src/funclib/hof.py"}
def positive(x):
    return x > 0

print filter(positive, [-5, 3, -2, 9, 0])
[3, 9]
~~~~

Another is `map`, which applies a function to every element of a list
and returns a list of results:

~~~~ {src="src/funclib/hof.py"}
def bump(x):
    return x + 10

print map(bump, [-5, 3, -2, 9, 0])
[5, 13, 8, 19, 10]
~~~~

And then there's `reduce`, which combines values using a binary
function, returning a single value as a result:

~~~~ {src="src/funclib/hof.py"}
def add(x, y):
    return x + y

print reduce(add, [-5, 3, -2, 9, 0])
5
~~~~

Combining all of these is a very powerful way to do a lot of computation
with very little typing:

~~~~ {src="src/funclib/hof.py"}
print reduce(add, map(bump, filter(positive, [-5, 3, -2, 9, 0])))
32
~~~~

Reading from the inside out, we have:

1.  filtered the list, keeping only the positive values,
2.  bumped them up by 10, and
3.  summed the results.

Written out, this is:

~~~~ {src="src/funclib/hof.py"}
total = 0
for val in [-5, 3, -2, 9, 0]:
    if val > 0:
        total += (val + 10)
print total
~~~~

The functional approach is usually more economical, and isn't too bad to
read once calls are indented:

    print reduce(add,
                 map(bump,
                 filter(positive,
                        [-5, 3, -2, 9, 0])))

However, the all-in-one-loop approach *is* faster, since each call in
the functional approach is creating its own temporary list of results,
only to have it discarded by the next function in the chain. As always,
we should only worry about this once we are sure that (a) the program is
working correctly, and (b) its performance really is a problem.

### List Comprehensions

explain list comprehensions

### Summary

-   A function is just another kind of data.
-   Defining a function creates a function object and assigns it to a
    variable.
-   Functions can be assigned to other variables, put in lists, and
    passed as parameters.
-   Writing higher-order functions helps eliminate redundancy in
    programs.
-   Use `filter` to select values from a list.
-   Use `map` to apply a function to each element of a list.
-   Use `reduce` to combine the elements of a list.

Summing Up
----------

Functions are a way to divide code up into more comprehensible pieces:
essentially, to replace several pieces of information with one to make
the whole easier to understand. Functions are therefore not just about
eliminating redundancy: they are worth writing even if they're only
called once.

In fact, functions are such a powerful idea that many people regard
programming as the art of defining a mini-language in which the solution
to the original problem is trivial. To close off this chapter, let's try
to answer a frequently-asked question: when should we write functions?
And what should we put in them?

The answers to these questions depend on the fact that human short-term
memory can only hold a few things at a time. If we try to remember more
than a double handful of unrelated bits of information for more than a
few seconds, they become jumbled and we start making mistakes. In
particular, if someone has to keep several dozen things straight in
their mind in order to understand a piece of code, that code is too
long.

Let's consider an example:

~~~~ {src="src/funclib/cognitive_limits_initial.py"}
for x in range(1, GRID_WIDTH-1):
  for y in range(1, GRID_HEIGHT-1):
    if (density[x-1][y] > density_threshold) or \
       (density[x+1][y] > density_threshold):
      if (flow[x][y-1] < flow_threshold) or\
         (flow[x][y+1] < flow_threshold):
        temp = (density[x-1][y] + density[x+1][y]) / 2
        if abs(temp - density[x][y]) > update_threshold:
          density[x][y] = temp
~~~~

This code uses meaningful variable names, and is well structured, but
it's still a lot to digest in one go. Let's replace the loop bounds with
function calls that give us a bit more context:

~~~~ {src="src/funclib/cognitive_limits_bounds.py"}
for x in grid_interior(GRID_WIDTH):
  for y in grid_interior(GRID_HEIGHT):
    if (density[x-1][y] > density_threshold) or \
       (density[x+1][y] > density_threshold):
      if (flow[x][y-1] < flow_threshold) or\
         (flow[x][y+1] < flow_threshold):
        temp = (density[x-1][y] + density[x+1][y]) / 2
        if abs(temp - density[x][y]) > update_threshold:
          density[x][y] = temp
~~~~

`grid_interior(num)` might just return `range(1, num-1)`, but try
reading the first two lines of this code aloud, and then the first two
lines of what it replaced, and see which is easier to understand.

Now let's replace those two `if` statements with function calls as well:

~~~~ {src="src/funclib/cognitive_limits_threshold.py"}
for x in grid_interior(GRID_WIDTH):
  for y in grid_interior(GRID_HEIGHT):
    if density_exceeds(density, x, y, density_threshold):
      if flow_exceeds(flow, x, y, flow_threshold):
        temp = (density[x-1][y] + density[x+1][y]) / 2
        if abs(temp - density[x][y]) > tolerance:
          density[x][y] = temp
~~~~

Again, we've provided more information about what we're actually doing.
Finally, let's create and call a function to handle updates to our data
structure:

~~~~ {src="src/funclib/cognitive_limits_final.py"}
for x in grid_interior(GRID_WIDTH):
  for y in grid_interior(GRID_HEIGHT):
    if density_exceeds(density, x, y, density_threshold):
      if flow_exceeds(flow, x, y, flow_threshold):
        update_on_tolerance(density, x, y, tolerance)
~~~~

Our original nine lines have become five, and those five are all at the
same mental level. It's hard to pin down exactly what that phrase means,
but most programmers would agree that the first version mixed high-level
ideas about boundaries and update conditions with low-level details of
grid access and cell value comparisons. In contrast, this version only
has the high-level stuff; the low-level implementation details are
hidden in those functions.

A conscientious programmer who wrote the code we started with would go
back and [refactor](glossary.html#refactor) it to turn it into something
like our final version before committing it to [version
control](svn.html). If she did this often enough, she would eventually
find herself writing the final version first, just as mathematicians
find themselves skipping more and more "obvious" steps as they do more
proofs. When we see someone "just writing" something elegant, the odds
are good that they have spent time rewriting their own poor code, and in
doing so, turned conscious decision into unconscious action.
