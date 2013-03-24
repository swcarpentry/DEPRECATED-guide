Conclusion
==========

Our real goal in the preceding chapters was not to teach you the syntax
of Python or how to commit a file to version control. Our real goal was
to convey eight big ideas that every good scientific programmer knows,
whether she realizes it or not.

Computers Don't Understand, They Obey
-------------------------------------

If you look at [Figure 1](#f:word_data), you can't help but see the word
"data":

![The Word 'Data'](img/concl/word_data.png)

A machine doesn't. It doesn't even see four blobs of blue pixels on a
gray background, because it doesn't "see" anything. The computer stores
this image as bits in memory. If those bits happen to correspond to
pixels arranged in a certain way, then an optical character recognition
program might output 'd', 'a', 't', 'a', but *it doesn't understand*.

What it does instead is obey. Depending on what instructions we tell the
computer to execute, the thirty-two bits
01100100011000010111100001100001 can be:

-   the word "data";
-   the integer 1,684,108,385;
-   the floating-point number 1.6635613602263159e+22;
-   a bluish-gray pixel that's slightly transparent;
-   four and a half microseconds of a high 'A' that's slightly louder in
    the left channel than the right,
-   an instruction to copy the contents of register 100 to the location
    in memory whose address is stored in register 116; or
-   a point on the outer edge of a superconducting magnets a CAD model
    of a CAT scanner.

The fact is, computers don't understand what they're doing: they just
obey the instructions they're given.

### Examples:

-   [Most files' names are `something.extension`; the extension isn't
    required, and doesn't guarantee anything, but is normally used to
    indicate the type of data in the file.](shell.html#k:filedir)
-   [Everything is stored as bytes, but the bytes in binary files do not
    represent characters.](shell.html#k:find)
-   [Strings and numbers cannot be added because the behavior is
    ambiguous: convert one to the other type
    first.](python.html#k:types)

Programs Are Data Too
---------------------

The corollary of our first big idea is that programs are data too: in
fact, this is the key insight that all of modern computing is built on.
The source code for a program is just a bunch of text files, no
different from a thesis. Translating that text into bytes that happen to
represent instructions the machine can execute is no different from
translating the bytes that represent red-green-blue values into pretty
lights on your screen. And once a program's text is compiled into
instructions, pushing those bytes around is no different from correcting
a typo in an address list or changing the color of a pixel in an image
file.

### Examples:

-   [Any Python file can be imported as a
    library.](funclib.html#k:libraries)
-   [A function is just another kind of data.](funclib.html#k:funcobj)

Models for Computers, Views for People
--------------------------------------

Another corollary of our first idea is that computers should work with
models, and people should work with views. A model (or to give its full
name, a "data model") is a digital representation of facts and
relationships, while a view is a way of displaying part or all of a
model that human beings can comprehend. For example, an HTML document
logically consists of elements with attributes that may contain other
elements and blocks of text ([Figure 2](#f:html_page)):

![An HTML Page](img/concl/html_page.png)

That model can be rendered in a browser, turned into speech for someone
who is visually impaired, or displayed as text using angle brackets,
quotes, and some indentation. None of these *is* the model: they're all
views that make the model's content accessible to human beings in
different contexts. The model itself isn't just easier for the computer
to work with: it's essential, since as we said in the previous section,
the computer can't "see" the views that we create for human beings.

Turning one of those views back into a model is hard: parsing the
textual representation of HTML takes thousands of lines of code, and
doing OCR or speech recognition takes millions. What this big idea
implies, therefore, is that structured data is better than unstructured
data, because it makes the view-to-model translation faster, simpler,
and more accurate. To borrow an example from Jon Udell, a PDF with a
cartoon whose caption says, "The knitting circle meets on the second
Tuesday of every month" is a lot easier for human beings to understand
than a blob of iCal-formatted text, but the second is much easier for
the computer to process ([Figure 3](#f:structured_data)):

![Structured vs. Unstructured Data](img/concl/structured_data.png)

### Examples:

-   [A relational database stores information in tables with fields and
    records.](db.html#k:select)
-   [Each field in a database table should store a single atomic
    value.](db.html#k:design)
-   [No fact in a database should ever be duplicated.](db.html#k:design)
-   [Every record in a table should be uniquely identified by the value
    of its primary key.](db.html#k:join)

Programming is a Human Activity
-------------------------------

Our fourth big idea is that the real bottleneck in most computing today
is not in our machines: it's between our ears. The time required to
solve a problem is the sum of the time required to write correct code
and the time spent running it. While computers are getting faster every
day, our brains are not, so the first term in this sum is increasingly
the most important. When we're trying to solve a computational problem,
it therefore makes sense to minimize how long it will take to build the
program we need, even if that means the program itself will run slower
than it otherwise might.

### Examples:

-   [Use wildcards to match filenames.](shell.html#k:pipefilter)
-   [Use a `for` loop to repeat commands once for every thing in a
    list.](shell.html#k:loop)
-   [Use the up-arrow key to scroll up through previous commands to edit
    and repeat them.](shell.html#k:loop)
-   [Use `history` to display recent commands, and `!number` to repeat a
    command by number.](shell.html#k:loop)
-   [Save commands in files (usually called shell scripts) for
    re-use.](shell.html#k:scripts)
-   [It also keeps a complete history of changes made to the master so
    that old versions can be recovered reliably.](svn.html#k:basics)
-   [Each change should be commented to make the history more
    readable.](svn.html#k:basics)
-   [Use meaningful, descriptive names for
    variables.](python.html#k:basic)
-   [Grouping operations in functions makes code easier to understand
    and re-use.](funclib.html#k:basics)
-   [Programmers often write constants' names in upper case to make
    their intention easier to recognize.](funclib.html#k:global)
-   [Functions should *not* communicate by modifying global
    variables.](funclib.html#k:global)
-   [Define default values for parameters to make functions more
    convenient to use.](funclib.html#k:args)
-   [Build up queries a bit at a time, and test them against small data
    sets.](db.html#k:filter)
-   [High-level libraries are usually more efficient for numerical
    programming than hand-coded loops.](numpy.html#k:basics)
-   [Assertions help people understand how programs
    work.](quality.html#k:defensive)
-   [Writing tests helps us design better code by clarifying our
    intentions.](quality.html#k:unit)
-   [Separating interface from implementation makes code easier to test
    and re-use.](quality.html#k:testable)
-   [Get something simple working, then start to add features, rather
    than putting everything in the program at the
    start.](dev.html#k:grid)
-   [Put programs together piece by piece.](dev.html#k:assembly)
-   [Before speeding a program up, ask, "Does it need to be faster?"
    and, "Is it correct?"](dev.html#k:performance)

Paranoia Makes Us Productive
----------------------------

Big idea number five is a consequence of big idea number four: the best
way to improve productivity (in fact, the only way) is to improve
quality, and that this starts before we write the first line of code. "I
want to count all the stars in this photograph" is easy to say, but what
does it actually mean? What constitutes a star? When do you decide that
a lumpy blob of pixels is two stars rather than one, or three instead of
two? Every program embodies decisions about questions like these, even
if you don't realize that there was a question and that you made a
choice. The sooner we worry about this, the less time we'll waste
building the wrong thing.

Of course, we don't stop worrying once we've typed our code in. We check
that data is formatted properly to protect ourselves against "garbage
in, garbage out". We put checks in our code to make sure that parameters
are sensible, data structures consistent, files aren't empty, and so on.
And we write tests, and run them after every code change, to catch
errors as soon as possible. This might feel like it's slowing us down at
first, but study after study has shown that it works.

One of the best ways to apply this principle is to automate everything.
As Alfred North Whitehead said, "Civilization advances by extending the
number of important operations which we can perform without thinking
about them." We don't just write programs because we want to do things
quickly: we write them because we don't want to do some things ever
again. Version control systems keep track of our work for us;
spreadsheets update graphs and summary statistics whenever a single
value changes, and so on. Every time we automate a task, we reduce the
chances of getting it wrong the next time, and have more time to think
about things that machines *can't* do for us. And it's not just a
one-time saving: if we automate things well, that extra time is ours
over and over again.

### Examples:

-   [Give files consistent names that are easy to match with wildcard
    patterns to make it easy to select them for
    looping.](shell.html#k:loop)
-   [Use the up-arrow key to scroll up through previous commands to edit
    and repeat them.](shell.html#k:loop)
-   [Use `history` to display recent commands, and `!number` to repeat a
    command by number.](shell.html#k:loop)
-   [Save commands in files (usually called shell scripts) for
    re-use.](shell.html#k:scripts)
-   [The version control system prevents people from overwriting each
    other's work by forcing them to merge concurrent changes before
    committing.](svn.html#k:basics)
-   [Put version numbers in programs' output to establish provenance for
    data.](svn.html#k:provenance)
-   [Put version numbers in programs' output to establish provenance for
    data.](python.html#k:provenance)
-   [Programs that explicitly test values' types are more brittle than
    ones that rely on those values' common
    properties.](funclib.html#k:filter)
-   [Design programs to catch both internal errors and usage
    errors.](quality.html#k:defensive)
-   [Use assertions to check whether things that ought to be true in a
    program actually are.](quality.html#k:defensive)
-   [When bugs are fixed, add assertions to the program to prevent their
    reappearance.](quality.html#k:defensive)
-   [Every test should be able to run independently: tests should *not*
    depend on one another.](quality.html#k:unit)
-   [Use a coverage analyzer to see which parts of a program have been
    tested and which have not.](quality.html#k:coverage)
-   [Initialize values from actual data instead of trying to guess what
    values could "never" occur.](setdict.html#k:examples)
-   [Put programs together piece by piece.](dev.html#k:assembly)
-   [Test programs with successively more complex
    cases.](dev.html#k:bugs)

Better Algorithms Beat Better Hardware
--------------------------------------

Of course, machine performance does matter, and that's where big idea
number six comes in. One of the greatest mathematical advances of the
Twentieth Century was the idea of *algorithmic complexity*: we can
estimate how the number of operations an algorithm will do increases as
the problem we're trying to solve grows larger, and use this to predict
a program's performance. It turns out that some algorithms slow down
gently as their inputs get larger, while others slow down so much that
even if the whole universe was one large computer, it couldn't solve any
problem big enough to be interesting. Faster chips help, but the real
key to speed is to focus on what we're doing, not what we're doing it
with.

But algorithms are nothing without data structures to operate on, just
as data structures are pointless without algorithms to manipulate them.
That's why the two topics are usually taught together: arrays with
loops, trees with recursion, and so on.

### Examples:

-   [Sets are stored in hash tables, which guarantee fast access for
    arbitrary keys.](setdict.html#k:storage)
-   [Problems that are described using matrices can often be solved more
    efficiently using dictionaries.](setdict.html#k:phylotree)
-   [Analyze algorithms to predict how a program's performance will
    change with problem size.](dev.html#k:performance)
-   [Better algorithms are better than better
    hardware.](dev.html#k:lazy)

The Tool Shapes the Hand
------------------------

Our last big idea is something that artisans have known for thousands of
years: the tool shapes the hand (and the mind). Building software
changes how you use software; making computers do new things changes
your understanding of what computers can do. That's why this course asks
you to write programs as well as use pre-existing ones: however
frustrating it may sometimes be, it's the only way to show you what's
possible.

### Examples:

-   [The best way to use the shell is to use pipes to combine simple
    single-purpose programs (filters).](shell.html#k:pipefilter)
-   [Letting users decide what files to process is more flexible and
    more consistent with built-in Unix commands.](shell.html#k:scripts)
-   [Use sets to store distinct unique values.](setdict.html#k:sets)
-   [Use dictionaries to store key-value pairs with distinct
    keys.](setdict.html#k:dict)
-   [Use a profiler to determine which parts of a program are
    responsible for most of its running time.](dev.html#k:profile)

Summary
-------

And that's it: that's pretty much what you need to know to get more done
with computers in less time. We hope you have as much fun learning to
think this way as we've had—thank you for listening, and may you always
see the world with the eyes of a child.
