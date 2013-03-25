# Sets and Dictionaries in Python

<div class="contents">
**Contents:**

1.  [Sets](#s:sets)
2.  [Storage](#s:storage)
3.  [Dictionaries](#s:dict)
4.  [Simple Examples](#s:examples)
5.  [Nanotech Inventory](#s:nanotech)
6.  [Phylogenetic Trees](#s:phylotree)
7.  [Summing Up](#s:summary)
</div>

Fan Fullerene has just joined Molecules'R'Us,
a nanotechnology startup that fabricates molecules
using only the highest quality atoms.
His first job is to build a simple inventory management system
that compares incoming orders for molecules
to the stock of atoms in the company's supercooled warehouse
to see how many of those molecules we can build.
For example,
if the warehouse holds 20 hydrogen atoms,
5 oxygen atoms,
and 11 nitrogen atoms,
Fan could make 10 water molecules (H<sub>2</sub>O)
or 6 ammonia molecules (NH<sub>3</sub>),
but could not make any methane (CH<sub>4</sub>)
because there isn't any carbon.

Fan could solve this problem using the tools we've seen so far.
As we'll see, though,
it's a lot more efficient to do it using a different data structure.
And "efficient" means both "takes less programmer time to create"
and "takes less computer time to execute":
the data structures introduced in this chapter are both simpler to use and faster
than the lists most programmers are introduced to first.

<div class="guide">
## For Instructors

1.  Introduce learners to a non-linear data structure
    -   Most have only ever seen lists/arrays
2.  Introduce computational complexity (big-oh) via back-of-the-envelope calculations
3.  Prepare learners for:
    -   Performance optimization via improvements to algorithms and data structures (in invasion percolation example)
    -   Relational databases (unordered and associative)
4.  Teaching order:
    -   Start with sets
        - Familiar concept
        - No confusion between keys and values
    -   Explain hash tables (with lots of hand waving)
        -   Why are they fast?
        -   Why do elements have to be immutable?
        -   What can go wrong in other languages if hashes can contain mutable values?
    -   Then introduce dictionaries as "sets with extra information attached to each entry"
    -   Canonical example: counting things
    -   Solve original motivating problem
        -   Requires a dictionary of dictionaries, but they have seen lists of lists
        -   Re-emphasize modular breakdown of code into functions
    -   For advanced learners: work through phylogenetic trees example
        -   Usually presented as a table, which makes an array a natural representation
        -   Showing how and why to use dictionaries instead is as important as showing vector operations when introducing NumPy
        -   But example is currently hard to follow/debug without graphical representation of generated tree...
</div>

<section id="s:sets">

## 1. Sets

<div class="understand">

### Understand:
- That one-dimensional structures like lists are not the only data structures available to programmers.
- That a set stores unique values.
- How to perform common operations on sets.
- How to use a set to eliminate duplicate values from data.

</div>

Let's start with something simpler than our actual inventory problem.
Suppose we have a list of all the atoms in the warehouse,
and we want to know which different kinds we have&mdash;not how many,
but just their types.
We could solve this problem using a list to store
the unique atomic symbols we have seen.
Here's a function that adds a new atom to such a list:

    def another_atom(seen, atom):
        for i in range(len(seen)):
            if seen[i] == atom:
                return <span class="comment"># atom is already present, so do not re-add</span>
        seen.append(atom)

`another_atom`'s arguments are
a list of the unique atoms we've already seen,
and the symbol of the atom we're adding.
Inside the function,
we loop over the atoms that are already in the list.
If we find the one we're trying to add,
we exit the function immediately:
we aren't supposed to have duplicates in our list,
so we shouldn't add this atom.
If we reach the end of the list without finding this atom,
though,
we append it.
This is a common [design pattern](glossary.html#design-pattern):
either we find pre-existing data in a loop and return right away,
or take some default action if we finish the loop without finding a match.
  
Let's watch this function in action.
We start with an empty list.
If the first atomic symbol is `'Na'`,
we find no match (since the list is empty),
so we add it.
The next symbol is `'Fe'`;
it doesn't match `'Na'`,
so we add it as well.
Our third symbol is `'Na'` again.
It matches the first entry in the list,
so we exit the function immediately.

<table>
  <tr>
    <td> **Before** </td>
    <td> **Adding** </td>
    <td> **After** </td>
  </tr>
  <tr>
    <td> `[]` </td>
    <td> `'Na'` </td>
    <td> `['Na']` </td>
  </tr> 
  <tr>
    <td> `['Na']` </td>
    <td> `'Fe'` </td>
    <td> `['Na', 'Fe']` </td>
  </tr> 
  <tr>
    <td> `['Na', 'Fe']` </td>
    <td> `'Na'` </td>
    <td> `['Na', 'Fe']` </td>
  </tr> 
</table>

This code works,
but it is inefficient.
Suppose there are *V* distinct atomic symbols in our data,
and *N* symbols in total.
Each time we add an observation to our list,
we have to look through an average of *V/2* entries.
The total running time for our program is therefore approximately *NV/2*.
If *V* is small,
this is only a few times larger than *N*,
but what happens if we're keeping track of something like patient records rather than atoms?
In that case,
most values are distinct,
so *V* is approximately the same as *N*,
which means that our running time is proportional to *N<sup>2</sup>/2*.
That's bad news:
if we double the size of our data set,
our program runs four times slower,
and if we double it again,
our program will have slowed down by a factor of 16.
  
There's a better way to solve this problem
that is simpler to use and runs much faster.
The trick is to use a [set](glossary.html#set)
to store the symbols.
A set is an unordered collection of distinct items.
The word "collection" means that a set can hold zero or more values.
The word "distinct" means that any particular value is either in the set or not:
a set can't store two or more copies of the same thing.
And finally, "unordered" means that values are simply "in" the set.
They're not in any particular order,
and there's no first value or last value.
(They actually are stored in some order,
but as we'll discuss in [the next section](#s:storage),
that order is as random as the computer can make it.)
  
To create a set,
we simply write down its elements inside curly braces:

    >>> primes = {3, 5, 7}

<figure id="f:simple_set">
  <img src="setdict/simple_set.png" alt="A Simple Set" />
</figure>

<!-- continue -->
However,
we have to use `set()` to create an empty set,
because the symbol `{}` was already being used for something else
when sets were added to Python:
  
    >>> even_primes = set() <span class="comment"># not '{}' as in math</span>

<!-- continue -->
(We'll meet that "something else" <a href="#s:dict">later in this chapter</a>.)
  
To see what we can do with sets,
let's create three holding the integers 0 through 9,
the first half of that same range of numbers (0 through 4),
and the odd values 1, 3, 5, 7, and 9:
  
    >>> ten  = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
    >>> lows = {0, 1, 2, 3, 4}
    >>> odds = {1, 3, 5, 7, 9}

If we ask Python to display one of our sets,
it shows us this:
  
    >>> print lows
    <span class="out">set([0, 1, 2, 3, 4])</span>

<!-- continue -->
rather than using the curly-bracket notation.
I personally regard this as a design flaw,
but it does remind us that we can create always create a set from a list.
  
Sets have methods just like strings and lists,
and,
like the methods of strings and lists,
most of those methods create new sets
instead of modifying the set they are called for.
These three come straight from mathematics:
  
    >>> print lows.union(odds)
    <span class="out">set([0, 1, 2, 3, 4, 5, 7, 9])</span>
    >>> print lows.intersection(odds)
    <span class="out">set([1, 3])</span>
    >>> print lows.difference(odds)
    <span class="out">set([0, 2, 4])</span>

Another method that creates a new set is `symmetric_difference`
(sometimes called "exclusive or")
that returns the values that are in one set or another,
but not in both:
  
    >>> print lows.symmetric_difference(odds)
    <span class="out">set([0, 2, 4, 5, 7, 9])</span>
  
Not all set methods return new sets.
`issubset` returns `True` or `False`
depending on whether all the elements in one set are present in another:
  
    >>> print lows.issubset(ten)
    <span class="out">True</span>

<!-- continue -->
The complementary method `issuperset` does the obvious thing:
  
    >>> print lows.issuperset(odds)
    <span class="out">False</span>

We can count how many values are in a set using `len`
(just as we would to find the length of a list or string),
and check whether a particular value is in the set or not using `in`:
  
    >>> print len(odds)
    <span class="out">7</span>
    >>> print 6 in odds
    <span class="out">False</span>

<!-- continue -->
Finally,
some methods modify the sets they are called for.
The most commonly used is `add`,
which adds an element to the set:
  
    >>> lows.add(9)
    >>> print lows
    <span class="out">set([0, 1, 2, 3, 4, 9])</span>

<!-- continue -->
If the thing being added is already in the set,
`add` has no effect,
because any specific thing can appear in a set at most once:
  
    >>> lows.add(9)
    >>> print lows
    <span class="out">set([0, 1, 2, 3, 4, 9])</span>

<!-- continue -->
This behavior is different from that of `list.append`,
which always adds a new element to a list.

Finally,
we can remove individual elements from the set:
  
    >>> lows.remove(0)
    >>> print lows
    <span class="out">set([1, 2, 3, 4])</span>

<!-- continue -->
or clear it entirely:

    >>> lows.clear()
    >>> print lows
    <span class="out">set()</span>
  
Removing elements is similar to deleting things from a list,
but there's an important difference.
When we delete something from a list,
we specify its *location*.
When we delete something from a set,
though,
we specify the *value* that we want to take out,
because sets are not ordered.
If that value isn't in the set,
`remove` does nothing.
  
To help make programs easier to type and read,
most of the methods we've just seen can be written using arithmetic operators as well.
For example, instead of `lows.issubset(ten)`,
we can write `lows <= ten`,
just as if we were using pen and paper.
There are even a couple of operators,
like the strict subset test `<`,
that don't have long-winded equivalents.
  
<table>
  <tr>
    <td> **Operation** </td>
    <td> **Method** </td>
    <td> **Operator** </td>
  </tr>
  <tr>
    <td> *difference* </td>
    <td> `lows.difference(odds)` </td>
    <td> `lows - odds` </td>
  </tr>
  <tr>
    <td> *intersection* </td>
    <td> `lows.intersection(odds)` </td>
    <td> `lows &amp; odds` </td>
  </tr>
  <tr>
    <td> *subset* </td>
    <td> `lows.issubset(ten)` </td>
    <td> `lows <= ten` </td>
  </tr>
  <tr>
    <td> *strict subset* </td> <td> </td>
    <td> `lows < ten` </td>
  </tr>
  <tr>
    <td> *superset* </td>
    <td> `lows.issuperset(ten)` </td>
    <td> `lows >= odds` </td>
  </tr>
  <tr>
    <td> *strict superset* </td> <td> </td>
    <td> `lows >= odds` </td>
  </tr>
  <tr>
    <td> *exclusive or* </td>
    <td> `lows.symmetric_difference(odds)` </td>
    <td> `lows ^ odds` </td>
  </tr>
  <tr>
    <td> *union* </td>
    <td> `lows.union(odds)` </td>
    <td> `lows | odds` </td>
  </tr>
</table>

The fact that the values in a set are distinct makes them
a convenient way to get rid of duplicate values,
like the "unique atoms" problem at the start of this section.
Suppose we have a file containing the names of all the atoms in our warehouse,
and our task is to produce a list of the their types.
Here's how simple that code is:
  
    import sys
    filename = sys.argv[1]
    source = open(filename, 'r')
    atoms = set()
    for line in source:
        name = line.strip()
        atoms.add(name)
    source.close()
    print atoms

We start by opening the file
and creating an empty set which we will fill with atomic symbols.
As we read the lines in the file,
we strip off any whitespace (such as the newline character at the end of the line)
and put the resulting strings in the set.
If our input is the file:

    Na
    Fe
    Na
    Si
    Pd
    Na

then our output is:

    <span class="output">set(['Fe', 'Si', 'Na'])</span>

The right atoms are there,
but what are those extra square brackets for?
The answer is that
if we want to construct a set with values using `set()`,
we have to pass those values in a single collection,
such as a list.
This syntax:

<pre>
set('Na', 'Fe', 'Si')
</pre>

<!-- continue -->
would be more natural,
but doesn't work.
On the positive side,
this means that we can construct a set from almost anything
that a `for` loop can iterate over:

    >>> set('lithium')
    <span class="out">set(['i', 'h', 'm', 'l', 'u', 't'])</span>

But hang on:
if we're adding characters to the set in the order
`'l'`, `'i'`, `'t'`, `'h'`, `'i'`, `'u'`, `'m'`,
why does Python show them in the order
`'i'`, `'h'`, `'m'`, `'l'`, `'u'`, `'t'`?
And why did it show `'Fe'` first in our set of atoms,
when `'Na'` was the first atom added?
To answer that question,
we need to look at how sets are actually stored
and why they're stored that way.

<div class="keypoints">

### Summary

- Use sets to store distinct unique values.
- Create sets using `set()` or `{*v1*, *v2*, ...}`.
- Sets are mutable, i.e., they can be updated in place like lists.
- A loop over a set produces each element once, in arbitrary order.
- Use sets to find unique things.

</div>

<div class="challenges">

### Challenges

1. Mathematicians are quite comfortable negating sets:
for example, the negation of the set `{1, 2}` is all numbers that aren't 1 or 2.
Why don't Python's sets have a *`not` operator?

2. Fan has created a set containing the names of five noble gases:

        >>> print gases
        <span class="out">set(['helium', 'argon', 'neon', 'xenon', 'radon'])</span>

<!-- continue -->
He would like to print them in alphabetical order.  What is one simple way
to do this?  (Hint: the `list` function converts its arguments to a list.)

3. Fan has the following code:

        left = {'He', 'Ar', 'Ne'}
        right = set()
        while len(left) > len(right):
            temp = left.pop()
            right.add(temp)

<!-- continue -->
What values could `left` and `right` have after this code is finished running?
Explain why your answer makes this code hard to test.

4. Fan has written the following code:

        left = {'He', 'Ar', 'Ne'}
        right = {'Ar', 'Xe'}
        for element in left:                <span class="comment"># X</span>
            if element not in right:        <span class="comment"># X</span>
                right.add(element)          <span class="comment"># X</span>
        assert left.issubset(right)

<!-- continue -->
What single line could be used in place of the three marked with
'X' to achieve the same effect?
    
</div>

<div class="slides">

### Slides

#### Motivating Problem

-   Want to know what kinds of atoms we have in our warehouse
-   Could use a list of unique atomic symbols seen so far
-   But checking and inserting are expensive
    - Takes an average of N<sup>2</sup> steps to do either
    - So doubling the size of the data slows the program down 4X

#### Introducing Sets

-   An unordered collection of distinct items
    - Collection: contains zero or more values
    - Distinct: each value is either in the set or not (no duplicates)
    - Unordered: elements are present or not (no sense of "first", "next", or "last")
-   Create a set using `{3, 5, 7}`
    - But must use `set()` for empty sets, because `{}` already meant something else when sets were added to Python
-   Support all the expected operations:
    - Union and intersection
    - Difference and symmetric difference (also called "exclusive or")
    - Subset/superset
    - Add/remove element
    - Clear

#### Solution to Problem

    import sys
    filename = sys.argv[1]
    source = open(filename, 'r')
    atoms = set()
    for line in source:
        name = line.strip()
        atoms.add(name)
    source.close()
    print atoms

Input:

    Na
    Fe
    Na
    Si
    Pd
    Na

Output:

    set(['Fe', 'Si', 'Na'])

#### Why The Square Brackets?

-   `set('Fe', 'Si', 'Na')` doesn't work: need to pass values as a single collection (like a list)
-   So default printed representation looks like that

</div>

</section>
