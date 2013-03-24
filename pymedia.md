Basic Programming With Python and Images
========================================

Valerie Visual is studying human visual processing. More specifically,
she is studying the way the brain interprets missing or noisy
information. For one of her experiments, she wants to introduce
successively larger amounts of random noise into a series of pictures to
see when differnet people start to notice that something is wrong.

If Valerie only wanted to use one or two images, the simplest way to
create the images she needs might be to use a tool like Photoshop.
However, she wants to show each test subject several dozen images. What
she *doesn't* want to do is spend more time creating images than running
the actual experiments. She's going to have to learn how to program, and
that's what the next couple of chapters are about.

We will use a programming language called Python for our examples.
Python is free, reasonably well documented, and widely used in science
and engineering. Our main reason for choosing it, though, is that
newcomers find it easier to read than most other languages. It also
allows people to do useful things without having to master advanced
concepts like object-oriented programming.

Our programs will use a library for manipulating images that was
specifically written for novices. Many of the things we will do in five
or ten lines can actually be done in a single line by an experienced
programmer, but since our goal is to show you how to write programs of
your own, we will leave the training wheels on for now.

Basic Operations
----------------

### Understand:

-   How to use the Python interpreter interactively.
-   How to do basic arithmetic.
-   How to assign values to variables.

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

Types
-----

### Understand:

-   What data types are.
-   The differences between integers, floating-point numbers, and
    strings.
-   How to call a function.
-   Why computers shouldn't guess what people want.

Let's take another look at our program:

~~~~ {src="src/python/fahrenheit_to_kelvin.py"}
>>> temp_fahr = 98.6
>>> temp_kelvin = (temp_fahr - 32.0) * (5.0 / 9.0) + 273.15
>>> print "body temperature in Kelvin:", temp_kelvin
body temperature in Kelvin: 310.15
~~~~

Why have we written 5.0/9.0 instead of 5/9? Let's see what happens if we
take out the .0's:

~~~~ {src="src/python/fahrenheit_to_kelvin_int.py"}
>>> temp_fahr = 98.6
>>> temp_kelvin = (temp_fahr - 32) * (5 / 9) + 273.15
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
    <type 'int>
    >>> type(12.0)
    <type 'float>

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

Displaying Images
-----------------

### Understand:

-   How to open and display images.
-   What a library is.
-   Why programs are built out of libraries.
-   What a method is and how to call one.

Now that we can do basic arithmetic, let's look at some images:

    >>> from skimage import novice
    >>> flower = novice.open('flower.jpg')
    >>> flower.show()

