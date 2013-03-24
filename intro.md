Here's the dream:

> Computers have revolutionized research, and that revolution is only
> beginning. Every day, scientists and engineers all over the world use
> them to study things that are too big, too small, too fast, too slow,
> too expensive, too dangerous, or just too hard to study any other way.

Now here's the reality:

> Every day, scientists and engineers all over the world waste time
> wrestling with computers. Tasks that should take a few moments take
> hours or days, and many things never work at all. And even when things
> *do* work, most scientists have no idea how reliable their results
> are.

Most of the pain that researchers feel stems from not knowing how to
develop software systematically, how to tell if their programs are
working correctly, how to share their work with others (except by
mailing files to one another), or how to keep track of what they've
done. This sorry state of affairs persists for four reasons:

 No room, no time. 
:   Everybody's curriculum is full—there's simply not space to add more
    about computing without dropping something else. Or as a scientist
    once asked me, "What should we cut from our physics degree to make
    room for this stuff: thermodynamics or quantum mechanics?" (And
    taking five minutes out of each lecture to talk about computing
    doesn't work: that still adds up to four courses over a four-year
    degree, and anyway, it'll be the first thing cut when the lecturer
    is running late.)
 No standards. 
:   Reviewers and granting agencies don't expect computational work to
    meet the same standards as other experimental work, much less
    require it to, so there's no incentive for scientists to learn how
    to do so.
 The blind leading the blind. 
:   Senior researchers can't teach the next generation how to do things
    that they don't know how to do themselves.
 The cult of big iron. 
:   While most scientists and engineers work on desktop-scale machines,
    most attention and money goes to supercomputers that senators and
    university presidents can stand beside on opening day. As a result,
    basic skills are neglected, just as nurses' salaries and basic
    public health initiatives are often sacrificed to fund the
    construction of a new wing at the hospital.

Our goal is to break this vicious cycle by showing scientists and
engineers how to do more in less time and with less pain. To do this, we
combine half a dozen tools with an equal number of working practices
borrowed from open source software developers. Both can be learned in
under thirty hours; together, they can save most researchers up to a day
a week for the rest of their careers, and make whole new areas of
research feasible.

More specifically, we address these questions:

1.  How can I manage this data?
2.  How can I process it?
3.  How can I tell if I've processed it correctly?
4.  How can I find and fix bugs when I haven't?
5.  How can I keep track of what I've done?
6.  How can I find and use other people's work?
7.  How can other people find and use mine?
8.  How can I do all these things faster?

Our answers rest on four big ideas:

 Software is just another kind of experimental apparatus. 
:   A program is no different from a telescope or oscilloscope. Like
    them, programs need to be assembled, checked, and documented well
    enough for other people (including our future selves) to repeat
    experiments if desired.
 Programming is a human activity. 
:   The most important constraints on software are not what machines can
    do, but what *people* can do. In particular, many of the tools and
    methods we'll meet in coming chapters exist because people can only
    fit a small number of things into short term memory at once, because
    predictability (and paranoia) make us more productive, or because
    getting the program to work often takes longer than actually running
    it.
 Programs are just another kind of data. 
:   A file full of code sitting on a hard drive is just text, and can be
    processed like any other kind of text. Equally, a program running in
    memory is just another data structure, albeit one that describes the
    actions we want a CPU to take rather than the density of
    interstellar gas in the galactic core. Thinking of programs this way
    is the single most powerful idea in programming.
 Better algorithms are better than better hardware. 
:   A supercomputer can reduce your program's running time from months
    to days; a better algorithm (and data structure) can reduce it to
    minutes. The problem is knowing which is best in any particular
    situation, but a handful are good enough for ninety percent of
    real-world situations.

These might not make sense right now, but we hope they will start to
soon. We also hope that by the time you are done with this course you
will think of programming as something more than a tax you have to pay
in order to do the research that you love.

> This book is dedicated to [Charles
> Darwin](http://en.wikipedia.org/wiki/Charles_Darwin), [John
> Scopes](http://en.wikipedia.org/wiki/John_Scopes), \
>  and everyone else who believes that the truth is more important than
> doctrine, \
>  and \
>  to my sister, who did not live to see it finished.
