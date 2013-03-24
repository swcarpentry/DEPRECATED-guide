Reading Documents
-----------------

### Understand:

-   How the Document Object Model represents HTML and XML.

People usually write their home pages by hand, but most pages that
display lists of experimental results, or second-hand lab equipment for
sale, are created by programs. For historical reasons, Python's standard
library includes several libraries that process XML (including HTML);
we'll use the simplest one, called `ElementTree`, but you will often run
into programs that use others.

Most of these libraries represent the nested structure of XML using
something called the [Document Object
Model](glossary.html#document-object-model) (DOM). This stores the
document as a [tree](glossary.html#tree) with one node for each element
or block of text. The root element of the document, such as the
all-enclosing `html` in a web page, is the root node of the tree. Every
other element or block of text is a child of it, or a child of a child,
and so on. For example, the tree representing our web page about
dimorphism looks like [Figure XXX](#f:dimorphism_tree).

![Tree Representation of Dimorphism Page](img/web/dimorphism_tree.png)

There are basically two ways to create a tree like this: parse a string
(or file) containing XML, or build the nodes one by one and put them
together manually. The former is more common, since the usual way to
store and exchange XML or HTML is as text, so we will explore that
first. Let's begin by turning text into HTML and then back into text:

~~~~ {src="src/web/parse_simple_page.py"}
import xml.etree.ElementTree as ET

page = '''<html>
  <body>
    <h1>Dimorphism</h1>
    <p class="definition">Occurring or existing in two different <u>forms</u>.</p>
    <p>
      The most notable form is sexual dimorphism,
      in which males and females have noticeably different appearances.
    </p>
  </body>
</html>'''

doc = ET.fromstring(page)
text = ET.tostring(doc, 'utf-8')
print text
~~~~

We start by importing the `xml.etree.ElementTree` library and giving it
the alias `ET` (which is a lot easier to type and read). The multi-line
string assigned to the variable `page` is the "document" we will parse;
most real programs will read data from a file instead.

Parsing itself takes just a single call to `ET.fromstring`; it returns
the root node of the DOM tree corresponding to that document. We then
convert that tree back to text by calling `ET.tostring`. The `'utf-8'`
argument specifies how we want characters represented; you should always
use this option unless you know enough to know that you want something
else. need a better explanation than this

The program's output is:

    <html>
      <body>
        <h1>Dimorphism</h1>
        <p class="definition">Occurring or existing in two different <u>forms</u>.</p>
        <p>
          The most notable form is sexual dimorphism,
          in which males and females have noticeably different appearances.
        </p>
      </body>
    </html>

which is exactly what we started with.

point out how much simpler this is than parsing...

In the example above, our output was exactly the same as our input, but
that won't always be the case. Here's another simple program that
converts text to a node tree and back:

~~~~ {src="src/web/round_trip.py"}
import xml.etree.ElementTree as ET

original = '''<root><node
                     front="1"
                     back="2">content</node></root>'''


doc = ET.fromstring(original)
print ET.tostring(doc, 'utf-8')
<root><node back="2" front="1">content</node></root>
~~~~

`node`'s attributes are all on one line in the output, and in a
different order than they were in the input. The reason for the first
difference is that XML ignores whitespace inside elements: the parser
simply throws away the extra spaces and newlines inside the definition
of `<node…>`. The reason for the second is that attributes are treated
as a dictionary, and dictionary keys are unordered. As far as the rules
of XML are concerned, the input and output are the same thing.
Unfortunately, as far as string comparison and tools like `diff` are
concerned, they are not.

Since almost all XML or HTML documents are stored in files, the
ElementTree library provides a convenience function that parses files
directly. If `dimorphism.html` contains our definition of sexual
dimorphism, then:

    import xml.etree.ElementTree as ET
    doc = ET.parse('dimorphism.html')

reads the text in that file, converts it to a DOM tree, and returns the
tree's root node.

### Summary

-   Use `xml.etree.ElementTree` to parse HTML and XML.

Finding Nodes
-------------

### Understand:

-   How to find DOM elements using XPath.

Most databases are read more often than they're written, so most of [our
discussion of SQL](db.html) focuses on finding things. Most web pages
are read more than once too, so libraries like ElementTree provide tools
for locating nodes of interest. The most important of these is the
`findall` method, which searches all the children of a node to find ones
that match a pattern. For example, if some molecular formulas are stored
like this:

~~~~ {src="src/web/molecular_formulas.xml"}
<formulas>
  <formula name="ammonia">
    <atom symbol="N" number="1"/>
    <atom symbol="H" number="3"/>
  </formula>
  <formula name="water">
    <atom symbol="H" number="2"/>
    <atom symbol="O" number="1"/>
  </formula>
  <formula name="methanol">
    <atom symbol="C" number="1"/>
    <atom symbol="O" number="1"/>
    <atom symbol="H" number="4"/>
  </formula>
</formulas>
~~~~

then this program will count how many formulas there are:

~~~~ {src="src/web/count_formulas.py"}
import sys
import xml.etree.ElementTree as ET

doc = ET.parse(sys.argv[1])
root = doc.getroot()
formulas = root.findall("./formula")
print len(formulas)
3
~~~~

The key to this programs is `root.findall("./formula")`. The pattern
`"./formula"` means, "Starting with this node ('.'), examine its
children ('/') for elements with the tag 'formula." The result of the
`findall` call is a list of nodes that match.

The mini-language used for patterns is called
[XPath](glossary.html#xpath). Some parts, like '.' and '/', are
deliberately reminiscent of the way paths are described in [the Unix
filesystem](shell.html#s:filedir). Other parts are more complicated, but
it's possible to do a lot without using them. Some common XPath
expressions are:

  --------------------- ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  `tag`                 All immediate children with the given tag. `formula` selects all child `formula` elements, and `formula/atom` selects all `atom` elements that are children of `formula` children.
  `*`                   All child elements. `*/atom` selects all grandchild `atom` elements, regardless of what the intervening parent is.
  //                    All subelements on all levels beneath the current element. `.//atom` selects all `atoms` elements in the entire tree.
  `.`                   The current node. It is mostly used at the beginning of a path to indicate that it is a relative path.
  `..`                  The parent of the current node.
  `[@attrib]`           All elements with the given attribute (regardless of that attribute's value). `.//atom[@name]` selects all atoms in the tree that have a `name` attribute, but not any `atom` elements that are missing that attribute.
  `[@attrib="value"]`   All elements for which the given attribute has the given value. `.//atom[@symbol="C"]` finds all carbon atoms.
  `[tag]`               All elements that have a child element with the given tag. `atom[comment]` finds all `atom` nodes that have an immediate child of type `comment`.
  `[position]`          All elements that located in the given position relative to their parent. The position can be either an integer (1 is the first position), the expression `last()` for the last position, or a position relative to `last()`, such as `last()-1`.
  --------------------- ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Let's use these expressions to check that a data file is properly
formatted by looking for all the `atom` nodes that are *not* immediate
children of `formula` nodes. Our data file is:

~~~~ {src="src/web/bad_formulas.xml"}
<formulas>
  <formula name="ammonia">
    <atom symbol="N" number="1"/>
    <atom symbol="H" number="3"/>
  </formula>
  <atom symbol="H" number="2"/>       <!-- mistake! -->
  <formula name="water">
    <atom symbol="O" number="1">
      <atom symbol="H" number="2"/>   <!-- another mistake -->
    </atom>
  </formula>
</formulas>
~~~~

and our program is:

~~~~ {src="src/web/validate_doc.py"}
import xml.etree.ElementTree as ET

doc = ET.parse('bad_formulas.xml')
all_atoms = doc.findall('.//atom')
proper_atoms = doc.findall('.//formula/atom')
wrongly_placed = set(all_atoms) - set(proper_atoms)
for atom in wrongly_placed:
    print ET.tostring(atom)
<atom number="2" symbol="H" />

<atom number="2" symbol="H" />

~~~~

After converting the XML document to a tree, this program uses
`doc.findall` to get all of the `atom` nodes, and then uses it again to
find all the `atom` nodes that are immediate children of `formula`
nodes. Subtracting the second set from the first gives the nodes that
are *not* immediate children of `formula` nodes, i.e., that are in the
wrong place.

A couple of things are worth pointing out about this program. First, the
ElementTree library doesn't record where in the document nodes are from,
so we can't pinpoint the line or character position of the offending
nodes. Second, the double-spacing on the output comes from the fact that
our original document contained lots of whitespace to make it easier for
human beings to read, and ElementTree kept this whitespace (storing it
as the `tail` value for various nodes). This kind of extra whitespace is
always an annoyance when we're programming, so it's tempting to leave it
out. However, doing so makes it harder for human beings to read the raw
XML using line-oriented editors. Most modern browsers will display the
XML as a tree ([Figure XXX](#f:xml_in_browser)) but native XML-oriented
editing tools are still clumsy.

![XML in the Browser](img/web/xml_in_browser.png)

### Summary

-   Use XPath expressions to identify nodes in a document.
-   Use a node's `findall` method to find children matching an XPath
    expression.

Creating Documents
------------------

### Understand:

-   How to create DOM in memory and turn it into a document.

So much for reading XML: how do we create it? Let's start by writing a
program that re-creates our dimorphism page one element at time:

~~~~ {src="src/web/build_simple_page.py"}
import xml.etree.ElementTree as ET

root = ET.Element('html')

body = ET.Element('body')
root.append(body)

title = ET.SubElement(body, 'h1')
title.text = 'Dimorphism'

p1 = ET.SubElement(body, 'p')
p1.text = 'Occurring or existing in two different '
u = ET.SubElement(p1, 'u')
u.text = 'forms'
p1.tail = '.'

long_text = '''The most notable form is sexual dimorphism,
in which males and females have noticeably different appearances.'''
ET.SubElement(body, 'p').text = long_text

print ET.tostring(root)
~~~~

There is much less to this program than first appears. It starts by
creating an object of type `Element`, which is the class the ElementTree
library uses to represent nodes. The argument to `Element`'s
constructor, `html`, specifies the element's type.

The next two lines create another node of type `body` and then append
that to the root node. At this point, our tree looks like [Figure
XXX](#f:partial_tree):

![Partially-Constructed Tree](img/web/partial_tree.png)

The rest of the program does little more than create and append nodes.
Because creating a node and appending it to another one is so common,
ElementTree provides a convenience function called `SubElement` which
combines the two steps. The two lines:

    title = ET.SubElement(body, 'h1')
    title.text = 'Dimorphism'

create a new node of type `h1`, append it to the `body` node, and then
set the text content of the title node to be the string `'Dimorphism'`.

The next step is the most complicated. We need to create a paragraph
node whose `class` attribute has the value `definition`, and which
contains three things:

1.  the text `'Occurring or existing in two different '` (with a space
    at the end);
2.  a `u` element containing the text `'forms'`; and
3.  another piece of text containing the period '.' that ends the
    sentence.

Creating the paragraph node and appending it to our body node is easy:
we just call `SubElement`. Setting an attribute is also easy: every node
has a dictionary called `attrib` whose keys are attribute names and
whose values are those attributes' values. The single line:

    p1.attrib['class'] = 'definition'

therefore creates the attribute we want.

Now for the paragraph's content. Again, the first part is easy: we just
set `p1.text`. And underlining the word "forms" is easy too: we create a
node of type `u` and append it to the paragraph. But where should the
closing period be stored?

Along with `text`, ElementTree nodes have another text field called
`tail`, which stores the text *after* the node but before the start of
anything else. Since the period is in the paragraph, the right place to
store it is therefore `u.tail` (since putting it in `p1.tail` would
imply that it came after the end of the first paragraph, but before the
start of the next paragraph).

Finally, we create the second paragraph that elaborates dimorphism's
definition by combining node creation and text setting in a single line:

    ET.SubElement(body, 'p').text = long_text

This works because `SubElement` returns the node it just created, so we
can immediately set its `text` value.

![Final Tree](img/web/final_tree.png)

In memory, our document is now something like [Figure
XXX](#f:final_tree). If we convert it to text, we get:

    <html><body><h1>Dimorphism</h1><p class="definition">Occurring or existing in two↵
    different <u>forms</u>.</p><p>The most notable form is sexual dimorphism,
    in which males and females have noticeably different appearances.</p></body></html>

(As before, we use ↵ to break a line that's too long to fit on the
screen.) This has all the content we created, but *only* that content.
We didn't create text nodes containing carriage returns and blanks, so
`tostring` didn't insert them. Most machine-generated XML isn't nicely
indented because computers don't care, but XML intended for human beings
to read usually is.

in practice, of course, programs usually wrap all these steps up in
functions. For example, this function converts a Python list into an
HTML ordered list:

~~~~ {src="src/web/list_to_ol.py"}
import xml.etree.ElementTree as ET

def convert(values):
    '''Convert a list of values to an <ol> list.'''

    result = ET.Element('ol')
    for v in values:
        ET.SubElement(result, 'li').text = str(v)
    return result

root = convert([1, "two", 3.4])
print ET.tostring(root)
<ol><li>1</li><li>two</li><li>3.4</li></ol>
~~~~

The line:

            ET.SubElement(result, 'li').text = str(v)

does two things at once. First, it creates a new `li` (list element)
node and returns it. Second, it sets the `text` of that node to be the
string representation of the next list value. What it *doesn't* do is
store a reference to that node in a separate variable. We could do this,
as in:

        for v in values:
            node = ET.SubElement(result, 'li')
            node.text = str(v)

It's a matter of taste which is less unreadable, but since we're about
to see a different approach that most people find better anyway, the
question is moot.

### Summary

-   Use the same library to create elements in memory rather than
    concatenating and printing strings.
-   An element's `text` property stores the text it contains.
-   An element's `tail` property stores the text that comes immediately
    after it.