This three-line program introduces one new idea per line. The first
statement asks Python to find a library called `skimage` (the SciKit
image processing library) and load something called `novice` from it.
The second statement asks `novice` to open a file called `flower.jpg`;
the result of that operation is assigned to a variable called `flower`.
The final statement asks the thing `flower` now points at to display
itself. If all has gone well, this should show a picture of the world's
cutest child ([Figure XXX](#f:flower)).

![The World's Cutest Child](img/pymedia/flower.jpg)

A [library](glossary.html#library) (or
[module](glossary.html#module)—for our purposes, the terms mean the same
thing) is one of the most important ideas in all of programming. No
language could possibly contain every single feature that everyone might
ever want. Even if it did, people's needs evolve over time, so an "all
inclusive" approach would mean constantly releasing new versions of the
language. Instead, every programming language provides a way for people
to define new tools themselves, and then load those tools into other
programs. In this case, someone wrote an image processing library called
`skimage`, and someone else (a graduate student named Mike Hansen) added
a sub-library to it called `novice` to provide an easy-to-use interface
for people who are just learning to program. When we write:

    from skimage import novice

we are asking Python to find the `skimage` library, search inside it for
`novice`, and load that into memory for use.

To get at the things `novice` contains, we then refer to them as
`novice.something`. This [dotted
notation](glossary.html#dotted-notation) was invented to deal with the
fact that people often choose the same names for different things. For
example, `skimage.novice`'s `open` looks for a file on disk and opens
that, but another library called `web` might provide something called
`open` that opened a connection to a web site. Using
`thing.subthing.subsubthing` to name things is exactly like using the
genus and species names to identify particular organisms.

### There's More Than One Way to Name It

You may have noticed above that we referred to `novice` as
`skimage.novice`. If we want to do this in our program, we could rewrite
it as:

    import skimage
    flower = skimage.novice.open('flower.jpg')
    flower.show()

which performs exactly the same operations as the original. What we
*can't* do is:

    import skimage
    flower = novice.open('flower.jpg')

or:

    from skimage import novice
    flower = skimage.novice.open('flower.jpg')

The first (`import skimage`) doesn't define anything in our program
called `novice`; it only defines `skimage`. The second does the reverse:
it defines `novice` *without* defining `skimage`.

And yes, we could do this:

    from skimage.novice import open
    flower = open('flower.jpg')

but it would be a very bad idea. Python actually has a built-in function
called `open` that opens arbitrary files so that the bytes in them can
be read. If we run the code shown immediately above, that built-in
function will be replaced by `skimage.novice`'s `open`, which will
probably break most programs (since most files aren't actually images).

With that out of the way, the second statement in:

    from skimage import novice
    flower = novice.open('flower.jpg')
    flower.show()

should be pretty easy to understand. It's a function call: it just
happens that the function being called is contained in the `novice`
library. Similarly, the expression `flower.show()` is another call that
asks whatever the variable `flower` points at to call the `show`
function it contains.

Another way to think about this program is shown in [Figure
XXX](#f:memory_model_image_display). After the first statement, Python
has created a variable called `novice` that refers to `skimage`'s
`novice` module. After the second statement, that module has loaded
bytes from an image file on disk into memory, wrapped an object around
them, and creatd a variable called `flower` to refer to that object.

![Memory Model of Image Display
Program](img/pymedia/memory_model_image_display.jpg)

### Summary

-   Write summary
-   Explain scope of imports: program session

Creating Programs
-----------------

### Understand:

-   How to create and run programs.

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

Of course, we can do this with our image display program as well:

    import skimage
    flower = skimage.novice.open('flower.jpg')
    flower.show()

When we save this as `showflower.py`, and run it as:

    $ python showflower.py

it displays our picture. explain how to kill it

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

-   Store programs in files whose names end in `.py`.
-   Run programs using `python name.py`.

Image Properties
----------------

### Understand:

-   How to inspect and modify the properties of images.
-   How to save images to files.

Let's take another look at the world's cutest child:

    >>> from skimage import novice
    >>> flower = novice.open('flower.jpg')
    >>> flower.show()

What else can we do besides display this image?

    >>> print flower.format
    JPEG
    >>> print flower.path
    /home/gvwilson/examples/flower.jpg
    >>> print flower.height
    180
    >>> print flower.width
    240

As this example shows, a picture object has
[properties](glossary.html#property): its format (JPEG, PNG, and so on),
the path to the file it was loaded from, and its height and width in
pixels. Some of these are unchangeable, so that we can confuse our
program by fooling it into thinking that a JPEG image is actually stored
as a PNG, or that it was loaded from a different file than it actually
was:

    >>> flower.format = 'PNG'
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AttributeError: can't set attribute
    >>> flower.path = '/profiles/alan-turing.jpg'
    Traceback (most recent call last):
      File "<stdin>", line 2, in <module>
    AttributeError: can't set attribute

Others, however, are changeable. For example, we can squish the image by
altering its height ([Figure XXX](#f:flower_squished)).

    >>> flower.height = 90
    >>> flower.show()

![Squishing a Picture](img/pymedia/flower_squished.jpg)

We can now save this picture to a new file if we want:

    >>> flower.save('squished.jpg')

When we do this, the object's `path` property is automatically updated
to reflect its new location:

    >>> print flower.path
    /home/gvwilson/examples/squished.jpg

And if we want to change its format, we can do that by saving it to a
file with the appropriate suffix:

    >>> flower.save('squished.png')
    >>> print flower.path
    /home/gvwilson/examples/squished.png

Now, suppose we want to create a thumbnail of a picture to put on a web
page. We want the thumbnail to be exactly 30 pixels wide to fit into a
table, and we want its height scaled proportionally. Here's what we
could do:

    from skimage import novice
    picture = novice.open('mac.jpg')
    new_height = picture.height * 30 / picture.width
    picture.height = new_height
    picture.width = 30
    picture.save('thumb-mac.jpg')

Colors
------

### Understand:

-   How computers represent colors.
-   How to create images from scratch.
-   How to change the color of every pixel in an image.

Before we go any further, we need to talk about how computers represent
colors. The most common scheme, called "RGB", stores red, green, and
blue values for each pixel in an image. This is an additive color model:
the color we see is the sum of the individual color values, each of
which can range between 0 and 255. Why 255? Because computer memory is
organized into 8-bit bytes, and 255 (11111111 in base 2) is the largest
integer that can be represented in one byte.

In RGB, black is (0, 0, 0), i.e., nothing of any color. White is the
maximum value of all three colors, or (255, 255, 255). We can think of
this color model is as a cube ([Figure XXX](#f:color_cube)).: the three
axes represent the primary colors, while secondary colors are
combinations of maximum values, and each actual color is a coordinate in
this cube.

![A Color Cube](img/pymedia/color_cube.png)

Let's have a look at how the three primary colors actually appear:

    from skimage import novice
    all_red = novice.new((200, 200), (255, 0, 0))
    all_red.show()
    all_green = novice.new((200, 200), (0, 255, 0))
    all_green.show()
    all_blue = novice.new((200, 200), (0, 0, 255))
    all_blue.show()

![Primary Colors](img/pymedia/primary_colors.png)

This program produces the three images shown in [Figure
XXX](#f:primary_colors) in turn. The most important thing about it,
though, is actually where the parentheses are. Just as in math, programs
often use parentheses to group values together. Here, we are using them
to group (200, 200) together as the size of the image in pixels, and
(255, 0, 0) together as an RGB color value. The designer of this library
*could* have let us pass these values without the grouping, as in:

    novice.new(200, 200, 255, 0, 0)

but as the number of values grows, it quickly becomes difficult to keep
track of which ones belong together. A group of parenthesized values is
called a [tuple](glossary.html#tuple); we can assign tuples to
variables, and then use those variables in our programs to make our code
easier to read:

    from skimage import novice
    image_size = (200, 200)
    all_red = novice.new(image_size, (255, 0, 0))
    all_red.show()
    all_green = novice.new(image_size, (0, 255, 0))
    all_green.show()
    all_blue = novice.new(image_size, (0, 0, 255))
    all_blue.show()

One nice side effect of this is that it also makes our programs easier
to change. If we want our images to be 300 pixels across instead of 200,
we only have to change the value of `image_size`, and everything else
just works. This is a basic rule of good program design: any given piece
of information should be stored in one place, once, so that any change
requires only one change in one place.

`skimage.novice` lets us change image colors using properties as well.
If we don't initially specify a color for an image, the image's pixels
are all set to black:

    from skimage import novice
    image_size = (200, 200)
    picture = novice.new(image_size)

We can now change the red, green, or blue values of all its pixels like
this ([Figure XXX](#f:color_properties)):

    picture.red   = 128
    picture.green = 192
    picture.blue  = 255
    picture.show()

![Color Properties](img/pymedia/color_properties.png)

Manipulating Pixels
-------------------

Changing the color of the entire image at once is useful for creating
backgrounds, but most pictures have more detail than that. If we want to
change the color of a single pixel, we need a way to refer to it. In
Python and most other languages, we do that by providing an
[index](glossary.html#index), which is just the coordinates of the pixel
we want to access. To create a red image with a single white pixel in
the lower-left corner, we would do this:

    from skimage import novice
    block = novice.new((10, 10), (255, 0, 0))
    block[0, 0] = (255, 255, 255)
    block.show()

The first thing to notice about this example is that the lower-left
corner is at (0, 0), not at (1, 1). Programming languages derived from C
(which includes C++, Java, Python, Perl, and Ruby) count from 0: the
first five indices into anything are 0, 1, 2, 3, and 4. Some other
languages (notably Fortran, MATLAB, and R) count from 1. The latter is
more sensible—nobody says, "Zero, one, two, three, four," when counting
their fingers—but we're stuck with the former for programming.

The second thing to notice about this example is that a 10×10 image is
hard to see, and a single white pixel is almost invisible. Let's try
this:

    from skimage import novice
    block = novice.new((10, 10), (255, 0, 0))
    block[0, 0] = (255, 255, 255)
    block.inflation = 10
    block.show()

An image's `inflation` property tells the library how large to make each
pixel when displaying or saving the image. This doesn't change how many
pixels there actually are, or how they're indexed; it's purely a
convenience to help us see what we're doing.

What if we want to make the upper-right pixel white instead? We happen
to know that our image is 10×10, so we could do this:

    block[9, 9] = (255, 255, 255)

The upper-right index is (9, 9) because we're counting from 0: if the
image is ten pixels across, its X coordinates are 0..9. This works in
this specific case, but it's a bad long-term solution: if someone
changes the size of the image, the upper-right pixel probably won't be
at (9, 9) any longer, and we don't want to have to check our program
line-by-line to find things like this.

Here's one better solution:

    block_width = 10
    block_height = 10
    block = novice.new((block_width, block_height), (255, 0, 0))
    block[block_width - 1, block_height - 1] = (255, 255, 255)

If someone changes the block's height or width now, the index expression
in the last line will automatically adjust. This version of the program
also makes the image's size a lot easier to find: instead of being
buried inside a function call, `block`'s height and width are identified
by name.

We can improve this program even further like this:

    block_width = 10
    block_height = 10
    red = (255, 0, 0)
    white = (255, 255, 255)
    block = novice.new((block_width, block_height), red)
    block[block_width - 1, block_height - 1] = white

and then go one step further like this:

    block_width = 10
    block_height = 10
    red = (255, 0, 0)
    white = (255, 255, 255)
    block = novice.new((block_width, block_height), red)
    block[-1, -1] = white

Unlike most languages, Python is happy with negative indices: it uses
them to count backward from the ends of things, rather than forward from
the start ([Figure XXX](#f:negative_indices)). Once you get used to it,
it makes programs much easier to read—as the examples above show, the
`-1` can be easy to miss when it's tacked onto the end of a long
expression.

![Negative Indices](img/pymedia/negative_indices.png)

Now, what if we want to put a white border around our image? We could do
this:

    block[0, 0] = white
    block[0, 1] = white
    block[0, 2] = white
    ...
    block[0, 9] = white

and then repeat it for the other three sides but that would be a lot of
work to type in, we'd probably make mistakes along the way, and if the
image size changes, we'll have to add or remove dozens or hundreds of
lines. Here's a better way:

    block[0, :]  = white
    block[-1, :] = white
    block[:, 0]  = white
    block[:, -1] = white

As you can probably guess, ':' on its own means "all indices"—it's a
[wildcard](shell.html#pipefilter), just like '\*' in filenames in the
shell. Behind the scenes, the computer is still executing something like
our original code—after all, each of the pixels on the border does need
to be modified somehow—but:

1.  this code is much faster to write,
2.  much more likely to be correct, and
3.  once the computer knows it's supposed to update all the pixels in a
    row or column, it can probably do it faster than we could by hand.
4.  

':' on its own is actually a special case of something much more general
called a [slice](glossary.html#slice). Let's modify the program like
this:

    from skimage import novice
    block_width = 200
    block_height = 200
    green = (0, 255, 0)
    white = (255, 255, 255)
    block = novice.new((block_width, block_height), green)
    block[0:40, 0:40] = white

When we display the image that this program creates, it is a single
white tile in the lower-left of a green background ([Figure
XXX](#f:single_tile)):

![A Single Tile](img/pymedia/single_tile.png)

You can probably guess that the expression `0:40` refers to a range of
pixels. What you might not guess is that the range goes from index 0 to
index 39 inclusive, i.e., from the lower limit up to, but not including,
the upper limit. It may seem odd not to include the upper limit; the
usual justifications are:

1.  When the ranges `lower:middle` and `middle:upper` are joined
    together, the pixel at coordinate `middle` is only included once.
2.  If the axis in question has `length` pixels, the expression
    `0:length` refers to each pixel exactly once.

Command-Line Arguments
----------------------

### Understand:

-   How to work with command-line arguments.
-   That slicing works in many places.

Let's go back to our thumbnail creation program for a moment. It would
be much more useful if we could create a thumbnail of any image we
wanted without having to edit the program each time to change the name
of the file. What we want is something like this:

    $ ls *.jpg
    mac.jpg
    $ python thumbnail mac.jpg
    $ ls *.jpg
    mac.jpg    thumb-mac.jpg

To make this work, we need a way to get filenames from the command line
into our program. To do that, we need to use another library called
`sys` (short for "system"). It defines constants to tell us what version
of Python we're using, what operating system we're running on, and so
on:

    >>> import sys
    >>> print sys.version
    2.7 (r27:82525, Jul  4 2010, 09:01:59) [MSC v.1500 32 bit (Intel)]
    >>> print sys.platform
    win32

The most commonly-used element of `sys`, though, is `sys.argv`, which
holds the [command-line arguments](glossary.html#command-line-arguments)
used to run the program. These are accessed using indices, just like
individual pixels; the biggest differences are that `sys.argv` is
one-dimensional instead of two-dimensional, and that its values are
strings rather than pixels. The name of the script itself is in
`sys.argv[0]`; all the other arguments are put in `sys.argv[1]`,
`sys.argv[2]`, and so on. For example, here's a program that does
nothing except print its first three command-line arguments:

    import sys
    print 'location 0:', sys.argv[0]
    print 'location 1:', sys.argv[1]
    print 'location 2:', sys.argv[2]

If we run save this code in a file called `three.py`, and run it like
this:

    $ python three.py alpha beta

it prints:

    location 0: three.py
    location 1: alpha
    location 2: beta

However, if we run it with no arguments, or only one, we get this:

    $ python three.py
    location 0: /Users/gwilson/three.py
    location 1:
    Traceback (most recent call last):
      File "/Users/gwilson/three.py", line 3, in <module>
        print 'location 1:', sys.argv[1]
    IndexError: list index out of range

The problem is that `sys.argv[1]` doesn't exist, and Python won't let us
read a value that isn't there. It's exactly like the undefined variables
we encountered at the start of this chapter.

Let's ignore that problem for now and go back to our thumbnail creator.
Here's how we can make it work for an arbitrary file:

    import sys
    from skimage import novice

    FIXED_WIDTH = 30

    filename = sys.argv[1]
    picture = novice.open(filename)
    new_height = picture.height * fixed_width / picture.width
    picture.height = new_height
    picture.width = fixed_width
    picture.save('thumb-' + filename)

Let's walk through it piece by piece:

-   We start by importing the libraries we need. `import` statements can
    actually be anywhere in the program, but it's considered good style
    to put them at the top, as it makes it easy for people to see what
    the program depends on.
-   We give the fixed width we want thumbnails to have a name, so that
    we don't have to scatter the number 30 throughout the program.
    Values that are meant to be constants are usually written in UPPER
    CASE; again, it's not a requirement, but it's what most people do,
    so by sticking to this convention you will make it easier for other
    people to understand your code.
-   The name of the image to be thumbnailed is supposed to be the
    program's single command-line argument, which means it will be in
    `sys.argv[1]`. (Remember, the program's name is in `sys.argv[0]`.)
    We could just use `sys.argv[1]` everywhere, but assigning the value
    to the variable `filename` makes our program easier to follow.
-   We calculate the picture's new size and resize the picture as
    before.
-   Finally, we create the new filename by concatenating `'thumb-'` and
    the original filename, and save the thumbnail to that file.

Repeating Things
----------------

### Understand:

-   How to repeat things using a loop.
-   That the loop variable takes on a different value each time through
    the loop.
-   How to tell what statements are in the body of a loop.

Computers are useful because they can do lots of calculations on lots of
data, which means we need a concise way to represent multiple steps.
(After all, writing out a million additions would take longer than doing
them.) Let's start by writing a program called `show.py` that displays
its command-line arguments one by one:

    import sys
    for arg in sys.argv:
        print arg

Here's what happens when we run it:

    $ python show.py first second third
    show.py
    first
    second
    third

The keywords `for` and `in` are used to create a [for
loop](glossary.html#for-loop). Just like a [loop in the
shell](shell.html#loop), a `for` loop in Python repeats one or more
instructions for each value in some set. The indented line is called the
[body](glossary.html#loop-body) of the loop: it's the command that
Python executes repeatedly. The variable `arg` is sometimes called the
[loop variable](glossary.html#loop-variable). There's nothing special
about its name: we could equally well have called it `something`. What's
important is that the `for` loop repeatedly assigns a value to it, then
executes the loop body one more time.

Python always uses indentation to show what's in the body of a loop (or
anything else—we'll see other things that have bodies soon). This means
that:

    for arg in sys.argv:
        print arg
        print "all done"

and:

    for arg in sys.argv:
        print arg
    print "all done"

are different programs. The first one would print:

    show.py
    all done
    first
    all done
    second
    all done
    third
    all done

because the statement `print "all done"` is inside the loop body. The
second is probably what we actually want, as it prints:

    show.py
    first
    second
    third
    all done

because the final `print` is outside the loop.

### Why Indentation?

Most other languages use keywords like `do` and `done` or `begin` and
`end` to show what's in the body of a loop, or even curly braces '{}'.
Python uses indentation because studies done in the 1970s and 1980s
showed that's what people actually pay attention to. If we write
something as:

    for value in data
    begin
        print value
    print "done"
    end

then most people reading the code in a hurry will "see" the second
`print` statement as being outside the loop.

Let's go back and teach our thumbnail program how to process multiple
files at once:

    import sys
    from skimage import novice

    FIXED_WIDTH = 30

    for filename in sys.argv:
        picture = novice.open(filename)
        new_height = picture.height * fixed_width / picture.width
        picture.height = new_height
        picture.width = fixed_width
        picture.save('thumb-' + filename)

Almost everything has stayed the same: the only change is that instead
of assigning `sys.argv[1]` to `filename`, we're using a loop to assign
it each value in `sys.argv` in turn. Let's try running it:

    $ python thumbnail.py flower.jpg mac.jpg
    Traceback (most recent call last):
    ...several lines of error message...
    IOError: cannot identify image file

Whoops: the first time through the loop, `filename` is assigned
`sys.argv[0]`, which is the name of the Python program itself. The
`novice.open` call then tries to open a Python program (i.e., a text
file) as if it were an image. Unsurprisingly, that doesn't work.

How can we fix this? By using a slice that starts at index 1 and runs to
the end of the list of filenames:

    import sys
    from skimage import novice

    FIXED_WIDTH = 30

    for filename in sys.argv[1:len(sys.argv)]:
        picture = novice.open(filename)
        new_height = picture.height * fixed_width / picture.width
        picture.height = new_height
        picture.width = fixed_width
        picture.save('thumb-' + filename)

Remember, a slice starts at its low index, and goes up to, but not
including, its upper index. The expression `stuff[1:len(stuff)]` is
therefore everything in `stuff` except the element at location zero
([Figure XXX](#f:all_but_the_first)):

![All But The First Element](img/pymedia/all_but_the_first.png)

We can make this even simpler. If we don't specify the lower end of a
slice, it defaults to 0, so `stuff[:3]` is elements 0, 1, and 2 of
`stuff`. Similarly, if we don't specify the slice's upper end, it
defaults to the end, so `stuff[3:]` is elements 3, 4, 5, and so on to
the end. In particular, `stuff[1:]` is everything in `stuff` except the
element at index 0, so we can rewrite our thumbnailer one more time as:

    import sys
    from skimage import novice

    FIXED_WIDTH = 30

    for filename in sys.argv[1:]:
        picture = novice.open(filename)
        new_height = picture.height * fixed_width / picture.width
        picture.height = new_height
        picture.width = fixed_width
        picture.save('thumb-' + filename)

### One Thing, Many Uses

Slices are a good example of a powerful idea in program design: if
something works in one place, it ought to work everywhere. For example,
if we want to select the first four characters from a string, you
shouldn't be surprised that we do it like this:

    >>> full_name = 'Alan Turing'
    >>> first_name = full_name[:4]
    >>> print first_name
    Alan

or that if we want to print each character from the string on a line of
its own, we use:

    >>> for char in 'Alan':
    ...     print char
    A
    l
    a
    n

Here's something else we can do with a loop:

    from skimage import novice

    picture = novice.open('mac.jpg')
    picture.show()
    for pixel in picture:
        pixel.red = pixel.red / 2
    picture.show()

[Figure XXX](#f:less_red) shows the original and modified images side by
side. The second version looks bluish-green because the amount of red in
each pixel has been cut in half. That's what the `for` loop has done:
each time through the loop, `pixel` has been assigned the next pixel in
the image, and the statement:

        pixel.red = pixel.red / 2

has half the original value of the pixel's `red` property and assigned
it back to the pixel.

![Reducing the Red](img/pymedia/less_red.png)

What happens if we try to double the red instead?

    >>> picture = novice.open('mac.jpg')
    >>> for pixel in picture:
    ...    pixel.red = pixel.red * 2
    ...

    Traceback (most recent call last):
    ...several lines of error message...
    ValueError: Expected an integer between 0 and 255, but got 294 instead!

Just as Python won't let us use an index that's out of range,
`skimage.novice` won't let us assign a color value that's out of the
range from 0 to 255. If we want to make sure the value is in that range,
we can do this instead:

    picture = novice.open('mac.jpg')
    for pixel in picture:
        pixel.red = min(255, pixel.red * 2)

This works, and gives the result shown in [Figure XXX](#f:more_red).

![Increasing the Red](img/pymedia/more_red.png)

### Summary

-   Use `for variable in something:` to loop over the parts of
    something.
-   The body of a loop must be indented consistently.
-   The parts of a string are its characters; the parts of an image are
    its pixels.

Making Choices
--------------

### Understand:

-   How to choose what statements to execute using conditionals.
-   How to combine conditional tests.
-   What an in-place operator is.

Using the `min` function is one way to clip values. Another is to use a
[conditional](glossary.html#conditional) statement. Let's start with a
simple example:

    if 5 > 0:
        print '5 is greater than 0'

    if 5 < 0:
        print '5 is less than 0'

When we run this program, it prints:

    5 is greater than 0

The logic is fairly easy to follow. The keyword `if` is followed by an
expression. If that expression is true, Python executes the indented
block of code, but if the expression is false, it doesn't. In this case,
since 5 actually is greater than 0, the first `print` statement is run,
but not the second.

Now let's try this:

    for char in 'GATTACA':
        if char == 'A':
            print 'found an A'
    found an A
    found an A
    found an A

Python uses a double equals sign '==' to test for equality (because the
single equals sign '=' is used for assignment). Each time through the
loop above, it compares the current value of `char` to the character
'A'. When the two are equal, it prints a message; since the letter
appears three times in 'GATTACA', the message is printed three times.

All right, how about this?

    VOWELS = 'AEIOU'
    num_vowels = 0
    num_other = 0
    for char in 'GATTACA':
        if char in VOWELS:
            num_vowels = num_vowels + 1
        else:
            num_other = num_other + 1
    print num_vowels, 'vowels'
    print num_other, 'other characters'
    3 vowels
    4 other characters

This little program introduces two new language features. The first is
the `in` operator, which, as its name suggests, tests whether one value
is in another. In this case, we're using it to see if the current
character is in our list of vowels.

The other feature is the keyword `else`, which is used to introduce an
alternative to an `if`. Here, if a character is a vowel, Python
increments `num_vowels`. If that test fails—i.e., if the character
*isn't* in `VOWELS`—Python executes the both of the `else` and
increments `num_other` instead.

We can make this program a bit more readable by writing the body of the
loop like this:

    for char in 'GATTACA':
        if char in VOWELS:
            num_vowels += 1
        else:
            num_other += 1

The notation `x += 1` means, "Add one to the variable `x`." This is
called an [in-place operator](glossary.html#in-place-operator); we can
similarly use `x += 5` to add 5 to `x`, `x *= 3` to triple it, and so
on. It may seem like a small saving, but it actually prevents a lot of
bugs by eliminating duplicated code.

With conditionals in hand, let's go back and rewrite our reddening
program:

    picture = novice.open('mac.jpg')
    for pixel in picture:
        if pixel.red < 128:
            pixel.red *= 2
        else:
            pixel.red = 255

Lists
-----

### Understand:

-   How to store many related values in a list.
-   How to use a loop to operate on the values in a list.
-   That programs should be tested on small, simple cases.

It's time to double back and have a closer look at `sys.argv`. It's
obviously not an image; instead, it's a [list](glossary.html#list). To
start our exploration of lists, let's run an interpreter and try this:

~~~~ {src="src/python/sum_values.py"}
>>> data = [1, 3, 5]
>>> for value in data:
...     print value
...
1
3
5
~~~~

`[1, 3, 5]` is a list: a single object that stores multiple values
([Figure XXX](#f:simple_list)). Just as a `for` loop over an open file
reads lines from that file one by one and assigns them to the loop
variable, a `for` loop over a list assigns each value in the list to the
loop variable in turn.

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

More About Lists
----------------

### Understand:

-   That lists can be modified in place.
-   How to access arbitrary elements in a list.
-   What an out-of-bounds error is.
-   How to generate a list of legal indices for a list.
-   When to use short or long variable names.

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

The solution to our problem is, not surprisingly, to index the list.
Here are some examples:

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

Coordinates
-----------

### Understand:

-   Write something

Let's try an experiment in two parts. First, run this program and look
at the image files it creates:

    from skimage import novice

    BASE    = 128
    STEP    = 4
    SPACING = 4
    NUMBER  = 6
    GRAY    = (BASE, BASE, BASE)
    SIZE    = 200

    for color in range(BASE + STEP, BASE + NUMBER * STEP, STEP):
        image = novice.new((SIZE, SIZE), GRAY)
        image[::SPACING, ::SPACING] = (color, color, color)
        filename = 'step-' + str(color) + '.png'
        image.save(filename)

These files have named like `step-132.png`, `step-136.png`, and so on.
Each one has white pixels spaced evenly across a gray background, with
the white slowly getting whiter. Images like these are sometimes used in
vision tests, since different spacings and colorings are noticeable to
different people.

Having told you that, we've spoiled the second part of our experiment,
which is to see how much knowing what a program does helps you figure
out how it works. As you might suspect, the answer is, "A lot." Let's go
through this one.

The constants at the top don't tell us much, although `GRAY` is
obviously an RGB color value and `SIZE` is (probably) an image size.
Next is our loop: given the name of its index variable, `color`, we can
guess that we're looping over colors, and sure enough, two lines down,
we see `(color, color, color)`, which is creating a shade of gray
defined by the current value of `color`.

Backing up a line, we're creating a `SIZE`×`SIZE` image using
`novice.new` and setting all its pixels to the fixed color `GRAY`. We're
then—hm. What does `::SPACING` do? If it was `:SPACING` (with a single
colon), it would mean, "From the start up to `SPACING`," but there's a
double colon there.

The answer is that Python ranges can actually have three parts: the
start, the end, and the [stride](glossary.html#stride), which is the
separation between each entry. We can find out more about this inside
the interpreter using the built-in `help` function:

    >>> help(range)
    range(...)
        range([start,] stop[, step]) -> list of integers
        
        Return a list containing an arithmetic progression of integers.
        range(i, j) returns [i, i+1, i+2, ..., j-1]; start (!) defaults to 0.
        When step is given, it specifies the increment (or decrement).
        For example, range(4) returns [0, 1, 2, 3].  The end point is omitted!
        These are exactly the valid indices for a list of 4 elements.

However, that doesn't tell us that strides also work in indices: that's
something we just have to know.

So, going back to our program, the key lines are:

    for color in range(BASE + STEP, BASE + NUMBER * STEP, STEP):
        ...create image...
        image[::SPACING, ::SPACING] = (color, color, color)

The loop is going from `BASE + STEP` up to `BASE + NUMBER * STEP` in
increments of `STEP`. `BASE` is 128—our initial shade of gray. `STEP` is
4: that's the increment each time we go around the loop. And `NUMBER` is
how many we're doing, so this loop is creating a bunch of images with
the same gray background, but whiter and whiter points spaced at equal
intervals across them.

### Summary

-   Write something

Nesting Loops
-------------

### Understand:

-   That loops can be nested to operate on combinations of items.
-   That the range of inner loops can depend on the state of outer
    loops.
-   That doing this allows programs to handle more cases without
    changes.

Explain nested loops in terms of triangles on images.

Cutting Up Images
-----------------

We now have everything we need to solve Valerie's original problem,
which is to cut an image into pieces and colorize those pieces in
different ways. First, let's figure out what our input file is, and how
many pieces we want along the X and Y axes:

    import sys
    from skimage import novice

    if len(sys.argv) != 4:
        print 'Expected source filename and number of tiles on X and Y'
        sys.exit(1)

    original_filename = sys.argv[1]
    tile_x = int(sys.argv[2])
    tile_y = int(sys.argv[3])

After importing our libraries, this program checks that it has the right
number of arguments. (Once again, the number is 4 because `sys.argv[0]`
is the name of the program.) If something is wrong, the program prints
an error message and exits. explain why 1 It then stores the name of the
source file in `original_filename`, and converts the other two arguments
to integers.

    original = novice.open(original_filename)
    size_x = original.width / tile_x
    size_y = original.height / tile_y
    if (size_x == 0) or (size_y == 0):
        print 'Cannot create that many tiles.'
        sys.exit(1)

Here, the program opens the source file and figures out how large each
tile is going to be along the X and Y axes. Once again, it checks to
make sure the answer is reasonable: if, for example, we ask for 2000
tiles along an axis that's 200 pixels large, the integer-over-integer
division will set the size to zero, and we should exit right away.

    for x in range(0, size_x * tile_x, size_x):
        for y in range(0, size_y * tile_y, size_y):
            tile = novice.new((size_x, size_y))
            tile[:, :] = original[x:x+size_x, y:y+size_y]
            tile_filename = str(x) + '-' + str(y) + '-' + original_filename
            tile.save(tile_filename)

This nested loop creates our slices. The loop variables `x` and `y` are
coordinates of the lower-left corners of the slices; for each
combination of their values, we create a new blank image (which we
assign to `tile`), then copy over a section of the original image. We
then construct a filename like `100-140-bicycle.jpg` and save that tile.
