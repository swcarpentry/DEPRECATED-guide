1.  [How We Got Here](#s:history)
2.  [Formatting Rules](#s:formatting)
3.  [Attributes](#s:attributes)
4.  [More HTML](#s:morehtml)
5.  [Creating Documents](#s:templating)
6.  [How the Web Works](#s:http)
7.  [Getting Data](#s:client)
8.  [Providing Data](#s:server)
9.  [Creating an Index](#s:index)
10. [Syndicating Data](#s:syndicate)
11. [Summing Up](#s:summary)

Carla Climate is studying climate change in the Northern and Southern
hemispheres. As part of her work, she wants to see whether the gap
between annual temperatures in Canada and Australia increased during the
Twentieth Century. The raw data she needs is available online; her goal
is to get it, do her calculations, and then post her results so that
other scientists can use them.

This chapter is about how she can do that. More specifically, it's about
how to fetch data from the web, and how to create web pages that are
useful to both human beings and computers. What we will *not* cover is
how to build interactive web applications: our experience has shown that
all we can do in the time we have is show you how to create security
holes, which we're reluctant to do. However, everything in this chapter
is a prerequisite for doing that, and there are lots of other good
tutorials available if you decide that's what you really need.

How We Got Here
---------------

### Understand:

-   The difference between structured and unstructured data.
-   The relationship between HTML and XML.

To start, let's have another look at the hearing tests from [our chapter
on Python programming](python.html). Most people would probably store
these results in a plain text file with one row for each test:

    Date         Experimenter        Subject          Test       Score
    ----------   ------------        -------          -----      -----
    2011-05-02   A. Binet            H. Ebbinghaus    DL-11      88%
    2011-05-07   A. Binet            H. Ebbinghaus    DL-12      71%
    2011-05-02   A. Binet            W. Wundt         DL-11      29%
    2011-05-02   C. S. Pierce        W. Wundt         DL-11      45%

This is pretty much what a conscientious researcher would write in a lab
notebook, and is easy for a human being to read. It's a lot harder for a
computer to understand, though. Any program that wanted to load this
data would have to know that the first line of the file contains column
titles, that the second can be ignored, that the first field of each row
thereafter should be translated from text into a date, that the fields
after that start in particular columns (since the number of spaces
between them is variable, and the number of spaces inside names can also
vary—compare "A. Binet" with "C. S. Pierce"), and so on. Such a program
would not be hard to write, but having to write, debug, and maintain a
separate program for each data set would be tedious.

Now consider something a little less structured, like this quotation
from Richard Feynman's 1965 Nobel Prize acceptance speech:

> As a by-product of this same view, I received a telephone call one day
> at the graduate college at Princeton from Professor Wheeler, in which
> he said, "Feynman, I know why all electrons have the same charge and
> the same mass." "Why?" "Because, they are all the same electron!"

A lot of information is implicit in these four sentences, like the fact
that "Wheeler" and "Feynman" are particular people, that "Princeton" is
a place, that the speakers are alternating (with Wheeler speaking
first), and so on. None of that is "visible" to a computer program, so
if we had a database containing millions of documents and wanted to see
which ones mentioned both John Wheeler (the physicist, not the
geologist) and Princeton (the university, not the glacier), we might
have to wade through a lot of false matches. What we need is some way to
explicitly tell a computer all the things that human beings are able to
infer.

The first major effort to tackle this problem dates back to 1969, when
Charles Goldfarb and others at IBM created the [Standard Generalized
Markup Language](glossary.html#sgml), or SGML. It was designed as a way
of adding extra data to medical and legal documents so that programs
could search them more accurately. SGML was very complex (the
specification is over 500 pages long), and unless you were a specialist,
you probably didn't even know it existed: all you saw were the programs
that used it.

But in 1989 Tim Berners-Lee borrowed the syntax of SGML to create the
[HyperText Markup Language](glossary.html#html), or HTML, for his new
"World Wide Web". HTML looked superficially the same as SGML, but it was
much (much) simpler: almost anyone could write it, so almost everyone
did. However, HTML only had a small vocabulary, which users could not
change or extend. They could say, "This is a paragraph," or, "This is a
table," but not, "This is a chemical formula," or, "This is a person's
name."

Instead of adding thousands of new terms for different application
domains, a new standard for *defining* terms was created in 1998. This
standard is called the [Extensible Markup Language](glossary.html#xml)
(XML); it's much more complex than HTML, but still simpler than SGML,
and hundreds of specialized vocabularies have now been defined in terms
of it.

make analogy between XML and defining functions

More recently, a new version of HTML called HTML5 has been created. Web
programmers are very excited about it, primarily because its new
features allow them to create sophisticated user interfaces that run on
smart phones and tablets as well as conventional computers. In what
follows, though, we'll focus on some basics that haven't changed (much)
in 20 years.

### Summary

-   Structured data is much easier for machines to process than
    unstructured data.
-   Markup languages like HTML and XML can be used to add semantic
    information to text.

Formatting Rules
----------------

### Understand:

-   How HTML elements are represented as text.
-   That HTML elements must be nested to form a tree.

A basic HTML [document](glossary.html#document) contains
[elements](glossary.html#element) and [text](glossary.html#text). (The
full specification allows for many other things with names like
"external entity references" and "processing instructions", but we'll
ignore them.) The text in a document is just character data, and as far
as HTML is concerned, it has no intrinsic meaning: "Feynman" is just
seven characters, not a person.

Elements are [metadata](glossary.html#metadata) that describe the
meaning of the document's content. For example, one element might
indicate a heading, while another might signal that something is a
cross-reference or a person's name.

Elements are written using [tags](glossary.html#tag-xml), which must be
enclosed in angle brackets `<…>`. For example, `<cite>` is used to mark
the start of a citation, and `</cite>` is used to mark its end. Elements
must be properly nested: if an element called `inner` begins inside an
element called `outer`, `inner` must end before `outer` ends. This means
that `<outer>…<inner>…</inner></outer>` is legal HTML, but
`<outer>…<inner>…</outer></inner>` is not.

Here are some commonly-used HTML tags:

  Tag      Usage
  -------- -------------------------------------------------------------------------------
  `html`   Root element of entire HTML document.
  `body`   Body of page (i.e., visible content).
  `h1`     Top-level heading. Use `h2`, `h3`, etc. for second- and third-level headings.
  `p`      Paragraph.
  `em`     Emphasized text.

Finally, every well-formed document started with a `DOCTYPE`
declaration, which looks like:

    <!DOCTYPE html>

This tells programs what kind of elements are allowed to appear in the
document: 'html' (by far the most common case), 'math' for MathML, and
so on. Here is a simple HTML document that uses everything we've seen so
far:

    <!DOCTYPE html><html><body><h1>Dimorphism</h1><p>Occurring or existing in two different <em>forms</em>.</p></body></html>

A web browser like Firefox might present this document as:

![A Very Simple Web Page](web/very_simple.png)

Other devices will display it differently. A phone, for example, might
use a different background color for the heading, while a screen reader
for someone with visual disabilities would read the text aloud.

These different presentations are possible because HTML separates
content from presentation, or in computer science jargon, separates
[models](glossary.html#model) from [views](glossary.html#view). The
model is the data itself; the view is how that data is displayed, such
as a particular pattern of pixels on our screen or a particular sequence
of sounds on our headphones. A given model may be viewed in many
different ways, just as what files are on your hard drive can be viewed
as a list, as snapshots, or as a hierarchical tree ([Figure
XXX](#f:filesystem_views)).

![Different Views of a File System](web/filesystem_views.png)

People can construct models from views almost effortlessly—if you are
able to read, it's almost impossible *not* to see the letters "HTML" in
the following block of text:

    *   *  *****  *   *  *
    *   *    *    ** **  *
    *****    *    * * *  *
    *   *    *    *   *  *
    *   *    *    *   *  ****

Computers, on the other hand, are very bad at reconstructing models from
views. In fact, many of the things we do without apparent effort, like
understanding sentences, are still open research problems in computer
science. That's why markup languages were invented: they allow us to
explicitly specify the "what" that we infer so easily for computers'
benefit.

There are a couple of other formatting rules we need to know in order to
create and understand documents. If we are writing HTML by hand instead
of using a [WYSIWYG](glossary.html#wysiwyg) editor like LibreOffice or
Microsoft Word, we might lay it out like this to make it easier to read:

    <!DOCTYPE html>
    <html>
      <body>
        <h1>Dimorphism</h1>
        <p>Occurring or existing in two different <em>forms</em>.</p>
      </body>
    </html>

Doing this doesn't change how most browsers render the document, since
they usually ignore "extra" whitespace (highlighted above). refer back
to 'highlight' later when talking about CSS and semantic separation As
we'll see when we start writing programs of our own, though, that
whitespace doesn't magically disappear when a program reads the document
in, so at some point we have to decide what to do with it.

Second, we must use [escape sequences](glossary.html#escape-sequence) to
represent the special characters `<` and `>` for the same reason that we
have to use `\"` inside a double-quoted string in a program. where do we
explain escape sequences? In HTML and XML, an escape sequence is an
ampersand '&' followed by the abbreviated name of the character (such as
'amp' for "ampersand") and a semi-colon. The four most common escape
sequences are:

  Sequence   Character
  ---------- -----------
  `&lt;`     `<`
  `&gt;`     `>`
  `&quot;`   `"`
  `&amp;`    `&`

One final formatting rule is that every document must have a single
[root element](glossary.html#root-element), i.e., a single element must
enclose everything else. When combined with the rule that elements must
be properly nested, this means that every document can be thought of as
a [tree](glossary.html#tree). For example, we could draw the logical
structure of our little document as shown in [Figure
XXX](#f:very_simple_tree).

![Tree View of a Very Simple Web Page](web/very_simple_tree.png)

A document like this, on the other hand, is not strictly legal:

    <h1>Dimorphism</h1>
    <p>Occurring or existing in two different <em>forms</em>.</p>

because it has two top-level elements (the `h1` and the `p`). Most
browsers will render it correctly, since they're designed to accommodate
improperly-formatted HTML, but most programs won't, because they're not.
mention BeautifulSoup?

### Summary

-   HTML documents contain elements and text.
-   Elements are represented using tags.
-   Different devices may display HTML differently.
-   Every document must have a single root element.
-   Tags must be properly nested to form a tree.
-   Special characters must be written using escape sequences beginning
    with &.

Attributes
----------

### Understand:

-   How to customize elements with attributes.
-   When to use attributes rather than nested elements.

Elements can be customized by giving them
[attributes](glossary.html#attribute). These are name/value pairs
enclosed in the opening tag like this:

    <h1 align="center">A Centered Heading</h1>

or:

    <p class="disclaimer">This planet provided as-is.</p>

Any particular attribute name may appear at most once in any element,
just like keys may be present at most once in a
[dictionary](setdict.html#s:dict), so
`<p align="left" align="right">…</p>` is illegal. Attributes' values
*must* be in quotes in XML; HTML5 allows single-word values to be
unquoted, but quoting is still recommended.

Another similarity between attributes and dictionaries is that
attributes are unordered. They have to be *written* in some order, just
as the keys and values in a dictionary have to be displayed in some
order when they are printed, but as far as the rules of HTML are
concerned, the elements:

    <p align="center" class="disclaimer">This web page is made from 100% recycled pixels.</p>

and:

    <p class="disclaimer" align="center">This web page is made from 100% recycled pixels.</p>

mean the same thing.

### Attributes vs. Nested Elements

When should we use attributes, and when should we nest elements? As a
general rule, we should use attributes when:

-   each value can occur at most once for any element;
-   the order of the values doesn't matter; and
-   those values have no internal structure, i.e., we will never need to
    parse an attribute's value in order to understand it.

In all other cases, we should use nested elements. However, many
widely-used XML formats break these rules in order to make it easier for
people to write XML by hand. For example, in the Scalable Vector
Graphics (SVG) format used to describe images as XML, we would define a
rectangle as follows:

    <rect width="300" height="100" style="fill:rgb(0,0,255); stroke-width:1; stroke:rgb(0,0,0)"/>

In order to understand the `style` attribute, a program has to somehow
know to split it on semicolons, and then to split each piece on colons.
This means that general-purpose programs for handling XML can't extract
all the information that's implicit in SVG, which partly defeats the
purpose of using XML in the first place. compare to database rules: no
internal structure in columns

### Summary

-   Elements can be customized by adding key-value pairs called
    attributes.
-   An element's attributes must be unique, and are unordered.
-   Attribute values should not have any internal structure.

More HTML
---------

### Understand:

-   How to add lists, tables, images, and links to HTML.
-   That metadata should go in the document's head.

As anyone who has surfed the web has seen, web pages can contain a lot
more than just headings and paragraphs. To start with, HTML provides two
kinds of lists: `ul` to mark an unordered (bulleted) list, and `ol` for
an ordered (numbered) one. Items inside either kind of list must be
wrapped in `li` elements:

~~~~ {src="web/nested_lists.html"}
<!DOCTYPE html>
<html>
  <body>
    <ul>
      <li>A. Binet
        <ol>
          <li>H. Ebbinghaus</li>
          <li>W. Wundt</li>
        </ol>
      </li>
      <li>C. S. Pierce
        <ol>
          <li>W. Wundt</li>
        </ol>
      </li>
  </body>
</html>
~~~~

![Nested Lists](web/nested_lists.png)

Note how elements are nested: since the ordered lists "belong" to the
unordered list items above them, they are inside those items'
`<li>…</li>` tags. And remember, the indentation used to make this list
easier for people to read means nothing to the computer: we could put
the whole thing on one line, or write it as:

    <!DOCTYPE html>
    <html>
    <body>
      <ul>
        <li>A. Binet
      <ol>
        <li>H. Ebbinghaus</li>
        <li>W. Wundt</li>
      </ol>
        </li>
        <li>C. S. Pierce
      <ol>
        <li>W. Wundt</li>
      </ol>
        </li>
    </body>
    </html>

and the computer would interpret and display it the same way. A human
being, on the other hand, would find the inconsistent indentation of the
second layout much harder to follow.

HTML also provides tables, but they are awkward to use: tables are
naturally two-dimensional, but text is one-dimensional. This is exactly
like the problem of representing a two-dimensional array in memory, and
we solve it in the same way: by writing down the rows, and the columns
within each row, in a fixed order. link back to dev.html and numpy.html
The `table` element marks the table itself; within that, each row is
wrapped in `tr` (for "table row"), and within those, column items are
wrapped in `th` (for "table heading") or `td` (for "table data"):

~~~~ {src="web/simple_table.html"}
<!DOCTYPE html>
<html>
  <body>
    <table>
      <tr>
        <th></th>
        <th>A. Binet</th>
        <th>C. S. Pierce</th>
      </tr>
      <tr>
        <th>H. Ebbinghaus</th>
        <td>88%</td>
        <td>NA</td>
      </tr>
      <tr>
        <th>W. Wundt</th>
        <td>29%</td>
        <td>45%</td>
      </tr>
    </table>
  </body>
</html>
~~~~

![A Simple Table](web/simple_table.png)

### Tables and Multi-Column Layout

Tables are sometimes used to do multi-column layout, as well as for
tabular data, but this is a bad idea. To understand why, consider two
other HTML tags: `i`, meaning "italics", and `em`, meaning "emphasis".
The former directly controls how text is displayed, but by doing so, it
breaks the separation between model and view that is the heart of
markup's usefulness. Without understanding the text that has been
italicized, a program cannot understand whether it is meant to indicate
someone shouting, the definition of a new term, or the title of a book.
The `em` tag, on the other hand, has exactly one meaning, and that
meaning is different from the meaning of `dfn` (a definition) or `cite`
(a citation).

Similarly, finish the thought...

HTML pages can also contain images. (In fact, the World Wide Web didn't
really take off until the Mosaic browser allowed people to mix images
with text.) The word "contain" is misleading, though: HTML documents can
only contain text, so we cannot store an image "in" a page. Instead, we
must put it in some other file, and insert a reference to that file in
the HTML using the `img` tag. Its `src` attribute specifies where to
find the image file; this can be a path to a file on the same host as
the web page, or a URL for something stored elsewhere. For example, when
a browser displays this:

~~~~ {src="web/simple_image.html"}
<!DOCTYPE html>
<html>
  <body>
    <p>My daughter's first online chat:</p>
    <img src="madeleine.jpg"/>
    <p>but probably not her last.</p>
  </body>
</html>
~~~~

it looks for the file `madeleine.jpg` in the same directory as the HTML
file:

![Simple Images](web/simple_image.png)

Notice, by the way, that the `img` element is written as `<img…/>`,
i.e., with a trailing slash inside the `<>` rather than with a separate
closing tag. This makes sense because the element doesn't contain any
text: the content is referred to by its `src` attribute. Any element
that doesn't contain anything can be written using this short form.

Images don't have to be in the same directory as the pages that refer to
them. When the browser displays this:

~~~~ {src="web/image_with_path.html"}
<!DOCTYPE html>
<html>
  <body>
    <p>Yes, she knows she's cute:</p>
    <img src="img/cute-smile.jpg"/>
  </body>
</html>
~~~~

it looks in the directory containing the page for a sub-directory called
`img`, and loads the image file from there, while if it's given:

~~~~ {src="web/image_with_url.html"}
<!DOCTYPE html>
<html>
  <body>
    <img src="http://software-carpentry.org/img/software-carpentry-logo.png"/>
  </body>
</html>
~~~~

it downloads the image from the URL
`http://software-carpentry.org/img/software-carpentry-logo.png` and
displays that.

Whenever we refer to an image, we should use the `img` tag's `alt`
attribute to provide a title or description of the image. This is what
screen readers for people with visual handicaps will say aloud to
"display" the image; it's also what search engines use to classify
images so that people can find them. Adding this to our previous example
gives:

    <!DOCTYPE html>
    <html>
      <body>
        <p>My daughter's first online chat:</p>
        <img src="madeleine.jpg" alt="Madeleine's first online chat"/>
        <p>but probably not her last.</p>
      </body>
    </html>

The most important use of URLs in documents is to create the links
within and between pages that make HTML "hypertext". We create links
using the `a` element. Whatever is inside the element is displayed and
(usually) underlined for clicking; this is usually a few words text, but
it can also be an entire paragraph, a table, or an image.

The `a` element's `href` attribute specifies what the link is pointing
at; as with images, this can be either a local filename or a URL. For
example, we can create a listing of the examples we've written so far
like this:

~~~~ {src="web/simple_listing.html"}
<!DOCTYPE html>
<html>
  <body>
    <p>
      Simple HTML examples for
      <a href="http://software-carpentry.org">Software Carpentry</a>.
    </p>
    <ol>
      <li><a href="very-simple.html">a very simple page</a></li>
      <li><a href="hide-paragraph.html">hiding paragraphs</a></li>
      <li><a href="nested-lists.html">nested lists</a></li>
      <li><a href="simple-table.html">a simple table</a></li>
      <li><a href="simple-image.html">a simple image</a></li>
    </ol>
  </body>
</html>
~~~~

![Using Hyperlinks](web/simple_listing.png)

The hyperlink element is called `a` because it can also used to create
[anchors](glossary.html#anchor) in documents by giving them a `name`
attribute instead of an `href`. An anchor is simply a location in a
document that can be linked to. For example, suppose we formatted the
Feynman quotation given earlier like this:

    <blockquote>
      As a by-product of this same view, I received a telephone call one day
      at the graduate college at <a name="pu">Princeton</a>
      from Professor Wheeler, in which he said,
      "Feynman, I know why all electrons have the same charge and the same mass."
      "Why?"
      "Because, they are all the same electron!"
    </blockquote>

If this quotation was in a file called `quote.html`, we could then
create a hyperlink directly to the mention of Princeton using
`<a href="quote.html#pu">`. The `#` in the `href`'s value separates the
path to the document from the anchor we're linking to. Inside
`quote.html` itself, we could link to that same location simply using
`<a href="#pu">`.

Using the `a` element for both links and targets was poor
design—programs are simpler to write if each element has one purpose,
and one alone—but we're stuck with it now. A more modern way to create
anchors is to add an `id` attribute to some other element. For example,
if we wanted to be able to link to the quotation itself, we could write:

    <blockquote id="wheeler-electron-quote">
      As a by-product of this same view, I received a telephone call one day
      at the graduate college at <a name="pu">Princeton</a>
      from Professor Wheeler, in which he said,
      "Feynman, I know why all electrons have the same charge and the same mass."
      "Why?"
      "Because, they are all the same electron!"
    </blockquote>

and then refer to `quote.html#wheeler-electron-quote`.

Finally, well-written HTML pages have a `head` element as well as a
`body`. The head isn't displayed; instead, it's used to store metadata
about the page as a whole. The most common element inside `head` is
`title`, which, as its name suggests, gives the page's title. (This is
usually displayed in the browser's title bar.) Another common item is
`meta`, whose two attributes `name` and `content` allow authors to embed
arbitrary information in their pages. If we add these to the web page we
wrote earlier, we might have:

    <!DOCTYPE html>
    <html>
      <head>
        <title>Dimorphism Defined<title>
        <meta name="author" content="Alan Turing"/>
        <meta name="institution" content="Euphoric State University"/>
      </head>
      <body>
        <h1>Dimorphism</h1>
        <p>Occurring or existing in two different <em>forms</em>.</p>
      </body>
    </html>

Well-written pages also use comments (just like code), which start with
`<!--` and end with `-->`.

### Hiding Content

Commenting out part of a page does *not* hide the content from people
who really want to see it: while a browser won't display what's inside a
comment, it's still in the page, and anyone who uses "View Source" can
read it. For example, if you are looking at this page in a web browser
right now, try viewing the source and searching for the word "Surprise".

If you really don't want people to be able to read something, the only
safe thing to do is to keep it off the web.

### Summary

-   Put metadata in `meta` elements in a page's `head` element.
-   Use `ul` for unordered lists and `ol` for ordered lists.
-   Add comments to pages using `<!--` and `-->`.
-   Use `table` for tables, with `tr` for rows and `td` for values.
-   Use `img` for images.
-   Use `a` to create hyperlinks.
-   Give elements a unique `id` attribute to link to it.

Creating Documents
------------------

### Understand:

-   How a page templating engine works.

Turning a Python list into an HTML `ol` or `ul` list seems like a
natural thing to do, so you might expect that programmers would have
created libraries to do it. In fact, they have gone one step further and
creating systems that allow people to put bits of code directly into
HTML files. Such a file is usually called a
[template](glossary.html#template), since it is the general pattern for
any number of potential pages.

Here's a simple example. Suppose we want to create a set of web pages to
display point-form biographies of famous scientists. We want each page
to look like this:

    <html>
      <head>
        <title>Biography of Beatrice Tinsley</title>
      </head>
      <body>
        <h1>Beatrice Tinsley</h1>
        <ol>
          <li>Born 1941</li>
          <li>Died 1981</li>
          <li>Studied stellar aging</li>
        </ol>
      </body>
    </html>

but since we expect to have hundreds of such pages, we don't want to
write each one by hand. (We certainly don't want to have to *revise*
each one by hand when the university decides it wants them in a slightly
different format...) To make things easier on ourselves, let's create a
single template page called `biography.html` that contains:

~~~~ {src="web/biography.html"}
<html>
  <head>
    <title>Biography of {{name}}</title>
  </head>
  <body>
    <h1>{{name}}</h1>
    <ol>
      {% for f in facts %}
      <li>{{f}}</li>
      {% endfor %}
    </ol>
  </body>
</html>
~~~~

This has the same general structure as a general biography, but there
are a few changes: it uses `{{name}}` instead of the scientist's name,
and rather than listing each biographical detail, it has something that
looks a lot like a `for` loop that iterates over something called
`facts`.

What we need next is a program that can expand this template using
particular values for `name` and `facts`. We will use a Python template
library called Jinja2 to do this; there are many others but they all
work in more or less the same way (which means, "They each have their
own slightly different rules for what can go in a page and how it's
expanded.").

First, let's put all the values we want to customize the page with into
variables:

~~~~ {src="web/template_expansion.py"}
name = 'Beatrice Tinsley'
facts = ['Born 1941', 'Died 1981', 'Studied stellar aging']
~~~~

Next, we have to import the Jinja2 library and do a bit of magic to load
the template for our page:

~~~~ {src="web/template_expansion.py"}
import jinja2

loader = jinja2.FileSystemLoader(['.'])
environment = jinja2.Environment(loader=loader)
template = environment.get_template('biography.html')
~~~~

We start by importing the `jinja2` library, and then create an object
called a "loader". Its job is to find template files for us; its
argument is a list of the directories we want it to search (in order).
For now, we are only looking in the current directory, so the list is
just `['.']`.

Once we have that loader, we use it to create a Jinja2 "environment",
which—well, honestly, we don't need two separate layers for what we're
doing, but more complicated applications might need several loaders, or
might be expanding different sets of templates in different ways, and
the complexity of the general case shows up here. What we *really* want
is the next line, which asks the environment to load the template file
`'biography.html'` and give us an object that knows how to expand
itself.

We're now ready to do the actual expansion:

~~~~ {src="web/template_expansion.py"}
result = template.render(name=name, facts=facts)
print result
~~~~

When we call `template.render`, we pass it any number of name-value
pairs. (Remember, the odd-looking expression `name=name` in the function
call means, "Assign the value of the variable `name` to the parameter
called `name`.") Those names are then available inside the template as
variables, so that `{{name}}` is replaced with the value of `name` and
we can iterate over the list in `facts`. The method call
`template.render` "runs" the template as if it were a program, and
returns the string that's created. When we print it out, we get:

    <html>
      <head>
        <title>Biography of Beatrice Tinsley</title>
      </head>
      <body>
        <h1>Beatrice Tinsley</h1>
        <ol>
          
          <li>Born 1941</li>
          
          <li>Died 1981</li>
          
          <li>Studied stellar aging</li>
          
        </ol>
      </body>
    </html>

Why go to all of this trouble? Because if we want to create another page
with exactly the same format, all we have to do is call:

    result = template.render(name='Helen Sawyer Hogg',
                             facts=['Born 1905',
                                    'Died 1993',
                                    'Studied globular clusters',
                                    'Wrote a popular astronomy column for 30 years'])

and we will get:

    <html>
      <head>
        <title>Biography of Helen Sawyer Hogg</title>
      </head>
      <body>
        <h1>Helen Sawyer Hogg</h1>
        <ol>
          
          <li>Born 1905</li>
          
          <li>Died 1993</li>
          
          <li>Studied globular clusters</li>
          
          <li>Wrote a popular astronomy column for 30 years</li>
          
        </ol>
      </body>
    </html>

Jinja2 templates support all the basic features of Python. For example,
we can modify our template file to say:

~~~~ {src="web/biography2.html"}
<html>
  <head>
    <title>Biography of {{name}}</title>
  </head>
  <body>
    <h1>{{name}}</h1>
    {% if facts %}
      <ol>
        {% for f in facts %}
        <li>{{f}}</li>
        {% endfor %}
      </ol>
    {% else %}
      <p>No facts available.<p>
    {% endif %}
  </body>
</html>
~~~~

so that if the list `facts` is empty, the page displays a paragraph
saying that, rather than an empty ordered list.

### Pros and Cons of Templating

Putting code in HTML templates and then expanding that to create actual
pages has both advantages and drawbacks. The advantage is that simple
things are simple to do: the biography template shown above is a lot
easier to understand than either a bunch of `print` statements, or a set
of functions that construct a tree of nodes in memory using `Element`
and `SubElement` calls and then turn the result into a string.

The biggest drawback of templating is the lack of support for debugging.
It's very common for template expansion to do what you said, rather than
what you meant, and working backward from a page that has the wrong
content to the bits of template that weren't quite right can be
complicated. One way to keep it manageable is to keep the templates as
simple as possible. Any calculations more complicated than simple
addition should be done in the program, and the result passed in as a
variable. Similarly, while deeply-nested conditional statements in
programs are hard to understand, their equivalents in templates are even
harder, and so should be avoided.

### Summary

-   How to use a page templating system.

How the Web Works
-----------------

### Understand:

-   The difference between client-server and peer-to-peer architectures.
-   What IP addresses, host names, and sockets are.
-   HTTP's request-response cycle.
-   What HTTP requests and responses contain.

Now that we know how to read and write the web's most common data
format, it's time to look at how data is moved around on the web.
Broadly speaking, web applications are built in one of two ways. In a
[client/server architecture](glossary.html#client-server-architecture)
many [clients](glossary.html#client) communicate with a central
[server](glossary.html#server) ([Figure XXX](#f:client_server)). This
model is asymmetric: clients ask for things, and servers provide them.
Web browsers and web servers like Firefox and Apache are the best-known
example of this model, but many [database management
systems](db.html#a:dbms) also use a client/server architecture.

![Client-Server Architecture](web/client_server.png)

In contrast, a [peer-to-peer
architecture](glossary.html#peer-to-peer-architecture) is one in which
all processes exchange information equally ([Figure
XXX](#f:peer_to_peer)). This is symmetric: every participant both
provides and receives data. The best-known example is probably
filesharing systems like BitTorrent, but again, there are many others.
Peer-to-peer systems are generally harder to design than client-server
systems, but they are also more resilient: if a centralized web server
fails, the whole system goes down, while if one node in a filesharing
network goes down, the rest can (usually) carry on.

![Peer-to-Peer Architecture](web/peer_to_peer.png)

Under the hood, both kinds of systems (and pretty much every other
networked application) run on a layered family of standards called
[Internet Protocol](glossary.html#internet-protocol) (IP). IP works by
breaking messages down into small [packets](glossary.html#packet), each
of which is forwarded from one machine to another along any available
route until it reaches its destination ([Figure XXX](#f:packets)).

![Packet-Based Communication](web/packets.png)

The only layer in IP that concerns us is the [Transmission Control
Protocol](glossary.html#tcp) layer. TCP/IP guarantees that every packet
we send is received, and that packets are received in the right order.
Putting it another way, it provides a reliable stream of data from one
place to another, so that sending data between computers looks as much
as possible like reading and writing files. ([Figure XXX](#f:streams)).

![Building Streams Out of Packets](web/streams.png)

Programs using IP communicate through [sockets](glossary.html#socket).
Each socket is one end of a point-to-point communication channel, and
provides the same kind of read and write operations as files ([Figure
XXX](#f:socket)).

![Sockets](web/socket.png)

A socket is identified by two numbers. The first is its [host
address](glossary.html#host-address) or [IP
address](glossary.html#ip-address), which identifies a particular
machine on the network. This consists of four 8-bit numbers, such as
`208.113.154.118`. The [Domain Name System](glossary.html#dns) (DNS)
matches these numbers to symbolic names like `"software-carpentry.org"`.
If we want, we can use tools like `nslookup` to query DNS directly:

    $ nslookup software-carpentry.org
    Server:  admin1.private.tor1.mozilla.com
    Address:  10.242.75.5

    Non-authoritative answer:
    Name:    software-carpentry.org
    Address:  173.236.199.157

A socket's [port number](glossary.html#port) is just a number in the
range 0-65535 that uniquely identifies the socket on the host machine.
(If the IP address is like a university's phone number, then the port
number is the extension.) Ports 0-1023 are reserved for the operating
system's use; anyone else can use the remaining ports.

![Sockets](web/sockets.png)

The [Hypertext Transfer Protocol](glossary.html#http) (HTTP) is a layer
on top of TCP/IP that specifies one way for programs to exchange
information. Originally, the communicating parties were web browsers and
web servers, but these days HTTP is used by many other kinds of
applications as well. In principle, HTTP communication is simple: the
client sends a request specifying what it wants over a socket
connection, and the server sends some data in response. (or an error
message). The data may be HTML copied from a file on disk, a similar
page generated dynamically by a program, an image, or just about
anything else ([Figure XXX](#f:http_content)).

### The Internet vs. the Web

A lot of people use these two terms synonymously, but they're actually
very different things. The Internet is a network of networks that allows
(almost) any computer to communicate with (almost) any other. That
communication can be email, File Transfer Protocol (FTP), streaming
video, or any of a hundred other things.

The World-Wide Web, on the other hand, is just one particular way to
share data on top of the kind of network that the Internet provides.
Originally, the web only allows people to view documents in browsers,
but its HTTP protocol has been used to do many other things since (such
as instant messaging and gaming).

![HTTP Content](web/http_content.png)

![HTTP Request Cycle](web/http_cycle.png)

![HTTP Request](web/http_request.png)

An HTTP request has three parts ([Figure XXX](#f:http_request)). The
HTTP method is almost always either `"GET"` (to fetch information) or
`"POST"` (to submit form data or upload files). The URL identifies the
thing the request wants; it may be a path to a file on disk, such as
`/research/experiments.html`, but it's entirely up to the server to
decide what to send back. The HTTP version is usually `"HTTP/1.0"` or
`"HTTP/1.1"`; the differences between the two don't matter to us.

An [HTTP header](glossary.html#http-header) is a key/value pair, such as
the three shown below:

    Accept: text/html
    Accept-Language: en, fr
    If-Modified-Since: 16-May-2005

A key may appear any number of times, so that (for example) a request
can specify that it's willing to accept several types of content.

The body is any extra data associated with the request. This is used
when submitting data via web forms, when uploading files, and so on.
There *must* be a blank line between the last header and the start of
the body to signal the end of the headers; forgetting it is a common
mistake.

One header, called `Content-Length`, tells the server how many bytes to
expect to read in the body of the request. There's no magic in any of
this: an HTTP request is just text, and any program that wants to can
create one or parse one.

![HTTP Response](web/http_response.png)

HTTP responses are formatted like HTTP requests ([Figure
XXX](#f:http_response)). The version, headers, and body have the same
form and mean the same thing. The status code is a number indicating
what happened when the request was processed by the server. 200 means
"everything worked", 404 means "not found", and other codes have other
meanings ([Figure XXX](#f:http_codes)). The status phrase repeats that
information in a human-readable phrase like "OK" or "not found".

  Code   Name                    Meaning
  ------ ----------------------- ---------------------------------------------------------------------------
  100    Continue                Client should continue sending data
  200    OK                      The request has succeeded
  204    No Content              The server has completed the request, but doesn't need to return any data
  301    Moved Permanently       The requested resource has moved to a new permanent location
  307    Temporary Redirect      The requested resource is temporarily at a different location
  400    Bad Request             The request is badly formatted
  401    Unauthorized            The request requires authentication
  404    Not Found               The requested resource could not be found
  408    Timeout                 The server gave up waiting for the client
  418    I'm a teapot            No, really
  500    Internal Server Error   An error occurred in the server that prevented it fulfilling the request
  601    Connection Timed Out    The server did not respond before the connection timed out

HTTP Codes

The one other thing that we need to know about HTTP is that it is
[stateless](glossary.html#stateless-protocol): each request is handled
on its own, and the server doesn't remember anything between one request
and the next. If an application wants to keep track of something like a
user's identity, it must do so itself.

### Summary

-   Most communication on the web uses TCP/IP sockets.
-   Socket endpoints are identified by a host address and a port number.
-   The Domain Name System translates human-readable names into host
    addresses.
-   An HTTP request contains a method, headers, and a body.
-   An HTTP response also contains a response code.
-   HTTP is a stateless request-response protocol.

Getting Data
------------

CONVERT EXAMPLE TO JSON THROUGHOUT

### Understand:

-   How to get data from the web using HTTP.
-   How URL query parameters are formatted.

Opening sockets, constructing HTTP requests, and parsing responses is
tedious, so most people use libraries to do most of the work. Python
comes with such a library called `urllib2` (because it's a replacement
for an earlier library called `urllib`), but it exposes a lot of
plumbing that most people never want to care about. Instead, we
recommend using the `Requests` library. Here's an example that uses it
to download a page from our web site:

~~~~ {src="web/requests_client.py"}
import requests
response = requests.get("http://software-carpentry.org/testpage.html")
print 'status code:', response.status_code
print 'content length:', response.headers['content-length']
print response.text
status code: 200
content length: 126
<html>
  <head>
    <title>Software Carpentry Test Page</title>
  </head>
  <body>
    <p>Use this page to test requests.</p>
  </body>
</html>
~~~~

As you can probably infer, the `get` function does an HTTP GET on a URL
and returns an object that stores the response. Its `status_code` member
is the response's status code, `content_length` tells us how many bytes
are in the response data, and `text` is the actual data (in this case,
an HTML page).

Sometimes a URL isn't enough on its own: for example, when searching on
Google, we have to specify what the search terms are. We could add these
to the path in the URL, but then every web site could have a different
convention about which parts actually belong to the path and which are
extras. Instead, what we should do is add parameters to the URL by
putting a '?' on the end of the URL, then adding key-value pairs
separated by the '&' character. For example, the URL
`http://www.google.ca?q=Python` ask Google to search for pages related
to Python, while `http://www.google.ca/search?q=Python&client=Firefox`
also tells Google that we're using Firefox. We can pass whatever
parameters we want, whenever we want, but it's up to the application
running on the web site to decide which ones to pay attention to, and
how to interpret them.

### You Are Who You Say You Are

Yes, this means that we could write a program of our own that tells
websites it's Firefox, Internet Explorer, or pretty much anything else.
We'll return to this and other security issues later.

Of course, if '?' and '&' are special characters, there must be a way to
escape them. The [URL encoding](glossary.html#url-encoding) standard
represents special characters using `"%"` followed by a 2-digit
hexadecimal code, and replaces spaces with the '+' character ([Figure
XXX](#f:url_encoding)). Thus, to search Google for "grade = A+" (with
the spaces), we would use the URL
`http://www.google.ca/search?q=grade+%3D+A%2B`.

  Character   Encoding
  ----------- ----------
  `"#"`       `%23`
  `"$"`       `%24`
  `"%"`       `%25`
  `"&"`       `%26`
  `"+"`       `%2B`
  `","`       `%2C`
  `"/"`       `%2F`
  `":"`       `%3A`
  `";"`       `%3B`
  `"="`       `%3D`
  `"?"`       `%3F`
  `"@"`       `%40`

URL Encoding

Encoding things by hand is very error-prone, so the Requests library
lets us pass in a dictionary of key-value pairs instead via the keyword
argument `params`:

~~~~ {src="web/urlencode.py"}
import requests
parameters = {'q' : 'Python', 'client' : 'Firefox'}
response = requests.get('http://www.google.com/search', params=parameters)
print 'actual URL:', response.url
actual URL: http://www.google.com/search?q=Python&client=Firefox
~~~~

You should *always* let the library build the URL for you, rather than
doing it yourself: there are subtleties we haven't covered, and even if
there weren't, there's no point duplicating code that's already been
written and tested.

Suppose we want to write a script that actually *does* search Google.
Constructing a URL is easy. Sending it and reading the response is easy
too, but parsing the response is hard, since there's a lot of stuff in
the page that Google sends back. Many first-generation web applications
relied on [screen scraping](glossary.html#screen-scraping) to get data,
i.e., they would search for substrings in the HTML. (They had to do this
because a lot of hand-written HTML was improperly formatted. For
example, it was quite common to use `<br>` on its own to break a line.)

Screen scraping is always hard to get right if the page layout is
complex. It is also fragile: whenever the layout of the pages changes,
the application will most likely break because data is no longer where
it was.

Most modern web applications try to sidestep this problem by providing
some sort of [web services](glossary.html#web-services) interface, which
is a lot simpler than it sounds. When a client sends a request, it
indicates whether it wants machine-oriented data rather than
human-readable HTML, either by using a slightly different URL or by
using a suffix like `.xml` instead of `.html`. ([Figure
XXX](#f:web_services)). If it asks for data, the server sends back XML
(or some other format) that is easy for a program to parse. If the
client asks for "real" HTML, on the other hand, the application turns
that data into HTML tables with italics and colored highlights and the
like to make it easy for human beings to read.

![Web Services](web/web_services.png)

Using "live" data from a web service is a powerful way to get a lot of
science done in a hurry, but only when it works. As a case in point, we
wanted to use bird-watching data from [ebird.org](http://ebird.org) in
this example, but their server was locked down for security reasons when
it came time for us to write our examples. (This is another way in which
software is like other experimental apparatus: odds are that when you
need it most, it will be broken or someone will have borrowed it.)

We therefore chose to use climate data from the World Bank instead.
According to [the
documentation](http://data.worldbank.org/developers/climate-data-api),
data for a particular country can be found at:

    http://climatedataapi.worldbank.org/climateweb/rest/v1/country/cru/VARIABLE/year/ISO.FORMAT

where:

-   *VARIABLE* is either "pr" (for precipitation) or "tas" (for
    *t*emperature *a*t *s*urface);
-   *ISO* is the International Standards Organization's 3-letter country
    code for the country of interest (e.g., "FRA" for France); and
-   *FORMAT* is "XML" for XML, and other strings for other formats that
    we'll discuss later.

Let's try getting some data:

    >>> import requests
    >>> url = 'http://climatedataapi.worldbank.org/climateweb/rest/v1/country/cru/tas/year/FRA.XML'
    >>> response = requests.get(url)
    >>> print response.text
    <list>
      <domain.web.V1WebCru>
        <year>1901</year>
        <data>21.357021</data>
      </domain.web.V1WebCru>
      <domain.web.V1WebCru>
        <year>1902</year>
        <data>21.382462</data>
      </domain.web.V1WebCru>
      ...
    </list>

All right: the outer `list` element (the document root) contains any
number of `domain.web.V1WebCru` elements, each of which contains `year`
and `data` elements. That long, clumsy name `domain.web.V1WebCru`
probably means something to someone, but we don't need to care: all we
need to know is that each element with that tag contains a single year's
data.

Let's write a program to compare the data for two countries (which is
the problem Carla wanted to solve at the start of this chapter). We need
to know which countries to compare:

~~~~ {src="web/temperatures.py"}
def main(args):
    first_country = 'AUS'
    second_country = 'CAN'
    if len(args) > 0:
        first_country = args[0]
    if len(args) > 1:
        second_country = args[1]
    ratios(first_country, second_country)

if __name__ == '__main__':
    main(sys.argv[1:])
~~~~

This program uses a function called `ratios` to fetch data and display
the annual ratios:

~~~~ {src="web/temperatures.py"}
def ratios(first_country, second_country):
    '''Show ratio of average temperatures for two countries over time.'''
    first = get_temps(first_country)
    second = get_temps(second_country)
    assert len(first) == len(second), 'Length mis-match in results'
    keys = first.keys()
    keys.sort()
    for k in keys:
        print k, first[k] / second[k]
~~~~

`ratios` depends in turn on a function `get_temps`:

~~~~ {src="web/temperatures.py"}
def get_temps(country_code):
    '''Get annual temperatures for a country.'''
    doc = get_xml(country_code)
    result = {}
    for element in doc.findall('domain.web.V1WebCru'):
        year = find_one(element, 'year').text
        temp = find_one(element, 'data').text
        result[int(year)] = kelvin(float(temp))
    return result
~~~~

which depends on a helper function called `get_xml` to actually download
text from the World Bank web site and parse it to produce an XML
document:

~~~~ {src="web/temperatures.py"}
def get_xml(country_code):
    '''Get XML temperature data for a country.'''
    url = 'http://climatedataapi.worldbank.org/climateweb/rest/v1/country/cru/tas/year/%s.XML'
    u = url % country_code
    response = requests.get(u)
    doc = ET.fromstring(response.text)
    return doc
~~~~

The last two functions we need to finish this program are `kelvin`,
which converts temperatures from Celsius to Kelvin, and `find_one`,
which pulls exactly one node out of an XML document:

~~~~ {src="web/temperatures.py"}
def kelvin(celsius):
    '''Convert degrees C to degrees K.'''
    return celsius + 273.15

def find_one(node, pattern):
    '''Get exactly one child that matches an XPath pattern.'''
    all_results = node.findall(pattern)
    assert len(all_results) == 1, 'Got %d children instead of 1' % len(all_results)
    return all_results[0]
~~~~

Let's try running this program with no arguments to compare Australia to
Canada, eh:

    $ python temperatures.py
    1901 1.10934799048
    1902 1.11023963325
    1903 1.10876094164
    ...  ...
    2007 1.10725265753
    2008 1.10793365185
    2009 1.10865537105

and then with arguments to compare Malaysia to Norway:

    $ python temperatures.py MYS NOR
    1901 1.08900632708
    1902 1.09536126502
    1903 1.08935268463
    ...  ...
    2007 1.08564675748
    2008 1.08481881663
    2009 1.08720464013

Only 24 lines in this program do anything webbish (the functions
`get_temps`, `get_xml`, and `find_one`), and six of those lines are
blank or documentation. The remaining 30 lines are the user interface
(handling command-line arguments and printing output) and data
manipulation (converting temperatures and calculating ratios).

### Summary

-   Use Python's Requests library to make HTTP requests.
-   Let the library format URL parameters.
-   Many web sites now provide machine-oriented data as well as
    human-readable pages.
-   The URLs and query parameters needed to fetch data are specified by
    the web site.

Providing Data
--------------

### Understand:

-   That writing secure dynamic web applications is hard.
-   That providing dynamically-generated static pages is a good
    alternative.
-   How and why to create an index for such pages.
-   How to keep track of what dynamic data has already been processed.

The next logical step is to provide data to others by writing some kind
of server application. The basic idea is simple: wait for someone to
connect to your server and send you an HTTP request, parse that request,
figure out what it's asking for, fetch that data (or run a program to
generate some data dynamically), format the data as HTML or XML, and
send it back ([Figure XXX](#f:web_application)).

![Web Application Lifecycle](web/web_application.png)

We're not going to show you how to do this, though, because experience
has shown that all we can actually do in a short lecture is show you how
to create security holes. Here's just one example. Suppose you want to
write a web application that accepts URLs of the form
`http://my.site/data?species=homo.sapiens` and fetches a database record
containing information about that species. One way to do it in Python
might look like this:

    def get_species(url):
        '''Get data for a particular species.'''
        params = url.split('?')[1]                                # Get everything after the '?'
        pairs = params.split('&')                                 # Get the name1=value1&name2=value2 pairs
        pairs = [pairs.split('=') for p in pairs]                 # Split the name=value pairs
        pairs = dict(pairs)                                       # Convert to a {name : value} dictionary
        species = pairs['species']                                # Get the species we want to look up
        sql = '''SELECT * FROM Species WHERE Name = "%s";'''      # Template for SQL query
        sql = sql % species                                       # Insert the species name
        cursor.execute(sql)                                       # Send query to database
        results = cursor.fetchall()                               # Get all the results
        return results[0]

We've taken out all the error-checking—for example, this code will fail
if there aren't actually any query parameters, or if the species' name
isn't in the database—but that's not the problem. The problem is what
happens if someone sends us this URL:

    http://my.site/data?species=homo.sapiens";DROP TABLE Species"--

Why? Because the dictionary of query parameters produced by the first
five lines of the function will be:

    { 'species' : 'homo.sapiens";DROP TABLE Species;--' }

which means that the SQL query will be:

    SELECT * FROM Species WHERE Name = "homo.sapiens";DROP TABLE Species;--";

which is the same as:

    SELECT * FROM Species WHERE Name = "homo.sapiens";
    DROP TABLE Species;

In other words, this selects something from the database, then throws
away the entire `Species` table. It's called an [SQL injection
attack](glossary.html#sql-injection), because the user is injecting
arbitrary (and usually damaging) SQL into our database query, and it's
just one of hundreds of different ways that villains can try to
compromise a web application.

Built properly, web sites can withstand such attacks, but learning how
to do things properly takes a long time. Instead, we will look at how to
write programs that create plain old HTML pages that can then be served
up to the world by a standard web server. Using our previous example
(ratios of average annual temperatures) as a starting point, we'll
create pages whose names look like
`http://my.site/tempratio/AUS-CAN.html`, and which contain data
formatted like this:

    <html>
      <head>
        <meta name="revised" content="2012-09-15" />
      </head>
      <body>
        <h1>Ratio of Average Annual Temperatures for AUS and CAN</h1>
        <table class="data">
          <tr>
            <td class="year">1901</td>
            <td class="data">1.10934799048</td>
          </tr>
          <tr>
            <td class="year">1902</td>
            <td class="data">1.11023963325</td>
          </tr>
          <tr>
            <td class="year">1903</td>
            <td class="data">1.10876094164</td>
          </tr>
          ...
          <tr>
            <td class="year">2007</td>
            <td class="data">1.10725265753</td>
          </tr>
          <tr>
            <td class="year">2008</td>
            <td class="data">1.10793365185</td>
          </tr>
          <tr>
            <td class="year">2009</td>
            <td class="data">1.10865537105</td>
          </tr>
        </table>
      </body>
    </html>

The first step is to calculate ratios, which we did in the [previous
section](#s:client). Our main program is:

~~~~ {src="web/make_data_page.py"}
def main(args):
    '''Create web page showing temperature ratios for two countries.'''

    assert len(args) == 4, \
           'Usage: make_data_page template_filename output_filename country_1 country_2'
    template_filename = args[0]
    output_filename = args[1]
    country_1 = args[2]
    country_2 = args[3]

    page = make_page(template_filename, country_1, country_2)

    writer = open(output_filename, 'w')
    writer.write(page)
    writer.close()
~~~~

The second step is to translate the temperature values into a web page.
We'll use the `get_temps` function we wrote above to grab temperature
data, get the years from that, and add the date as well. Once we have
all those

~~~~ {src="web/make_data_page.py"}
def make_page(template_filename, output_filename, country_1, country_2):
    '''Create page showing temperature ratios.'''

    data_1 = get_temps(country_1)
    data_2 = get_temps(country_2)
    years = data_1.keys()
    years.sort()
    the_date = date.isoformat(date.today())

    loader = jinja2.FileSystemLoader(['.'])
    environment = jinja2.Environment(loader=loader)
    template = environment.get_template(template_filename)
    result = template.render(country_1=country_1, data_1=data_1,
                             country_2=country_2, data_2=data_2,
                             years=years, the_date=the_date)

    return result
~~~~

Finally, we need a Jinja2 template for the pages we want to create:

~~~~ {src="web/temp_ratio.html"}
<!DOCTYPE html>
<html>
  <head>
    <title>Temperature Ratios of {{country_1}} and {{country_2}} as of {{the_date}}</title>
  </head>
  <body>
    <h1>Temperature Ratios of {{country_1}} and {{country_2}}</h1>
    <h2>Calculated {{the_date}}</h2>
    <table>
      <tr>
        <td>Year</td>
        <td>{{country_1}}</td>
        <td>{{country_2}}</td>
        <td>Ratio</td>
      </tr>
      {% for year in years %}
      <tr>
        <td>{{year}}</td>
        <td>{{data_1[year]}}</td>
        <td>{{data_2[year]}}</td>
        <td>{{data_1[year] / data_2[year]}}</td>
      </tr>
      {% endfor %}
    </table>
  </body>
</html>
~~~~

Let's run it for Australia and Canada:

    $ python make_data_page.py temp_ratio.html /tmp/aus-can.html AUS CAN

Sure enough, the file `/tmp/aus-can.html`contains:

~~~~ {src="web/aus-can-ratio.html"}
<!DOCTYPE html>
<html>
  <head>
    <title>Temperature Ratios of AUS and CAN as of 2013-02-10</title>
  </head>
  <body>
    <h1>Temperature Ratios of AUS and CAN</h1>
    <h2>Calculated 2013-02-10</h2>
    <table>
      <tr>
        <td>Year</td>
        <td>AUS</td>
        <td>CAN</td>
        <td>Ratio</td>
      </tr>
      
      <tr>
        <td>1901</td>
        <td>294.507021</td>
        <td>265.477581</td>
        <td>1.10934799048</td>
      </tr>
      
      <tr>
        <td>1902</td>
        <td>294.532462</td>
        <td>265.2872886</td>
        <td>1.11023963325</td>
      </tr>

      ...
      
      <tr>
        <td>2009</td>
        <td>295.07194</td>
        <td>266.1529883</td>
        <td>1.10865537105</td>
      </tr>
      
    </table>
  </body>
</html>
~~~~

### Summary

-   Creating static files is a safe alternative to providing content
    dynamically.

Creating an Index
-----------------

### Understand:

-   Why good data sets have an index.

Before leaving Carla's climate problem, let's go one step further and
make our solution more useful. If we're going to calculate these tables
for many different countries, how will other scientists know which ones
we've done? In other words, how can we make our data findable?

The standard answer for the last few hundred years has been, "Create an
index." On the web, we can do this by creating a file called
`index.html` and putting it in the directory that holds our data files,
because by default, most web servers will give clients that file when
they're asked for the directory itself. In other words, if someone
points a browser (or any other program) at `http://my.site/tempratio/`,
the web server will look for `/tempratio`. When it realizes that path is
a directory rather than a file, it will look inside that directory for a
file called `index.html` and return that. This is *not*
guaranteed—system administrators can and do set up other default
behaviors—but it is a common convention, and we can always tell our
colleagues to fetch `http://my.site/tempratio/` if they want the current
index anyway.

What should be in `index.html`? The answer is simple: a table of some
kind showing what files are available, when they were created, and where
they are. The first piece of information is the most important; the
second allows users to determine what has been added since they last
looked at our site without having to download actual data files, while
the third tells them how to get what they want. Our `index.html` will
therefore be something like this:

    <html>
      <head>
        <title>Index of Average Annual Temperature Ratios</title>
        <meta name="revised" content="2012-09-15" />
      </head>
      <body>
        <h1>Index of Average Annual Temperature Ratios</h1>
        <table class="data">
          <tr>
            <td class="country">AUS</td>
            <td class="country">CAN</td>
            <td class="revised">2012-09-12</td>
            <td class="revised"><a href="http://my.site/tempratio/AUS-CAN.html">download</a></td>
          </tr>
          ...
          <tr>
            <td class="country">MYS</td>
            <td class="country">NOR</td>
            <td class="revised">2012-09-15</td>
            <td class="download"><a href="http://my.site/tempratio/MYS-NOR.html">download</a></td>
          </tr>
        </table>
      </body>
    </html>

### Why Explicit URLs?

Strictly speaking, we don't need to store the URLs in the index file: we
could instead tell people that if they got the index from
`http://my.site/tempratio/index.html`, then the data for AUS and CAN is
in `http://my.site/tempratio/AUS-CAN.html`, and let them construct the
URL themselves. However, that puts more of a burden on the user both in
the short term (since more coding is required) and in the long term
(since the rule for constructing the URL for a particular data set could
well change). It also effectively hides our data from search engines,
since there's no way for them to know what our URL construction rule is.

Now, unlike our actual data files, this index file is added to
incrementally: each time we generate a new version, we have to include
all the data that was in the old version as well. We therefore need to
remember what we've done. The usual way to do this in a real application
is to use a database, but for our purposes, a plain old text file will
suffice.

We *could* make up a format to store the information we need, such as:

    Updated 2013-05-09
    AUS CAN 2013-03-07
    AUS NOR 2013-03-09
    CAN NOR 2013-04-22
    CAN MDG 2013-05-09

but there's a better solution. A growing number of applications use a
data format called [JSON](glossary.html#json), which stands for
"JavaScript Object Notation". Despite the name, it is a
language-independent way to store nested data structures made up of
lists, dictionaries, strings, numbers, Booleans, and the special value
`null` (equivalent to Python's `None`). Here's a program that creates a
dictionary representing the four data sets listed above and saves it in
`index.json`:

~~~~ {src="web/create-index.py"}
import json

index_data = {
    'updated' : '2013-05-09',
    'entries' : [
        ['AUS', 'CAN', '2013-03-07'],
        ['AUS', 'NOR', '2013-03-09'],
        ['CAN', 'NOR', '2013-04-22'],
        ['CAN', 'MDG', '2013-05-09']
    ]
}

writer = open('index.json', 'w')
json.dump(index_data, writer)
writer.close()
~~~~

When we run this, it creates a file called `index.json` that contains:

~~~~ {src="web/index.json"}
{"updated": "2013-05-09", "entries": [["AUS", "CAN", "2013-03-07"], ["AUS", "NOR", "2013-03-09"], ["CAN", "NOR", "2013-04-22"], ["CAN", "MDG", "2013-05-09"]]}
~~~~

If we want to check that it has worked, we can read the file's contents
back in to re-create the original data structure:

    >>> import json
    >>> reader = open('index.json', 'r')
    >>> check = json.load(reader)
    >>> print check
    {u'updated': u'2013-05-09', u'entries': [[u'AUS', u'CAN', u'2013-03-07'], [u'AUS', u'NOR', u'2013-03-09'], [u'CAN', u'NOR', u'2013-04-22'], [u'CAN', u'MDG', u'2013-05-09']]}

The 'u' in front of each string signals that these strings are actually
stored as Unicode, but we can safely ignore that for now. Let's rewrite
the main function of our program so that it creates the index as well as
the individual page:

~~~~ {src="web/make_indexed_page.py"}
import sys
import os
from datetime import date
import jinja2
import json
from temperatures import get_temps

INDIVIDUAL_PAGE = 'temp_ratio.html'
INDEX_PAGE = 'index.html'
INDEX_FILE = 'index.json'

def main(args):
    '''
    Create web page showing temperature ratios for two countries,
    and update the index.html page with the new entry.
    '''

    assert len(args) == 5, \
           'Usage: make_indexed_page url_base template_dir output_dir country_1 country_2'
    url_base, template_dir, output_dir, country_1, country_2 = args
    the_date = date.isoformat(date.today())

    loader = jinja2.FileSystemLoader([template_dir])
    environment = jinja2.Environment(loader=loader)

    page = make_page(environment, country_1, country_2, the_date)
    save_page(output_dir, '%s-%s.html' % (country_1, country_2), page)

    index_data = load_index(output_dir, INDEX_FILE)
    index_data['entries'].append([country_1, country_2, the_date])
    save_page(output_dir, INDEX_FILE, json.dumps(index_data))

    page = make_index(environment, url_base, index_data)
    save_page(output_dir, INDEX_PAGE, page)
~~~~

Since we will be expanding templates in a couple of different functions,
we move the creation of the Jinja2 environment to the main program. We
then pass that variable into `make_page` and a new function called
`update_index`, and use another new function `save_page` to save
generated pages where they need to go. (Note that we update the index
data *before* rewriting the index HTML page. The first version of this
program that we wrote updated the HTML page before updating the data it
was based on—oops.)

`save_page` is the simplest of these pages to write, so let's do that:

~~~~ {src="web/make_indexed_page.py"}
def save_page(output_dir, page_name, content):
    '''Save text in a file output_dir/page_name.'''
    path = os.path.join(output_dir, page_name)
    writer = open(path, 'w')
    writer.write(content)
    writer.close()
~~~~

Our revised `make_page` function is shorter than our original, since the
environment is now being created in `main`. `make_page` is also now
being passed the date (since that is used to update the index as well),
and uses a fixed template specified by the global variable
`INDIVIDUAL_PAGE`. The result is:

~~~~ {src="web/make_indexed_page.py"}
def make_page(environment, country_1, country_2, the_date):
    '''Create page showing temperature ratios.'''

    data_1 = get_temps(country_1)
    data_2 = get_temps(country_2)
    years = data_1.keys()
    years.sort()

    template = environment.get_template(INDIVIDUAL_PAGE)
    result = template.render(country_1=country_1, data_1=data_1,
                             country_2=country_2, data_2=data_2,
                             years=years, the_date=the_date)

    return result
~~~~

The function that loads existing index data is also pretty simple:

~~~~ {src="web/make_indexed_page.py"}
def load_index(output_dir, filename):
    '''Load index data from output_dir/filename.'''

    path = os.path.join(output_dir, filename)
    reader = open(path, 'r')
    result = json.load(reader)
    reader.close()
    return result
~~~~

All that's left is the function that regenerates the HTML version of the
index:

~~~~ {src="web/make_indexed_page.py"}
def make_index(environment, url_base, index_data):
    '''Refresh the HTML index page.'''

    template = environment.get_template(INDEX_PAGE)
    return template.render(url_base=url_base,
                           updated=index_data['updated'],
                           entries=index_data['entries'])
~~~~

and the HTML template it relies on:

~~~~ {src="web/index_template.html"}
<!DOCTYPE html>
<html>
  <head>
    <title>Index of Average Annual Temperature Ratios</title>
    <meta name="revised" content="{{updated}}" />
  </head>
  <body>
    <h1>Index of Average Annual Temperature Ratios</h1>
    <table class="data">
      {% for entry in entries %}
      <tr>
        <td class="country">{{entry[0]}}</td>
        <td class="country">{{entry[1]}}</td>
        <td class="revised">{{entry[2]}}</td>
        <td class="revised"><a href="{{url_base}}/{{entry[0]}}-{{entry[1]}}.html">download</a></td>
      </tr>
      {% endfor %}
    </table>
  </body>
</html>
~~~~

### Summary

-   Every collection of data should provide a machine-readable index.
-   Links between files should be explicit.

Syndicating Data
----------------

To end this chapter, we'll use what we have learned to build a simple
tool to download new temperature comparisons from a web site. In broad
strokes, our program will keep a list of URLs to download data from,
along with a timestamp showing when data was last downloaded. When we
run the program, it will poll each site to see if any new data sets have
been added since the last check. If any have, the program will display
their URLs.

In order for this to work, each of the sites that's providing data needs
to be able to tell us what data sets it has calculated, and when they
were created. This information is in the site's `index.html` file in
human-readable form, but it's also in the `index.json` file each site is
maintaining. This file can be loaded directly without any XML parsing or
XPath searching, so we'll use that.

The next step is to decide how to keep track of what we have downloaded
and when. The simplest thing is to create another JSON file containing
the timestamp and the list of URLs. We'll call this `sources.json`:

    {
        "timestamp" : "2013-05-02:07:04:03",
        "sites" : [
            "http://software-carpentry.org/temperatures/index.json",
            "http://some.other.site/some/path/index.json"
        ]
    }

(Again, a larger application would use a database of some kind, but
that's more than we need right now.) Each time we run our program, it
will read this file, then download each `index.json` file. If any of
those files contain links to data sets that are newer than the
timestamp, it will print the data set's URL. (A real data analysis
program would download the data and do something with it.) We will then
save a fresh copy of `sources.json` with an updated timestamp. Our main
program looks like this:

~~~~ {src="web/syndicate.py"}
import date

def main(sources_path):
    '''Check all data sites in list, then update timestamp of sources.json.'''
    old_timestamp, all_sources = read_sources(sources_path)
    new_timestamp = date.datetime.now()
    for source in all_sources:
        for url in get_new_datasets(old_timestamp, source):
            process(url)
    write_sources(sources_path, new_timestamp, sources)
~~~~

That seems pretty simple; the only subtlety is that we calculate the new
timestamp *before* we start checking for new datasets. The reason is
that this check might take anything from a few seconds to a few hours,
depending on how busy the Internet is and how much data we actually
download. If we wait until we're done and then record that moment as the
new timestamp, then the next time we run our program, we won't download
any datasets that were created between the time we started the first run
of our program and the time it finished ([Figure
XXX](#f:when_to_timestamp)).

![When to Create Timestamps](web/when_to_timestamp.png)

We now have four functions to write: `read_sources`, `write_sources`,
`get_new_datasets`, and `process`. Reading and writing the
`sources.json` file is pretty simple:

~~~~ {src="web/syndicate.py"}
import json

def read_sources(path):
    '''Read timestamp and data sources from JSON files.'''
    reader = open(path, 'r')
    data = json.load(reader)
    timestamp = data['timestamp']
    sources = data['sources']
    return timestamp, sources

def write_sources(sources_path, timestamp, sources):
    '''Write timestamp and data sources to JSON file.'''
    data = {'timestamp' : timestamp,
            'sources'   : sources}
    writer = open(sources_path, 'w')
    json.dump(data, writer)
    writer.close()
~~~~

What about processing a URL? Right now, we're just going to print it,
though in a real application we would probably download the data and do
some further calculations with it:

~~~~ {src="web/syndicate.py"}
def process(url):
    '''Placeholder for processing a data set given its URL.'''
    print url
~~~~

Finally, we need to construct a list of dataset URLs given the URL of an
`index.json` file:

~~~~ {src="web/syndicate.py"}
import requests

def get_new_datasets(last_checked, index_url):
    '''Return a list of URLs of datasets that are newer than the timestamp.'''
    response = requests.get(index_url)
    index_data = json.loads(index.text)
    result = []
    for (country_a, country_b, updated) in index_data:
        dataset_timestamp = datetime.parse(updated)
        if dataset_timestamp >= last_checked:
            dataset_url = make_dataset_url(index_url, country_a, country_b)
            result.append(dataset_url)
    return result
~~~~

The logic here is straightforward: grab the `index.json` file, check
each dataset to see if it's newer than the last time we checked, and if
it is—hm. This code uses a not-yet-written function called
`make_dataset_url` to construct the URL for the specific dataset from
the URL of the index file and the two country codes, but as we discussed
[earlier](#b:index:explicit), asking client programs to construct links
themselves is a bad idea. Instead, we should modify the `index.json`
files so that they include the URLs. Doing this is left as a final
exercise for the reader.

### Summary

-   Well-constructed files make data syndication simple.

Summing Up
----------

The web has changed in many ways over the last 20 years, not all of them
for the better. An HTML page on a modern commercial site is likely to
include dozens or hundreds of lines of Javascript that depend on several
large, complicated libraries, and which generate the page's content on
the fly inside the browser. Such a "page" is really a small (or
not-so-small) program rather than a document in the classical sense of
the word, and while that may produce a better experience for human
users, it makes life more difficult for programs (and for people with
disabilities, whose assistive aids are all too easy to confuse). And
while XML is widely used for representing data, many people believe that
younger alternatives like JSON do a better job of balancing the needs of
human and computer readers.

Regardless of the technology used, though, the web's [basic design
principles](http://blog.jonudell.net/2011/01/24/seven-ways-to-think-like-the-web/)
are both simple and stable: tell people where data is, rather than
giving them a copy; make the data itself and your names for it easy for
both human beings and computers to understand; remix other people's
data, and allow them to remix yours.
