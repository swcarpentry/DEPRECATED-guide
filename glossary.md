[A](#A) [B](#B) [C](#C) [D](#D) [E](#E) [F](#F) [G](#G) [H](#H) [I](#I)
[J](#J) [K](#K) [L](#L) [M](#M) [N](#N) [O](#O) [P](#P) [Q](#Q) [R](#R)
[S](#S) [T](#T) [U](#U) [V](#V) [W](#W) [X](#X) [Y](#Y) [Z](#Z)

A
-

absolute path
:   A [path](#path) that refers to a particular location in a file
    system. Absolute paths are usually written with respect to the file
    system's [root directory](#root-directory), and begin with either
    "/" (on Unix) or "\\" (on Microsoft Windows). See also: [relative
    path](#relative-path).
access control
:   A way to specify who has permission to view, edit, delete, run, or
    otherwise interact with something, by explicitly listing what rights
    each individual or group has. This is in contrast with the standard
    Unix [authorization](#authorization) mechanism, which only allows a
    fixed set of privileges to be listed for owner, one group, and
    everyone else.
access control list (ACL)
:   A way to specify who has permission to view, edit, delete, run, or
    otherwise interact with something, by explicitly listing what rights
    each individual or group has. This is in contrast with the standard
    Unix [authorization](#authorization) mechanism, which only allows a
    fixed set of privileges to be listed for owner, one group, and
    everyone else.
ACID
:   An acronym for atomic, consistent, isolated, and durable, which are
    the properties that a [database transaction](#transaction) must
    guarantee.
acquire a lock
:   To claim a [lock](#lock) in order to establish exclusive access to
    some resource. See also: [release a lock](#release-lock).
actual result
:   The actual result of a [unit test](#unit-test). If this matches the
    [expected result](#expected-result), the test passes.
aggregate
:   To create a single value by combining multiple values, e.g. by
    adding or averaging.
alias
:   A second (or subsequent) reference to a single piece of data.
    Aliasing can make programs more difficult to understand, since
    changes made through one reference "magically" affect the other.
Amdahl's Law
:   A rule first stated by Gene Amdahl that explains why adding more
    hardware can't keep making programs faster indefinitely. For
    example, if 90% of the program can take advantage of the extra
    hardware, but 10% cannot, the greatest possible speedup is a factor
    of ten.
anchor
:   An element of a [regular expression](#regular-expression) that
    matches a location, rather than a sequence of characters. `^`
    matches the beginning of a line, `\b` matches the break between word
    and non-word characters, and `$` matches the end of a line.
assertion
:   An expression which is supposed to be true at a particular point in
    a program. Programmers typically put assertions in their code to
    check for errors; if the assertion fails (i.e., if the expression
    evaluates as false), the program halts and produces an error
    message.
asymmetric cipher
:   A [cipher](#cipher) which has two [keys](#key), each of which undoes
    the other's effects. See also: [symmetric
    cipher](#symmetric-cipher).
atomic operation
:   Not interruptible. An atomic operation is one that always takes
    effect as a whole, no matter what else the system is doing.
atomic value
:   A value that cannot be decomposed into smaller pieces. For example,
    the number 12 is usually considered atomic (unless we are teaching
    addition to school children, in which case we might decompose it
    into tens and ones).
attribute
:   An extra property added to an XML [element](#element). Attributes
    are represented as name/value pairs; a given name may appear at most
    once for any particular element.
authentication
:   The act of establishing someone's identity. This is almost always
    done by requiring them to produce some credentials, such as a
    password. See also: [authorization](#authorization), [access
    control](#access-control).
authorization
:   The part of a computer security system that keeps track of who's
    allowed to do what. See also: [authentication](#authentication),
    [access control](#access-control).

B
-

boundary case
:   In testing, an input that is just at, or just beyond, some extreme
    value. A database containing no records, or a list whose length is
    the greatest possible integer, are both examples of boundary cases.
branch
:   A separate line of development managed by a [version control
    system](#version-control-system). Branches help projects manage
    incompatible sets of changes that are being made concurrently. See
    also: [merge](#merge).
breakpoint
:   A marker put in a program by a [debugger](#debugger) that causes it
    to pause so that the program's internal state can be inspected (and
    possibly modified).

C
-

call stack
:   A data structure used to keep track of functions that are currently
    being executed. Each time a function is called, a new [stack
    frame](#stack-frame) is put on the top of the stack to hold that
    function's local variables. When the function returns, the stack
    frame is discarded. See also: [heap](#heap), [static
    space](#static-space).
cascading delete
:   In a database, the practice of automatically deleting things that
    depend on, or refer to, a record when that record is deleted. See
    also: [referential integrity](#referential-integrity).
case insensitive
:   Treating text as if upper and lower case characters were the same.
    See also: [case sensitive](#case-sensitive).
case sensitive
:   Treating upper and lower case characters as different. See also:
    [case insensitive](#case-insensitive).
catch exception
:   To handle an [exception](#exception). See also: [raise
    exception](#raise-exception).
check out
:   To obtain an initial copy of a project from a version control
    system.
cipher
:   An algorithm used to [encrypt](#encryption) and
    [decrypt](#decryption) data.
ciphertext
:   The [encrypted](#encryption) form of a message. Ciphertext is
    usually produced from [plaintext](#plaintext) by a combination of a
    [cipher](#cipher) algorithm and a [key](#key).
chunk
:   A group of objects that are stored together in short-term memory,
    such as the seven digits in a North American phone number.
class
:   A definition that specifies the properties of a set of
    [objects](#object).
client
:   A software application that accesses data over a network. The
    provider is called a [server](#server).
client-server architecture
:   An asymmetric system in which many [clients](#client) communicate
    with a single centralized [server](#server).
CLUI
:   A command-line user interface. See also: [GUI](#gui).
code coverage
:   The proportion of a program which has been exercised by tests. Code
    coverage is typically expressed as "percentage of lines tested".
    However, even 100% coverage does not guarantee that all possible
    conditions and paths have been tested.
column major order
:   Storing matrix values by columns, and then by rows. See also: [row
    major order](#row-major-order).
command completion
:   Completing the rest of a command when the user presses a shortcut
    key (typically tab).
command-line arguments
:   Values passed to a program on the command line. In Unix, the name of
    the program itself is always the first command-line argument to a
    program.
command-line flag
:   A terse way to specify an option or setting to a command-line
    program. By convention, Unix applications use a dash followed by a
    single letter, such as `-v`, or two dashes followed by a word, such
    as `--verbose`, while DOS applications use a slash, such as `/V`.
    Depending on the application, a flag may be followed by a single
    argument, as in `-o /tmp/output.txt`.
commit
:   To send changes from a [working copy](#working-copy) to a [version
    control](#version-control-system)'s [repository](#repository) to
    create a new [revision](#revision) of the affected file(s). Changes
    must be committed in order for other users to see them. See also:
    [update](#update).
compiler
:   A program that transforms the source of a program into something
    that can be executed. That "something" can be saved for later use,
    or (in an [interpreter](#interpreter)) executed immediately.
concurrency
:   The situation in which two or more things are going on at once. See
    also: [serialization](#serialization).
conditional breakpoint
:   A [breakpoint](#breakpoint) that only causes the program to pause
    under certain conditions. For example, a [debugger](#debugger) may
    specify that the program is to pause only when a certain function
    parameter is an empty string, or when a loop index is greater than a
    specified value.
conflict
:   A change made by one user of a [version control
    system](#version-control-system) that is incompatible with changes
    made by other users. Helping users [resolve](#resolve) conflicts is
    one of the [version control system](#version-control-system)'s major
    tasks.
conflict marker
:   A string such as `<<<<<<`, `======`, or `>>>>>>` put into a local
    copy of a file by a [version control
    system](#version-control-system) to indicate where local changes
    overlap with incompatible changes made by someone else. The [version
    control system](#version-control-system) will typically not allow
    the user to [commit](#commit) changes until all conflicts have been
    [resolved](#resolve).
contract
:   The "agreement" between a function and its caller, usually expressed
    in terms of [preconditions](#precondition) that must be true when
    the function is called in order for it to execute correctly, and
    [postconditions](#postcondition) that the function guarantees will
    be true after the call completes.
core dump
:   A file containing a byte-for-byte representation of the contents of
    a program's memory. On some [operating systems](#operating-system),
    programs produce core dumps whenever they terminate abnormally
    (e.g., try to divide by zero, or access memory that is out of
    bounds). Core dumps are often used as the basis for [post mortem
    debugging](#post-mortem-debugging).
cross product
:   A pairing of all elements of one set with all elements of another.
    The cross product of two *N*-element vectors *L* and *R* is an *N×N*
    matrix *M*, in which *M~i,j~=L~i~R~j~*.
Cascading Style Sheets (CSS)
:   A language used to describe how HTML pages should be formatted for
    display.
current working directory
:   The directory that [relative paths](#relative-path) are calculated
    from; equivalently, the place where files referenced by name only
    are searched for. Every [process](#process) has a current working
    directory. The current working directory is usually referred to
    using the shorthand notation `.` (pronounced "dot").
cursor
:   A pointer into a database that keeps track of outstanding
    transactions and other operations.

D
-

data parallelism
:   Applying the same operation to many data values at once. This is the
    programming model that whole-array languages such as MATLAB use.
database manager
:   A set of values in a [relational database](#relational-database)
    that are organized into [fields](#field-database) and
    [records](#record-database).
database table
:   A set of values in a [relational database](#relational-database)
    that are organized into [fields](#field-database) and
    [records](#record-database).
deadlock
:   Any situation in which no one can proceed unless someone else does
    first (analogous to having two locked boxes, each of which holds the
    key to the other). See also: [race condition](#race-condition).
debuggee
:   See [target program](#target-program).
debugger
:   A computer program that is used to control and inspect another
    program (called the [target program](#target-program)). Most
    debuggers are *symbolic* debuggers that show the target program's
    state in terms of the variables that the programmer created, rather
    than showing the raw contents of memory.
decryption
:   The process of translating [encrypted](#encryption)
    [ciphertext](#ciphertext) back into the original
    [plaintext](#plaintext). See also: [cipher](#cipher), [key](#key).
defensive programming
:   The practice of checking input values, [invariants](#invariant), and
    other aspects of a program in order to catch errors as early as
    possible.
default value
:   A value to use if nothing else is specified explicitly.
design pattern
:   A standard solution to a commonly-occurring problem.
deterministic profiler
:   A [profiler](#profiler) that records events as they happen to
    produce an exact trace of a program's behavior. See also:
    [statistical profiler](#statistical-profiler).
directory tree
:   File system directories are normally organized hierarchically: each
    directory except the [root](#root-directory) has a single parent,
    and each may have zero or more children. This means that directories
    may be viewed as a tree. Since files may not contain directories or
    other files, they are always leaf nodes of this tree.
dictionary
:   A mutable unordered collection that pairs each [key](#key) with a
    single value. Dictionaries are also known as maps, hashes, or
    associative arrays, and are typically implemented using [hash
    tables](#hash-table).
docstring
:   Short for "documentation string", this refers to textual
    documentation embedded in Python programs. Unlike comments,
    docstrings are preserved in the running program, and can be examined
    in interactive sessions.
document
:   A well-formed instance of [XML](#xml). Documents can be represented
    as trees (using [DOM](#document-object-model)), stored as files on
    disk, etc.
Document Object Model (DOM)
:   A cross-language standard for representing XML documents as trees.
domain decomposition
:   Dividing the data used in a program into pieces, and having a
    separate processor operate on each piece.
Domain Name System (DNS)
:   A system which maps numeric [Internet Protocol](#internet-protocol)
    addresses, such as `128.100.171.16`, to human-readable names, such
    as `third-bit.com`.
drive letter
:   In Windows, a single character that identifies a specific [file
    system](#file-system). Drive letters originally referred to actual
    (physical) disk drives.

E
-

element
:   A named item in an [XML](#xml) [document](#document), which has a
    unique parent, and may contain [attributes](#attribute), text, and
    other elements. See also: [tag (in XML)](#tag-xml).
empty list
:   A list containing no values.
encryption
:   The process of translating [plaintext](#plaintext) that anyone can
    understand into [ciphertext](#ciphertext) that can only be
    understood by someone possessing the correct [cipher](#cipher) and
    [key](#key).
escape sequence
:   A sequence of characters that represents some other character or
    special entity. `\t` and `\n` are escape sequences in normal Python
    strings that represent tab and newline characters respectively;
    `&lt;` and `&amp;` are escape sequences in HTML and XML that
    represents the less than sign and ampersand.
exception
:   An object that represents an error condition. As a program executes,
    it creates a stack of [exception handlers](#exception-handler). When
    an exception is [raised](#raise-exception), the program searches
    this stack for the top-most handler, which
    [catches](#catch-exception) and handles the exception. Exceptions
    typically contain information such as the file and line where the
    error occurred, the type of the error, and an error message.
exception handler
:   A block of code that deals with the error signalled by an
    [exception](#exception). See also: [catch
    exception](#catch-exception), [raise exception](#raise-exception).
exclusive or
:   A logical operator that is true if one or other of its arguments is
    true, but not both. See also: [inclusive or](#inclusive-or).
expected result
:   The outcome a test must produce in order to pass. If the [actual
    result](#actual-result) is different, the test fails.
expression
:   Something in a program that has a value. "5" has the value 5,
    "len('abc')" has the value 3, and so on. Expressions may be used in
    [statements](#statement), but not vice versa.

F
-

faded example
:   FIXME
fall-through
:   In a program, the code we execute by default if we do not choose
    some other path explicitly.
field (in database)
:   A set of data values of a particular type, one for each record in a
    [table](#database-table), typically shown as a column. See also:
    [record](#record-database).
file system
:   A set of files, directories, and I/O devices (such as keyboards,
    screens, printers, and so on). A file system may be spread across
    many physical devices, or many file systems may be stored on a
    single physical device. The [operating system](#operating-system)
    will only allow some file operations (such as copying, or creating
    symbolic links or shortcuts) within a file system.
filename extension
:   The portion of a file's name that comes after the final "."
    character. By convention, this identifies the file's type: `.txt`
    means "text file", `.png` means "Portable Network Graphics file",
    and so on. These conventions are *not* enforced by most operating
    systems: it is perfectly possible to name an MP3 sound file
    `homepage.html`. Since many applications use filename extensions to
    identify the [MIME type](#mime) of the file, misnaming files may
    cause those applications to fail.
filter
:   A program that transforms a stream of data. Many Unix command-line
    tools are written as filters: they read data from [standard
    input](#standard-input), process it, and write the result to
    [standard output](#standard-output). Image processing applications
    are often constructed by connecting filters to one another.
fixture
:   The particular configuration of a system that is the subject of a
    [unit test](#unit-test). It is a good practice to create a fresh
    fixture for each test, so that the actions and outcomes of early
    tests cannot affect later ones.
flag
:   A variable used to track the current state of processing. For
    example, a flag can be used to show whether a negative number has
    previously been seen in a list of numbers.
floating point number
:   A number containing a fractional part and an exponent.
for loop
:   A loop that is executed once for each value in some kind of set,
    list, or range.
foreign key
:   One or more values in a [database table](#database-table) that
    identify a [records](#record-database) in another table.
function
:   A portion of a program with an independent identity that can be
    invoked by other parts of the program.

G
-

global scope
:   The top-level [variable scope](#variable-scope) that includes the
    entire program.
GUI
:   A graphical user interface. See also: [CLUI](#clui).

H
-

hash function
:   A function which takes an object as its input, and produces an
    integer value as its output. Good hash functions produce outputs
    that are as random as possible, i.e., they have the property that
    different inputs are likely to produce different outputs.
hash table
:   A data structure which allows programs to look up objects by value,
    rather than by location. Hash tables do this by using a [hash
    function](#hash-function) to calculate seemingly-random identifiers
    for values, and using those as indices into an array. Under normal
    conditions, it takes constant time to find a value in a hash table.
handle
:   A variable that refers to some external resource, such as an open
    file.
head
:   The most recent revision in a version control repository.
heap
:   An area of memory out of which a program can dynamically allocate
    blocks of various sizes in order to store values. See also: [call
    stack](#call-stack), [static space](#static-space).
heisenbug
:   A bug that hides when you are looking for it. Bugs can arise in
    sequential programs (for example, adding a `printf` call to a C
    program may move things around in memory so that the bug is no
    longer triggered), but are much more common in
    [concurrent](#concurrency) programs.
higher order functions
:   A function which operates on other functions.
home directory
:   The default directory associated with an account on a computer
    system. By convention, all of a user's files are stored in or below
    her home directory.
host address
:   A computer's Internet address.
HTML
:   The HyperText Markup Language used to format web pages.
Hypertext Transfer Protocol (HTTP)
:   A set of rules for exchanging data (especially files) on the World
    Wide Web.
HTTP header
:   A name/value pair at the start of an HTTP request or response.
    Unlike dictionary keys, names are not required to be unique.

I
-

idiom
:   definition
immutable
:   Unchangeable. The value of immutable data cannot be altered after it
    has been created. See also: [mutable](#mutable).
implementation
:   How a function, class, or other program element is constructed. The
    term is usually used in contrast with [interface](#interface).
inclusive or
:   A logical operator that is true if either or both of its arguments
    is true. See also: [exclusive or](#exclusive-or).
infinite loop
:   A loop which would never terminate without outside intervention,
    such as `while True: pass` in Python. In practice, all "infinite"
    loops are eventually terminated, if only by the computer being
    switched off.
inner loop
:   A loop that is inside another loop. See also: [outer
    loop](#outer-loop).
integration test
:   A test that checks whether the parts of a program work together. See
    also: [unit test](#unit-test).
interface
:   A specification of the behavior of a function, class, or other unit
    of software. The term is usually used in contrast with
    [implementation](#implementation).
invasion percolation
:   A physical process in which a fluid seeps into a porous material,
    displacing anything that might already be there.
Internet Protocol (IP)
:   A family of communication protocols, the most widely used of which
    are [UDP](#udp) and [TCP](#tcp).
invariant
:   An expression whose value doesn't change during the execution of a
    program. For example, an invariant property of a loop indexed by a
    variable `i` might be that the value of the variable `M` is always
    greater than or equal to the values of the array elements whose
    indices are less than `i`. See also: [precondition](#precondition),
    [postcondition](#postcondition).
IP address
:   A numerical identifier associated with a particular device on a
    network that uses the [Internet Protocol](#internet-protocol) for
    communication.

J
-

K
-

key
:   The data that is used to index a particular entry in a
    [dictionary](#dictionary). In a phone book, for example, people's
    names are keys.
key pair
:   definition

L
-

library
:   FIXME
list
:   FIXME
list indexing
:   FIXME
loader
:   FIXME
local scope
:   FIXME
lock
:   A mechanism used to control access to resources in [concurrent
    systems](#concurrency). If a [process](#process) A tries to
    [acquire](#acquire-lock) a lock held by some other
    [process](#process) B, A is forced to wait until B releases it.
loop body
:   FIXME
loop variable
:   FIXME

M
-

main line
:   FIXME
markup language
:   FIXME
mask
:   FIXME
mental model
:   FIXME
merge
:   To combine the contents of two or more versions of a file in order
    to [resolve](#resolve) overlapping edits; also, to combine material
    from two or more [branches](#branch).
metadata
:   Literally, "data about data", i.e., data such as a format
    descriptor, which describes other data.
method
:   In object-oriented programming, a function which is tied to a
    particular [object](#object). Typically, each of an object's methods
    implements one of the things it can do, or one of the questions it
    can answer.
Multipurpose Internet Mail Extensions (MIME)
:   An Internet standard for the format of email that also specifies
    which filename suffixes should be used to identify particular types
    of content (such as `.png` for a PNG-format image).
model
:   FIXME
module
:   A set of functions and variables that are grouped together to make
    them more manageable. In Python, every source file is automatically
    a module; in other languages, source files may contain many modules,
    or a single module may span several files.
multi-valued assignment
:   An assignment statement which changes several values at once. For
    example, `a,b = 2,3` sets `a` to 2 and `b` to 3, while `a,b = b,a`
    swaps those variables' values.
mutable
:   Changeable. The value of mutable data can be updated in place. See
    also: [immutable](#immutable).

N
-

namespace
:   FIXME
nested list
:   FIXME
nested loop
:   FIXME
nested query
:   A [query](#query) whose results are used as input by some other
    query.
notional machine
:   FIXME

O
-

object
:   A combination of data and functions (called [methods](#method)) that
    are meant to work together. In most programming languages, objects
    are instances of [classes](#class); each object represents one
    "thing" that the program can operate on.
operating system
:   The software responsible for managing a computer's hardware and
    other processes. Operating systems are also responsible for making
    different computers present the same interface to other programs, so
    that applications like word processors and compilers don't have to
    be re-written each time a new generation of chips comes out. Popular
    desktop operating systems include Microsoft Windows, Linux, and Mac
    OS X.
optimistic concurrency
:   Any scheme in which different processes are allowed to make changes
    that may prove incompatible, so long as they [resolve](#resolve)
    them later. See also: [pessimistic
    concurrency](#pessimistic-concurrency).
oracle
:   FIXME
outer loop
:   FIXME

P
-

pair programming
:   FIXME
parameter
:   FIXME
parent directory
:   The directory "above" a particular directory; equivalently, the
    directory that "contains" the one in question. Every directory in a
    file system except the [root](#root-directory) must a unique parent.
    A directory's parent is usually referred to using the shorthand
    notation `..` (pronounced "dot dot").
path
:   A non-empty string specifying a single file or directory. Paths
    consist of zero or more directory names, optionally followed by a
    filename. Directory and file names are separated by "/" (on Unix) or
    "\\" (on Microsoft Windows). If the path begins with this character,
    it is an [absolute path](#absolute-path); otherwise, it is a
    [relative path](#relative-path). On Microsoft Windows, a path may
    optionally begin with a [drive letter](#drive-letter).
path coverage
:   FIXME
peer instruction
:   FIXME
peer-to-peer architecture
:   FIXME
pessimistic concurrency
:   Any scheme which prevents different processes from ever making
    conflicting changes to a shared resource. See also: [optimistic
    concurrency](#optimistic-concurrency).
pipe
:   A connection from the output of one program to the input of another.
    When two or more programs are connected in this way, they are called
    a "pipeline".
pipe and filter
:   FIXME
FIXME
:   definition
plaintext
:   FIXME
port
:   FIXME
post mortem debugging
:   The act of debugging a program after it has terminated, typically by
    inspecting a [core dump](#core-dump).
postcondition
:   FIXME
precondition
:   FIXME
prepared statement
:   FIXME
primary key
:   One or more [fields](#field-database) in a [database
    table](#database-table) whose values are guaranteed to be unique for
    each [record](#record-database), i.e., whose values uniquely
    identify the entry.
FIXME
:   definition
private key
:   One of the two [keys](#key) used in an [asymmetric
    cipher](#asymmetric-cipher). The private key is kept secret, while
    the [public key](#public-key) is shared with anyone the key's owner
    wishes to communicate with.
process
:   A running instance of a program, containing code, variable values,
    open files and network connections, and so on. Processes are the
    "actors" that the [operating system](#operating-system) manages;
    typically, the OS runs each process for a few milliseconds at a time
    to give the impression that they are executing simultaneously.
FIXME
:   definition
prompt
:   FIXME
property (Subversion)
:   definition
protocol
:   FIXME
provenance
:   in art, the history of the ownership and location of an object; in
    computing, the record of how a particular data value was created.
    Computational provenance is intended to provide an audit trail
    allowing every result to be traced back to the program or programs
    that produced it, the settings or parameters used by those programs,
    the raw input values that were processed, etc.
public key
:   One of the two [keys](#key) used in an [asymmetric
    cipher](#asymmetric-cipher). The public key is shared with anyone
    the key's owner wishes to communicate with, while the [private
    key](#private-key) is kept secret.
public key cryptography
:   A cryptographic system based on an [asymmetric
    cipher](#asymmetric-cipher), in which the keys used for
    [encryption](#encryption) and [decryption](#decryption) are
    different, and one cannot be guessed or calculated from the other.
    See also: [private key](#private-key), [public key](#public-key).

Q
-

query
:   A database operation that reads values, but does not modify
    anything. Queries are expressed in a special-purpose language called
    [SQL](#sql).

R
-

race condition
:   A situation in which the final state of a system depends on the
    order in which two or more competing processes modifies the state
    last. For example, if two people make changes to a shared file, the
    final contents of the file depends on who saves their changes last.
    Race conditions are usually bugs, and are notoriously hard to track
    down.
raise exception
:   To signal an error by creating an [exception](#exception), and
    triggering the process by which the program searches for a matching
    [handler](#exception-handler). See also: [catch
    exception](#catch-exception).
record (in database)
:   A set of related values making up a single entry in a [database
    table](#database-table), typically shown as a row. See also: [field
    (database)](#field-database).
redirection
:   FIXME
refactor
:   To rewrite or reorganize software in order to improve its structure
    or readability.
referential integrity
:   The internal consistency of values in a database. If an entry in one
    table contains a [foreign key](#foreign-key), but the
    [record](#record-database) that key is supposed to identify doesn't
    exist, referential integrity has been violated.
regular expression (RE)
:   A pattern that specifies a set of character strings. In programs,
    regular expressions are most often used to find sequences of
    characters in strings.
relational database
:   A collection of data organized into [tables](#database-table).
relative path
:   A [path](#path) that specifies the location of a file or directory
    with respect to the [current working
    directory](#current-working-directory). Any [path](#path) that does
    *not* begin with a separator character ("/" or "\\") is a relative
    path. See also: [absolute path](#absolute-path).
release a lock
:   FIXME
remote login
:   definition
repository
:   A central storage area where a [version control
    system](#version-control-system) stores old [revisions](#revision)
    of files, along with information about who created them and when.
resolve
:   To eliminate the [conflicts](#conflict) between two or more
    incompatible changes to a file or set of files being managed by a
    [version control system](#version-control-system).
FIXME
:   definition
reverse merge
:   FIXME
revert
:   FIXME
revision
:   A particular state of a file, or a set of files, being managed by a
    [version control system](#version-control-system).
revision number
:   FIXME
root directory
:   The top-most directory in a [file system](#file-system)'s [directory
    tree](#directory-tree). Its name is the [operating
    system](#operating-system)'s separator character, i.e., "/" on Unix
    (including Linux and Mac OS X), and "\\" on Microsoft Windows.
root element
:   FIXME
row major order
:   Storing matrix values by row, and then by column. See also: [column
    major order](#column-major-order).

S
-

scope
:   FIXME
screen scraping
:   Using a program to extract information from an HTML page intended
    for human viewing. Screen scraping is a quick way to solve simple
    problems, but breaks down when the pages are complex, or their
    format changes frequently. See also: [web services](#web-services),
    [web spider](#web-spider).
secure shell (SSH)
:   definition
self-join
:   FIXME
sequence
:   A set of objects arranged in a dense, linear fashion, so that they
    may be referred to by their index. In Python, strings, lists, and
    tuples are built-in sequence types, since the elements of each may
    be referred to as `s[0]`, `s[1]`, and so on up to `s[N-1]`, where
    `N` is the sequence's length.
FIXME
:   definition
serialization
:   The act of forcing operations to execute one at a time, instead of
    [concurrently](#concurrency).
server
:   A software application that provides data to other programs. The
    consumer is called a [client](#client). See also: [web
    server](#web-server).
set
:   FIXME
SGML
:   FIXME
shell
:   A command-line user interface program, such as Bash (the
    Bourne-Again Shell) or the Microsoft Windows DOS shell. Shells
    commonly execute a read-evaluate-print cycle: when the user enters a
    command in response to a [prompt](#prompt), the shell either
    executes the command itself, or runs the program that the command
    has specified. In either case, output is sent to the shell window,
    and the user is prompted to enter another command. Most shells
    include commands for looping, conditionals, and defining functions,
    so that small (and sometimes large) programs can be written by
    putting a sequence of shell commands in a file.
shell script
:   FIXME
short-circuit evaluation
:   Evaluation of an expression from left to right that stops as soon as
    the expression's final value is known. For example, if `x` is false,
    the computer does not call the function `f` in the expression
    `x and f(x)`. Similarly, if `x` is true, `f` does not have to be
    called in `x or f(x)`.
side effect
:   FIXME
single-step
:   To advance a program by one instruction, or one line, while
    debugging. See also: [step into](#step-into), [step
    over](#step-over).
socket
:   One end of an [IP](#internet-protocol) communication channel.
sparse
:   Being mostly empty. A sparse vector or matrix is one in which most
    values are zero.
SQL
:   A special-purpose language for describing operations on [relational
    databases](#relational-database). SQL is *not* actually an acronym
    for "Structured Query Language".
SQL injection
:   FIXME
stack frame
:   A data structure that provides storage for a function's local
    variables. Each time a function is called, a new stack frame is
    created and put on the top of the [call stack](#call-stack). When
    the function returns, the stack frame is discarded.
standard error
:   A process's "other" default output stream, typically used for error
    messages. See also: [standard output](#standard-output).
standard input
:   A process's default input stream. In interactive command-line
    applications, it is typically connected to the keyboard; in a
    [pipeline](#pipe), it receives data from the [standard
    output](#standard-output) of the preceding process.
standard output
:   A process's default output stream. In interactive command-line
    applications, data sent to standard output is displayed on the
    screen; in a [pipeline](#pipe), it is passed to the [standard
    input](#standard-input) of the next process.
stateless protocol
:   A communication protocol in which each basic operation is
    independent of each other. [HTTP](#http) is the best-known example:
    [servers](#server) do not remember anything about [clients](#client)
    between requests.
statement
:   FIXME
static space
:   A portion of a program's memory reserved for storing values that are
    allocated even before the program starts to run, such as constant
    strings. See also: [call stack](#call-stack), [heap](#heap).
FIXME
:   definition
stdin
:   FIXME
stdout
:   FIXME
step into
:   To go into a function call when debugging. See also:
    [single-step](#single-step), [step over](#step-over).
step over
:   To execute a function without going into it when debugging. See
    also: [single-step](#single-step), [step into](#step-into).
stereotype-threat
:   FIXME
string
:   FIXME
FIXME
:   definition
subquery
:   FIXME
symmetric cipher
:   A [cipher](#cipher) in which a single key is used for both
    [encryption](#encryption) and [decryption](#decryption). Symmetric
    ciphers are less secure than [asymmetric](#asymmetric-cipher) ones,
    but are typically much faster.

T
-

table
:   FIXME
tag (in XML)
:   A textual representation of an [XML](#xml) [element](#element). Tags
    come in matched opening and closing pairs, such as `<x>` and `</x>`;
    if the element the tag pair represents does not contain text or
    other elements, the short form `<x/>` may be used. See also:
    [branch](#branch).
target program
:   The program being controlled by a [debugger](#debugger); also called
    the [debuggee](#debuggee).
FIXME
:   definition
Transmission Control Protocol (TCP)
:   A communication protocol in the [IP](#internet-protocol) family that
    provides reliable in-order delivery of data. Programs communicating
    via TCP can read and write as they would with files (at least, until
    something goes wrong). See also: [socket](#socket), [User Datagram
    Protocol (UDP)](#udp).
test action
:   FIXME
test report
:   FIXME
test result
:   FIXME
text
:   The non-[element](#element) content of an [XML](#xml)
    [document](#document); in an HTML page, the text is what is
    displayed, while the [tags](#tag-xml) control its formatting.
FIXME
:   definition
transaction
:   A set of operations which take effect in a reliable, consistent
    manner. If a transaction cannot be completed (e.g., because of a
    system failure), it is guaranteed to have no effect.
tree
:   FIXME
tuple
:   An immutable [sequence](#sequence).
type
:   FIXME

U
-

Unicode
:   An international standard for representing characters and other
    symbols. Each symbol is assigned a unique number; those numbers are
    then encoded in any of several standard ways (such as
    [UTF-8](#utf-8)).
unit test
:   A test that exercises a single basic element of a program, such as a
    particular function or method. See also: [integration
    test](#integration-test).
update
:   To update a [working copy](#working-copy) with the most recent
    changes in a [version control system](#version-control-system)
    [repository](#repository). See also: [commit](#commit).
URL encoding
:   A translation standard that replaces characters that are meaningful
    in URLs (such as `&` and `?`) with their hexadecimal encodings.
user group
:   FIXME
user group ID
:   FIXME
user group name
:   FIXME
user ID
:   FIXME
username
:   FIXME
UTF-8
:   A standard for encoding character data; the acronym is short for
    "[Unicode](#unicode) Transformation Format, 8-bit encoding form".

V
-

variable
:   FIXME
variable scope
:   FIXME
version control system
:   A tool for managing changes to a set of files. Each set of changes
    creates a new [revision](#revision) of the files; the version
    control system allows users to recover old [revisions](#revision)
    reliably, and helps manage conflicting changes made by different
    users.
view
:   FIXME

W
-

FIXME
:   definition
web server
:   A [server](#server) that handles [HTTP](#http) requests.
web services
:   A software application that exchanges data with others by sending
    [XML](#xml) data via the [HTTP](#http) protocol. Most modern web
    services encode data using the [SOAP](#soap) standard. See also:
    [screen scraping](#screen-scraping).
while loop
:   FIXME
whitespace
:   FIXME
wildcard
:   A character used in pattern matching. In the Unix shell, the
    wildcard "\*" matches zero or more characters, so that `*.txt`
    matches all files whose names end in `.txt`.
working copy
:   A personal copy of the files being managed by a [version control
    system](#version-control-system). Changes the user makes to the
    working copy do not affect other users until they are
    [committed](#commit) to the [repository](#repository).
wrapper function
:   FIXME
WYSIWYG
:   FIXME

X
-

XML
:   The Extensible Markup Language; a standard for defining
    application-specific markup languages. See also:
    [attribute](#attribute), [document](#document), [Document Object
    Model (DOM)](#document-object-model), [element](#element).
XPath
:   FIXME

Y
-

Z
-
