1.  [The Grid](#s:grid)
2.  [Aliasing](#s:alias)
3.  [Randomness](#s:random)
4.  [Neighbors](#s:neighbors)
5.  [Handling Ties](#s:ties)
6.  [Putting It All Together](#s:assembly)
7.  [Bugs](#s:bugs)
8.  [Refactoring](#s:refactor)
9.  [Testing](#s:test)
10. [Performance](#s:performance)
11. [Profiling](#s:profile)
12. [Speeding It Up](#s:fail)
13. [A New Beginning](#s:lazy)
14. [Summing Up](#s:summary)

Ethan Ecosystem is studying the way pollutants spreads through fractured
rock ([Figure XXX](#f:invasion_percolation)). To simulate this, he wants
to use a model called [invasion
percolation](glossary.html#invasion-percolation), which has been used to
model many other phenomena as well.

![Invasion Percolation](img/python/invasion_percolation.png)

In its simplest form, invasion percolation represents the rock that the
pollutant is spreading through as a two-dimensional grid of square cells
filled with random values. The algorithm starts by marking the center
cell as being polluted, then looks at that cell's four neighbors
([Figure XXX](#f:invasion_percolation_algorithm)). The one with the
lowest value is the one that has the least resistance to the spread of
the pollutant, so the algorithm marks that as being filled as well. It
then looks at the six neighbors of the entire filled region, and once
again finds and marks the one with the lowest value. This process
continues until a certain percentage of cells have been filled (i.e.,
there's no more pollutant), or until the pollution reaches the boundary
of the grid.

![Invasion Percolation
Algorithm](img/python/invasion_percolation_algorithm.png)

If two or more cells on the boundary are tied equal for the lowest
value, the algorithm can either fill them all in simultaneously, or pick
one at random and fill that in. Either way, the fractal this algorithm
produces will tell Ethan how quickly the pollutant will spread, and how
much of the rock will be contaminated.

But if Ethan wants to look at the statistical properties of these
fractals, he will need to do many simulation on large grids. That means
his program has to be fast, so this chapter will look at three things:

1.  How do we build a program like this in the first place?
2.  How do we tell if it's working correctly?
3.  How do we speed it up?

The order of the second and third steps is important. There's no point
speeding something up if it isn't working correctly, or if we don't know
whether it's working correctly or not. Once we know how to tell, on the
other hand, we can focus on performance improvement, secure in the
knowledge that if one of our bright ideas breaks things, our program
will let us know.

The Grid
--------

### Understand:

-   How to represent a two-dimensional grid using a list of lists.
-   How to leave markers in code to keep track of tasks that still need
    to be done.

Let's start by looking at how to represent a two-dimensional grid in
Python. By "two-dimensional", we mean something that's indexed by X and
Y coordinates. Our grid is discrete: we need to store values for
locations (1, 1), (1, 2), and so on, but not locations like (1.512,
7.243).

### Why Not Use a NumPy Array?

explain: pedagogic value, and we're going to throw it all away anyway

Each cell in the grid stores a single random value representing the
permeability of the rock. We also need a way to mark cells that have
been filled with pollutant. Once a cell has been filled, we don't care
about its value any longer, so we can use any number that isn't going to
appear in the grid otherwise as a marker to show which cells have been
filled. For now, we'll use -1.

Note that this means we're using integers in two ways. The first is as
actual data values; the second is as flags to represent the state of a
cell. This is simple to do, but if we ever get data who values happen to
contain the numbers that we're using to mark filled cells, our program
will misinterpret them. Bugs like this can be very hard to track down.

Before we go any further, we also have to make some decisions about the
shapes of our grids. First, do grids always have to be square, i.e.,
N×N, or can we have rectangular grids whose X and Y sizes are different?
Second, do grids always have to be odd-sized, so that there's a unique
center square for us to fill at the start, or can we have a grid that is
even in size along one or both axes?

The real question is, how general should we make the first version of
this program—indeed, of *any* program? Some people say, "Don't build it
until you need it," while others say, "A week of hard work can sometimes
save you an hour of thought." Both sayings are true, but as in any other
intellectually demanding field, knowing what rules to apply when comes
with experience, and the only way to get experience is to work through
many examples (and make a few mistakes). Again, let's do the simple
thing for now, and assume that grids are always square and odd-sized.

Now, how are we going to store the grid? One way is to use a [nested
list](python.html#g:nested-list). This lets us use double subscripts to
refer to elements, which is really what we mean by "two dimensional".
Here's a piece of code that builds a grid of 1's as a list of lists;
we'll come back later and show how to fill those cells with random
values instead:

~~~~ {src="src/programming/grid_ones.py"}
# Create an NxN grid of random integers in 1..Z.
assert N > 0, "Grid size must be positive"
assert N%2 == 1, "Grid size must be odd"
grid = []
for x in range(N):
    grid.append([])
    for y in range(N):
        grid[-1].append(1) # FIXME: need a random value
~~~~

The first thing we do is check that the grid size `N` is a sensible
value. We then assign an empty list to the variable `grid`. The first
time through the outer loop, we append a new empty list to the outer
list. Each pass through the inner loop, we append the value 1 to that
inner list ([Figure XXX](#f:building_grid)). We go back through the
outer loop to append another sub-list, which we grow by adding more 1's,
and so on until we get the grid that we wanted.

![Building the Grid](img/python/building_grid.png)

### FIXME

At any point when writing a program, there may be half a dozen things
that need to be done next. The problem is, we can only write one at a
time. It's therefore a common practice to add comments to the code to
remind ourselves of things we need to come back and fill in (or tidy up)
later. It's equally common to start such comments with a word like
"FIXME" or "TODO" to make them easier to find with tools like
[`grep`](shell.html#s:find).

### Summary

-   Get something simple working, then start to add features, rather
    than putting everything in the program at the start.
-   Leave FIXME markers in programs as you are developing them to remind
    yourself what still needs to be done.

Aliasing
--------

### Understand:

-   How list aliasing can cause subtle errors in programs.

Before we go further with our list-of-lists implementation, we need to
revisit the issue of [aliasing](python.html#s:alias) and look at some
bugs that can arise when your programs uses it. Take another look at the
list-of-lists in [Figure XXX](#f:building_grid). A single list serves as
the structure's spine, while the sublists store the actual cell values.

Here's some code that tries to create such a structure but gets it
wrong:

~~~~ {src="src/programming/alias_buggy.py"}
# Incorrect code
assert N > 0, "Grid size must be positive"
assert N%2 == 1, "Grid size must be odd"
grid = []
EMPTY = []
for x in range(N):
  grid.append(EMPTY)
  for y in range(N):
    grid[-1].append(1)
~~~~

The only change we've made is to introduce a variable called `EMPTY` so
that we can say, "Append EMPTY to the grid" in our loop. How can this be
a bug? Aren't meaningful variable names supposed to be a good thing?

To see what's wrong, let's trace the execution of this program. We start
by assigning an empty list to the variable `grid`. We then assign
another empty list to the variable `EMPTY`. In the first pass through
our loop, we append the empty list pointed to by `EMPTY` to the list
pointed to by `grid` to get the structure shown in [Figure
XXX](#f:alias_bug). We then go into our inner loop and append a 1 to
that sublist. Going around the inner loop again, we append another 1,
and another. We then go back to the outer loop and append `EMPTY` again.

![Aliasing Bug](img/python/alias_bug.png)

The structure shown on the left is now broken: both cells of the list
pointed to by `grid` point to the same sublist, because `EMPTY` is still
pointing to that list, even though we've changed it. When we go into the
inner loop the second time, we're appending 1's to the same list that we
used last time.

### Debugging With Pictures

Aliasing bugs are notoriously difficult to track down because the
program isn't doing anything illegal: it's just not doing what we want
in this particular case. Many debugging tools have been built over the
last thirty years that draw pictures of data structures to show
programmers what they're actually creating, but none has really caught
on yet, primarily because pictures of the objects and references in real
programs are too large and too cluttered to be comprehensible. As a
result, many programmers wind up drawing diagrams like [Figure
XXX](#f:alias_bug) by hand while they're debugging.

### Summary

-   Draw pictures of data structures to aid debugging.

Randomness
----------

### Understand:

-   That computer-generated "random" numbers aren't actually random.
-   How to create pseudo-random numbers in a program.
-   How to re-generate a particular sequence of pseudo-random numbers.

Now that we have a grid, let's fill it with random numbers chosen
uniformly from some range 1 to Z. We should check the science on this,
as there was nothing in our original specification that said the values
should be uniformly distributed, but once again we'll do something
simple, make sure it's working, and then change it later. Our code looks
like this:

~~~~ {src="src/programming/random_grid.py"}
from random import seed, randint
assert N > 0, "Grid size must be positive"
assert N%2 == 1, "Grid size must be odd"
assert Z > 0, "Range must be positive"
seed(S)
grid = []
for x in range(N):
    grid.append([])
    for y in range(N):
        grid[-1].append(randint(1, Z))
~~~~

The changes are pretty small: we import a couple of functions from a
library, check that the upper bound on our random number range makes
sense, initialize the random number generator, and then call `randint`
to generate a random number each time we need one.

To understand these changes, let's step back and look at a small program
that does nothing but generate a few seemingly random numbers:

~~~~ {src="src/programming/random_calls.py"}
from random import seed, randint
seed(4713983)
for i in range(5):
    print randint(1, 10),
7 2 6 6 5
~~~~

The first step is to import functions from the standard Python random
number library called (unsurprisingly) `random`. We then initialize the
sequence of "random" numbers we're going to generate—you'll see in a
moment why there are quotes around the word "random". We can then call
`randint` to produce the next random number in the sequence as many
times as we want.

Pseudo-random number generators like the one we're using have some
important limitations, and it's important that you understand them
before you use them in your programs. Consider this simple "random"
number generator:

~~~~ {src="src/programming/random_generator.py"}
base = 17  # a prime
value = 4  # anything in 0..base-1
for i in range(20):
    value = (3 * value + 5) % base
    print value,
0 5 3 14 13 10 1 8 12 7 9 15 16 2 11 4 0 5 3 14
~~~~

It depends on two values:

1.  The *base*, which is a prime number, determines how many integers
    we'll get before the sequence starts to repeat itself. Computers can
    only represent a finite range of numbers, so sooner or later, any
    supposedly random sequence will start to repeat. Once they do,
    values will appear in exactly the same order they did before.
2.  The *seed* controls where the sequence starts. With a seed of 4, the
    sequence starts at the value 0. Changing the seed to 9 shifts the
    sequence over: we get the same numbers in the same order, but
    starting from a different place. We'll use this fact later one when
    it comes time to test our invasion percolation program.

These numbers aren't actually very random at all. For example, did you
notice that the number 6 never appeared anywhere in the sequence? Its
absence would probably bias our statistics in ways that would be very
hard to detect. But look at what happens if 6 *does* appear:

~~~~ {src="src/programming/random_generator_6.py"}
base = 17
value = 6
for i in range(20):
    value = (3 * value + 5) % base
    print value,
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
~~~~

As you can see, 3 times 6 plus 5 mod 17 is 6 again, and so our sequence
gets stuck. How can we prove that this won't ever happen for an
arbitrary seed in a random number generator? And how can we prove that
something subtler won't go wrong?

In fact, computers can't generate real random numbers. But if we're
clever, they *can* generate numbers with many of the same statistical
properties as the real thing. This is very hard to get right, so you
should *never* try to build your own random number generator. Instead,
you should always use a function from a good, well-tested library (like
Python's).

> Any one who considers arithmetical methods of producing random digits
> is, of course, in a state of sin. For, as has been pointed out several
> times, there is no such thing as a random number. There are only
> methods to produce random numbers, and a strict arithmetic procedure
> of course is not such a method. \
>  — John von Neumann

### Summary

-   Use a well-tested random number generation library to generate
    pseudorandom values.
-   If a random number generation library is given the same seed, it
    will produce the same sequence of values.

Neighbors
---------

### Understand:

-   How to examine the neighbors of a cell in a two-dimensional grid.
-   What short-circuit evaluation is and when it occurs.

Now that we have filled our grid, let's find cells' neighbors. (We need
to do this because pollutant can only spread to cells that are adjacent
to ones that have already been filled.) The blue cell shown in [Figure
XXX](#f:filling_neighbors) is a neighbor of the filled region if any of
the green cells already have that special marker value. Note that we're
not looking at the cells that are on the diagonals: we should check the
science on this, but again, we'll do the simple thing for now and change
it later if we need to.

### How to Put Things Off

This is the second time we've said, "We'll change it later if we need
to." Each time we say this, we should design our software so that making
the change is as easy as possible—ideally, a matter of changing one
function call or one parameter value. We haven't done that yet, but we
will by the end of this chapter.

![Filling Neighbors](img/python/filling_neighbors.png)

Here's a piece of code that tests to see whether a cell is a candidate
for being filled in:

    # Is a cell a candidate for filling?
    # Version 1: has bugs!
    for x in range(N):
        for y in range(N):
            if is_filled(grid, x-1, y) \
            or is_filled(grid, x+1, y) \
            or is_filled(grid, x, y-1) \
            or is_filled(grid, x, y+1):
                ...cell (x, y) is a candidate...

It seems simple: for each (x, y) coordinate in the grid, look at the
cells that are left, right, up, and down. If any of them is filled, then
this cell is a candidate for filling.

However, this code doesn't take into account what happens at the edges.
If we subtract 1 when `x` is zero, we get an X coordinate of -1. In
Python, that means the last cell in the row (since negative indices
count backward from the end of a list). That will wrap around to the far
edge, which is definitely not what we want.

The situation on the other border isn't quite as bad: if we add one to
the X coordinate when we're at the right-hand edge, our neighbor index
will be out of bounds and Python will raise an exception, so at least
we'll know we did something wrong.

Here's another version of the code that tests for this:

    # Is a cell a candidate for filling?
    # Version 2: long-winded
    for x in range(N):
        for y in range(N):
            if x > 0:
                if is_filled(grid, x-1, y):
                    ...cell (x, y) is a candidate...
            ...repeat for the other three cases...

For each (x, y) coordinate, we test to make sure that `x` is greater
than zero, i.e, that we're not on the left edge, before checking to see
if the cell to our left is filled. We repeat a similar double test for
each of the other directions.

We can make this a bit more readable by combining the two tests with
`and`

    # Is a cell a candidate for filling?
    # Version 3: good enough for production
    for x in range(N):
        for y in range(N):
            if (x > 0) and is_filled(x-1, y):
                ...cell (x, y) is a candidate...
            elif (x < N-1) and is_filled(x+1, y):
                ...and so on...

This works because of [short-circuit
evaluation](glossary.html#short-circuit-evaluation). In Python (and in
most other modern programming languages), `and` only tests the second
condition if the first one is true, because if the first condition is
false, the `and` is guaranteed to be false. Similarly, if the first
condition in an `or` is true, Python doesn't both to evaluate the second
condition. We talk about this a bit more in [the
appendix](ref.html#s:bool).

### Options

There are several other good ways to structure even this short piece of
code. For example, we could check that the X and Y indices are in range
inside `is_filled`, and always return false if they're not. We could
also use one big conditional instead of an `if` and four `elif`s in
order to avoid duplicating the code that does something to a cell if it
is indeed a candidate:

            if ((x > 0)   and is_filled(x-1, y)) \
            or ((x < N-1) and is_filled(x+1, y)) \
            or ((y > 0)   and is_filled(x, y-1)) \
            or ((y < N-1) and is_filled(x, y+1)):
                ...cell (x, y) is a candidate...

There's no clear reason to choose any of these approaches over any of
the others, at least not yet, so we'll continue with the one we have.

### Summary

-   `and` and `or` stop evaluating arguments as soon as they have an
    answer.

Handling Ties
-------------

### Understand:

-   How to translate complex tests into program statements
    systematically.

The next thing on our to-do list is to resolve ties between cells that
share the lowest value on the boundary. For example, our specification
says that we should choose one of the three highlighted cells in [Figure
XXX](#f:handling_ties) at random. How do we keep track of the cells
we're supposed to be choosing from?

![Handling Ties](img/python/handling_ties.png)

We're going to do this using a set, which we will fill with (x,y) tuples
holding the coordinates of boundary cells that have the lowest value
we've seen so far, and use a separate variable to store that lowest
value. Every time we look at a new cell, we will have to consider three
cases:

1.  *Its value is greater than the minimum we've seen so far,* so we can
    ignore it, because we know there are better cells elsewhere.
2.  *The value of the new cell is equal to the current minimum,* so we
    must add the new cell's (x,y) coordinates to our set.
3.  *The new value is less than the current minimum,* so we must replace
    all the coordinates that are currently in the set with the
    coordinates of the new cell, and re-set our minimum to be this new
    value.

An example will make this clearer. Suppose the range of values cells can
take on is 1 to 10. Before we start looking at cells, we assign 11 to
`min_val` (because it is one greater than the maximum possible value
that could be in the grid) and assign an empty set to `min_set` (because
we haven't look at any cells yet). We then take a look at our first cell
([Figure XXX](#f:handling_ties_example)). Its value is less than
`min_val`, so we re-set `min_val` to 4 (the value of the cell), and we
put the coordinates of this cell (in this case, X equals 12, Y equals
23) into the set.

![Example of Handling Ties](img/python/handling_ties_example.png)

When we look at the next cell, its value is greater than the currently
known minimum value, so we ignore it. The third cell is tied equal for
the minimum value, so we add its coordinates—in this case, (11,22)—to
our set. The next cell is greater than the minimum value, so we ignore
it.

The fifth cell we examine has a value less than the minimum value we've
seen previously, so we throw out all of the coordinates we've saved in
the set, and put the coordinates of this cell into the set in their
place. Finally, the last boundary cell has a value equal to this new
minimum, so we add its coordinates to the set.

Here's the code that implements all this:

    # Keep track of cells tied for lowest value
    min_val = Z+1
    min_set = set()
    for x in range(N):
        for y in range(N):
            if ...is a neighbor...:
                if grid[x][y] == min_val:
                    min_set.add((x, y))
                elif grid[x][y] < min_val:
                    min_val = grid[x][y]
                    min_set = set([(x, y)])

### Seeing What Isn't There

Notice that since we don't need to do anything when a cell's value is
greater than the minimum we've seen so far, there isn't an `else` to
handle that case. Some people would add a comment to make that explicit,
so that the logic is complete:

                if grid[x][y] == min_val:
                    min_set.add((x, y))
                elif grid[x][y] < min_val:
                    min_val = grid[x][y]
                    min_set = set([(x, y)])
                else:
                    pass # do nothing if cell value > min_val

but other people would find this more confusing than helpful. As always,
the most important thing is to be consistent:

Once we have the set of candidate cells, we can use the `random`
library's `choice` function to pick one:

    # Choose a cell
    from random import ..., choice

    min_val = Z+1
    min_set = set()
    ...loop...
    assert min_set, "No cells found"
    candidates = list(min_set)
    x, y = choice(candidates)

Before we call `choice`, we check that the set actually has something in
it (because if there are no cells in the set when we finish our loop,
then something's gone wrong with our program). We then convert the set
to a list, because the random choice function requires an argument that
can be indexed, and then use that function to choose one element from
the list.

### Summary

-   Turn complex tests into conditional stepwise.
-   Include do-nothing branches if it makes the code easier to
    understand.

Putting It All Together
-----------------------

### Understand:

-   How to assemble a program once its pieces are understood.

We now know how to:

-   create a grid,
-   fill it with random numbers,
-   mark cells that have been filled,
-   find cells that might be filled next, and
-   choose one of them at random.

It's time to put all this together to create a complete program. We will
assemble the code in exactly the order we would write it (in fact, in
the order in which I *did* write it, because everything so far has
actually been a rational reconstruction of the things I realized I
needed to have known after I wrote the first version of this code).
We'll start at the top and work down, introducing functions and
variables as we need them, and tidy up a little bit along the way.
Here's what we write first:

~~~~ {src="src/dev/invperc_initial.py"}
'''Invasion percolation simulation.
usage: invperc.py grid_size value_range random_seed
'''
import sys, random

# Main driver.
if __name__ == '__main__':
    main(sys.argv[1:])
~~~~

We start with a [docstring](glossary.html#docstring) to remind ourselves
of what this program does. We then import the libraries we need and call
a `main` function, passing in all of the command-line arguments except
the first (which is the name of our script). That function starts like
this:

~~~~ {src="src/dev/invperc_initial.py"}
    # Parse parameters.
    arguments = sys.argv[1:]
    try:
        grid_size = int(arguments[0])
        value_range = int(arguments[1])
        random_seed = int(arguments[2])
    except IndexError:
        fail('Expected 3 arguments, got %d' % len(arguments))
    except ValueError:
        fail('Expected int arguments, got %s' % str(arguments))
~~~~

This code converts the first three values in `arguments` to integers and
assign them to `grid_size`, `value_range`, and `random_seed`. If we get
an `IndexError`, it means that one of the indices 0, 1, or 2 wasn't
valid, so we don't have enough arguments. If we get a `ValueError`, it
means that one of our attempts to convert a string to an integer failed,
so again we print an error message.

We have used a function called `fail` to report errors. This doesn't
exist yet, so we should go and write it:

~~~~ {src="src/dev/invperc_initial.py"}
def fail(msg):
    '''Print error message and halt program.'''
    print >> sys.stderr, msg
    sys.exit(1)
~~~~

We give the function a docstring because every function should have one.
Inside the function, we print the message to standard error so that it
will appear on the user's console, then exit. [Figure
XXX](#f:structure_a) shows the structure of the program so far: a
documentation string, our `fail` function, and the main driver of our
program.

![Program Structure (A)](img/python/structure_a.png)

The next step in `main` is to actually run the simulation. We do that by
seeding the random number generator, creating a random grid, marking the
center cell as filled, and then filling the rest of the grid:

~~~~ {src="src/dev/invperc_initial.py"}
    # Run simulation.
    random.seed(random_seed)
    grid = create_random_grid(grid_size, value_range)
    mark_filled(grid, grid_size/2, grid_size/2)
    fill_grid(grid) + 1
~~~~

This code uses three functions that don't exist yet, so we will have to
go back and write them. Before doing that, though, let's finish off the
main body of the program. The last task we have is to report results,
but we haven't actually decided what to do about this: nothing in our
specification told us whether we were supposed to draw the fractal,
calculate some statistics, or do something else entirely. For now, we'll
just print the number of cells we have filled in:

~~~~ {src="src/dev/invperc_initial.py"}
    # Run simulation.
    random.seed(random_seed)
    grid = create_random_grid(grid_size, value_range)
    mark_filled(grid, grid_size/2, grid_size/2)
    num_filled_cells = fill_grid(grid) + 1
    print '%d cells filled' % num_filled_cells
~~~~

We have changed `fill_grid` so that it returns the number of cells it
filled in, and then we print that number. Note that we have to add one
to the value returned by `fill_grid` because we marked the center cell
as being filled manually. This is a little bit clumsy: someone who
hasn't read our code carefully might reasonably think that `fill_grid`
returns the total number of cells that are filled, not one less than
that. We should go back and tidy that up later.

Here's the function to create a random grid, reproduced from earlier:

~~~~ {src="src/dev/invperc_initial.py"}
def create_random_grid(N, Z):
    '''Return an NxN grid of random values in 1..Z.
    Assumes the RNG has already been seeded.'''

    assert N > 0, 'Grid size must be positive'
    assert N%2 == 1, 'Grid size must be odd'
    assert Z > 0, 'Random range must be positive'
    grid = []
    for x in range(N):
        grid.append([])
        for y in range(N):
            grid[-1].append(random.randint(1, Z))
    return grid
~~~~

It checks that the parameters it's been passed make sense, then it
builds a list of lists of random values. It assumes that the random
number generator has already been seeded, i.e., it is not going to seed
the random number generator itself. [Figure XXX](#f:structure_b) shows
where we put this function in our program file.

![Program Structure (B)](img/python/structure_b.png)

Next is `mark_filled`, which, as its name suggests, marks a grid cell as
being filled:

~~~~ {src="src/dev/invperc_initial.py"}
def mark_filled(grid, x, y):
    '''Mark a grid cell as filled.'''

    assert 0 <= x < len(grid), \
           'X coordinate out of range (%d vs %d)' % \
           (x, len(grid))
    assert 0 <= y < len(grid), \
           'Y coordinate out of range (%d vs %d)' % \
           (y, len(grid))

    grid[x][y] = -1
~~~~

We use assertions to test that the X and Y coordinates we've been given
are actually in bounds. You might think we don't need this code, because
if the X or Y coordinate is out of bounds, Python will fail and print
its own error message, but there are three reasons to put these
assertions in:

1.  The assertions tell readers what we expect of X and Y.
2.  These error messages are more meaningful that Python's generic
    "IndexError: index out of range" message.
3.  Negative values of X and Y won't actually cause exceptions.

The last line in this function assigns -1 to `grid[x][y]`. We're using
-1 to indicate filled cells, but we don't know if people are going to
remember that when they're reading our code: if you say "grid at X, Y
assigned -1", it's not immediately clear what you're doing. So let's
make a small change right now: near the top of our program we'll create
a variable called `FILLED`, and give it the value -1, so that in our
function we can say "grid at X, Y is assigned FILLED":

~~~~ {src="src/dev/invperc_initial.py"}
FILLED = -1

...other functions...

def mark_filled(grid, x, y):
    ...body of function...
    grid[x][y] = FILLED
~~~~

`FILLED` is written in capital letters because we think of it as a
constant, and by convention, constants are normally written in all caps.
Putting constants at the top of the file is also a (strong) convention.

The next function in our to-do list is `fill_grid`. The docstring says
that it fills an N×N grid until the filled region hits the boundary, and
that it assumes that the center cell has been filled before it is
called:

~~~~ {src="src/dev/invperc_initial.py"}
def fill_grid(grid):
    '''Fill an NxN grid until filled region hits boundary.'''

    N = len(grid)
    num_filled = 0
    while True:
        candidates = find_candidates(grid)
        assert candidates, 'No fillable cells found!'
        x, y = random.choice(list(candidates))
        mark_filled(grid, x, y)
        num_filled += 1
        if x in (0, N-1) or y in (0, N-1):
            break

    return num_filled
~~~~

We begin by setting up `N` and `num_filled`, which are the grid size and
the number of cells that this function has filled so far We then go into
a seemingly-infinite loop, at the bottom of which we test to see if
we're done, and if so, break out. We could equally well do something
like this:

        filling = True
        while filling:
            ...
            if x in (0, N-1) or y in (0, N-1):
                filling = False

However we control filling, we use another function called
`find_candidates` to find the set of cells that we might fill. This
function hasn't been written yet, so we add it to our to-do list. We
then check that the set of candidates it has found has something in it,
because if we haven't found any candidates for filling, something has
probably gone wrong with our program. And then, as discussed
[earlier](#s:random), we make a random choice to choose the cell we're
going to fill, then mark it and increment our count of filled cells.
[Figure XXX](#f:structure_c) shows where this function fits in the file.

![Program Structure (C)](img/python/structure_c.png)

`find_candidates` is next on our to-do list:

~~~~ {src="src/dev/invperc_initial.py"}
def find_candidates(grid):
    '''Find low-valued neighbor cells.'''

    N = len(grid)
    min_val = sys.maxint
    min_set = set()
    for x in range(N):
        for y in range(N):
            if (x > 0) and (grid[x-1][y] == FILLED) \
            or (x < N-1) and (grid[x+1][y] == FILLED) \
            or (y > 0) and (grid[x][y+1] == FILLED) \
            or (y < N-1) and (grid[x][y+1] == FILLED):
                ...let's stop right there...
~~~~

We're going to stop right there because this code is already hard to
read and we haven't even finished it. In fact, it contains a bug—one of
those `y+1`'s should be a `y-1`—but you probably didn't notice that
because there was too much code to read at once.

A good rule of thumb is, "Listen to your code as you write it." If the
code is difficult to understand when read aloud, then it's probably
going to be difficult to understand when you're debugging, so you should
try to simplify it. This version of `find_candidates` introduces a
helper function called `is_candidate`:

~~~~ {src="src/dev/invperc_is_candidate.py"}
def find_candidates(grid):
    '''Find low-valued neighbor cells.'''
    N = len(grid)
    min_val = sys.maxint
    min_set = set()
    for x in range(N):
        for y in range(N):
            if is_candidate(grid, x, y):
                ...now we're talking...
~~~~

This is much clearer when read aloud. Let's finish the function by
adding the code we figured out earlier:

~~~~ {src="src/dev/invperc_is_candidate.py"}
                if is_candidate(grid, x, y):
                    # Has current lowest value.
                    if grid[x][y] == min_val:
                        min_set.add((x, y))
                    # New lowest value.
                    elif grid[x][y] < min_val:
                        min_val = grid[x][y]
                        min_set = set([(x, y)])
~~~~

![Program Structure (D)](img/python/structure_d.png)

As [Figure XXX](#f:structure_d) shows, the `find_candidates` function
fits right above `fill_grid` in our file. We can then insert the
`is_candidate` function we wrote in the previous section right above
`find_candidates` and write it:

~~~~ {src="src/dev/invperc_is_candidate.py"}
def is_candidate(grid, x, y):
    '''Is a cell a candidate for filling?'''

    return (x > 0) and (grid[x-1][y] == FILLED) \
        or (x < N-1) and (grid[x+1][y] == FILLED) \
        or (y > 0) and (grid[x][y-1] == FILLED) \
        or (y < N-1) and (grid[x][y+1] == FILLED)
~~~~

There are no functions left on our to-do list, so it's time to run our
program—except it's not. It's actually time to *test* our program,
because there's a bug lurking in the code that we just put together.
Take a moment, read over the final code, and try to find it before
moving on to the next section.

### Summary

-   Put programs together piece by piece.
-   Write one complete function at a time rather than diving into
    sub-functions right away.

Bugs
----

### Understand:

-   How to halt a running program.
-   That we should test programs on simple cases first.

Let's run the program that we created in the previous section:

    $ python invperc.py 3 10 17983
    2 cells filled

The program tells us that 2 cells have been filled, which is what we'd
expect: in a 3×3 grid, we fill always the center cell and one other,
then we hit the boundary. Let's try a larger grid:

    $ python invperc.py 5 10 27187
    ...a minute passes...
    Ctrl-C

After a minute, we use Control-C to halt the program. It's time to fire
up the debugger…

![Debugging the Grid](img/python/debugger.png)

The initial grid looks OK: it is a 3-element list, each of whose entries
is another 3-element list with values in the range 1 to 10. There's even
a -1 in the right place (remember, we're using -1 to mark filled cells).

The next cell gets chosen and filled correctly, and then the program
goes into an infinite loop in `find_candidates`. Inside this loop,
`min_set` contains the points (2,2) and (1,2), and `min_val` is -1.
That's our problem: our marker value, -1, is less than any of the actual
values in the grid. Once we have marked two cells, each of those marked
cells is adjacent to another marked cell, so we are repeatedly
re-marking cells that have already been marked without ever growing the
marked region.

This is easy to fix. The code that caused the problem is:

~~~~ {src="src/dev/invperc_initial.py"}
def find_candidates(grid):
    N = len(grid)
    min_val = sys.maxint
    min_set = set()
    for x in range(N):
        for y in range(N):
            if is_candidate(grid, x, y):
                ...handle == min_val and < min_val cases...
~~~~

All we have to do is insert a check to say, "If this cell is already
filled, continue to the next iteration of the loop." The code is:

~~~~ {src="src/programming/invperc_no_refill.py"}
def find_candidates(grid):
    N = len(grid)
    min_val = sys.maxint
    min_set = set()
    for x in range(N):
        for y in range(N):
            if grid[x][y] == FILLED:
                pass
            elif is_candidate(grid, x, y):
            ...handle == min_val and < min_val cases...
~~~~

With this change, our program now runs for several different values of
N. But that doesn't prove that it's correct; in order to convince
ourselves of that, we're going to have to do a bit more work.

### Summary

-   Test programs with successively more complex cases.

Refactoring
-----------

### Understand:

-   That reorganizing code can make testing (and maintenance) easier.
-   That randomness of any kind makes programs hard to test.
-   How to replace pseudo-random behavior in programs with predictable
    behavior.

We have found and fixed one bug in our program, but how many others
*haven't* we found? More generally, how do we validate and verify a
program like this? Those two terms sound similar, but mean different
things. Verification means, "Is our program free of bugs?" or, "Did we
built the program right?" Validation means, "Are we implementing the
right model?" i.e., "Did we build the right thing?" The second question
depends on the science we're doing, so we'll concentrate on the first.

To begin addressing it, we need to make our program more testable. And
since testing anything that involves randomness is difficult, we need to
come up with examples that *aren't* random. One is a grid has the value
2 everywhere, except in three cells that we have filled with 1's
([Figure XXX](#f:test_case_grid)). If our program is working correctly,
it should fill exactly those three cells and nothing else. If it
doesn't, we should be able to figure out pretty quickly why not.

![Test Case](img/python/test_case_grid.png)

How do we get there from here? The overall structure of our program is
shown in [Figure XXX](#f:before_refactoring):

![Program Before Refactoring](img/python/before_refactoring.png)

The function we want to test is `fill_grid`, so let's reorganize our
code to make it easier to create specific grids. Grids are created by
the function `create_random_grid`, which takes the grid size and random
value range as arguments:

    def create_random_grid(N, Z):
        ...

    def main(arguments):
        ...
        grid = create_random_grid(grid_size, value_range)
        ...

Let's split that into two pieces. The first will create an N×N grid
containing the value 0, and the second will overwrite those values with
random values in the range 1 to Z:

    ...
    def create_grid(N):
        ...

    def fill_grid_random(grid, Z):
        ...

    def main(arguments):
        ...
        grid = create_grid(grid_size)
        fill_grid_random(grid, value_range)
        ...

We can now use some other function to fill the grid with non-random
values when we want to test specific cases, *without* duplicating the
work of creating the grid structure.

Another part of the program we will need to change is the `main`
function that takes command-line arguments and converts them into a grid
size, a range of random values, and a random number seed:

    def main(arguments):
        '''Run the simulation.'''

        # Parse parameters.
        try:
            grid_size = int(arguments[0])
            value_range = int(arguments[1])
            random_seed = int(arguments[2])
        except IndexError:
            fail('Expected 3 arguments, got %d' % len(arguments))
        except ValueError:
            fail('Expected integer arguments, got %s' % str(arguments))

        # Run simulation.
        ...

Let's introduce a new argument in the first position called `scenario`:

    def main(arguments):
        '''Run the simulation.'''

        # Parse parameters.
        try:
            scenario = arguments[0]
            grid_size = int(arguments[1])
            value_range = int(arguments[2])
            random_seed = int(arguments[3])
        except IndexError:
            fail('Expected 3 arguments, got %d' % len(arguments))
        except ValueError:
            fail('Expected integer arguments, got %s' % str(arguments))

        # Run simulation.
        ...

`scenario` doesn't need to be converted to an integer: it's just a
string value specifying what we want to do. If the user gives us the
word "random", we'll do exactly what we've been doing all along. For the
moment, we will fail if the user gives us anything else, but later on we
will use `scenario` to determine which of our test cases we want to run.

But wait a moment: we're not going to use random numbers when we fill
the grid manually for testing. We're also not going to need the value
range, or even the grid size, so let's move argument handling and random
number generation seeding into the `if` branch that handles the random
scenario. Once we make this change, we determine the scenario by looking
at the first command-line argument, and then if that value is the word
"random", we look at the remaining arguments to determine the grid size,
the value range, and the random seed. If the first argument *isn't* the
word "random", then we fail:

        # Parse parameters.
        scenario = arguments[0]
        try:
            if scenario == 'random':

                # Parse arguments.
                grid_size = int(arguments[1])
                value_range = int(arguments[2])
                random_seed = int(arguments[3])

                # Run simulation.
                random.seed(random_seed)
                grid = create_random_grid(grid_size, value_range)
                mark_filled(grid, grid_size/2, grid_size/2)
                num_filled_cells = fill_grid(grid) + 1
                print '%d cells filled' % num_filled_cells

            else:
                fail('Unknown scenario "%s"' % scenario)
        except IndexError:
            fail('Expected 3 arguments, got %d' % len(arguments))
        except ValueError:
            fail('Expected integer arguments, got %s' % str(arguments))

The block of code inside the `if` is large enough that it's hard to see
how what `else` and the two `except`s line up with. Let's factor some
more:

    def do_random(arguments):
        # Parse arguments.
        grid_size = int(arguments[1])
        value_range = int(arguments[2])
        random_seed = int(arguments[3])

        # Run simulation.
        random.seed(random_seed)
        grid = create_random_grid(grid_size, value_range)
        mark_filled(grid, grid_size/2, grid_size/2)
        num_filled_cells = fill_grid(grid) + 1
        print '%d cells filled' % num_filled_cells

    def main(arguments):
        '''Run the simulation.'''

        scenario = arguments[0]
        try:
            if scenario == 'random':
                do_random(arguments)
            else:
                fail('Unknown scenario "%s"' % scenario)
        except IndexError:
            fail('Expected 3 arguments, got %d' % len(arguments))
        except ValueError:
            fail('Expected integer arguments, got %s' % str(arguments))

    # Main driver.
    if __name__ == '__main__':
        main(sys.argv[1:])

That's easier to follow, but selecting everything but the first
command-line argument in the `if` at the bottom, then selecting
everything but the first of *those* values at the start of `main`, is a
bit odd. Let's clean that up, and move the `try`/`except` into
`do_random` at the same time (since the functions that handle other
scenarios might have different error cases).

~~~~ {src="src/dev/invperc_refactoring.py"}
def do_random(arguments):
    '''Run a random simulation.'''

    # Parse arguments.
    try:
        grid_size = int(arguments[1])
        value_range = int(arguments[2])
        random_seed = int(arguments[3])
    except IndexError:
        fail('Expected 3 arguments, got %d' % len(arguments))
    except ValueError:
        fail('Expected integer arguments, got %s' % str(arguments))

    # Run simulation.
    random.seed(random_seed)
    grid = create_random_grid(grid_size, value_range)
    mark_filled(grid, grid_size/2, grid_size/2)
    num_filled_cells = fill_grid(grid) + 1
    return num_filled_cells
    print '%d cells filled' % num_filled_cells

def main(scenario, arguments):
    '''Run the simulation.'''

    if scenario == 'random':
        do_random(arguments)
    else:
        fail('Unknown scenario "%s"' % scenario)

# Main driver.
if __name__ == '__main__':
    assert len(sys.argv) > 1, 'Must have at least a scenario name'
    main(sys.argv[1], sys.argv[2:])
~~~~

![Result of Refactoring](img/python/revised_structure.png)

[Figure XXX](#f:revised_structure) shows the structure of our program
after refactoring. We have the documentation string, which we've updated
to remind people that the first argument is the name of the scenario.
Our `fail` function hasn't changed. We've split grid creation into two
functions. Our `fill_grid` function now fills the middle cell and
returns the count of *all* filled cells. And we have a function to parse
command-line arguments. This argument-parsing function is actually
specific to the random case. We should probably rename it, to make that
clear.

Now let's step back. We were supposed to be testing our program, but in
order to make it more testable, we had to reorganize it first. The
jargon term for this is "refactoring", which means "changing a program's
structure without modifying its behavior or functionality in order to
improve its quality." Now that we've done this refactoring, we can write
tests more easily. More importantly, now that we've thought this
through, we are more likely to write the next program of this kind in a
testable way right from the start.

### Summary

-   Refactor programs as necessary to make testing easier.
-   Replace randomness with predictability to make testing easier.

Testing
-------

### Understand:

-   How to build scaffolding to aid testing.
-   That building test scaffolding saves time in the long run.

Let's start by adding another clause to the main body of the program so
that if the scenario is `"5x5_line"` we will create a 5×5 grid, fill a
line of cells from the center to the edge with lower values, and then
check that `fill_grid` does the right thing ([Figure XXX](#f:5x5_line)):

~~~~ {src="src/dev/invperc_5x5.py"}
if __name__ == '__main__':
    scenario = sys.argv[1]
    if scenario == 'random':
        do_random(arguments)
    elif scenario == '5x5_line':
        do_5x5_line()
    else:
        fail('Unknown scenario "%s"' % scenario)
~~~~

![Racing for the Border](img/python/5x5_line.png)

The function `do_5x5_line` is pretty simple:

~~~~ {src="src/dev/invperc_5x5.py"}
def do_5x5_line():
    '''Run a test on a 5x5 grid with a run to the border.'''

    grid = create_grid(5)
    init_grid_5x5_line(grid)
    num_filled_cells = fill_grid(grid)
    check_grid_5x5_line(grid, num_filled_cells)
~~~~

The functions `create_grid` and `fill_grid` already exist: in fact, the
whole point of this exercise is that we're re-using `fill_grid` in order
to test it. The new test-specific functions are `init_grid_5x5_line` and
`check_grid_5x5_line`. We're going to have to write a similar pair of
functions for each of our tests, so we'll write the first pair, then use
that experience to guide some further refactoring. Here's the first
function

~~~~ {src="src/dev/invperc_5x5.py"}
def init_grid_NxN_line(grid):
    '''Fill NxN grid with straight line to edge for testing purposes.'''

    N = len(grid)
    for x in range(N):
        for y in range(N):
            grid[x][y] = 2

    for i in range(N/2 + 1):
        grid[N/2][i] = 1
~~~~

It's just as easy to write this function for the N×N case as for the 5×5
case, so we generalize early. The first part of the function is easy to
understand: find the value of N by looking at the grid, then fill all of
the cells with the integer 2. The second part, which fills the cells
from the center to the edge in a straight line with the lower value 1,
isn't as easy to understand: it's not immediately obvious that `i`
should go in the range from 0 to N/2+1, or that the X coordinate should
be N/2 and the Y coordinate should be `i` for the cells that we want to
fill.

When we say "it's not obvious," what we mean is, "There's the
possibility that it will contain bugs." If there are bugs in our test
cases, then we're just making more work for ourselves. We'll refactor
this code later so that it's easier for us to see that it's doing the
right thing.

Here's the code that checks that an N×N grid with a line of cells from
the center to the edge has been filled correctly:

    def check_grid_NxN_line(grid, num_filled):
        '''Check NxN grid straight line grid.'''

        N = len(grid)
        assert num_filled == N/2 + 1, 'Wrong number filled'

        for x in range(N):
            for y in range(N):
                if (x == N/2) and (y <= N/2):
                    assert grid[x][y] == FILLED, 'Not filled!'
                else:
                    assert grid[x][y] != FILLED, 'Wrongly filled!'

Again, it's as easy to check for the N×N case as the 5×5 case, so we've
generalized the function. But take a look at that `if`: are we sure that
the only cells that should be filled are the ones with X coordinate
equal to N/2 and Y coordinate from 0 to N/2? Shouldn't that be N/2+1? Or
1 to N/2, or maybe the X coordinate should be N/2+1.

In fact, these two functions *are* correct, and when they're run, they
report that `fill_grid` behaves properly. But writing and checking two
functions like this for each test won't actually increase our confidence
in our program, because the tests themselves might contain bugs. We need
a simpler way to create and check tests, so that our testing is actually
helping us create a correct program rather than giving us more things to
worry about. How do we do that?

Let's go back to the example in [Figure XXX](#f:5x5_line). Why don't we
just "draw" our test cases exactly as shown? The reason is that modern
programming languages don't actually let you draw things, but we can get
close with a little bit of work. Let's write our test fixture as a
string:

    fixture = '''2 2 2 2 2
                 2 2 2 2 2
                 1 1 1 2 2
                 2 2 2 2 2
                 2 2 2 2 2'''

and write the result as a similar string:

    result = '''. . . . .
                . . . . .
                * * * . .
                . . . . .
                . . . . .'''

As you can probably guess, the '\*' character means "this cell should be
filled", while the '.' means "this cell should hold whatever value it
had at the start". Here's how we want to use them:

~~~~ {src="src/dev/invperc_fixture.py"}
def do_5x5_line():
    '''Run a test on a 5x5 grid with a run to the border.'''

    fixture  = '''2 2 2 2 2
                  2 2 2 2 2
                  1 1 1 2 2
                  2 2 2 2 2
                  2 2 2 2 2'''

    expected = '''. . . . .
                  . . . . .
                  * * * . .
                  . . . . .
                  . . . . .'''

    fixture = parse_grid(fixture)
    num_filled_cells = fill_grid(fixture)
    check_result(expected, fixture, num_filled_cells)
~~~~

Parsing a grid is pretty easy:

~~~~ {src="src/dev/invperc_fixture.py"}
def parse_grid(fixture):
    '''Turn a string representation of a grid into a grid of numbers.'''

    result = [x.strip().split() for x in fixture.split('\n')]
    size = len(result)
    for row in result:
        if len(row) != size:
            fail('Badly formed fixture')
        for i in range(len(row)):
            row[i] = int(row[i])
    return result
~~~~

Checking cells is pretty easy too:

~~~~ {src="src/dev/invperc_fixture.py"}
def check_result(expected, grid, num_filled):
    '''Check the results of filling.'''
    expected, count = convert_grid(expected)

    if len(expected) != len(grid):
        fail('Mis-match between size of expected result and size of grid')
    if count != num_filled:
        fail('Wrong number of cells filled')

    for i in range(len(expected)):
        g = grid[i]
        e = expected[i]
        if len(g) != len(e):
            fail('Rows are not the same length')
        for j in range(len(g)):
            if g[j] and (e[j] != FILLED):
                fail('Cell %d,%d should be filled but is not' % (i, j))
            elif (not g[j]) and (e[j] == FILLED):
                fail('Cell %d,%d should not be filled but is' % (i, j))
    return result
~~~~

We still have one function to write, though—the one that parses a string
of '\*' and '.' characters and produces a grid of trues and falses. But
this is almost exactly the same as what we do to parse a fixture. The
only difference is how we convert individual items. Let's refactor:

~~~~ {src="src/dev/invperc_fixture.py"}
def is_star(x):
    '''Is this cell supposed to be filled?'''
    return x == '*'

def parse_general(fixture, converter):
    '''Turn a string representation of a grid into a grid of values.'''

    result = [x.strip().split() for x in fixture.split('\n')]
    size = len(result)
    for row in result:
        if len(row) != size:
            fail('Badly formed fixture')
        for i in range(len(row)):
            row[i] = converter(row[i])
    return result

def do_5x5_line():
    '''Run a test on a 5x5 grid with a run to the border.'''

    ...define fixture and expected strings...

    fixture = parse_general(fixture, int)
    num_filled_cells = fill_grid(fixture)
    expected = parse_general(fixture, is_star)
    check_result(expected, fixture, num_filled_cells)
~~~~

Writing the functions to parse fixture strings might seem like a lot of
work, but what are you comparing it to? Are you comparing the time to
write those functions to the time it would take to inspect printouts of
real grids, or step through the program over and over again in the
debugger? And did you think to include the time it would take to re-do
this after every change to your program? Or are you comparing it to the
time it would take to retract a published paper after you find a bug in
your code?

In real applications, it's not unusual for test code to be anywhere from
20% to 200% of the size of the actual application code (and yes, 200%
does mean more test code than application code). But that's no different
from physical experiments: if you look at the size and cost of the
machines used to create a space probe, it's many times greater than the
size and cost of the space probe itself.

The good news is, we're now in a position to replace our `fill_grid`
function with one that is harder to get right, but which will run many
times faster. If our tests have been designed well, they shouldn't have
to be rewritten because they'll all continue to work the same way. This
is a common pattern in scientific programming: create a simple version
first, check it, then replace the parts one by one with more
sophisticated parts that are harder to check but give better
performance.

### Summary

-   Write support code to make testing easier.

Performance
-----------

### Understand:

-   That many programs aren't actually worth speeding up.
-   That we should make sure programs are correct before trying to
    improve their performance.
-   How to measure a program's running time.
-   How to estimate the way a program's running time grows with problem
    size.

> Machine-independent code has machine-independent performance. \
>  — anonymous

Now that it's easy to write tests, we can start worrying about our
program's performance. When people use that phrase, they almost always
mean the program's speed. In fact, speed is why computers were invented:
until networks and fancy graphics came along, the reason computers
existed was to do in minutes or hours what would take human beings weeks
or years.

Scientists usually want programs to go faster for three reasons. First,
they want a solution to a single large problem, such as, "What's the
lift of this wing?" Second, they have many problems to solve, and need
answers to all of them—a typical example is, "Compare this DNA sequences
to every one in the database and tell me what the closest matches are."
Finally, scientists may have a deadline and a fixed set of resources and
want to solve as big a problem as possible within the constraints.
Weather prediction falls into this category: given more computing power,
scientists use more accurate (and more computationally demanding)
models, rather than solving the old models faster.

Before trying to make a program go faster, there are two questions we
should always ask ourselves. First, does our program actually need to go
faster? If we only use it once a day, and it only takes a minute to run,
speeding it up by a factor of 10 is probably not worth a week of our
time.

Second, is our program correct? There's no point making a buggy program
faster: more wrong answers per unit time doesn't move science forward
(although it may help us track down a bug). Just as importantly, almost
everything we do to make programs faster also makes them more
complicated, and therefore harder to debug. If our starting point is
correct, we can use its output to check the output of our optimized
version. If it isn't, we've probably made our life more difficult.

Let's go back to invasion percolation. To find out how fast our program
is, let's add a few lines to the program's main body:

    if __name__ == '__main__':

        ...get simulation parameters from command-line arguments...

        # Run simulation.
        start_time = time.time()
        random.seed(random_seed)
        grid = create_random_grid(grid_size, value_range)
        mark_filled(grid, grid_size/2, grid_size/2)
        num_filled = fill_grid(grid) + 1
        elapsed_time = time.time() - start_time
        print 'program=%s size=%d range=%d seed=%d filled=%d time=%f' % \
              (sys.argv[0], grid_size, value_range, random_seed, num_filled, elapsed_time)
        if graphics:
            show_grid(grid)

The first new line records the time when the program starts running. The
other new lines use that to calculate how long the simulation took, and
then display the program's parameters and running time.

We need to make one more change before we start running lots of
simulation. We were seeding the random number generator using the
computer's clock time:

        start_time = time.time()
        ...
        random_seed = int(start_time)

But what if a simulation runs very quickly? `time.time()` returns a
floating point number; `int` truncates this by throwing away the
fractional part, so if our simulation runs in less than a second, two
(or more) might wind up with the same seed, which in turn will mean they
have the same "random" values in their grids. (This isn't a theoretical
problem—we actually tripped over it while writing this chapter.)

One way to fix this is to to shift those numbers up. For now let's guess
that every simulation will take at least a tenth of a millisecond to
run, so we'll multiply the start time by ten thousand, then truncate it
so that it is less than a million:

    RAND_SCALE = 10000    # Try to make sure random seeds are distinct.
    RAND_RANGE = 1000000  # Range of random seeds.
    ...
        random_seed = int(start_time * RAND_SCALE) % RAND_RANGE

The final step is to write a shell script that runs the program multiple
times for various grid sizes:

    for size in {11..81..10}
    do
      for counter in {1..20}
      do
        python invperc.py -g -n $size -v 100
      done
    done

(We could equally well have added a few more lines to the program itself
to run a specified number of simulations instead of just one.) If we
average the 20 values for each grid size, we get the following:

  -------------- ---------- ---------- ---------- ---------- ---------- ----------
                 11         21         31         41         51         61
  cells filled   16.60      45.75      95.85      157.90     270.50     305.75
  time taken     0.003971   0.035381   0.155885   0.444160   1.157350   1.909516
  time/cell      0.000239   0.000773   0.001626   0.002813   0.004279   0.006245
  -------------- ---------- ---------- ---------- ---------- ---------- ----------

Is that good enough? Let's fit a couple of fourth-order polynomials to
our data:

  ------------ ---------------- ---------------- --------------- ---------------- ----------------
               *x^4^*           *x^3^*           *x^2^*          *x^1^*           *x^0^*
  time taken   2.678×10^-07^    -2.692×10^-05^   1.760×10^-03^   -3.983×10^-02^   2.681×10^-01^
  time/cell    -1.112×10^-10^   1.996×10^-08^    4.796×10^-07^   2.566×10^-05^    -1.295×10^-04^
  ------------ ---------------- ---------------- --------------- ---------------- ----------------

According to the first polynomial, a single run on a 1001×1001 grid will
take almost 68 hours. What can we do to make it faster? The *wrong*
answer is, "Guess why it's slow, start tweaking the code, and hope for
the best." The right answer is to ask the computer where the time is
going.

Before we do that, though, we really ought to justify our decision to
model the program's performance using a fourth-order polynomial. Suppose
our grid is N×N. Each time it wants to find the next cell to fill, our
program examines each of the N^2^ cells. In the best case, it has to
fill about N/2 cells to reach the boundary (basically, by racing
straight for the edge of the grid). In the worst case, it has to fill
all of the interior cells before "breaking out" to the boundary, which
means it has to fill (N-2)×(N-2) cells. That worst case therefore has a
runtime of N^2^(N-2)^2^ steps, which, for large N, is approximately
N^4^. (For example, when N is 71, the difference between the two values
is only about 5%.)

This kind of analysis is computing's equivalent of engineers'
back-of-the-envelope calculations. In technical terms, we would say that
our algorithm is O(N^4^). In reality, because we're creating a fractal,
we're actually going to fill about N^1.5^ cells on average, so our
running time is actually O(N^3.5^). That's still too big for practical
simulations, though, so it's time to figure out what we can do about it.

### Summary

-   Scientists want faster programs both to handle bigger problems and
    to handle more problems with available resources.
-   Before speeding a program up, ask, "Does it need to be faster?" and,
    "Is it correct?"
-   Recording start and end times is a simple way to measure
    performance.
-   Analyze algorithms to predict how a program's performance will
    change with problem size.

Profiling
---------

### Understand:

-   What an execution profiler is.
-   The difference between deterministic and statistical profilers.
-   How to interpret a profiler's output.

Timing an entire program is a good way to find out if we're making
things better or not, but some way to know where the time is going would
be even better. The tool that will do that for us is called a
[profiler](glossary.html#profiler) because it creates a profile of a
program's execution time, i.e., it reports how much time is spent in
each function in the program, or even on each line.

There are two kinds of profilers. A
[deterministic](glossary.html#deterministic-profiler) profiler inserts
instructions in a program to record the clock time at the start and end
of every function. It doesn't actually modify the source code: instead,
it adds those instructions behind the scenes after the code has been
translated into something the computer can actually run. For example,
suppose our program looks like this:

    def swap(values):
        for i in range(len(values)/2):
            values[i], values[-1-i] = values[-1-i], values[i]

    def upto(N):
        for i in xrange(1, N):
            temp = [0] * i
            swap(temp)

    upto(100)

A deterministic profiler would insert timing calls that worked like
this:

    def swap(values):
        _num_calls['swap'] += 1
        _start_time = time.time()
        for i in range(len(values)/2):
            values[i], values[-1-i] = values[-1-i], values[i]
        _total_time['swap'] += (time.time() - _start_time)

    def upto(N):
        _num_calls['upto'] += 1
        _start_time = time.time()
        for i in xrange(1, N):
            temp = [0] * i
            swap(temp)
        _total_time['upto'] += (time.time() - _start_time)

    _num_calls['swap'] = 0
    _total_time['swap'] = 0
    _num_calls['upto'] = 0
    _total_time['upto'] = 0
    upto(100)

(Note that the profiler wouldn't actually change the source of our
program; these extra operations are inserted after the program has been
loaded into memory.)

Once the program has been run, the profiler can use the two dictionaries
`_num_calls` and `_total_time` to report the average running time per
function call. Going further, the profiler can also keep track of which
functions are calling which, so that (for example) it can report times
for calls to `swap` from `upto` separately from calls to `swap` from
some other function `downfrom`.

The problem with deterministic profiling is that adding those timing
calls changes the runtime of the functions being measured, since reading
the computer's clock and recording the result both take time. The
smaller the function's runtime, the larger the distortion. This can be
avoided by using a [statistical](glossary.html#statistical-profiler)
profiler. Instead of adding timing calls to the code, it freezes the
program every millisecond or so and makes a note of what function is
running. Like any sampling procedure, this produces become more accurate
as more data is collected, so statistical profilers work well on
long-running programs, but can produce misleading results for short
ones.

Python's `cProfile` module is a deterministic profiler. It records times
and call counts and saves data in a file for later analysis. We can use
it to see where time goes in our initial list-of-lists invasion
percolation program:

~~~~ {src="src/dev/profile_first.py"}
import cProfile, pstats
from invperc import main

cProfile.run('main(["51", "100", "127391"])', 'list.prof')
p = pstats.Stats('list.prof')
p.strip_dirs().sort_stats('time').print_stats()
~~~~

We start by importing `cProfile`, the actual profiling tool, on line 1.
We also import `pstats`, a helper module for analyzing the data files
`cProfile` produces.

The second line imports the `main` function from our program. We give
that starting point to `cProfile.run` on line 3, along with the name of
the file we want the profiling results stored in. Notice that the call
is passed as a string: `cProfile` uses Python's built-in `eval` function
to run the command in this string, just as if we had typed it into the
interpreter. Notice also that the arguments are passed as strings, since
that's what `main` is expecting.

Line 4 reads the profiling data back into our program and wraps it up in
a `pstats.Stats` object. It may seem silly to write the data out only to
read it back in, but the two activities are often completely separate:
we can accumulate profiling data across many different runs of a
program, then analyze it all at once.

Finally, line 5 strips directory names off the accumulated data, sorts
them according to run time, and prints the result. We strip directory
names because all of the code we're profiling is in a single file; in
larger programs, we'll keep the directory information (even though it
makes the output a bit harder to read) so that we can separate
`fred.calculate`'s running time from `jane.calculate`'s.

Here's what the output looks like:

~~~~ {src="src/dev/profile_first.txt"}
135 cells filled
Thu Jun 28 13:54:55 2012    list.prof

         697631 function calls in 0.526 CPU seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
   339489    0.355    0.000    0.376    0.000 invperc.py:64(is_candidate)
      134    0.136    0.001    0.515    0.004 invperc.py:73(find_candidates)
   340029    0.021    0.000    0.021    0.000 {len}
     2601    0.005    0.000    0.005    0.000 random.py:160(randrange)
     7072    0.004    0.000    0.004    0.000 {range}
     2601    0.002    0.000    0.007    0.000 random.py:224(randint)
        1    0.001    0.001    0.008    0.008 invperc.py:39(fill_random_grid)
        1    0.001    0.001    0.001    0.001 invperc.py:27(create_grid)
        1    0.001    0.001    0.516    0.516 invperc.py:92(fill_grid)
     2735    0.000    0.000    0.000    0.000 {method 'random' of '_random.Random' objects}
     2652    0.000    0.000    0.000    0.000 {method 'append' of 'list' objects}
      134    0.000    0.000    0.000    0.000 random.py:259(choice)
      135    0.000    0.000    0.000    0.000 invperc.py:52(mark_filled)
        1    0.000    0.000    0.526    0.526 invperc.py:108(do_random)
        1    0.000    0.000    0.526    0.526 invperc.py:186(main)
        1    0.000    0.000    0.000    0.000 {function seed at 0x0221C2B0}
       40    0.000    0.000    0.000    0.000 {method 'add' of 'set' objects}
        1    0.000    0.000    0.000    0.000 random.py:99(seed)
        1    0.000    0.000    0.526    0.526 <string>:1(<module>)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
~~~~

The columns are the number of calls, the total time spent in that
function, the time per call, the total cumulative time (i.e., the total
time for that function and everything it calls), the cumulative time per
call, and then which function the stat is for. As we can see,
`is_candidate` accounts for two thirds of our runtime: if we want to
make this program faster, that's what we should speed up.

### Wall Clock Time vs. CPU Time

When profiling programs, particularly on machines that are running other
applications at the same time, it's important to remember the
distinction between [CPU time](glossary.html#cpu-time) and [wall-clock
time](glossary.html#wall-clock-time). The first is how much time the
computer's processor actually spent running the program; the second is
how long the program actually took to run. The two are different because
the CPU has a lot of things to do besides running our program, even on a
machine that's supposedly otherwise idle. The operating system itself
needs time, for example, as do disk and network I/O.

### Summary

-   Use a profiler to determine which parts of a program are responsible
    for most of its running time.

A New Beginning
---------------

### Understand:

-   That using a more efficient algorithm is usually a better way to
    improve performance than tuning an inefficient algorithm.
-   That programs can usually trade space (extra memory) for running
    time.
-   The importance of building a simple, trustworthy version of a
    program before trying to build a faster but more complex version.

If checking whether cells are candidates is the slowest step, let's try
to reduce the number of times we have to do that. Instead of
re-examining every cell in the grid each time we want to fill one, let's
keep track of which cells are currently on the boundary in some kind of
auxiliary data structure, then choose randomly from all the cells in
that set that share the current lowest value. When we fill in a cell, we
add its neighbors to the "pool" of neighbors (unless they're already
there).

Here's the modified `fill_grid` function:

~~~~ {src="src/dev/invperc_pool.py"}
def fill_grid(grid):
    '''Fill an NxN grid until filled region hits boundary.'''

    x, y = grid.size/2, grid.size/2
    pool = set()
    pool.add((grid[x][y], x, y))
    num_filled = 0
    on_edge = False

    while not on_edge:
        x, y = get_next(pool)
        grid.mark_filled(x, y)
        num_filled += 1
        if (x == 0) or (x == grid.size-1) or (y == 0) or (y == grid.size-1):
            on_edge = True
        else:
            if x > 0:           make_candidate(grid, pool, x-1, y)
            if x < grid.size-1: make_candidate(grid, pool, x+1, y)
            if y > 0:           make_candidate(grid, pool, x,   y-1)
            if y < grid.size-1: make_candidate(grid, pool, x,   y+1)

    return num_filled
~~~~

This function creates a set called `pool` that keeps track of the cells
currently on the edge of the filled region. Each loop iteration gets the
next cell out of this pool, fills it in, and (potentially) adds its
neighbors to the set.

This function is 21 lines long, compared to 15 for our original
`fill_grid` function, but four of those six lines are the calls to
`make_candidate`, which adds a neighbor to the pool if it isn't already
there. Let's have a look at `get_next` and `make_candidate`:

    def get_next(pool):
        '''Take a cell randomly from the equal-valued front section.'''

        temp = list(pool)
        temp.sort()
        v = temp[0][0]
        i = 1
        while (i < len(temp)) and (temp[i][0] == v):
            i += 1
        i = random.randint(0, i-1)
        v, x, y = temp[i]
        pool.discard((v, x, y))
        return x, y

    def make_candidate(grid, pool, x, y):
        '''Ensure that (x, y, v) is a candidate.'''

        v = grid_get(grid, x, y)
        if v == FILLED:
            return
        pool.add((v, x, y))

This is definitely more complicated that what we started with: we now
have to keep a second data structure (the pool) up to date, and in sync
with the grid. But look at the payoff:

  --------------- ---------- ---------- ---------- ---------- ---------- ----------
                  11         21         31         41         51         61
  list of lists   0.000333   0.025667   0.088833   0.227167   0.455000   1.362667
  set pool        0.000050   0.003000   0.009100   0.016130   0.012000   0.027050
  ratio           6.66       8.56       9.76       14.1       37.9       50.4
  --------------- ---------- ---------- ---------- ---------- ---------- ----------

Now *that* is a speedup. If we assume that we fill about N^1.5^ cells in
an N×N grid, the running time of our algorithm is about N^1.5^ instead
of N^3.5^, because we only need to inspect four new cells in every
iteration instead of checking all N^2^ each time. As a result, the
bigger our grids get, the bigger our savings are.

### Summary

-   Better algorithms are better than better hardware.

Summing Up
----------

There are two important lessons to take away from this exercise. First,
choosing the right algorithms and data structures can yield enormous
speedups, so we should always look there first for performance gains.
This is where a broad knowledge of computer science comes in handy: any
good book on data structures and algorithms describes dozens or hundreds
of things that are exactly what's needed to solve some obscure but vital
performance problem.

Second, well-structured programs are easier to optimize than
poorly-structured ones. If we build our program as a collection of
functions, we ought to be able to change those functions more or less
independently of one another to try out new ideas. As is almost always
the case, improving the quality of our work improves our performance: it
is the opposite of an either/or tradeoff.
