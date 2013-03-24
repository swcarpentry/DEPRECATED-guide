Numerical Programming With NumPy
================================

Madica Medicine is studying patients with Babbage's Syndrome, a rare
disorder whose sufferers believe they are living in Victorian England.
She has data on how well each patient has responded to several different
treatments, and would like to know how similar patients' responses are
to one another, and whether one treatment is superior to another.

Since Madica is new to this research area, she would also like to know
what papers would be most useful for her to read. Luckily, she has
access to a web site where scientists post ratings of papers, and she
knows the names of a few key researchers in the area. What she needs is
some way to combine their ratings to create recommendations.

All three problems can be solved by manipulating matrices. In this
chapter, we'll look at how Madica (and other scientists) can do this
efficiently, both in terms of their time and the computer's.

Basics
------

### Understand:

-   Why most numerical programmers should use high-level libraries
    instead of writing loops directly.
-   That most numerical libraries use a data-parallel programming model.
-   How to create multi-dimensional arrays with specific values.
-   How to create arrays with commonly-occurring values.
-   Why the values in such arrays must be homogeneous.
-   How to specify or change the type of the values in an array.
-   How to copy the values in an array.

One way to manipulate matrices in a program is to write lots of loops,
but doing this obscures the underlying mathematical operations. In most
languages, for example, something as simple as *a~i,j~ = b~i,j~+kv~i~*
turns into three lines, two of which are just management:

    for i in 1..N:
        for j in 1..N:
            a[i, j] = b[i, j] + k * v[i]

