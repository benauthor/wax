Whitespaced Analogue to XML
===========================

XML is just a tree, right? And xhtml is just xml. Bam.

It's way nicer to write

    div#main
        h1.title: Welcome to my home page!
        ul.nav
            li: Home
            li: Hobbies
            li: About me
            li: Lucy, my dog

        p: I hope you enjoy reading all about me!

than to type out all the brackets and quotes and crap. Ugh.


This is still just a kernel of an idea. It does not actually work yet. Check
back hourly for exciting updates!

* * *

Tests are written with [nose of yeti](https://github.com/delfick/nose-of-yeti).
You'll need the noseOfYeti and nosetests packages. I like pinocchio too, for
its nice spec-style output. I run tests like this:

    nosetests --with-noy --with-spec --spec-color
