Databases
=========

> We're here to do research, they pay us to teach, we spend our time on
> administration. \
>  — Eleni Stroulia

As many scientists have found out the hard way, the real challenges in
research have nothing to do with quantum mechanics, protein folding, or
the rate at which vulgar toads reproduce in the absence of natural
predators. No, the real challenges are all about accounting and
administration. In this chapter, we'll see how to use a database to keep
track of what our graduate students have worked on. The techniques we'll
explore apply directly to other kinds of databases as well, and as we'll
see, knowing how to get information *out* of a database is essential to
figuring out how to put data *in*.

Selecting
---------

### Learning Objectives:

-   Explain the difference between a table, a database, and a database
    manager.
-   Explain the difference between a field and a record.
-   Select specific fields from specific tables, and display them in a
    specific order.

A [relational database](glossary.html#relational-database) is a way to
store and manipulate information that is arranged as
[tables](glossary.html#table). Each table has columns (also known as
[fields](glossary.html#field-database)) which describe the data, and
rows (also known as [records](glossary.html#record-database)) which
contain the data.

When we are using a spreadsheet, we put formulas into cells to calculate
new values based on old ones. When we are using a database, we send
commands (usually called [queries](glossary.html#query)) to a [database
manager](glossary.html#database-manager): a program that manipulates the
database for us. The database manager does whatever lookups and
calculations the query specifies, returning the results in a tabular
form that we can then use as a starting point for further queries.

Queries are written in a language called [SQL](glossary.html#sql), which
stands for "Structured Query Language". SQL provides hundreds of
different ways to analyze and recombine data; we will only look at a
handful, but that handful accounts for most of what scientists do.

Here's a simple database that records how many hours scientists have
spent on various projects in a research lab. It consists of a single
table called `Experiments` with three fields—scientists, experiment, and
hours—and eight records. Each record stores a scientist's hours on one
project.

  -------------------- --------------- -----------
  **Experiments**
  **Scientist**        **Project**     **Hours**
  Sofia Kovalevskaya   Antigravity     6.5
  Sofia Kovalevskaya   Teleportation   11.0
  Sofia Kovalevskaya   Teleportation   5.0
  Mikhail Lomonosov    Antigravity     4.0
  Mikhail Lomonosov    Time Travel     -2.0
  Dmitri Mendeleev     Antigravity     9.0
  Ivan Pavlov          Teleportation   9.0
  Ivan Pavlov          Time Travel     -7.0
  -------------------- --------------- -----------

Notice that there are two entries for Sofia Kovalevskaya's work on the
Teleportation project. This could mean that she worked on it at two
different times, or it could be a data entry error. We'll come back to
this question [later](#a:keys).

For now, let's write an SQL query that gets people's names and hours. We
do this using the SQL command `SELECT`, giving it the names of the
columns we want to read and the table to read them from. (We have to
provide the table name because most databases contain more than one
table.) Our query looks like this:

~~~~ {src="src/db/select_scientist_hours.sql"}
SELECT Scientist, Hours FROM Experiments;
~~~~

We have capitalized the words `SELECT` and `FROM` because they are SQL
keywords. SQL is actually case insensitive—we could write `select` or
`sElEcT`—but we will stick to upper case so that it is clear what is a
keyword and what is not. The semi-colon at the end tells the database
manager that the command is complete. When it runs, it shows us the two
columns of the `Experiments` table that we asked for:

  -------------------- ------
  Sofia Kovalevskaya   6.5
  Sofia Kovalevskaya   11.0
  Sofia Kovalevskaya   5.0
  Mikhail Lomonosov    4.0
  Mikhail Lomonosov    -2.0
  Dmitri Mendeleev     9.0
  Ivan Pavlov          9.0
  Ivan Pavlov          -7.0
  -------------------- ------

Exactly *how* the database displays the query's results depends on what
kind of interface we are using. If we are running `sqlite` from the
shell, its default output looks like this:

    Sofia Kovalevskaya|6.5
    Sofia Kovalevskaya|11.0
    Sofia Kovalevskaya|5.0
    Mikhail Lomonosov|4.0
    Mikhail Lomonosov|-2.0
    Dmitri Mendeleev|9.0
    Ivan Pavlov|9.0
    Ivan Pavlov|-7.0

If we are using a graphical interface, such as the [SQLite
Manager](https://addons.mozilla.org/en-US/firefox/addon/sqlite-manager/)
plugin for Firefox, our output will be displayed more readably ([Figure
XXX](#f:firefox_plugin)). We'll use a simple table-based display for
now.

![SQLite Manager Plugin for Firefox](img/db/firefox_plugin.png)

If we want the project name to our output, we can just add that to the
list of fields:

~~~~ {src="src/db/select_scientist_hours_project.sql"}
SELECT Scientist, Hours, Project FROM Experiments;
~~~~

  -------------------- ------ ---------------
  Sofia Kovalevskaya   6.5    Antigravity
  Sofia Kovalevskaya   11.0   Teleportation
  Sofia Kovalevskaya   5.0    Teleportation
  Mikhail Lomonosov    4.0    Antigravity
  Mikhail Lomonosov    -2.0   Time Travel
  Dmitri Mendeleev     9.0    Antigravity
  Ivan Pavlov          9.0    Teleportation
  Ivan Pavlov          -7.0   Time Travel
  -------------------- ------ ---------------

It's important to understand that the rows and columns in a database
table aren't actually stored in any particular order. They will always
be *displayed* in some order, but we can control that in various ways.
For example, we could rearrange the columns in the output by writing our
query as:

~~~~ {src="src/db/select_project_scientist_hours.sql"}
SELECT Project, Scientist, Hours FROM Experiments;
~~~~

  --------------- -------------------- ------
  Antigravity     Sofia Kovalevskaya   6.5
  Teleportation   Sofia Kovalevskaya   11.0
  Teleportation   Sofia Kovalevskaya   5.0
  Antigravity     Mikhail Lomonosov    4.0
  Time Travel     Mikhail Lomonosov    -2.0
  Antigravity     Dmitri Mendeleev     9.0
  Teleportation   Ivan Pavlov          9.0
  Time Travel     Ivan Pavlov          -7.0
  --------------- -------------------- ------

or even repeat columns:

~~~~ {make="select_project_project"}
SELECT Project, Project FROM Experiments;
~~~~

  --------------- ---------------
  Antigravity     Antigravity
  Teleportation   Teleportation
  Teleportation   Teleportation
  Antigravity     Antigravity
  Time Travel     Time Travel
  Antigravity     Antigravity
  Teleportation   Teleportation
  Time Travel     Time Travel
  --------------- ---------------

We will see ways to rearrange the rows [later](#s:sort).

As a shortcut, we can select all of the columns in a table using the
wildcard `*`. For example:

~~~~ {src="src/db/select_star"}
SELECT * FROM Experiments;
~~~~

selects all of the data in the `Experiments` table:

  -------------------- --------------- ------
  Sofia Kovalevskaya   Antigravity     6.5
  Sofia Kovalevskaya   Teleportation   11.0
  Sofia Kovalevskaya   Teleportation   5.0
  Mikhail Lomonosov    Antigravity     4.0
  Mikhail Lomonosov    Time Travel     -2.0
  Dmitri Mendeleev     Antigravity     9.0
  Ivan Pavlov          Teleportation   9.0
  Ivan Pavlov          Time Travel     -7.0
  -------------------- --------------- ------

### Summary

-   A relational database stores information in tables with fields and
    records.
-   A database manager is a program that manipulates a database.
-   The commands or queries given to a database manager are usually
    written in a specialized language called SQL.
-   SQL is case insensitive.
-   The rows and columns of a database table aren't stored in any
    particular order.
-   Use `SELECT fields FROM table` to get all the values for specific
    fields from a single table.
-   Use `SELECT * FROM table` to select everything from a table.

Removing Duplicates
-------------------

### Learning Objectives:

-   Write queries that only display each different result once.

Queries often return redundant information. For example:

~~~~ {src="src/db/select_project.sql"}
SELECT Project FROM Experiments;
~~~~

displays some project names multiple times (once for each occurrence):

  ---------------
  Antigravity
  Teleportation
  Teleportation
  Antigravity
  Time Travel
  Antigravity
  Teleportation
  Time Travel
  ---------------

We can eliminate the redundant copies by adding the `DISTINCT` keyword
to our query:

~~~~ {src="src/db/select_distinct_project.sql"}
SELECT DISTINCT Project FROM Experiments;
~~~~

  ---------------
  Antigravity
  Teleportation
  Time Travel
  ---------------

If we select more than one column—for example, both the project name and
the hours—then the distinct pairs of values are returned. For example,
the query below only displays Sofia Kovalevskaya and the Teleportation
project once, even though there are two entries in the database for the
hours she spent on it:

~~~~ {src="src/db/select_distinct_project_hours.sql"}
SELECT DISTINCT Project, Scientist FROM Experiment;
~~~~

  --------------- --------------------
  Antigravity     Dmitri Mendeleev
  Antigravity     Mikhail Lomonosov
  Antigravity     Sofia Kovalevskaya
  Teleportation   Ivan Pavlov
  Teleportation   Sofia Kovalevskaya
  Time Travel     Ivan Pavlov
  Time Travel     Mikhail Lomonosov
  --------------- --------------------

Notice in both cases that duplicates are removed even if they didn't
appear to be adjacent in the database. Once again, it's important to
remember that rows aren't actually ordered: they're just displayed that
way.

### Summary

-   Use `SELECT DISTINCT` to eliminate duplicates from a query's output.

Calculating New Values
----------------------

### Learning Objectives:

-   Write queries that do arithmetic using the values in individual
    records.

Suppose that 10% of the time spent on each experiment was prep work that
needs to be accounted for separately. We can add an expression to our
`SELECT` statement to do the required computation for each row like
this:

~~~~ {src="src/db/select_simple_formula.sql"}
SELECT *, 0.1 * Hours FROM Experiments;
~~~~

  -------------------- --------------- ------ ------
  Sofia Kovalevskaya   Antigravity     6.5    0.65
  Sofia Kovalevskaya   Teleportation   11.0   1.1
  Sofia Kovalevskaya   Teleportation   5.0    0.5
  Mikhail Lomonosov    Antigravity     4.0    0.4
  Mikhail Lomonosov    Time Travel     -2.0   -0.2
  Dmitri Mendeleev     Antigravity     9.0    0.9
  Ivan Pavlov          Teleportation   9.0    0.9
  Ivan Pavlov          Time Travel     -7.0   -0.7
  -------------------- --------------- ------ ------

When we run the query, the expression `0.1 * Hours` is evaluated for
each row and appended to that row. Expressions can use any of the
fields, all of usual arithmetic operators, and a variety of built-in
functions (the most commonly used of which are summarized in [the
appendix](ref.html#s:db)). For example, we could round values to a
single decimal place using the `ROUND` function, and pair that value
with the scientist's name:

~~~~ {src="src/db/select_scientist_formula.sql"}
SELECT Scientist, ROUND(0.1 * Hours, 1) FROM Experiments;
~~~~

  -------------------- ------
  Sofia Kovalevskaya   0.7
  Sofia Kovalevskaya   1.1
  Sofia Kovalevskaya   0.5
  Mikhail Lomonosov    0.4
  Mikhail Lomonosov    -0.2
  Dmitri Mendeleev     0.9
  Ivan Pavlov          0.9
  Ivan Pavlov          -0.7
  -------------------- ------

### Summary

-   Use expressions in place of field names to calculate per-record
    values.

Filtering
---------

### Learning Objectives:

-   Write queries that select records based on the values of their
    fields.
-   Write queries that select records using combinations of several
    tests on their fields' values.
-   Build up complex filtering criteria incrementally.
-   Explain the logical order in which filtering by field value and
    displaying fields takes place.

One of the most powerful features of a database is the ability to
[filter](glossary.html#filter) data, i.e., to select only those records
that match certain criteria. For example, suppose we want to see all of
the experiments that took more than two hours to complete. We can select
these by adding a `WHERE` clause to our query:

~~~~ {src="src/db/select_where_hours.sql"}
SELECT * FROM Experiments WHERE Hours > 2.0;
~~~~

  -------------------- --------------- ------
  Sofia Kovalevskaya   Antigravity     6.5
  Sofia Kovalevskaya   Teleportation   11.0
  Sofia Kovalevskaya   Teleportation   5.0
  Mikhail Lomonosov    Antigravity     4.0
  Dmitri Mendeleev     Antigravity     9.0
  Ivan Pavlov          Teleportation   9.0
  -------------------- --------------- ------

We can understand how this query works by imagining that the database
executes it in two stages ([Figure XXX](#f:pipeline_where)). First, the
database looks at each row in the `Experiments` table to see which ones
satisfy the `WHERE` condition. It then uses the column names immediately
following the `SELECT` keyword to determine what columns to keep (or, if
there are expressions, what new values to calculate).

![Two-Stage Query Processing Pipeline](img/db/pipeline_where.png)

We can use many other operators to filter our data. For example, we
could ask for all of the experiments that were done by Ivan Pavlov:

~~~~ {src="src/db/select_where_pavlov.sql"}
SELECT * FROM Experiment WHERE Scientist = "Ivan Pavlov";
~~~~

  ------------- --------------- ------
  Ivan Pavlov   Teleportation   9.0
  Ivan Pavlov   Time Travel     -7.0
  ------------- --------------- ------

We can also make our `WHERE` conditions more sophisticated by combining
tests with `AND` and `OR`. For example, suppose we want to know which
project Mikhail Lomonosov spent more than three hours working on. We're
only interested in rows that satisfy *both* criteria, so we combine the
two tests with `AND`:

~~~~ {src="src/db/select_where_lomonosov_three_hours.sql"}
SELECT * FROM Experiments WHERE (Hours > 3) AND (Scientist = "Mikhail Lomonosov");
~~~~

  ------------------- ------------- -----
  Mikhail Lomonosov   Antigravity   4.0
  ------------------- ------------- -----

(The parentheses around each test aren't strictly required, but they
help make the query easier to read.)

If we wanted experiments that either Ivan or Mikhail had worked on, we
would combine the tests on their names like this:

~~~~ {src="src/db/select_where_lomonosov_or_pavlov.sql"}
SELECT * FROM Experiments WHERE (Scientist = "Mikhail Lomonosov") OR (Scientist = "Ivan Pavlov");
~~~~

  ------------------- --------------- ------
  Mikhail Lomonosov   Antigravity     4.0
  Mikhail Lomonosov   Time Travel     -2.0
  Ivan Pavlov         Teleportation   9.0
  Ivan Pavlov         Time Travel     -7.0
  ------------------- --------------- ------

And if we wanted project that either scientist had spent more than three
hours on, we would combine our tests:

~~~~ {src="src/db/select_where_lomonosov_or_pavlov_three_hours.sql"}
SELECT * FROM Experiments WHERE (Hours > 3) AND ((Scientist = "Mikhail Lomonosov") OR (Scientist = "Ivan Pavlov"));
~~~~

  ------------------- --------------- -----
  Mikhail Lomonosov   Antigravity     4.0
  Ivan Pavlov         Teleportation   9.0
  ------------------- --------------- -----

The extra parentheses around the checks on the scientists' names ensure
that the `AND` and `OR` are combined the way we want. Without them, the
computer might decide that we meant:

~~~~ {src="src/db/select_where_badly_grouped.sql"}
SELECT * FROM Experiments WHERE ((Hours > 3) AND (Scientist = "Mikhail Lomonosov")) OR (Scientist = "Ivan Pavlov");
~~~~

i.e., that we want projects where Mikhail spent a lot of time, or any
projects that Ivan worked on, regardless of hours. Since this is
actually a different query, it gives a different (and wrong) answer:

  ------------------- --------------- ------
  Mikhail Lomonosov   Antigravity     4.0
  Ivan Pavlov         Teleportation   9.0
  Ivan Pavlov         Time Travel     -7.0
  ------------------- --------------- ------

Instead of using `OR` to match one of several values, we can use the
`IN` operator along with a list of values we would like to match. For
example, we could rewrite our query as:

~~~~ {src="src/db/select_where_using_in.sql"}
SELECT * FROM Experiments WHERE (Hours > 3) AND (Scientist IN ("Mikhail Lomonosov", "Ivan Pavlov"));
~~~~

This produces the same two rows as the correctly-parenthesized query,
but is easier to understand, particularly as the number of options
grows.

Knowing how to translate what we want into appropriate `WHERE` clauses
When in doubt, refer to the earlier discussion of [Boolean
logic](python.html#s:bool).

### Growing Queries

What we have just done is how most people "grow" their SQL queries. We
started with something simple that did part of what we wanted, then
added more clauses one by one, testing their effects as we went. This is
a good strategy—in fact, for complex queries it's often the *only*
strategy—but it depends on quick turnaround, and on us recognizing the
right answer when we get it.

The best way to achieve quick turnaround is often to put a subset of
data in a temporary database and run our queries against that, or to
fill a small database with synthesized records. For example, instead of
trying our queries against an actual database of 20 million Australians,
we could run it against a sample of ten thousand, or write a small
program to generate ten thousand random (but plausible) records and use
that.

### Summary

-   Use `WHERE test` in a query to filter records based on logical
    tests.
-   Use `AND` and `OR` to combine tests in filters.
-   Use `IN` to test whether a value is in a set.
-   Build up queries a bit at a time, and test them against small data
    sets.

Sorting
-------

### Learning Objectives:

-   Write queries that order results according to fields' values.
-   Write queries that order results according to calculated values.
-   Explain why it is possible to sort records using the values of
    fields that are not displayed.

As we mentioned earlier, database records are not stored in any
particular order. This means that query results aren't necessarily
sorted, and even if they are, we often want to sort them in a different
way, e.g., by the name of the project instead of by the name of the
scientist. We can do this in SQL by adding an `ORDER BY` clause to our
query as shown here:

~~~~ {src="src/db/select_order_project_asc.sql"}
SELECT * FROM Experiments ORDER BY Project ASC;
~~~~

  -------------------- --------------- ------
  Sofia Kovalevskaya   Antigravity     6.5
  Mikhail Lomonosov    Antigravity     4.0
  Dmitri Mendeleev     Antigravity     9.0
  Sofia Kovalevskaya   Teleportation   11.0
  Sofia Kovalevskaya   Teleportation   5.0
  Ivan Pavlov          Teleportation   9.0
  Mikhail Lomonosov    Time Travel     -2.0
  Ivan Pavlov          Time Travel     -7.0
  -------------------- --------------- ------

The keyword `ASC` at the end is short for "ascending", and means
"smallest first". We can sort in the opposite order using `DESC` (for
"descending") instead:

~~~~ {src="src/db/select_order_project_desc.sql"}
SELECT * FROM Experiments ORDER BY Project DESC;
~~~~

  -------------------- --------------- ------
  Mikhail Lomonosov    Time Travel     -2.0
  Ivan Pavlov          Time Travel     -7.0
  Sofia Kovalevskaya   Teleportation   11.0
  Sofia Kovalevskaya   Teleportation   5.0
  Ivan Pavlov          Teleportation   9.0
  Sofia Kovalevskaya   Antigravity     6.5
  Mikhail Lomonosov    Antigravity     4.0
  Dmitri Mendeleev     Antigravity     9.0
  -------------------- --------------- ------

We can also sort on several fields at once. For example, this query
sorts results in ascending order by project name, and then sorts the
results for each project in descending order by name:

~~~~ {src="src/db/select_order_multiple.sql"}
SELECT * FROM Experiments ORDER BY Project ASC, Scientist DESC;
~~~~

  -------------------- --------------- ------
  Sofia Kovalevskaya   Antigravity     6.5
  Mikhail Lomonosov    Antigravity     4.0
  Dmitri Mendeleev     Antigravity     9.0
  Sofia Kovalevskaya   Teleportation   11.0
  Sofia Kovalevskaya   Teleportation   5.0
  Ivan Pavlov          Teleportation   9.0
  Mikhail Lomonosov    Time Travel     -2.0
  Ivan Pavlov          Time Travel     -7.0
  -------------------- --------------- ------

We can even sort the results by the value of an expression. In SQLite,
for example, the `RANDOM` function returns a pseudo-random integer:

~~~~ {src="src/db/select_random.sql"}
SELECT RANDOM() FROM Experiments;
~~~~

  ----------------------
  -4333583529515760313
  3661398752594229354
  -1239522849593007459
  5085104577194332809
  7406392079669228295
  8157275644606127629
  4936669514230061450
  3027346145930117288
  ----------------------

(Try running the query twice and watch the random values change.) So to
randomize the order of our query results, we can sort them by the value
of this function:

~~~~ {src="src/db/select_order_random.sql"}
SELECT * FROM Experiments ORDER BY RANDOM();
~~~~

  -------------------- --------------- ------
  Mikhail Lomonosov    Time Travel     -2.0
  Sofia Kovalevskaya   Teleportation   5.0
  Mikhail Lomonosov    Antigravity     4.0
  Dmitri Mendeleev     Antigravity     9.0
  Sofia Kovalevskaya   Teleportation   11.0
  Ivan Pavlov          Time Travel     -7.0
  Ivan Pavlov          Teleportation   9.0
  Sofia Kovalevskaya   Antigravity     6.5
  -------------------- --------------- ------

We don't actually have to display a column in order to sort by it. For
example, the query below sorts by the project name, but only displays
the scientist's name and hours. (It is also split across several lines
to make it easier to read, which is a good practice for complicated
queries).

~~~~ {src="src/db/select_order_project_display_scientist_hours.sql"}
SELECT   Scientist, Hours
FROM     Experiments
ORDER BY Project;
~~~~

  -------------------- ------
  Sofia Kovalevskaya   6.5
  Mikhail Lomonosov    4.0
  Dmitri Mendeleev     9.0
  Sofia Kovalevskaya   11.0
  Sofia Kovalevskaya   5.0
  Ivan Pavlov          9.0
  Mikhail Lomonosov    -2.0
  Ivan Pavlov          -7.0
  -------------------- ------

We can sort on fields that aren't displayed because sorting happens
earlier in the processing pipeline than field selection ([Figure
XXX](#f:pipeline_sort)). Once we include sorting, our pipeline:

-   filters rows according to the `WHERE` clause (if any);
-   sorts the results according to the `ORDER BY` clause (if there is
    one); and
-   displays the specified columns and/or expressions.

![Three-Stage Query Processing Pipeline](img/db/pipeline_sort.png)

Let's put everything we've seen so far together in a single query:

~~~~ {src="src/db/select_all_options.sql"}
SELECT   *, ROUND(0.1 * Hours, 1)
FROM     Experiments
WHERE    Hours > 3
ORDER BY Project DESC;
~~~~

  -------------------- --------------- ------ -----
  Sofia Kovalevskaya   Teleportation   11.0   1.1
  Sofia Kovalevskaya   Teleportation   5.0    0.5
  Ivan Pavlov          Teleportation   9.0    0.9
  Sofia Kovalevskaya   Antigravity     6.5    0.7
  Mikhail Lomonosov    Antigravity     4.0    0.4
  Dmitri Mendeleev     Antigravity     9.0    0.9
  -------------------- --------------- ------ -----

The order of the clauses is required by `SQL`: the `SELECT` must come
before the `FROM`, the `WHERE ` clause must come next, and the
`ORDER BY ` clause must come last.

### Summary

-   Use `ORDER BY field ASC` (or `DESC`) to order a query's results in
    ascending (or descending) order.

Aggregation
-----------

### Learning Objectives:

-   Write queries that combine values from many records to create a
    single aggregate value.
-   Write queries that put records into groups based on their values.
-   Write queries that combine values group by group.
-   Explain what is displayed for *unaggregated* fields when some fields
    are aggregated.
-   Explain how to order aggregated results.
-   Explain when grouping and aggregating occur during query processing.

Now suppose we want to know how many our grad students have spent on all
projects combined. We know how to fetch the hours:

~~~~ {src="src/db/select_hours.sql"}
SELECT Hours FROM Experiment;
~~~~

but how can we add them together? The solution is to use the `SUM`
function:

~~~~ {src="src/db/agg_sum_hours.sql"}
SELECT SUM(Hours) FROM Experiments;
~~~~

The output is a table containing a single row and column:

  ------
  35.5
  ------

`SUM` is just one of the [aggregation](glossary.html#aggregate)
functions built into SQL. In their simplest form, aggregation functions
reduce all the rows returned by a query to a single row. `MAX`, `MIN`,
and `AVG` are also aggregation functions, and do what their names
suggest:

~~~~ {src="src/db/agg_functions_hours.sql"}
SELECT SUM(Hours), MAX(Hours), MIN(Hours), AVG(Hours) FROM Experiments;
~~~~

  ------ ------ ------ --------
  35.5   11.0   -7.0   4.4375
  ------ ------ ------ --------

Another handy aggregation function is `COUNT`, which counts how many
records there are in a set:

~~~~ {src="src/db/agg_count_hours.sql"}
SELECT COUNT(Hours) FROM Experiments;
~~~~

  ---
  8
  ---

We used `COUNT(Hours)` here, but we could just as easily have counted
`Project` or any other field in the table, or even used `COUNT(*)`,
since the function doesn't care about the values themselves, just how
many values there are.

Aggregation is very useful, but there are a few traps for the unwary.
For example, what if we want the total number of hours each scientist
has worked so far? We can find out how much time a *particular*
scientist has spent in the lab like this:

~~~~ {src="src/db/agg_hours_mendeleev.sql"}
SELECT SUM(Hours) FROM Experiments WHERE Scientist = "Dmitri Mendeleev";
~~~~

  ---
  9
  ---

but we would have to write a separate query for each scientist, and
remember to add a new query each time someone joined the lab. What we
want is a query that gives us one row per scientist with the scientist's
name and the total of his or her hours. Our first attempt look like
this:

~~~~ {src="src/db/agg_per_scientist_wrong.sql"}
SELECT Scientist, SUM(Hours) FROM Experiments;
~~~~

  ------------- ------
  Ivan Pavlov   35.5
  ------------- ------

Why does this query return only one row, rather than one per scientist?
And why does that row have Ivan Pavlov's name, but the total hours for
*all* the scientists?

The answer lies in the fact that when we used `SUM`, the database
combined the rows in the table by summing the `Hours` column, but since
we didn't specify a aggregation function for `Scientist`, the database
picked an arbitrary value from that column and returned it ([Figure
XXX](#f:bad_aggregation)). In general, if your query selects fields
directly from a table and aggregates at the same time, the values for
unaggregated fields can be any value from the records being aggregated.

![Incorrect Aggregation](img/db/bad_aggregation.png)

If we really do want each scientist's hours, we need to tell the
database to aggregate the hours for each scientist separately using a
`GROUP BY` clause:

~~~~ {src="src/db/group_by_scientist.sql"}
SELECT   Scientist, Hours
FROM     Experiments
GROUP BY Scientist;
~~~~

  -------------------- ------
  Dmitri Mendeleev     9.0
  Ivan Pavlov          -7.0
  Mikhail Lomonosov    -2.0
  Sofia Kovalevskaya   5.0
  -------------------- ------

Here, the database has grouped all the records with the same value for
`Scientist` together, then selected one row from each group to display
([Figure XXX](#f:correct_aggregation)). Since all the rows in each group
have the same scientist's name, we get that name; the value for `Hours`
is just one of the values for that scientist, chosen randomly for the
same reason that the scientist's name was chosen randomly when we used
`SUM(Hours)` a couple of queries ago.

![Correct Aggregation](img/db/correct_aggregation.png)

But look what happens when we put the call to `SUM` back in our query:

~~~~ {src="src/db/agg_sum_by_scientist.sql"}
SELECT   Scientist, SUM(Hours)
FROM     Experiments
GROUP BY Scientist;
~~~~

  -------------------- ------
  Dmitri Mendeleev     9.0
  Ivan Pavlov          2.0
  Mikhail Lomonosov    2.0
  Sofia Kovalevskaya   22.5
  -------------------- ------

This is the total number of hours for each scientist, which is what we
wanted. And just as we can sort by multiple criteria at once, we can
also group by multiple criteria. To get the number of hours each
scientist has spent on each project, for example, we would group by both
columns:

~~~~ {src="src/db/agg_sum_by_scientist_project.sql"}
SELECT   Scientist, Project, SUM(Hours)
FROM     Experiments
GROUP BY Scientist, Project;
~~~~

  -------------------- --------------- ------
  Dmitri Mendeleev     Antigravity     9.0
  Ivan Pavlov          Teleportation   9.0
  Ivan Pavlov          Time Travel     -7.0
  Mikhail Lomonosov    Antigravity     4.0
  Mikhail Lomonosov    Time Travel     -2.0
  Sofia Kovalevskaya   Antigravity     6.5
  Sofia Kovalevskaya   Teleportation   16.0
  -------------------- --------------- ------

Note that we have added `Project` to the list of columns we display,
since the results wouldn't make much sense otherwise.

The other aggregation functions work in the same way. For example, we
can calculate the number of records for each scientist:

~~~~ {src="src/db/agg_count_scientist.sql"}
SELECT   Scientist, COUNT(*)
FROM     Experiments
GROUP BY Scientist;
~~~~

  -------------------- ---
  Dmitri Mendeleev     1
  Ivan Pavlov          2
  Mikhail Lomonosov    2
  Sofia Kovalevskaya   3
  -------------------- ---

We can also sort and aggregate based on grouped and aggregated values.
For example, if we want the total time spent on each project sorted by
project name, we would use:

~~~~ {src="src/db/agg_hours_project_ordered.sql"}
SELECT   Project, SUM(Hours) FROM Experiments
GROUP BY Project
ORDER BY Project ASC;
~~~~

  --------------- ------
  Antigravity     19.5
  Teleportation   25.0
  Time Travel     -9.0
  --------------- ------

The `ORDER BY` clause always goes after the `GROUP BY` clause because we
are ordering the results of aggregation. Putting it another way,
ordering the results before doing the `GROUP BY` wouldn't make any
difference to the final answer, so that's not what SQL does.

What if we want to sort the results by the total number of hours spent?
Instead of using a plain field to sort on, like `Project`, we can use an
aggregation function as our sorting criterion:

~~~~ {src="src/db/agg_hours_order_agg.sql"}
SELECT   Project, SUM(Hours) FROM Experiments
GROUP BY Project
ORDER BY SUM(Hours) ASC;
~~~~

  --------------- ------
  Time Travel     -9.0
  Antigravity     19.5
  Teleportation   25.0
  --------------- ------

This query doesn't sort the results based on a field from the table, but
by the results of aggregating values from that table.

Let's keep going and remove the negative hours for the Time Travel
project before adding things up (since negative times confuse the
payroll department). We can do this by adding a `WHERE` clause to our
query to filter out values we don't want *before* they are grouped and
aggregated:

~~~~ {src="src/db/agg_hours_positive.sql"}
SELECT   Project, SUM(Hours) FROM Experiments
WHERE    Hours >= 0
GROUP BY Project
ORDER BY SUM(Hours) ASC;
~~~~

  --------------- ------
  Antigravity     19.5
  Teleportation   25.0
  --------------- ------

Notice that there isn't a row in the result at all for the Time Travel
project: all of the hours recorded for it were negative, so none of
those records got past the `WHERE` to be summed. Looking more closely,
this query:

1.  selected rows from the table where the `Hours` are non-negative;
2.  grouped those rows into sets that have the same values for
    `Project`;
3.  replaced each group with a single row whose values are the sum of
    the hours in the group, and the project name of the group; and
4.  ordered those rows according to the total hours.

Aggregation is therefore a fourth stage in our query processing pipeline
([Figure XXX](#f:pipeline_aggregate)).

![Four-Stage Query Processing Pipeline](img/db/pipeline_aggregate.png)

### Summary

-   Use aggregation functions like `SUM` `MAX` to combine many query
    results into a single value.
-   Use the `COUNT` function to count the number of results.
-   If some fields are aggregated, and others are not, the database
    manager displays an arbitrary result for the unaggregated field.
-   Use `GROUP BY` to group values before aggregation.

Database Design
---------------

### Learning Objectives:

-   Explain what an atomic value is.
-   Be able to tell whether a value is atomic or not.
-   Explain why fields in database tables should store atomic values.
-   Explain why databases should not store redundant information.
-   Be able to tell whether information is redundant or not.
-   Be able to reorganize database tables to eliminate redundancy.

Let's go back to sorting for a moment, and see if we can produce a list
of scientists ordered by family name. We want our output to look like
this:

  ---------------------
  Kovalevskaya, Sofia
  Lomonosov, Mikhail
  Mendeleev, Dmitri
  Pavlov, Ivan
  ---------------------

This is easy to do in a programming language like Python: we just split
the names on the space character, then join the two parts using a comma
and a space.

    result = []
    for name in list_of_names:
        personal_name, family_name = name.split(' ')
        new_name = family_name + ', ' + personal_name
        result.append(new_name)
    result.sort()

We can do something like this in some dialects of SQL, but not all, and
even when we can, it's harder to read. For example, if we're using
Microsoft SQL Server, the query we need is:

    SELECT SUBSTRING(Scientist, 1, CHARINDEX(Scientist, " ")-1)
           || ", "
           || SUBSTRING(Scientist, CHARINDEX(Scientist, " ")+1, LEN(Scientist))
           FROM Experiments;

Here, `CHARINDEX` and `SUBSTRING` are built-in functions that find the
locations of characters and take substrings respectively, and `||`
concatenates strings. This won't work as written with other databases,
though, since their equivalents of `CHARINDEX` have different names (or,
in the case of SQLite, may not exist at all). And even when it does
work, it's still not a complete solution, since it doesn't sort the
names.

We could get further by using [nested queries](#s:nested), which we will
discuss later in this chapter, but the right solution is to reformulate
the problem. What we're trying to do is difficult because we have
violated one of the fundamental rules of database design. The values in
the `Scientist` field have several parts that we care about; in
technical terms, they are not [atomic
values](glossary.html#atomic-value). In a well-designed database, every
value *is* atomic, so that it can be accessed directly.

Here's what our table looks like when we split names into their
component parts:

  ------------------ ---------------- --------------- -----------
  **Experiments**
  **PersonalName**   **FamilyName**   **Project**     **Hours**
  Sofia              Kovalevskaya     Antigravity     6.5
  Sofia              Kovalevskaya     Teleportation   11.0
  Sofia              Kovalevskaya     Teleportation   5.0
  Mikhail            Lomonosov        Antigravity     4.0
  Mikhail            Lomonosov        Time Travel     -2.0
  Dmitri             Mendeleev        Antigravity     9.0
  Ivan               Pavlov           Teleportation   9.0
  Ivan               Pavlov           Time Travel     -7.0
  ------------------ ---------------- --------------- -----------

It looks like a small change, but it has major implications. First, it
makes the SQL simpler, since we no longer have to do substring
operations to get values:

~~~~ {make="select-distinct-names"}
SELECT DISTINCT FamilyName || ", " || PersonalName FROM Experiments;
~~~~

Second, this SQL will be much more efficient, since repeatedly finding
substrings takes more time than simply matching values directly.

### Why Personal and Family Names?

`PersonalName` and `FamilyName` may seem like odd labels for database
fields: `FirstName` and `LastName` would be shorter. However, the latter
pair of labels assume a cultural convention that isn't true for many
people. In China, Japan, and other East Asian countries, for example,
the family name is usually written first. This may sound like a small
thing, but it's a good habit to get into: when we're designing a
database, we should always think about the meaning of data, rather than
how it is presented.

Our redesigned table still violates an important rule of database
design. To see how, let's look at what happens if we want to store
people's email addresses:

  ------------------ ---------------- ------------------------ --------------- -----------
  **Experiments**
  **PersonalName**   **FamilyName**   **Email**                **Project**     **Hours**
  Sofia              Kovalevskaya     skol@euphoric.edu        Antigravity     6.5
  Sofia              Kovalevskaya     skol@euphoric.edu        Teleportation   11.0
  Sofia              Kovalevskaya     skol@euphoric.edu        Teleportation   5.0
  Mikhail            Lomonosov        mikki@freesci.org        Antigravity     4.0
  Mikhail            Lomonosov        mikki@freesci.org        Time Travel     -2.0
  Dmitri             Mendeleev        mendeleev@euphoric.edu   Antigravity     9.0
  Ivan               Pavlov           pablum@euphoric.edu      Teleportation   9.0
  Ivan               Pavlov           pablum@euphoric.edu      Time Travel     -7.0
  ------------------ ---------------- ------------------------ --------------- -----------

There's a lot of redundancy in this table: every time "Sofia" appears as
a personal name, the family name is always "Kovalevskaya", and the email
address is always "skol@euphoric.edu". If we use this design, we will
have to eliminate duplicates almost every time we run a query, and if
Sofia changes her email address, we will have to update several rows of
the database.

The right way to store this data is to separate information about
scientists from information about experiments, so that no fact is ever
duplicated. We can do this by splitting our table in two:

  ----------------- --------------- ------
  **Experiments**
  skol              Antigravity     6.5
  skol              Teleportation   11.0
  skol              Teleportation   5.0
  mlom              Antigravity     4.0
  mlom              Time Travel     -2.0
  dmen              Antigravity     9.0
  ipav              Teleportation   9.0
  ipav              Time Travel     -7.0
  ----------------- --------------- ------

  ---------------- -------------- --------- ------------------------
  **Scientists**
  skol             Kovalevskaya   Sofia     skol@euphoric.edu
  mlom             Lomonosov      Mikhail   mikki@freesci.org
  dmen             Mendeleev      Dmitri    mendeleev@euphoric.edu
  ipav             Pavlov         Ivan      pablum@euphoric.edu
  ---------------- -------------- --------- ------------------------

Facts about our scientists now appear exactly once, as do the entries
for experiments. The only exception is the two entries for Sofia
Kovalevskaya's hours on the Teleportation project, which was in the
original data. At this point, we should either insist that all the hours
each scientist has spent on a particular project appear in a single
database entry, or document the reasons for having multiple entries
(e.g., because each entry is the hours worked in a single week or
month).

### Summary

-   Each field in a database table should store a single atomic value.
-   No fact in a database should ever be duplicated.

Combining Data
--------------

### Learning Objectives:

-   Explain what primary keys and foreign keys are.
-   Write queries that combine information from two or more tables by
    matching keys.
-   Write queries using aliases for table names.
-   Explain why the `tablename.fieldname` notation is needed when tables
    are joined.
-   Explain the logical sequence of operations that occurs when two or
    more tables are joined.

If we divide our data between several tables, we must have some way to
bring it back together again. The key to doing this is the fact that
both tables have a `PersonID` field, and that the values in these
columns are shared.

Suppose we want to combine all the data from the `Experiments` and
`Scientists` tables. The SQL command to join the two tables is `JOIN`:

~~~~ {src="src/db/join_scientists_experiments.sql"}
SELECT * FROM Scientists JOIN Experiments;
~~~~

which means, "Combine the rows of the `Scientists` table with the rows
of the `Experiments` table and return all of the columns in the result."
The result isn't quite what we want:

  ------ -------------- --------- ------------------------ ------ --------------- ------
  skol   Kovalevskaya   Sofia     skol@euphoric.edu        skol   Antigravity     6.5
  skol   Kovalevskaya   Sofia     skol@euphoric.edu        skol   Teleportation   11.0
  skol   Kovalevskaya   Sofia     skol@euphoric.edu        skol   Teleportation   5.0
  skol   Kovalevskaya   Sofia     skol@euphoric.edu        mlom   Antigravity     4.0
  skol   Kovalevskaya   Sofia     skol@euphoric.edu        mlom   Time Travel     -2.0
  skol   Kovalevskaya   Sofia     skol@euphoric.edu        dmen   Antigravity     9.0
  skol   Kovalevskaya   Sofia     skol@euphoric.edu        ipav   Teleportation   9.0
  skol   Kovalevskaya   Sofia     skol@euphoric.edu        ipav   Time Travel     -7.0
  mlom   Lomonosov      Mikhail   mikki@freesci.org        skol   Antigravity     6.5
  mlom   Lomonosov      Mikhail   mikki@freesci.org        skol   Teleportation   11.0
  mlom   Lomonosov      Mikhail   mikki@freesci.org        skol   Teleportation   5.0
  mlom   Lomonosov      Mikhail   mikki@freesci.org        mlom   Antigravity     4.0
  mlom   Lomonosov      Mikhail   mikki@freesci.org        mlom   Time Travel     -2.0
  mlom   Lomonosov      Mikhail   mikki@freesci.org        dmen   Antigravity     9.0
  mlom   Lomonosov      Mikhail   mikki@freesci.org        ipav   Teleportation   9.0
  mlom   Lomonosov      Mikhail   mikki@freesci.org        ipav   Time Travel     -7.0
  dmen   Mendeleev      Dmitri    mendeleev@euphoric.edu   skol   Antigravity     6.5
  dmen   Mendeleev      Dmitri    mendeleev@euphoric.edu   skol   Teleportation   11.0
  dmen   Mendeleev      Dmitri    mendeleev@euphoric.edu   skol   Teleportation   5.0
  dmen   Mendeleev      Dmitri    mendeleev@euphoric.edu   mlom   Antigravity     4.0
  dmen   Mendeleev      Dmitri    mendeleev@euphoric.edu   mlom   Time Travel     -2.0
  dmen   Mendeleev      Dmitri    mendeleev@euphoric.edu   dmen   Antigravity     9.0
  dmen   Mendeleev      Dmitri    mendeleev@euphoric.edu   ipav   Teleportation   9.0
  dmen   Mendeleev      Dmitri    mendeleev@euphoric.edu   ipav   Time Travel     -7.0
  ipav   Pavlov         Ivan      pablum@euphoric.edu      skol   Antigravity     6.5
  ipav   Pavlov         Ivan      pablum@euphoric.edu      skol   Teleportation   11.0
  ipav   Pavlov         Ivan      pablum@euphoric.edu      skol   Teleportation   5.0
  ipav   Pavlov         Ivan      pablum@euphoric.edu      mlom   Antigravity     4.0
  ipav   Pavlov         Ivan      pablum@euphoric.edu      mlom   Time Travel     -2.0
  ipav   Pavlov         Ivan      pablum@euphoric.edu      dmen   Antigravity     9.0
  ipav   Pavlov         Ivan      pablum@euphoric.edu      ipav   Teleportation   9.0
  ipav   Pavlov         Ivan      pablum@euphoric.edu      ipav   Time Travel     -7.0
  ------ -------------- --------- ------------------------ ------ --------------- ------

When a database does a join, it combines every row of one table with
every row of the other: in mathematical terms, it creates the [cross
product](glossary.html#cross-product) of the sets of rows. It doesn't
try to figure out if those rows have anything to do with each other
because it has no way of knowing whether they do or not—we have to tell
it.

What we want is combinations of rows from the `Scientists` and
`Experiments` tables that refer to the same person, i.e., that have the
same `PersonID` values. To express this in SQL we need to add an `ON`
clause to our query:

~~~~ {make="join-scientists-experiments-on"}
SELECT *
FROM   Scientists JOIN Experiments
ON     Scientists.PersonID = Experiments.PersonID;
~~~~

  ------ -------------- --------- ------------------------ ------ --------------- ------
  skol   Kovalevskaya   Sofia     skol@euphoric.edu        skol   Antigravity     6.5
  skol   Kovalevskaya   Sofia     skol@euphoric.edu        skol   Teleportation   5.0
  skol   Kovalevskaya   Sofia     skol@euphoric.edu        skol   Teleportation   11.0
  mlom   Lomonosov      Mikhail   mikki@freesci.org        mlom   Antigravity     4.0
  mlom   Lomonosov      Mikhail   mikki@freesci.org        mlom   Time Travel     -2.0
  dmen   Mendeleev      Dmitri    mendeleev@euphoric.edu   dmen   Antigravity     9.0
  ipav   Pavlov         Ivan      pablum@euphoric.edu      ipav   Teleportation   9.0
  ipav   Pavlov         Ivan      pablum@euphoric.edu      ipav   Time Travel     -7.0
  ------ -------------- --------- ------------------------ ------ --------------- ------

`ON` is like `WHERE`: it filters things according to some test
condition. More specifically, it filters rows as they are being joined
and only keeps the ones that pass some test.

Note how in the query above we used `TableName.FieldName` to remove any
ambiguity on what is being compared to what. We could do this just as
well *after* joining rows using a `WHERE` clause as a filter:

~~~~ {src="src/db/join_scientists_experiments_where.sql"}
SELECT *
FROM   Scientists JOIN Experiments
WHERE  Scientists.PersonID = Experiments.PersonID;
~~~~

but using `ON` makes it clear that the relationship is being used in the
join. It may also be more efficient, since the database won't construct
rows during the join just to throw them away during the `WHERE`.
However, a good database manager will do that particular optimization
automatically.

We can use the `TableName.FieldName` notation to specify the columns we
want returned by our query. For example, the query below returns the
email addresses of the scientists who have worked on particular
projects:

~~~~ {src="src/db/join_email_project.sql"}
SELECT DISTINCT Experiments.Project, Scientists.Email
FROM            Scientists JOIN Experiments
ON              Scientists.PersonID = Experiments.PersonID;
~~~~

  --------------- ------------------------
  Antigravity     mendeleev@euphoric.edu
  Antigravity     mikki@freesci.org
  Antigravity     skol@euphoric.edu
  Teleportation   pablum@euphoric.edu
  Teleportation   skol@euphoric.edu
  Time Travel     mikki@freesci.org
  Time Travel     pablum@euphoric.edu
  --------------- ------------------------

We can sometimes make long queries more readable by creating
[aliases](glossary.html#alias) for the tables we are joining:

~~~~ {src="src/db/join_using_alias.sql"}
SELECT DISTINCT e.Project, s.Email
FROM            Experiments e JOIN Scientists s
ON              e.PersonID = s.PersonID;
~~~~

Here, we're temporarily using the names `e` and `s` for the
`Experiments` and `Scientists` tables. This produces the same set of
results as before. However, since the database may display rows in any
order it likes, the output from this query and the previous one may not
be textually identical. If we sort them, though, they are guaranteed to
match:

~~~~ {src="src/db/join_and_order.sql"}
SELECT DISTINCT e.Project, s.Email
FROM            Experiments e JOIN Scientists s
ON              e.PersonID = s.PersonID
ORDER BY        e.Project, s.Email;
~~~~

If joining two tables is good, joining multiple tables must be better.
In fact, we can join any number of tables simply by adding more `JOIN`
clauses. To see how this works, let's add two more tables to our
database called `Papers` that keeps track of who co-authored the papers
our group has produced so far:

  ------------- ---------------------
  **Authors**
  skol          antigrav-lit-survey
  skol          teleport-quantum
  mlom          antigrav-lit-survey
  ipav          teleport-quantum
  ------------- ---------------------

  --------------------- ----------------------------------- --------------------
  **Papers**
  **CiteKey**           **Title**                           **Journal**
  antigrav-lit-survey   Antigravity: A Survey               J. Improb. Physics
  teleport-quantum      Quantum Teleportation and Why Not   Quantum Rev. Let.
  --------------------- ----------------------------------- --------------------

Why two tables? Because putting all the information into one would break
the rules we described in the previous section—for example, the paper's
title and journal would appear together in multiple records. What we
have done instead is give each paper a unique citation key (which we
would use in BibTeX or some kind of reference manager), and then combine
it once, and once only, with each author, and with the paper's details.

Let's construct a query to get the full name of the experimenter and the
title of every paper he or she has co-authored. We'll start by writing
down the fields we want:

    SELECT Scientists.PersonalName, Scientists.FamilyName, Papers.Title
    …

These fields are coming from the `Scientists` and `Papers` tables, so we
have to combine those tables with `JOIN`. But how? None of the values in
`Scientists` appear in `Papers`, or vice versa. How can we match records
up?

The solution is to add the `Authors` table to our query.
`Scientists.PersonID` is supposed to match `Authors.PersonID`, and
`Authors.CiteKey` matches `Papers.CiteKey`, so that extra stage lets us
combine people and papers. Our query now looks like this:

~~~~ {src="src/db/join_three.sql"}
SELECT Scientists.PersonalName, Scientists.FamilyName, Papers.Title
FROM   Scientists JOIN Authors JOIN Papers
ON     (Scientists.PersonID = Authors.PersonID) AND (Authors.CiteKey = Papers.CiteKey);
~~~~

  --------- -------------- -----------------------------------
  Sofia     Kovalevskaya   Antigravity: A Survey
  Sofia     Kovalevskaya   Quantum Teleportation and Why Not
  Mikhail   Lomonosov      Antigravity: A Survey
  Ivan      Pavlov         Quantum Teleportation and Why Not
  --------- -------------- -----------------------------------

The technical terms for the concepts we have been using in this section
are [primary key](glossary.html#primary-key) and [foreign
key](glossary.html#foreign-key). A primary key is a value, or
combination of values, that uniquely identifies each row in a table. For
example, the primary key for the `Scientists` table is `PersonID`: if
two records ever have the same value for this, something has probably
gone wrong.

A foreign key is a value (or combination of values) from one table that
identifies a unique record in another table. Another way of saying this
is that a foreign key is the primary key of one table that appears in
some other table. In our database, `Experiments.PersonID` is a foreign
key into the `Scientists` table.

What is the primary key for the `Experiments` table? If there was only
one entry pairing `skol` with `Teleportation`, then that pair would be
the primary key. As it is, we can't even be sure that using all three
fields will be unique, since there could, for example, be two entries
saying that `dmen` spent 6.5 hours working on antigravity.

Most database designers believe that every table should have a
well-defined primary key. (If nothing else, this allows us to print or
delete specific records.) If the entries in `Experiments` are monthly
totals, we should include the month in the table (and the year as well,
so that we don't wind up with multiple entries for each month after a
few years running the lab).

Alternatively, we could create an arbitrary, unique ID for each record
as we add it to the database. This is actually very common: those IDs
have names like "student numbers" and "patient numbers", and they almost
always turn out to have originally been a unique record identifier in
some database system or other. As the query below demonstrates, SQLite
automatically numbers records as they're added to tables, and we can use
those record numbers in queries:

~~~~ {src="src/db/select_rowid.sql"}
SELECT ROWID, * FROM Experiments;
~~~~

  --- ------ --------------- ------
  1   skol   Antigravity     6.5
  2   skol   Teleportation   11.0
  3   skol   Teleportation   5.0
  4   mlom   Antigravity     4.0
  5   mlom   Time Travel     -2.0
  6   dmen   Antigravity     9.0
  7   ipav   Teleportation   9.0
  8   ipav   Time Travel     -7.0
  --- ------ --------------- ------

### Summary

-   Use `JOIN` to create all possible combinations of records from two
    or more tables.
-   Use `JOIN tables ON test` to keep only those combinations that pass
    some test.
-   Use `table.field` to specify a particular field of a particular
    table.
-   Use aliases to make queries more readable.
-   Every record in a table should be uniquely identified by the value
    of its primary key.

Self Join
---------

### Learning Objectives:

-   Explain what a self-join is and give examples of when self-joins are
    useful.

One special case of joining tables comes up so often that it has its own
name: [self join](glossary.html#self-join). As the name suggests, this
means joining a table with itself. To see why this is useful, let's try
to find out how many scientists have worked on two or more projects. Our
first guess looks like this:

~~~~ {src="src/db/self_join_incorrect.sql"}
SELECT PersonID, COUNT(*) FROM Experiments GROUP BY PersonID WHERE COUNT(*) > 1;
~~~~

but that's not legal SQL—we can't use an aggregated value in our `WHERE`
clause, because `WHERE` is applied row-by-row before aggregation
happens.

Instead, let's join the `Experiments` table to itself. We will give each
copy of the table an alias, so that we can tell which values came from
which copy:

~~~~ {src="src/db/self_join_all.sql"}
SELECT * FROM Experiments a JOIN Experiments b;
~~~~

The result has 64 rows, a few of which are shown below:

  ---------------- --------------- ------------- ---------------- --------------- -------------
  **a.PersonID**   **a.Project**   **a.Hours**   **b.PersonID**   **b.Project**   **b.Hours**
  skol             Antigravity     6.5           skol             Antigravity     6.5
  skol             Antigravity     6.5           skol             Teleportation   11.0
  skol             Antigravity     6.5           skol             Teleportation   5.0
  skol             Antigravity     6.5           mlom             Antigravity     4.0
  skol             Antigravity     6.5           mlom             Time Travel     -2.0
  skol             Antigravity     6.5           dmen             Antigravity     9.0
  skol             Antigravity     6.5           ipav             Teleportation   9.0
  skol             Antigravity     6.5           ipav             Time Travel     -7.0
  skol             Teleportation   11.0          skol             Antigravity     6.5
  skol             Teleportation   11.0          skol             Teleportation   11.0
  …                …               …             …                …               …
  mlom             Antigravity     4.0           skol             Antigravity     6.5
  mlom             Antigravity     4.0           skol             Teleportation   11.0
  …                …               …             …                …               …
  ---------------- --------------- ------------- ---------------- --------------- -------------

Now let's add a `WHERE` clause to filter out rows that have different
`PersonID` values, i.e., where we have joined information about one
person with information about another:

~~~~ {src="src/db/self_join_personid.sql"}
SELECT * FROM Experiments a JOIN Experiments b WHERE a.PersonID = b.PersonID;
~~~~

  ---------------- --------------- ------------- ---------------- --------------- -------------
  **a.PersonID**   **a.Project**   **a.Hours**   **b.PersonID**   **b.Project**   **b.Hours**
  skol             Antigravity     6.5           skol             Antigravity     6.5
  skol             Antigravity     6.5           skol             Teleportation   5.0
  skol             Antigravity     6.5           skol             Teleportation   11.0
  skol             Teleportation   11.0          skol             Antigravity     6.5
  skol             Teleportation   11.0          skol             Teleportation   5.0
  skol             Teleportation   11.0          skol             Teleportation   11.0
  skol             Teleportation   5.0           skol             Antigravity     6.5
  skol             Teleportation   5.0           skol             Teleportation   5.0
  skol             Teleportation   5.0           skol             Teleportation   11.0
  mlom             Antigravity     4.0           mlom             Antigravity     4.0
  mlom             Antigravity     4.0           mlom             Time Travel     -2.0
  mlom             Time Travel     -2.0          mlom             Antigravity     4.0
  mlom             Time Travel     -2.0          mlom             Time Travel     -2.0
  dmen             Antigravity     9.0           dmen             Antigravity     9.0
  ipav             Teleportation   9.0           ipav             Teleportation   9.0
  ipav             Teleportation   9.0           ipav             Time Travel     -7.0
  ipav             Time Travel     -7.0          ipav             Teleportation   9.0
  ipav             Time Travel     -7.0          ipav             Time Travel     -7.0
  ---------------- --------------- ------------- ---------------- --------------- -------------

Now let's add another clause to our `WHERE` to get rid of records where
the two project names are the same:

~~~~ {src="src/db/self_join_project.sql"}
SELECT * FROM Experiments a JOIN Experiments b
WHERE (a.PersonID = b.PersonID) AND (a.Project != b.Project);
~~~~

  ------ --------------- ------ ------ --------------- ------
  skol   Antigravity     6.5    skol   Teleportation   5.0
  skol   Antigravity     6.5    skol   Teleportation   11.0
  skol   Teleportation   11.0   skol   Antigravity     6.5
  skol   Teleportation   5.0    skol   Antigravity     6.5
  mlom   Antigravity     4.0    mlom   Time Travel     -2.0
  mlom   Time Travel     -2.0   mlom   Antigravity     4.0
  ipav   Teleportation   9.0    ipav   Time Travel     -7.0
  ipav   Time Travel     -7.0   ipav   Teleportation   9.0
  ------ --------------- ------ ------ --------------- ------

This may not seem like progress, but we have almost answered our
original question. Each of these records represents the fact that some
person has worked on two different projects. Putting it another way, if
someone has only ever worked on one project (or hasn't worked on any
projects at all), their ID will not appear in any record in this set. To
get the list of names of people who have worked on two or more projects,
therefore, all we have to do is display either `a.PersonID` or
`b.PersonID` (and eliminate duplicates using `DISTINCT`). We will split
our final query across several lines to make it easier to read, and use
an `ORDER BY` to ensure that our results are sorted:

~~~~ {src="src/db/self_join_final.sql"}
SELECT DISTINCT a.PersonID
FROM            Experiments a JOIN Experiments b
WHERE           (a.PersonID = b.PersonID) AND (a.Project != b.Project)
ORDER BY        a.PersonID ASC;
~~~~

  ------
  ipav
  mlom
  skol
  ------

If you hang around programmers long enough, you will eventually hear
someone call this trick "intuitive". They are using that word the way
certain mathematicians use "obvious": it means, "You only have to read
the proof a couple of times to get it." There actually is a rich
mathematical theory underneath SQL, and if you immerse yourself in that
theory, tricks like joining a table to itself do eventually seem
obvious. For the rest of us, though, it's enough to learn this pattern
and recognize when it should be used.

### Summary

-   Use a self join to combine a table with itself.

Missing Data
------------

### Learning Objectives:

-   Explain what databases use the special value `NULL` to represent.
-   Explain why databases should *not* uses their own special values
    (like 9999 or "N/A") to represent missing or unknown data.
-   Explain what atomic and aggregate calculations involving `NULL`
    produce, and why.
-   Write queries that include or exclude records containing `NULL`.

In the real world data is not always complete—there are always holes. A
database uses a special value for these holes: `NULL`. `NULL` is not
zero, `False`, or the empty string: it is a one-of-a-kind value that
means "nothing here". Dealing with `NULL` requires a few special tricks,
and sometimes some careful thinking.

As an example, here is our `Experiments` table with a few times replaced
by `NULL`:

  ------ --------------- ------
  skol   Antigravity     6.5
  skol   Teleportation   NULL
  skol   Teleportation   5.0
  mlom   Antigravity     4.0
  mlom   Time Travel     NULL
  dmen   Antigravity     9.0
  ipav   Teleportation   9.0
  ipav   Time Travel     NULL
  ------ --------------- ------

These `NULL`s might represent values that were missing, that haven't
been entered yet, or that someone erased them because they looked
suspicious. We can't tell just by looking at the data, but we *do* have
to take these missing values into account when writing queries.

### Displaying NULL

Different databases display NULL values differently. For example,
SQLite's default is to print a blank, so that the data above is actually
shown as:

    |skol|Antigravity|6.5|
    |skol|Teleportation||
    |skol|Teleportation|5.0|
    |mlom|Antigravity|4.0|
    |mlom|Time Travel||
    |dmen|Antigravity|9.0|
    |ipav|Teleportation|9.0|
    |ipav|Time Travel||

This format makes it easy to overlook NULLs, particularly if they're in
the middle of a long row.

Let's start by finding out which experiments are missing `Hours` data.
The natural thing to try is:

~~~~ {src="src/db/select_null_equal_error.sql"}
SELECT * FROM Experiments WHERE Hours = NULL;
~~~~

but it produces no results. The reason is that `NULL` cannot be compared
to anything else. It cannot be added to anything, either; in fact,
anything combined with NULL, using any operator, is NULL. This means
that our `WHERE` is always false, so no records are selected.

Notice that the opposite test also fails: if we select rows where
`Hours` is *not* equal to `NULL`, we still don't get any rows because
once again the comparison always fails:

~~~~ {src="src/db/select_null_not_equal_error.sql"}
SELECT * FROM Experiments WHERE Hours != NULL;
~~~~

To check whether a value is `NULL` or not, we must use the special
`IS NULL` operator:

~~~~ {src="src/db/select_null.sql"}
SELECT * FROM Experiments WHERE Hours IS NULL;
~~~~

  ------ --------------- ------
  skol   Teleportation   NULL
  mlom   Time Travel     NULL
  ipav   Time Travel     NULL
  ------ --------------- ------

To find all of the rows that do *not* have a `NULL`, we use
`IS NOT NULL`:

~~~~ {src="src/db/select_not_null.sql"}
SELECT * FROM Experiments WHERE Hours IS NOT NULL;
~~~~

  ------ --------------- -----
  skol   Antigravity     6.5
  skol   Teleportation   5.0
  mlom   Antigravity     4.0
  dmen   Antigravity     9.0
  ipav   Teleportation   9.0
  ------ --------------- -----

`NULL` causes headaches wherever it appears. For example, suppose we
want to find the all of the experiments that didn't take exactly nine
hours to do. It is natural to write:

~~~~ {src="src/db/select_not_nine_hours.sql"}
SELECT * FROM Experiments WHERE Hours != 9.0;
~~~~

  ------ --------------- -----
  skol   Antigravity     6.5
  skol   Teleportation   5.0
  mlom   Antigravity     4.0
  ------ --------------- -----

but this query filters out all the records that have `NULL` hours as
well as those that took something other than one hour. Once again, the
reason is that when `Hours` is `NULL`, the `!=` comparison fails. If we
want to keep the rows that have `NULL` `Hours`, we need to add an
explicit check using `IS`:

~~~~ {src="src/db/select_not_nine_hours_keep_null.sql"}
SELECT * FROM Experiments WHERE (Hours != 9.0) OR (Hours IS NULL);
~~~~

  ------ --------------- -----
  skol   Antigravity     6.5
  skol   Teleportation    
  skol   Teleportation   5.0
  mlom   Antigravity     4.0
  mlom   Time Travel      
  ipav   Time Travel      
  ------ --------------- -----

This query really does exclude only those records marked as taking one
hour. It's up to use to decide if this is the right thing to do or not
based on how we're going to use the query's results, but this technique
gives us the choice.

`NULL` also needs careful handling when we are aggregating. Most
aggregation functions skip `NULL` values in their calculations. For
example, the query:

~~~~ {src="src/db/select_sum_hours_null.sql"}
SELECT SUM(Hours) FROM Experiments;
~~~~

  ------
  33.5
  ------

adds up everyone's hours, skipping the `NULL`s. This might seem like a
sensible default behavior, but consider what happens when we calculate
an average with:

~~~~ {src="src/db/select_avg_hours_null.sql"}
SELECT AVG(Hours) FROM Experiments;
~~~~

  -----
  6.7
  -----

Once again, `NULL` values have not been included, so this average is the
sum of the five actual values we have, divided by five, rather than the
sum divided by the number of experiments—i.e., it does *not* treat the
`NULL` values as contributing zero to the total. Again, it's up to us to
decide whether this is the right behavior or not.

### Summary

-   Use `NULL` in place of missing information.
-   Almost every operation involving `NULL` produces `NULL` as a result.
-   Test for nulls using `IS NULL` and `IS NOT NULL`.
-   Most aggregation functions skip nulls when combining values.

Nested Queries
--------------

### Learning Objectives:

-   Write queries whose results are used as input by other queries.
-   Explain why the "obvious" way to calculate negative results is
    usually wrong.
-   Write queries that calculate negative results correctly.

Let's switch back to the `Experiments` table that doesn't contain
`NULL`s. How do we find scientists who have *not* been working on time
travel? Our first guess might be:

~~~~ {src="src/db/select_not_time_travel_flawed.sql"}
SELECT DISTINCT PersonID FROM Experiments WHERE Project != "Time Travel";
~~~~

Unfortunately, this doesn't give us what we want. `ivan` and `skol` have
both worked both on Time Travel, but show up in the results:

  ------
  dmen
  ipav
  mlom
  skol
  ------

Let's think this through. There are scientists who have worked on Time
Travel, scientists who have only worked on other projects, and
scientists who have done both. Our query returns all of the scientists
who have worked on projects other than Time Travel, but that includes
ones who have worked on Time Travel *and* other projects ([Figure
XXX](#f:venn_time_travel)).

![Scientists and Time Travel](img/db/venn_time_travel.png)

The trick to answering this question—and it *is* a trick—is to subtract
those scientists who *have* worked on Time Travel (i.e., the ones we
*don't* want) from the set of all scientists. To do this, we will need
to use a [nested query](glossary.html#nested-query) (also called a
[subquery](glossary.html#subquery)).

Let's work up to it in stages. Finding all of the scientists is easy:

    SELECT DISTINCT PersonID FROM Experiments;

If we knew in advance which scientists we didn't want, we could use
`NOT IN` to subtract a fixed set, like this:

    SELECT DISTINCT PersonID FROM Experiment WHERE PersonID NOT IN ('ivan', 'skol');

We don't actually know which scientists who have worked on Time Travel,
but we can generate it with this query:

~~~~ {src="src/db/time_travel_subquery.sql"}
SELECT DISTINCT PersonID FROM Experiment WHERE Project = "Time Travel";
~~~~

What we want to do is somehow use the result of the second query in the
first. SQL allows us to do exactly this, i.e., to nest one query inside
another so that we can use the results of the nested query in the filter
conditions of the main query. Here's what it looks like:

~~~~ {src="src/db/select_nested_subtract.sql"}
SELECT DISTINCT PersonID FROM Experiments WHERE PersonID NOT IN
       (SELECT DISTINCT PersonID FROM Experiments WHERE Project = "Time Travel");
~~~~

  ------
  dmen
  skol
  ------

We can read this query as saying, "Fetch all of the scientists who have
done experiments, except for the ones that appear in the list of
scientists who have worked on Time Travel". It isn't intuitive, but the
pattern is easy to learn, and very useful.

Nested queries can also be used as if they were tables in their own
right. For example, suppose we want to know how many different projects
each scientist has worked on. We can begin by finding the distinct list
of projects for scientist like this:

    SELECT DISTINCT PersonID, Project FROM Experiments;

Now we want to count how many results there are for each scientist.
Since counting is an aggregation, we need to use the results of this
query as input for another query that does the aggregation. We can do
this by wrapping the first query in parentheses and putting it in the
`FROM` clause of the second query:

    …
    FROM (SELECT DISTINCT PersonID, Project FROM Experiments);

The next step is to write the outer query. We want the scientist, and
count of their projects:

    SELECT PersonID, COUNT(*)
    FROM   (SELECT DISTINCT PersonID, Project FROM Experiments);

and since we want the count for each scientists, we have to add a
`GROUP BY` for the outer query. The whole thing is therefore:

~~~~ {src="src/db/nested_query_group_by.sql"}
SELECT   PersonID, COUNT(*)
FROM     (SELECT DISTINCT PersonID, Project FROM Experiments)
GROUP BY PersonID;
~~~~

  ------ ---
  dmen   1
  ipav   2
  mlom   2
  skol   2
  ------ ---

Nesting queries like this is really useful if the data we want isn't
present in exactly the right form in the database. We can use one query
to get the data in the form we need it in, and then wrap another query
around it to get the answer we originally wanted.

### Summary

-   Use nested queries to create temporary sets of results for further
    querying.
-   Use nested queries to subtract unwanted results from all results to
    leave desired results.

Creating and Modifying Tables
-----------------------------

### Understand:

-   Write queries that create database tables with fields of common
    types.
-   Write queries that specify the primary and foreign key relationships
    of tables.
-   Write queries that specify whether field values must be unique
    and/or are allowed to be `NULL`.
-   Write queries that erase database tables.
-   Write queries that add records to database tables.
-   Write queries that delete specific records from tables.
-   Explain why it's important to be careful when deleting records from
    tables.
-   Explain what referential integrity is, and how a database can become
    inconsistent as data is changed.

We have only looked at how to get information out of a database so far,
both because that is more frequent than adding information, and because
most other operations only make sense once queries are understood. If we
want to create and modify data, we need to know two other pairs of
commands.

The first pair are `CREATE TABLE` and `DROP TABLE`. While they are
written as two words, they are actually single commands. The first one
creates a new table; its arguments are the names and types of the
table's columns. For example, the following statements create the four
tables in our experiments database:

~~~~ {src="src/db/create_tables.sql"}
CREATE TABLE Experiments(PersonID TEXT, Project TEXT, Hours REAL);
CREATE TABLE Scientists(PersonID TEXT, FamilyName TEXT, PersonalName TEXT, Email TEXT);
CREATE TABLE Authors(PersonID TEXT, CiteKey TEXT);
CREATE TABLE Papers(CiteKey TEXT, Title TEXT, Journal TEXT);
~~~~

and we can get rid of one of our tables using:

~~~~ {src="src/db/drop_tables.sql"}
DROP TABLE Experiments;
~~~~

Be very careful when doing this: most databases have some support for
undoing changes, but it's better not to have to rely on it.

Different database systems support different data types for table
columns, but most provide the following:

  ----------- -----------------------------------------------------------
  `INTEGER`   A signed integer.
  `REAL`      A floating point value.
  `TEXT`      A string.
  `BLOB`      Any "binary large object" such as an image or audio file.
  ----------- -----------------------------------------------------------

Most databases also support Booleans and date/time values; SQLite uses
the integers 0 and 1 for the former, and represents the latter either as
numbers or as strings in the format YYYY-MM-DD HH:MM:SS.SSS. An
increasing number of databases also support geographic data types, such
as latitude and longitude. Keeping track of what particular systems do
or do not offer, and what names they give different data types, is yet
another portability headache.

What may be more interesting is the fact that we can specify properties
and constraints for columns when creating a table. For example, a better
definition for the `Scientists` table would be:

~~~~ {src="src/db/create_constraints.sql"}
CREATE TABLE Scientists(
    PersonID     TEXT PRIMARY KEY,        -- uniquely identifies entries
    FamilyName   TEXT NOT NULL,           -- must have value
    PersonalName TEXT NOT NULL,           -- ditto
    Email        TEXT UNIQUE              -- no duplicates
);
~~~~

Constraints are declared after the type name; once again, exactly which
ones are available, and what they're called, depends on which database
manager we are using. (And note that we are finally commenting our SQL
using `--`, which we should have been doing all along.)

Once tables have been created, we can add and remove records using our
other pair of commands, `INSERT` and `DELETE`. The simplest form of
`INSERT` statement lists values in order:

~~~~ {src="src/db/simple_insert.sql"}
INSERT INTO Scientists VALUES("skol", "Kovalevskaya", "Sofia", "skol@euphoric.edu");
INSERT INTO Scientists VALUES("mlom", "Lomonosov", "Mikhail", "mikki@freesci.org");
INSERT INTO Scientists VALUES("dmen", "Mendeleev", "Dmitri", "mendeleev@euphoric.edu");
INSERT INTO Scientists VALUES("ipav", "Pavlov", "Ivan", "pablum@euphoric.edu");
~~~~

We can also insert values into one table directly from another:

~~~~ {src="src/db/insert_from_query.sql"}
CREATE TABLE JustEmail(PersonID TEXT, Email TEXT);
INSERT INTO JustEmail SELECT PersonId, Email FROM Scientists;
~~~~

Deleting records can be a bit trickier, because we have to ensure that
the database remains internally consistent. If all we care about is a
single table, we can use the `DELETE` command with a `WHERE` clause that
matches the records we want to discard. For example, if Dmitri Mendeleev
leaves our lab, we can remove him from the `Scientists` table like this:

~~~~ {src="src/db/simple_delete.sql"}
DELETE FROM Scientists WHERE PersonID = "dmen";
~~~~

But now we have a problem—a potentially catastrophic one. Our
`Experiments` table still contains a record recording the fact that
Dmitri spent nine hours working on the Antigravity project:

    SELECT * FROM Experiments WHERE PersonID = "dmen";

  ------ ------------- -----
  dmen   Antigravity   9.0
  ------ ------------- -----

That's never supposed to happen: `Experiments.PersonID` is a foreign key
into the `Scientists` table, and all our queries assume there will be a
row in the latter matching every value in the former.

This problem is called [referential
integrity](glossary.html#referential-integrity): we need to ensure that
all references between tables can always be resolved correctly. One
solution, if our database supports it, is to use a [cascading
delete](glossary.html#cascading-delete), so that when a record in one
table is deleted, the database automatically deletes other records that
refer to it. However, this technique is outside the scope of this
chapter.

### Summary

-   Use `CREATE TABlE name(...)` to create a table.
-   Use `DROP TABLE name` to erase a table.
-   Specify field names and types when creating tables.
-   Specify `PRIMARY KEY`, `NOT NULL`, and other constraints when
    creating tables.
-   Use `INSERT INTO table VALUES(...)` to add records to a table.
-   Use `DELETE FROM table WHERE test` to erase records from a table.
-   Maintain referential integrity when creating or deleting
    information.

Transactions
------------

### Learning Objectives:

-   Explain what a race condition is.
-   Explain why database operations sometimes have to be grouped
    together to ensure correct behavior.
-   Write queries that group operations together in transactions.
-   Explain what it means to commit a transaction.

Let's look at another problem. Suppose we have another table that shows
which pieces of equipment have been borrowed by which scientists:

  --------------- -------------------------
  **Equipment**
  **PersonID**    **EquipmentID**
  skol            CX-211 oscilloscope
  skol            Greenworth balance
  mlom            Cavorite damping plates
  --------------- -------------------------

(We should actually give each piece of equipment a unique ID, and use
that ID here instead of the full name, just as we created a separate
table for scientists earlier in this chapter, but we will bend the rules
for now.) If Sofia Kovalevskaya gives the oscilloscope to Ivan Pavlov,
we need to execute two statements to update this table:

    DELETE FROM Equipment WHERE PersonID = "skol" and EquipmentID = "CX-211 oscilloscope";
    INSERT INTO Equipment VALUES("ipav", "CX-211 oscilloscope");

This is all fine—unless our program or our database happen to crash
between the first statement and the second. If that happens, the
`Equipment` table won't have a record for the oscilloscope at all. Such
a crash may seem unlikely, but remember: if a computer can do two
billion operations per second, that means there are two billion
opportunities every second for something to go wrong. And if our
operations take a long time to complete—as they will when we are working
with large datasets, or when the database is being heavily used—the odds
of failure increase.

What we really want is a way to ensure that every operation is
[ACID](glossary.html#acid): [atomic](glossary.html#atomic-operation)
(i.e. indivisible), consistent, isolated, and durable. The precise
meanings of these terms doesn't matter; what does is the notion that
every logical operation on the database should either run to completion
as if nothing else was going on at the same time, or fail without having
any effect at all.

The tool we use to ensure that this happens is called a
[transaction](glossary.html#transaction). Here's how we should actually
write the statements to move the oscilloscope from one person to
another:

~~~~ {src="src/db/simple_transaction.sql"}
BEGIN TRANSACTION;
DELETE FROM Equipment WHERE PersonID = "skol" and EquipmentID = "CX-211 oscilloscope";
INSERT INTO Equipment VALUES("ipav", "CX-211 oscilloscope");
END TRANSACTION;
~~~~

When we do this, the database manager treats everything in the
transaction as one large statement. If anything goes wrong inside, then
none of the changes made in the transaction will actually be written to
the database—it will be as if the transaction had never happened.
Changes are only stored permanently when we
[commit](glossary.html#commit) them at the end of the transaction.

### Transactions and Commits

We first used the term "transaction" in [our discussion of version
control](svn.html#b:basics:transaction). That's not a coincidence:
behind the scenes, tools like Subversion are using many of the same
algorithms as database managers to ensure that either everything happens
consistently or nothing happens at all. We [use the term
"commit"](svn.html#a:commit) for the same reason: just as our changes to
local files aren't written back to the version control repository until
we commit them, our (apparent) changes to a database aren't written to
disk until we say so.

Transactions serve another purpose as well. Suppose we have decided that
the `Experiments` table will store the total number of hours that each
scientist has worked on each project. At one point in time, there are
two records for Mikhail Lomonosov:

  ------ ------------- ------
  mlom   Antigravity   4.0
  mlom   Time Travel   -2.0
  ------ ------------- ------

Late one Friday afternoon, Mikhail remembers that he forgot to add three
hours to his time on the Antigravity project. He uses these two
statements:

~~~~ {src="src/db/update_mlom_hours.sql"}
UPDATE Experiments
  SET Hours = 3.0 + (SELECT Hours FROM Experiments WHERE PersonID = "mlom" and Project = "Antigravity")
WHERE PersonID = "mlom" and Project = "Antigravity";
~~~~

The inner select gets the old value for Mikhail's hours; the outer
`UPDATE` adds 3.0 to that and writes the result back to the database.

At the same moment as Mikhail runs his command, though, Dmitri Mendeleev
decides to add six hours to Mikhail's time on the project in recognition
of the work he did putting a poster together for a conference. His
command looks exactly the same as the one above, except he adds 6.0
instead of 3.0.

After both operations have completed, the database should show that
Mikhail has spent 13 hours working on antigravity (the 4.0 we started
with, plus the 3.0 that he added, plus 6.0 more that Dmitry added).
However, there is a small chance that it won't. To see why, let's break
the two queries into their respective read and write steps and place
them side by side:

  --------------------------------------------------- ---------------------------------------------------
  `X = read Experiments("mlom", "Antigravity")`       `Y = read Experiments("mlom", "Antigravity")`
  `write Experiments("mlom", "Antigravity", X+3.0)`   `write Experiments("mlom", "Antigravity", Y+6.0)`
  --------------------------------------------------- ---------------------------------------------------

The database can only actually do one thing at once, so it must put
these four operations into some sequential order. That order has to
respect the original order within each column, but the database can
interleave the two columns any way it wants. If it orders them like
this:

  ---------------------------------------------------
  `X = read Experiments("mlom", "Antigravity")`
  `write Experiments("mlom", "Antigravity", X+3.0)`
  `Y = read Experiments("mlom", "Antigravity")`
  `write Experiments("mlom", "Antigravity", Y+6.0)`
  ---------------------------------------------------

then all is well: the final value in the database is 13.0. But what if
it interleaves the operations like this:

  ---------------------------------------------------
  `X = read Experiments("mlom", "Antigravity")`
  `Y = read Experiments("mlom", "Antigravity")`
  `write Experiments("mlom", "Antigravity", X+3.0)`
  `write Experiments("mlom", "Antigravity", Y+6.0)`
  ---------------------------------------------------

This ordering puts the initial value, 4.0, into both `X` and `Y`. It
then writes 7.0 back to the database (the third statement), and then
writes 10.0, since `Y` holds 4.0 and we're adding 6.0 to it.

This is called a [race condition](glossary.html#race-condition), since
the final result depends on a race between the two operations. Race
conditions are part of what makes parallel programming such a nightmare:
they are difficult to spot in advance (since they are caused by the
interactions between components, rather than by anything in any one of
those components), and can be almost impossible to debug (since they
usually occur intermittently and infrequently).

Transactions come to our rescue once again. If both users put their
statements in transactions, the database will act as if it executed all
of one and then all of the other. Whether or not it actually does this
is up to whoever wrote the database program itself: modern databases use
very sophisticated algorithms to determine which operations actually
have to be run sequentially, and which can safely be run in parallel to
improve performance.

### Summary

-   Place operations in a transaction to ensure that they appear to be
    atomic, consistent, isolated, and durable.

Programming With Databases
--------------------------

### Understand:

-   Write a Python program that connects to a database, issues a query,
    and processes the results.
-   Explain what an SQL injection attack is.
-   Write a program that safely interpolates values into queries.

To end this chapter, let's have a look at how to access a database from
a general-purpose programming language like Python. Other languages use
almost exactly the same model: library and function names may differ,
but the concepts are the same.

Here's a short Python program that selects scientists' IDs and email
addresses from an SQLite database stored in a file called `lab.db`:

    import sqlite3                                                  # 0
                                                                    # 1
    connection = sqlite3.connect("lab.db")                          # 2
    cursor = connection.cursor()                                    # 3
    cursor.execute("SELECT PersonID, Email FROM Scientists;")       # 4
    results = cursor.fetchall();                                    # 5
    for r in results:                                               # 6
        print r                                                     # 7
    cursor.close();                                                 # 8
    connection.close();                                             # 9
    (u'skol', u'skol@euphoric.edu')
    (u'mlom', u'mikki@freesci.org')
    (u'dmen', u'mendeleev@euphoric.edu')
    (u'ipav', u'pablum@euphoric.edu')

The program starts by importing the `sqlite3` library. If we were
connecting to MySQL, DB2, or some other database, we would import a
different library, but all of them provide the same functions, so that
the rest of our program does not have to change (at least, not much) if
we switch from one database to another.

Line 2 establishes a connection to the database. Since we're using
SQLite, all we need to specify is the name of the database file. Other
systems may require us to provide a username and password as well. Line
3 then uses this connection to create a [cursor](glossary.html#cursor).
Just like the cursor in an editor, its role is to keep track of where we
are in the database.

On line 4, we use that cursor to ask the database to execute a query for
us. The query is written in SQL, and passed to `cursor.execute` as a
string. It's our job to make sure that SQL is properly formatted; if it
isn't, or if something goes wrong when it is being executed, the
database will report an error.

The database returns the results of the query to us in response to the
`cursor.fetchall` call on line 5. This result is a list with one entry
for each record in the result set; if we loop over that list (line 6)
and print those list entries (line 7), we can see that each one is a
tuple with one element for each field we asked for.

Finally, lines 8 and 9 close our cursor and our connection, since the
database can only keep a limited number of these open at one time. Since
establishing a connection takes time, though, we shouldn't open a
connection, do one operation, then close the connection, only to reopen
it a few microseconds later to do another operation. Instead, it's
normal to create one connection that stays open for the lifetime of the
program.

### What Are The u's For?

You may have noticed that each of the strings in our output has a
lower-case 'u' in front of it. That is Python's way of telling us that
the string is stored in [Unicode](glossary.html#unicode), which is used
to handle characters beyond the A-Z and 0-9 used in most English words.

Let's have another look at the query on line 4. In real life, queries
will often depend on values from a program's user. For example, our
program might read a list of user IDs and project names and display the
hours those people have spent on those projects. It is tempting to write
that program like this:

    import sys, sqlite3

    statement = '''SELECT PersonID, Project, Hours
    FROM Experiments
    WHERE PersonID = "%s" and Project = "%s";
    '''

    connection = sqlite3.connect("lab.db")
    cursor = connection.cursor()
    for line in sys.stdin:
        person, project = line.split(' ', 1)
        s = statement % (person, project)
        cursor.execute(s)
        results = cursor.fetchall();
        for r in results:
            print r
    cursor.close()
    connection.close()

The variable `statement` holds the statement we want to execute, with
`%s` format strings where we want to insert the hours, the person's ID,
and the name of the project. Each time we read a line from standard
input, we split it into two pieces at the first space, then create a new
string based on `statement` that includes them. For example, if we read
in the line:

    mlom Antigravity

we use these two values to fill in our query, which becomes:

    SELECT PersonID, Project, Hours
    FROM Experiments
    WHERE PersonID = "mlom" and Project = "Antigravity";

But what happens if someone gives the program this input?

    mlom Antigravity"; DROP TABLE Scientists;

It looks like there's garbage after the name of the project, but it is
very carefully chosen garbage. Everything from the word "Antigravity" to
the end of the line will be inserted into our query, making it:

    SELECT PersonID, Project, Hours
    FROM Experiments
    WHERE PersonID = "mlom" and Project = "Antigravity"; DROP TABLE  Scientists;

The double quote and semicolon at the end of the input end the `SELECT`
statement; the rest of the input then puts a `DROP TABLE` statement in
our query. If we run this, it will erase one of the tables in our
database.

This technique is called [SQL injection](glossary.html#sql-injection),
and it has been used to attack thousands of programs over the years. In
particular, many web sites that take data from users insert values
directly into queries without checking them carefully first.

Since a villain might try to smuggle commands into our queries in many
different ways, the safest way to deal with this threat is to replace
characters like quotes with their escaped equivalents, so that we can
safely put whatever the user gives us inside a string. We can do this by
using a [prepared statement](glossary.html#prepared-statement) instead
of formatting our statements as strings. Here's what our example program
looks like if we do this:

    import sys, sqlite3

    statement = '''
    SELECT PersonID, Project, Hours
    FROM Experiments
    WHERE PersonID = ? and Project = ?;
    '''

    connection = sqlite3.connect("lab.db")
    cursor = connection.cursor()
    for line in sys.stdin:
        person, project = line.strip().split(' ', 1)
        cursor.execute(statement, (person, project))
        results = cursor.fetchall();
        for r in results:
            print r
    cursor.close()
    connection.close()

The key changes are in the query template string `statement`, and the
`execute` call inside the loop. Instead of formatting the query
ourselves, we put question marks in the query template where we want to
insert values. When we call `execute`, we provide a tuple as a second
argument that contains exactly as many values as there are question
marks in the template. The library matches values to question marks in
order, and translates any special characters in the values into their
escaped equivalents so that they are safe to use.

### Summary

-   Most applications that use databases embed SQL in a general-purpose
    programming language.
-   Database libraries use connections and cursors to manage
    interactions.
-   Programs can fetch all results at once, or a few results at a time.
-   If queries are constructed dynamically using input from users,
    malicious users may be able to inject their own commands into the
    queries.
-   Dynamically-constructed queries can use SQL's native formatting to
    safeguard against such attacks.

Summing Up
----------

A database is the right tool for managing complex and structured data.
Thousands of programmer-years have gone into their design and
implementation so that they can handle very large datasets—terabytes or
more—quickly and reliably. Queries allow for great flexibility in how
you are able to analyze your data, which makes databases a good choice
when you are exploring data. On the other hand, there are lots of things
databases *can't* do, or can't do well: that's why we have
general-purpose programming languages like Python.