Instead of repeatedly writing loops like these, most programmers use
high-performance libraries written in low-level languages like Fortran
and C. For example, the Fortran subroutine in [Figure XXX](#f:packing),
which is taken from a numerical package called LAPACK, adds a complex
vector to the product of a constant and another complex vector:

![CAXPY Fortran Subroutine](img/numpy/caxpy.png)

People devote their entire careers to writing and tuning functions like
this, and most large scientific programs today are built by gluing
together calls to these libraries. However, functions with names like
`CAXPY` and half a dozen arguments aren't any more readable than the
double loop they replace (though they are usually much faster, since
they'll have been tuned by specialists). For this reason, many
programmers today write numerical code in high-level languages like
MATLAB, R, or Python. The features in these langauges are almost always
implemented using the same high-performance libraries people could call
directly; while wrapping them up does cost a little in performance, they
increase overall productivity in all but a handful of cases.

Most high-level numerical languages and tools use a
[data-parallel](glossary.html#data-parallel) programming model, which
means operations act on entire arrays instead of using a lot of loops.
This chapter will show a few of the things that those libraries can do,
and, more importantly, how to think when using them. We will use
Python's NumPy for our examples, but the ideas translate directly to
MATLAB and similar languages.

It's important to keep in mind that scientific programmers use arrays in
at least three ways: as matrices in the mathematical sense, to represent
physical grids (like a latitude-longitude grid in climate modeling), or
as general-purpose multi-dimensional data storage. These different use
cases are one of the reasons why arrays have such a bewildering variety
of features: in a sense, their usability is a victim of their own
usefulness.

NumPy (which is short for "Numerical Python") provides high-performance
arrays for Python. Most importantly, it provides a data-parallel
programming model: if we want to multiply a vector, a matrix, and the
transpose of the vector, we write `x*A*x.T` and the computer fills in
any loops that are required.

To get started with NumPy, let's create an array from a list of numbers:

~~~~ {src="src/numpy/create_array.py"}
import numpy
vals = [1, 2, 3]
arr = numpy.array(vals)
print 'array is', arr
[1 2 3]
~~~~

We `import numpy` and then call `numpy.array` with a list of initial
values as an argument. The resulting array is three elements long. Note
that if we use `print` to display the array, Python shows us its values
in square brackets, without the separating commas that it uses for
lists. If we just ask Python to display the array interactively, on the
other hand, it shows us what we would have to type in to re-create it:

    >>> import numpy
    >>> arr = numpy.array([1, 2, 3])
    >>> arr
    array([1, 2, 3])

Unlike Python lists, NumPy arrays must be
[homogeneous](glossary.html#homogeneous): all values must have exactly
the same type. This allows values to be packed together as shown in
[Figure XXX](#f:packing), which not saves memory, but is also faster to
process. We'll discuss this in more detail in [the next
section](#s:storage).

![Packing Values](img/numpy/packing.png)

If we give NumPy initial values of different types, it finds the most
general type and stores all the values in the array using that type. For
example, if we construct an array from an integer and a float, the
array's values are both floats:

~~~~ {src="src/numpy/mixed_types.py"}
arr = numpy.array([1, 2.3])
print arr
[1.  2.3]
~~~~

If we want a specific type, we can pass an optional argument to `array`
called `dtype` (for "data type"). For example, we can tell NumPy to
create an array of 32-bit floats even though all the initial values are
integers:

~~~~ {src="src/numpy/force_type.py"}
print numpy.array([1, 2, 3, 4], dtype=numpy.float32)
[ 1. 2. 3. 4.]
~~~~

NumPy provides many basic numerical data types, each of which is
identified by a name like `float32`. The three called `int`, `float`,
and `complex` are whatever the underlying hardware uses as its native
type, which is usually either 32 or 64 bits long. That word "either" is
why programs usually shouldn't use them: halving or doubling the
precision of the values in a program will almost always change its
results.

### The Dangers of Making Things Simple

Programs that use `int`, `float`, and `complex` should *not* import them
as:

    from numpy import int, float, complex

because those three names are also the names of built-in Python types.

If we have a matrix whose values are of one type, but for some reason
want values of another type, we can use its `astype` method to create a
new matrix:

~~~~ {src="src/numpy/astype.py"}
arr = numpy.array([1, 2, 3, 4], dtype=numpy.int32)
print arr
[1 2 3 4]
print arr.astype(numpy.float32)
[ 1.  2.  3.  4.]
~~~~

What we should *not* do is change the array's data type directly (even
though the language lets us do this). If, for example, we tell NumPy to
start treating an array of floating point numbers as integers, it won't
convert the values: instead, it will just start interpreting their bits
differently:

~~~~ {src="src/numpy/change_dtype.py"}
import numpy
arr = numpy.array([1.0, 2.0, 3.0, 4.0], dtype=numpy.float32)
print arr
[ 1.  2.  3.  4.]
arr.dtype = numpy.int32
print arr
[1065353216 1073741824 1077936128 1082130432]
~~~~

There are many other ways to create arrays besides calling `array`. For
example, the `zeros` function takes a tuple specifying array dimensions
as an argument and returns an array of zeros of that size:

~~~~ {src="src/numpy/zeros.py"}
import numpy as np
z = np.zeros((2, 3))
print z
[[0. 0. 0.],
 [0. 0. 0.]]
~~~~

Note that we are importing NumPy as `np` in order to save a bit of
typing. We'll do this in all the examples below as well. Notice also
that the array's data type is `float` unless something else is specified
using `dtype`.

The `ones` and `identity` functions work much the same way as `zeros`:

~~~~ {src="src/numpy/ones_identity.py"}
o = np.ones((2, 3))
print o
[[1. 1. 1.],
 [1. 1. 1.]]
z = np.identity((2))
print z
[[1. 0.],
 [0. 1.]]
~~~~

It's also possible to create NumPy arrays without filling them with data
using the `empty` function. This function does not initialize the
values, so the array contains whatever bits were lying around in memory
when it was called:

~~~~ {src="src/numpy/empty.py"}
e = np.empty((2, 2))
print e
[[3.82265e-297, 4.94944e+173],
 [1.93390e-309, 1.00000e+000]]
~~~~

This might not seem particularly useful, but if a program is going to
overwrite an array immediately after creating it, there's no point
taking the time to fill it.

### The Simplest Case Looks Odd

Calls to `zeros`, `ones`, `identity`, and `empty` can look a little odd
when they're being used to create vectors:

~~~~ {src="src/numpy/vector_ones.py"}
print np.ones((5,))
[ 1.  1.  1.  1.  1.]
~~~~

The inner parentheses are there because dimensions have to be given as a
tuple, rather than separately. The comma is there because otherwise
`(5)` would be interpreted as "the number 5" rather than "the tuple
containing only the number 5" in order to be consistent with `(3+2)`.

As with everything else in Python, assigning an array to a variable does
not copy its data, but instead creates an alias for the original data:

~~~~ {src="src/numpy/alias.py"}
first = np.ones((2, 2))
print first
[[1. 1.],
 [1. 1.]]
second = first
print second
[[1. 1.],
 [1. 1.]]
second[0, 0] = 9
print first
[[9. 1.],
 [1. 1.]]
~~~~

Notice while we're here that when we subscript a NumPy array to select a
single element, we put all the indices inside one set of square brackets
separated with commas, rather than bracketing each index separately:
it's `a[0, 1]`, not `a[0][1]`, because the array is a single object,
taking a single subscript, rather than something like a list of lists,
which requires one index for the outer list and another for the inner.

If we really want a copy of the array so that we can make changes
without affecting the original data, we must use the `copy` method:

~~~~ {src="src/numpy/alias.py"}
print first
[[1. 1.],
 [1. 1.]]
second = first.copy()
second[0, 0] = 9
print first
[[1. 1.],
 [1. 1.]]
~~~~

Arrays have properties as well as methods. We have already met the
array's data type, `dtype`. Another important property is `shape`, which
is a tuple of the array's size along each dimension:

~~~~ {src="src/numpy/shape.py"}
print first
[[1. 1.],
 [1. 1.]]
print first.shape
(2, 2)
~~~~

Notice that there are no parentheses after `shape`: it is a piece of
data, not a method call. Also note that the tuple in `shape` is exactly
what we pass into functions like `zeros` to create new arrays, which
makes it easy to reproduce the shape of existing data:

    blank = np.zeros(first.shape)
    print blank
    [[ 0.  0.]
     [ 0.  0.]]

Another data member is `size`, which is the total number of elements in
the array:

    block = np.zeros((4, 7, 3))
    print block.size
    84

Strictly speaking, `size` is redundant, since its value is always the
product of the elements in the array's `shape`, but it's often very
handy to have.

### Summary

-   High-level libraries are usually more efficient for numerical
    programming than hand-coded loops.
-   Most such libraries use a data-parallel programming model.
-   Arrays can be used as matrices, as physical grids, or to store
    general multi-dimensional data.
-   NumPy is a high-level array library for Python.
-   `import numpy` to import NumPy into a program.
-   Use `numpy.array(values)` to create an array.
-   Initial values must be provided in a list (or a list of lists).
-   NumPy arrays store homogeneous values whose type is identified by
    `array.dtype`.
-   Use `old.astype(newtype)` to create a new array with a different
    type rather than assigning to `dtype`.
-   `numpy.zeros` creates a new array filled with 0.
-   `numpy.ones` creates a new array filled with 1.
-   `numpy.identity` creates a new identity matrix.
-   `numpy.empty` creates an array but does not initialize its values
    (which means they are unpredictable).
-   Assigning an array to a variable creates an alias rather than
    copying the array.
-   Use `array.copy` to create a copy of an array.
-   Put all array indices in a single set of square brackets, like
    `array[i0, i1].`
-   `array.shape` is a tuple of the array's size in each dimension.
-   `array.size` is the total number of elements in the array.

Storage
-------

### Understand:

-   That arrays are stored using descriptors and data blocks.
-   That many operations on arrays create new descriptors that alias
    existing data blocks.

In order to do anything more with NumPy arrays, we need to understand
how they are stored in memory, just as we needed to learn about [hash
tables](setdict.html#s:storage) in order to understand sets and
dictionaries. To start, let's take a look at what happens when we
transpose a matrix:

~~~~ {src="src/numpy/transpose.py"}
first = np.array([[1, 2, 3],
                  [4, 5, 6]])
print first
[[1 2 3],
 [4 5 6]]
t = first.transpose()
print t
[[1 4],
 [2 5],
 [3 6]]
first[1, 1] = 999
print t
[[1 4],
 [2 999],
 [3 6]]
~~~~

The transposed array's elements appear to be in a different order, as
desired. On the other hand, it looks like `transpose` is creating an
alias, since changes to the original array are reflected in the
transposed array.

The secret is that NumPy doesn't store an array as a single block of
memory. Instead, it stores two things: the data, and a
[descriptor](glossary.html#descriptor) that specifies how to interpret
the data block: what data type it is, how many dimensions it has, its
size along each dimension, and the [stride](glossary.html#stride), or
spacing of elements, along each axis ([Figure XXX](#f:descriptor)).

![Array Descriptors](img/numpy/descriptor.png)

When we "transpose" a matrix, NumPy doesn't change the data itself.
Instead, it creates a new descriptor that points at the same data, but
counts down instead of up ([Figure XXX](#f:transpose)):

![Array Transposition](img/numpy/transpose.png)

NumPy does this because it's a lot faster than copying the actual data.
If we have a 1000×1000 matrix *A*, for example, we shouldn't have to
copy a million numbers just to calculate *A·A^T^*

The `ravel` method does something similar to `transpose`: it creates a
one-dimensional alias for the original data. As you'd expect, the
result's shape has a single value, which is the number of elements we
started with:

~~~~ {src="src/numpy/ravel.py"}
first = np.zeros((2, 3))
second = first.ravel()
print second.shape
(6,)
~~~~

What order do raveled values appear in? Let's start by thinking about a
2×4 array `A`. It looks two-dimensional, but the computer's memory is
1-dimensional: each location is identified by a single integer address.
Any program that works with multi-dimensional data must lay those values
out in some order. One possibility is [row-major
order](glossary.html#row-major-order), which concatenates the rows
([Figure XXX](#f:array_layout)). This is what C uses, and since Python
was originally written in C, it uses the same convention. In contrast,
[column-major order](glossary.html#column-major-order) concatenates the
columns. Fortran does this, and MATLAB follows along.

![Array Layout](img/numpy/array_layout.png)

Neither option is intrinsically better than the other, but the fact that
there are two choices causes headaches when data has to be moved from
one programming language to another. If your Python code wants to call
an eigenvalue function written in Fortran, you will probably have to
rearrange the data first, just as you have to be careful about 0-based
versus 1-based indexing. (Note that you cannot use the array's
`transpose` method to do this, since, as explained earlier, it doesn't
actually move data around.)

There are many other ways to reshape arrays, which once again create
aliases instead of rearranging the data. The most common is
(unsurprisingly) called `reshape`. Its arguments are the array's new
dimensions, *not* a tuple of those dimensions (which is proof that no
library is completely consistent):

~~~~ {src="src/numpy/reshape.py"}
first = np.array([1, 2, 3, 4, 5, 6])
print first.shape
(6,)
second = first.reshape(2, 3)
print second
[[1 2 3],
 [4 5 6]]
~~~~

Since `reshape` re-uses the existing data, the new shape must have the
same size as the original—we cannot add or drop elements:

~~~~ {src="src/numpy/bad_reshape.py"}
first = np.zeros((2, 2))
print first.reshape(3, 3)
ValueError: total size of new array must be unchanged
~~~~

If we really want to change the physical size of the data, we have to
use `array.resize`. This works in place, i.e., it actually modifies the
array instead of just creating a new descriptor:

~~~~ {src="src/numpy/resize.py"}
print block
[[ 10  20  30],
 [110 120 130],
 [210 220 230]])
block.resize(2, 2)
print block
[[ 10  20],
 [ 30 110]]
~~~~

As the example above shows, when we resize a 3×3 array to be 2×2, we get
the first four values from the data block, rather than the values from
the first two rows and columns. (And note that, once again, the new
dimensions are passed directly rather than in a tuple.)

If we enlarge the array by resizing, the new locations are assigned
zero. Which locations are "new" is determined by the raveling order of
the array: as the example below shows, the existing values are packed
into the first part of memory, *not* into the upper left corner of the
logical matrix.

~~~~ {src="src/numpy/ravel_resize.py"}
ones = np.ones((2, 2))
print ones
[[ 1.  1.]
 [ 1.  1.]]
ones.resize(3, 3)
print ones
[[ 1.  1.  1.]
 [ 1.  0.  0.]
 [ 0.  0.  0.]]
~~~~

### Summary

-   Arrays are stored using descriptors and data blocks.
-   Many operations create a new descriptor, but alias the original data
    block.
-   Array elements are stored in row-major order.
-   `array.transpose` creates a transposed alias for an array's data.
-   `array.ravel` creates a one-dimensional alias for an array's data.
-   `array.reshape` creates an arbitrarily-shaped alias for an array's
    data.
-   `array.resize` resizes an array's data in place, filling with zero
    as necessary.

Indexing
--------

### Understand:

-   How to operate on regular subsets of the elements of an array.
-   How to operate on array elements at arbitrary locations.
-   How to operate on array elements according to their values.

Arrays are subscripted by integers, just like lists and strings, and
they can be sliced like other sequences as well. For example, if `block`
is the array shown in [Figure XXX](#f:slicing), then `block[0:3, 0:2]`
selects its first three rows and the first two columns. As always, a
slice `start:end` includes the element at `start`, but not the element
at `end`.

![Slicing Arrays](img/numpy/slicing.png)

As with other sliceable things, it's possible to assign to slices of
arrays. For example, we can assign zero to the center elements of
`block` in a single statement:

~~~~ {src="src/numpy/assign_to_slice.py"}
print block
[[ 10  20  30  40],
 [110 120 130 140],
 [210 220 230 240]]
block[1, 1:3] = 0
print block
[[ 10  20  30  40],
 [110   0   0 140],
 [210 220 230 240]]
~~~~

One important difference between slicing arrays and slicing lists is
that slicing an array creates an alias—or rather, a new descriptor that
only refers to a portion of the original array's data block ([Figure
XXX](#f:slice_alias)):

~~~~ {src="src/numpy/slice_alias.py"}
original = np.ones((3, 2))
print original
[[ 1.  1.]
 [ 1.  1.]
 [ 1.  1.]]
slice = original[0:2, 0:2]
print slice
[[ 1.  1.]
 [ 1.  1.]]
slice[:,:] = 0
print slice
[[ 0.  0.]
 [ 0.  0.]]
print original
[[ 0.  0.]
 [ 0.  0.]
 [ 1.  1.]]
~~~~

![Slicing and Alaising](img/numpy/slice_alias.png)

Notice in the example above that we used `slice[:,:]` to refer to all of
the array's elements at once. All of Python's other slicing shortcuts
work as well, so that expressions like `original[-2:, 1:]` behave
consistently (though it may take a bit of practice to figure out exactly
what they mean).

Slicing on both sides of an assignment is a handy way to move data
around. If `vector` is a one-dimensional array, then `vector[1:4]`
selects locations 1, 2, and 3, while `vector[0:3]` selects locations 0,
1, and 2. Assigning the former to the latter therefore overwrites the
lower three values with the upper three, leaving the uppermost value
untouched:

~~~~ {src="src/numpy/slice_shift.py"}
vector = np.array([10, 20, 30, 40])
vector[0:3] = vector[1:4]
print vector
[20 30 40 40]
~~~~

The same thing works if we shift the data up instead of down:

~~~~ {src="src/numpy/slice_shift.py"}
vector = np.array([10, 20, 30, 40])
vector[1:4] = vector[0:3]
print vector
[10 10 20 30]
~~~~

It's worth mentioning this because if we try to do these shifts by
writing loops ourselves, it's all too easy to copy one value upward (or
downward) instead of shifting values:

~~~~ {src="src/numpy/loop_shift.py"}
vector = [10, 20, 30, 40]
for i in range(1, len(vector)):
    vector[i] = vector[i-1]
print vector
[10, 10, 10, 10]
~~~~

Try fixing this code so that it actually does a shift, and you'll see
why most programmers prefer to use slices and let the library figure out
the details.

We can do even more sophisticated things by using a list or another
array as a subscript. For example, if `subscript` is the list
`[3, 1, 2]`, then `vector[subscript]` creates a new array whose elements
are pulled from `vector` in that order ([Figure
XXX](#f:list_subscript)):

~~~~ {src="src/numpy/subscript_list.py"}
vector = np.array([0, 10, 20, 30])
print vector
[ 0 10 20 30]
subscript = [3, 1, 2]
print vector[subscript]
[30 10 20]
~~~~

![Subscripting With a List](img/numpy/list_subscript.png)

This works in multiple dimensions as well. For example, if we have a 2×2
matrix, and subscript it with the list containing only the index 1, the
result is the second row of the matrix:

~~~~ {src="src/numpy/subscript_2d.py"}
square = np.array([[5, 6], [7, 8]])
print square[ [1] ]
[[7 8]]
~~~~

Why does the subscript have to be in a list? And why does it return that
particular row? The answers are in the NumPy documentation, and while
those answers aren't simple, every bit of complexity is there for a good
reason.

Let's have a look at another way to subscript. If we compare our
vector's elements to the value 25, we get a vector with `True` where the
element passed the test and `False` where it didn't. (As we saw in the
previous section, `dtype=bool` is NumPy's way of telling us what the
array elements' data type is.)

~~~~ {src="src/numpy/vector_less.py"}
print vector
[ 0 10 20 30]
print vector < 25
[ True  True  True False]
~~~~

We can use a Boolean array like this as a [mask](glossary.html#mask) to
select certain elements from our original array. Here, the expression
`vector[vector<25]` gives us a vector containing only the elements that
passed the test ([Figure XXX](#f:vector_mask)):

~~~~ {src="src/numpy/vector_mask.py"}
print vector
[ 0 10 20 30]
print vector[ vector < 25 ]
[ 0 10 20]
~~~~

![Masking a Vector](img/numpy/vector_mask.png)

When we subscript an array with a list, another array, or a Boolean
mask, the result is *not* an alias: data actually is copied. The reason
is that we cannot represent the mask as a combination of strides and
offsets, so we cannot simply created a new descriptor to alias the
existing data. Despite this, some magic behind the scenes *does* let us
assign to masked arrays:

~~~~ {src="src/numpy/assign_to_mask.py"}
print vec
[0 1 2 3]
vec[vec < 2] = 100
print vec
[100 100   2   3]
~~~~

Operators like `<` and `==` work the way we would expect with arrays,
i.e., they do whatever they would do for individual elements, but for
every corresponding pair of elements. There is one trick, though. Python
does not allow objects to re-define the meaning of `and`, `or`, and
`not`, since they are keywords. The expression
`(vector <= 20) and (vector >= 20)` therefore produces an error message
instead of selecting elements with exactly the value 20:

~~~~ {src="src/numpy/cannot_and.py"}
print vector
[0 10 20 30]
print vector <= 20
[True True True False], dtype=bool)
print (vector <= 20) and (vector >= 20)
ValueError: The truth value of an array with more than one element is ambiguous.
~~~~

One solution is to use the functions `logical_and` and `logical_or`,
which combine the elements of Boolean arrays like their namesakes:

~~~~ {src="src/numpy/logical_funcs.py"}
print vector
print np.logical_and(vector <= 20, vector >= 20)
[False False  True False]
print vector[np.logical_and(vector <= 20, vector >= 20)]
[20]
~~~~

Another is to use the `&` and `|` operators. These normally work on the
bits making up data, but NumPy redefines them to be "and" and "or" for
Boolean arrays:

~~~~ {src="src/numpy/logical_funcs.py"}
print vector[(vector <= 20) & (vector >= 20)]
[20]
~~~~

Finally, NumPy provides a whole-array alternative to `if` and `else`
called `where`. Its first argument is a Boolean mask. Where that is
true, it takes the value from its second argument; where it is false, it
takes its third. For example, `where(vector < 25, vector, 0)` produces
an array whose values are taken from `vector` where they are less than
25, and 0 where they are greater than or equal to 25. Similarly,
`where(vector > 25, vector/10, vector)` scales large values or leaves
values alone:

~~~~ {src="src/numpy/where.py"}
print vector
[10 20 30 40]
print np.where(vector < 25, vector, 0)
[10 20  0  0]
print np.where(vector > 25, vector/10, vector)
[10 20  3  4]
~~~~

The `choose` and `select` functions do similar things, but work in
slightly different ways ([Figure XXX](#f:array_conditionals)). Again,
the number of possibilities can be overwhelming at first, but each of
these functions exists for a reason, and if we are going to spend a lot
of time doing matrix calculations, it is worth learning their ins and
outs.

![Array Conditionals](img/numpy/array_conditionals.png)

### Summary

-   Arrays can be sliced using `start:end:stride` along each axis.
-   Values can be assigned to slices as well as read from them.
-   Arrays can be used as subscripts to select items in arbitrary ways.
-   Masks containing `True` and `False` can be used to select subsets of
    elements from arrays.
-   Use '&' and '|' (or `logical_and` and `logical_or`) to combine tests
    when subscripting arrays.
-   Use `where`, `choose`, or `select` to select elements or
    alternatives in a single step.

Linear Algebra
--------------

### Understand:

-   How to perform common linear algebra operations on arrays.

NumPy arrays make it easy to do things with rectangular blocks of data,
but they aren't the matrices that mathematicians use. For example, let's
create an array and then multiply it by itself:

~~~~ {src="elementwise_mult.py"}
print a
[[1 2]
 [3 4]]
print a * a
[[ 1  4]
 [ 9 16]]
~~~~

NumPy does the operation elementwise instead of doing "real" matrix
multiplication. To do the latter, we must use the `dot` method:

~~~~ {src="elementwise_mult.py"}
print np.dot(a, a)
[[ 7 10]
 [15 22]]
~~~~

On the bright side, elementwise operation means that array addition
works as you would expect:

~~~~ {src="elementwise_mult.py"}
print a + a
[[2 4]
 [6 8]]
~~~~

And since there's only one sensible way to interpret an expression like
"array plus one", NumPy does the sensible thing there too:

~~~~ {src="elementwise_mult.py"}
print a + 1
[[2 3]
 [4 5]]
~~~~

Like other array-based libraries or languages, NumPy provides many
useful tools for common linear algebra operations. We can add up the
values in our array with a single function call:

~~~~ {src="src/numpy/linalg_ops.py"}
print np.sum(a)
10
~~~~

We can also calculate partial sums along each axis by passing an extra
argument into `sum` ([Figure XXX](#f:sum_axis)):

~~~~ {src="src/numpy/linalg_ops.py"}
print np.sum(a, 0)
[4 6]
print np.sum(a, 1)
[3 7]
~~~~

![Summing Along Axes](img/numpy/sum_axis.png)

It's very important to use NumPy's summation function (`np.sum` in the
examples above) rather than Python's built-in `sum`:

~~~~ {src="src/numpy/linalg_ops.py"}
print sum(a)
[4 6]
print sum(a, 0)
[4 6]
print sum(a, 1)
[5 7]
~~~~

This is one of the reasons most people prefer to use array methods
instead of functions:

~~~~ {src="src/numpy/linalg_methods.py"}
print a
[[1, 2], [3, 4]]
print a.sum()
10
print a.sum(0)
[4 6]
print a.sum(1)
[3 7]
~~~~

Let's return to the original example in this chapter. Madica is studying
the progress of Babbage's Syndrome in some test subjects. Her
observations are in an array: each row corresponds to one patient, and
each column is an hourly count of responsive T cells:

~~~~ {src="src/numpy/patient_data.py"}
print data
[[ 1  3  3  5 12 10  9]
 [ 0  1  2  4  8  7  8]
 [ 0  4 11 15 21 28 37]
 [ 2  2  2  3  3  2  1]
 [ 1  3  4  5 10  8  6]]
~~~~

This means that the zeroth column of our data is the initial T cell
count for all patients, while the zeroth row is all hourly samples for
patient 0:

~~~~ {src="src/numpy/patient_data.py"}
print data[:, 0]   # t0 count for all patients
[1 0 0 2 1]
print data[0, :]   # all samples for patient 0
[ 1  3  3  5 12 10  9]
~~~~

`data.mean()` gives us the average T cell count for all patients at all
times:

~~~~ {src="src/numpy/patient_data.py"}
data.mean()
6.88571428571
~~~~

It's nice to know we can do this, but it's not a particularly meaningful
statistic. The mean of the data along axis 0, on the other hand, gives
us the average across all patients for each hour:

~~~~ {src="src/numpy/patient_data.py"}
data.mean(0)   # over time
[  0.8   2.6   4.4   6.4  10.8  11.   12.2]
~~~~

This is much more useful, since it is the average progress of the
disease. Similarly, the mean along axis 1 gives us the average T cell
count per patient across all times, which could be useful if we need to
normalize the data:

~~~~ {src="src/numpy/patient_data.py"}
data.mean(1)   # per patient
[  6.14285714   4.28571429  16.57142857   2.14285714   5.28571429]
~~~~

It might be even more interesting to look at what happened to people who
started with no responsive T cells at all. The first step is to select
the first column of data, i.e., the initial T cell counts for each
patient, and compare these to zero. This produces a Boolean array with
`True` for each row of the array that meets our criteria:

~~~~ {src="src/numpy/patient_data.py"}
print data[:, 0]
[1 0 0 2 1]
print data[:, 0] == 0.
[False  True  True False False]
~~~~

If we use this to index the original array, we get the two rows for
which the count at *t~0~* is zero:

~~~~ {src="src/numpy/patient_data.py"}
data[ data[:, 0] == 0. ]
[[ 0  1  2  4  8  7  8]
 [ 0  4 11 15 21 28 37]]
~~~~

Now let's find the mean T cell count over time for just those people.
Once again, we start by selecting column 0 and testing it to create a
Boolean mask. Using that mask as a subscript gives us the rows that have
zero in the first place. We can now use the `mean` function along axis
zero (i.e., across patients) which gives us the average behavior of
patients who started with no responsive T cells at all:

~~~~ {src="src/numpy/patient_data.py"}
print data[ data[:, 0] == 0. ].mean(0)
[  0.    2.5   6.5   9.5  14.5  17.5  22.5]
~~~~

This example highlights two key practices for good matrix programming.
The first is to build expressions from the inside out. For example, the
one-liner above is logically equivalent to:

    first_col = data[:, 0]
    zero_at_zero = (first_col == 0)
    patient_rows = data[zero_at_zero]
    patient_rows.mean(0)

Beginners find the four-line version easier to figure out, but with
practice, naturally start writing the denser form.

The other key practice, which we alluded to in the introduction, is to
write high-level statements without loops and let the computer worry
about how to do the operations element by element. This is just as true
for MATLAB or R as it is for Python.

### Summary

-   Addition, multiplication, and other arithmetic operations work on
    arrays element-by-element.
-   Operations involving arrays and scalars combine the scalar with each
    element of the array.
-   `array.dot` performs "real" matrix multiplication.
-   `array.sum` calculates sums or partial sums of array elements.
-   `array.mean` calculates array averages.

Plotting
--------

Plotting: visualize the medical data versus time.

Making Recommendations
----------------------

### Understand:

-   How to get data into matrix form for efficient manipulation.
-   How to do simple statistical calculations involving matrices.

We can now use NumPy to build the academic matchmaking tool that Madica
wanted. More specifically, we can build a recommendation tool that
measures how similar people's reading interests are based on their
ratings of papers they have read and the ratings given by other people
in their field. Our program will be based on the movie recommendation
example in Toby Segaran's excellent book [Programming Collective
Intelligence](bib.html#segaran-collective-intelligence).

The first step is to decide on recommendation criteria. We want to take
into account how highly the paper was rated by other people, but we also
want to consider how similar people are to one another: if you and I
both rate the same papers highly, I should put more weight on your
rating of a new paper than on a rating from someone who likes papers I
dislike and vice versa.

We will divide our program into three pieces. First, we will take a list
of previous ratings and store them in a NumPy array. Second, we will
construct two ways to measure the similarity between two papers or
between two people's ratings. And finally, we will use those measures to
tell people who has interests similar to theirs.

Most people have only read a few of the thousands of papers in any
field. This means our rating data is [sparse](glossary.html#sparse),
i.e., mostly empty. One way to store sparse data is to use a dictionary
of dictionaries: the keys in the outer dictionary are people, while the
inner dictionaries store pairs of papers and ratings:

    raw_scores = {
        'Bhargan Basepair' : {
            'Jackson 1999' : 2.5,
            'Chen 2002' : 3.5,
        },
        'Fan Fullerene' : {
            'Jackson 1999' : 3.0,
            …
            …    …    …

Let's write a function called `prep_data` to convert this structure into
a list with the names of all the people, another list with the IDs of
all the papers, and a NumPy array of ratings:

    def prep_data(all_scores):
        # 1. Names of all people in alphabetical order.
        people = all_scores.keys()
        people.sort()

        # 2. Names of all papers in alphabetical order.
        papers = set()
        for person in people:
            for title in all_scores[person].keys():
                papers.add(title)
        papers = list(papers)
        papers.sort()

        # 3. Create and fill array.
        ratings = np.zeros((len(people), len(papers)))
        for (person_id, person) in enumerate(people):
            for (title_id, title) in enumerate(papers):
                r = scores[person].get(title, 0)
                ratings[person_id, title_id] = float(r)

        return people, papers, ratings

Let's have a closer look at how this function works ([Figure
XXX](#f:reformat_data)): The main dictionary of ratings has people's
names as keys, so all we need to do in step 1 to get a list of names is
ask the dictionary for its keys. We sort this list to help with testing:
Python doesn't store dictionary entries in any particular order, but our
sorted list will always be in a unique order.

![Reformatting Data](img/numpy/reformat_data.png)

Getting a list of all the papers' names in step 2 is a bit more
complicated. We start by creating an empty set called `papers`, then
loop over the sub-dictionaries in `all_scores` to add the names of the
papers in each to our set. This takes care of any duplication, since set
elements are guaranteed to be unique. Once everything is in the set, we
convert it to a list and sort it.

We can now create our ratings matrix (step 3). We know how many unique
people and papers there are, so we create an array of zeroes with that
many rows and columns. We then loop over the lists we created in steps 1
and 2 and use those values to index our dictionary-of-dictionaries. If
there is a score for a particular combination of person and paper, we
copy it into our matrix; otherwise, we put in a zero.

The next step is to figure out how we're going to measure similarity.
Dozens of different measures have been developed, but whichever we use,
we have to treat zeroes in our matrix carefully: a 0 specifies no
ranking rather than a very poor ranking, which means we need to mask on
our array so that we only do statistics on papers that have actually
been rated by both of the people we are comparing.

Our first similarity measure is called the inverse sum of squares. It is
based on the distance between two N-dimensional vectors, where N is the
number of papers that both people rated. In two dimensions the distance
is given by the norm *distance^2^ = (x~A~-x~B~)^2^ + (y~A~-y~B~)^2^*. In
higher dimensions, we simply add more (*x~i~-x~j~)^2^* terms.

A small sum of squares means the ratings being considered are all nearly
the same. Since we want 1 to correspond to perfect agreement and a 0 to
complete disagreement, we invert the sum of squares, adding 1 the
denominator to achieve the desired range and to avoid division by zero.
The final formula is *sim(A,B) = 1/(1 + norm(A,B))*.

Let's write a function to calculate this:

    def sim_distance(prefs, left_index, right_index):

        # Where do both people have preferences?
        left_has_prefs  = prefs[left_index,  :] > 0
        right_has_prefs = prefs[right_index, :] > 0
        mask = np.logical_and(left_has_prefs, right_has_prefs)

        # Not enough signal.
        if np.sum(mask) < EPS:
            return 0

        # Return sum-of-squares distance.
        diff = prefs[left_index, mask] - prefs[right_index, mask]
        sum_of_squares = np.linalg.norm(diff) ** 2
        return 1/(1 + sum_of_squares)

`left_index` and `right_index` are the rows of the data we are
interested in, i.e., the people whose preferences we are comparing.
Since we only want to compare rankings if two people have both rated a
paper, the first thing we do is create a mask that is `True` in those
columns where both rows are nonzero. If no papers were rated by both
people, we return zero immediately. Otherwise, we compute the norm of
the difference of the ratings and we return the similarity score. (We
can use a library function `np.linalg.norm` to compute the actual
difference, but we need to square it to get the sum of squares.)

One problem with the inverse sum of squares is that it penalizes people
for using different scales. For example, if one person tends to be twice
as harsh or twice as enthusiastic as another, this metric will judge
them to be very different. We might get better answers if we look at how
papers are ranked relative to other rankings instead of at absolute
values. Pearson's Correlation score does this by normalizing the data
and reporting the correlation between scores.

Pearson's Correlation is related to the line of best fit. For example,
the graph in [Figure XXX](#f:correlation) shows high correlation because
the papers that were rated highly by Jean were also rated highly by
Betty. if the points were randomly scattered, we would call that low
correlation and want to report a low score.

![Correlation](img/numpy/correlation.png)

To calculate Pearson's Correlation, we need to know two things:

1.  the standard deviation, which is the average amount that a rating
    deviates from the mean rating; and
2.  the covariance, which measures how two variables change together.
    Covariance is positive and large if higher values of X correspond to
    higher values of Y, negative and large if higher values of X
    correspond to lower values of Y, and it will be zero if there is no
    pattern.

Pearson's Correlation score is the covariance normalized by both
standard deviations, i.e., *cov(X, Y) / σ~X~σ~Y~*. We want to use NumPy
routines to do as much of the calculation as possible, so after hunting
around the documentation, we find that `np.cov` can take two N×1 arrays
and produce a matrix that contains:

  ------------- -------------
  *var(X)*      *cov(X, Y)*
  *cov(X, Y)*   *var(Y)*
  ------------- -------------

Since the standard deviation is the square root of the variance, it
looks like this one function is all we will need. Here's our function:

    def sim_pearson(prefs, left_index, right_index):

        # 1. Where do both have ratings?
        rating_left  = prefs[left_index,  :]
        rating_right = prefs[right_index, :]
        mask = np.logical_and(rating_left > 0, rating_right > 0)

        # 2. Return zero if there are no common ratings.
        num_common = sum(mask)
        if num_common == 0:
            return 0

        # 3. Calculate Pearson score "r"
        varcovar = np.cov(rating_left[mask], rating_right[mask])
        numerator = varcovar[0, 1]
        denominator = sqrt(varcovar[0, 0]) * sqrt(varcovar[1,1])
        if denominator < EPS:
            return 0
        r = numerator / denominator
        return r

Step 1 is to create a mask so that we only include elements of the two
arrays that are nonzero. If there are no common ratings, we return zero
in step 2 as we did in our previous function. If there are some common
ratings, we can go ahead and compute the Pearson score. The variance of
the left rating is stored in position `[0,0]` of the matrix `varcovar`,
the variance of the right rating is stored at `[1,1]`, and off-diagonal
elements are the covariance. After a quick check to avoid division by
zero, we return the quotient of the covariance and the product of the
standard deviations.

Now that we have tools for scoring pairs of people, we can answer our
original question: who is most similar to whom? Since each row of our
matrix is a single person's scores, this comes down to applying either
similarity metric to the rows of the array and then sorting the results
to find the *N* people who are most similar:

    def top_matches(ratings, person, num, similarity):
        scores = []
        for other in range(ratings.shape[0]):
            if other != person:
                s = similarity(ratings, person, other)
                scores.append((s, other))

        scores.sort()
        scores.reverse()

        return scores[0:num]

Here, `person` is who we're trying to match other people against. For
each of those other people, we compute a similarity score and append it
to the list. Finally, we sort the list, then reverse it so that the
highest scores will be at the front and return the first `num` entries.

One thing to notice about this function is that we are passing in the
particular similarity function to use as an argument (called, not
surprisingly, `similarity`). This will be either `sim_distance` or
`sim_pearson`; since both functions take the same arguments, and produce
interchangeable results, we only have to write `top_matches` once.

We can use what we just built to measure how similar papers are to each
other simply by transposing our matrix so that rows represent papers
instead of people. With a bit more work, we can also use it to recommend
papers based on similarity scores, just as Amazon.com recommends books
that are like ones previously purchased.

The most important lesson, though, is that leaving all the number
crunching to NumPy let us build a high-performance solution with only a
page of code. In fact, the bulk of this program is there to get data
into a format the library can work with. That is typical of most data
crunching problems, and is another reason why general-purpose languages
like Python are the right choice for scientific computing: they come
with tools to do the "other 90%" of the work scientists need to do.

### Sparse Arrays

Describe SciPy sparse arrays.

### Summary

-   Getting data in the right format for processing often requires more
    code than actually processing it.
-   Data with many gaps should be stored in sparse arrays.
-   `numpy.cov` calculates variancess and covariances.

The Game of Life
----------------

### Understand:

-   How to use arrays to represent grids rather than matrices.
-   How to manage boundary conditions using "extra" array cells.
-   That most array operations are already implemented in standard
    libraries.

As we said in the introduction, scientific programmers use arrays in
several different ways. The recommendation example above shows them
being used for linear algebra; in this section, we'll see how to use
them to represent a physical grid.

The problem we'll tackle is called the Game of Life, and was invented by
the mathematician John Conway in 1970. The game's world is a rectangular
grid of cells, each of which is either "alive" or "dead". At each time
step, every cell simultaneously updates itself according to the
following rule:

1.  If a live cell has two or three live neighbors, it stays alive.
2.  If a dead cell has exactly three live neighbors, it becomes alive.
3.  In all other cases, the cell either dies or stays dead.

These simple rules produce a bewildering variety of behaviors depending
on the grid's initial state. In fact, it has been shown that the Game of
Life is [Turing complete](glossary.html#turing-complete), i.e., it can
perform any imaginable computation given enough time and space.

Let's start by writing the main body of our simulation:

~~~~ {src="src/numpy/life_looping.py"}
def main(args):
    length = int(args[1])
    if len(args) > 2:
        generations = int(args[2])
    else:
        generations = length - 1
    evolve(length, generations)

if __name__ == '__main__':
    main(sys.argv)
~~~~

This expects the user to give it a length, which is the size of the
(square) world, and optionally the number of generations to run the
simulation for. It then calls the function `evolve` to run the
simulation.

The `evolve` function looks like this:

~~~~ {src="src/numpy/life_looping.py"}
def evolve(length, generations):
    current = np.zeros((length, length), np.uint8)  # create the initial world
    current[length/2, 1:(length-1)] = 1             # initialize the world
    next = np.zeros_like(current)                   # hold the world's next state

    # advance through each time step
    show(current)
    for i in range(generations):
        advance(current, next)
        current, next = next, current
        show(current)
~~~~

Here, `current` holds the current state of the world, which we evolve
forward into a similarly-sized array `next`. We initialize `current`
with a single vertical bar of cells; this isn't as interesting as other
patterns, but we can come back and build more interesting initializers
later. The main loop then displays the current state of the world and
repeatedly advances it, leapfrogging `current` and `next` after each
update ([Figure XXX](#f:leapfrog)):

![Leapfrogging the Simulation](img/numpy/leapfrog.png)

We'll skip over the implementation of `show`: it just prints stars and
spaces to show live and dead cells ([Figure XXX](#f:ascii_output)).
`advance` ought to be simple too: given an N×N world, it just loops over
the (i,j) indices of `current`, counts the number of neighbors each cell
has, then assigns either 1 or 0 to `next`.

    +-----+
    |     |
    |  *  |
    |  *  |
    |  *  |
    |     |
    +-----+

ASCII Output

But just as [real-world data has holes](db.html#s:null), real-world
simulations have boundaries. How should we update the cell at (0,0)?
Should we assume its hypothetical neighbors outside the world are all 0
(or all 1)? Or give them random values? Or wrap the edges around to
create a torus ([Figure XXX](#f:torus)), or invent special update rules
for edge and corner cells?

![Periodic Boundary Conditions](img/numpy/torus.png)

The simplest solution for now is to fix the values of the boundary cells
at 0, and only update the (N-2)×(N-2) cells in the interior—again, we
can come back later and implement something more sophisticated once we
have the basic simulation working. With that decision made, our
`advance` function looks like this:

~~~~ {src="src/numpy/life_looping.py"}
def advance(current, next):
    assert current.shape[0] == current.shape[1], \
           'Expected square universe'
    length = current.shape[0]
    next[:, :] = 0
    for i in range(1, length-1):
        for j in range(1, length-1):
            neighbors = np.sum(current[i-1:i+2, j-1:j+2])
            if current[i, j] == 1:
                if 2 <= (neighbors-1) <= 3:
                    next[i, j] = 1
            else:
                if neighbors == 3:
                    next[i, j] = 1
~~~~

The hardest part of writing this is getting the indexing right. We want
to loop over the interior cells, so we use `range(1, length-1)` as the
span of our loops. To select the 3×3 region around cell (i,j) we use
`[i-1:i+2, j-1:j+2]`; the asymmetry (-1 but +2) comes from the fact that
Python includes the lower bound of a range but excludes the upper bound.
The test in the inner `if` then looks at `neighbors-1` instead of
`neighbors` because we don't want to include the 1 for the cell we're
checking in our considerations. We could change the inner `if` to be:

                    if 3 <= neighbors <= 4:

but that will confuse most readers: the rules mention 2 and 3, not 3 and
4, so we should use the former values.

At this point we have a working program, but it breaks one of our rules:
we're looping over the elements of the array. We can fix this using a
function from the SciPy signal processing library called `convolve`.
Convolution can be thought of as the product of two functions, or, if
we're working with grids, as the result of combining the values in one
grid according to the weights in another. To use it, we import the
function:

~~~~ {src="src/numpy/life_convolve.py"}
from scipy.signal import convolve
~~~~

and then define the weights we want around each cell:

~~~~ {src="src/numpy/life_convolve.py"}
FILTER = np.array([[1, 1, 1],
                   [1, 0, 1],
                   [1, 1, 1]], dtype=np.uint8)
~~~~

Advancing to the next time step is then as simple as:

~~~~ {src="src/numpy/life_convolve.py"}
def advance(current, next):
    assert current.shape[0] == current.shape[1], \
           'Expected square universe'
    next[:, :] = 0
    neighbors = convolve(current, FILTER, mode='same')
    next[(current == 1) & ((neighbors == 2) | (neighbors == 3))] = 1
    next[(current == 0) & (neighbors == 3)] = 1
~~~~

(As explained [earlier](#p:boolean-ops), we have to use `&` and `|`
instead of `and` and `or` to combine tests on arrays.) This
implementation isn't just shorter than our first version: it's also more
efficient, since `convolve` works directly on the low-level data blocks
inside our arrays. The hardest part is actually discovering that
`convolve` exists, and figuring out that it's the tool we need for this
job.

### Summary

-   Padding arrays with fixed elements is an easy way to implement
    boundary conditions.
-   `scipy.signal.convolve` applies a weighted mask to each element of
    an array.

Summing Up
----------

Mention Pandas.

Finally, always remember that you're not the first person to program
with matrices. Always take a look at the online documentation for NumPy
before writing any functions of your own. The library includes routines
to conjugate, convolve, and correlate matrices, to extract diagonals,
calculate FFTs, gradients, histograms, and least squares, and to find
net present value if you're doing financial mathematics. It can find
roots, solve sets of linear equations, and do singular value
decomposition. These functions are all faster than anything you could
easily write, and what's more, someone else has tested and debugged
them.
