# coding: spec

from lex import lex_line

"""
The XML spec is here:
http://www.w3.org/TR/2008/REC-xml-20081126/

[Definition: Each XML document contains one or more elements, the boundaries of which are either delimited by start-tags
and end-tags, or, for empty elements, by an empty-element tag. Each element has a type, identified by name, sometimes
called its "generic identifier" (GI), and may have a set of attribute specifications.] Each attribute specification has
a name and a value.

TODO
empty tags
"""
describe "prolog":
    """
    <?xml version="1.0" encoding="ISO-8859-1"?>
    ?xml|version 1.0|encoding ISO-8859-1

    some sugar:
    <?xml version="1.0"?>
    ?xml1
    """
    pass

describe "processing instruction":
    """
    <?xml-stylesheet type="text/xsl" href="style.xsl"?>
    ?xml-stylesheet | type text/xsl | href style.xsl
    <?php echo $a; ?>
    ?php echo $a;
    """
    pass

describe "doctype declaration":
    """
    <!DOCTYPE greeting SYSTEM "hello.dtd">
    !greeting 
    sugar:
    <!DOCTYPE html>
    !html5
    or
    !!!
    """
    pass

describe "element type declaration":
    """
    <!ELEMENT br EMPTY>
    !EL br EMPTY
    """

describe "entity declaration":
    """
    <!ENTITY % draft 'INCLUDE' >
    !ENT % draft 'INCLUDE'
    %ISOLat2;
    %ISOLat2
    """
    pass

describe "attribute type declaration":
    """
    <!ATTRIBUTE etc>
    !ATTR
    <!ATTLIST form
              method  CDATA   #FIXED "POST">
    !ATTL form
          method CDATA #FIXED "POST"
    """
    pass

describe "cdata":
    """
    <[CDATA[ ... ]]>
    [[ ... ]]
    """
    pass


"""
Comment

A comment is a comment, but xml's are too type-y.

    <!-- a comment -->

    =>

    //a comment

"""
describe "comment":
    it "should identify a comment":
        data = lex_line("something//a comment")
        assert data.comment == "a comment"

    it "should be ignored by the parser":
        data = lex_line("something//a comment")
        assert "a comment" not in data.content


"""
Element

The element is the building block of xml. Similarly, it is the building
block of Wax. Just a simple, unadorned name.

    <element></element>

    =>

    element

"""
describe "element":

    it "should be identified in a line":
        data = lex_line("div")
        assert data.element == "div"

    it "should be indentified amongst whitespace":
        data = lex_line("    p    ")
        assert data.element == "p"

    it "should be indentified amongst other words":
        data = lex_line("wat is all this junk")
        assert data.element == "wat"

    it "namespaced elements should not break":
        data = lex_line("namespaced:thing")
        assert data.element == "namespaced:thing"

    it "can have an underscore":
        data = lex_line("a_nother")
        assert data.element == "a_nother"

"""
Indentation

White space is significant. You indent your code anyways, so why not?

    one
        two
            three

"""
describe "indentation":
    it "should count four spaces per indent":
        data = lex_line("    that was four")
        assert data.indent == (1, 0)

    it "should note off-multiple spacing":
        data = lex_line("      there were six there")
        assert data.indent == (1, 2)


"""
Text

What it's all about.

    an_element: With some text inside.
    :Or text on a line of its own.
"""
describe "text":
    it "should be permitted after an element":
        data = lex_line("div: Hello, world!")
        assert data.text == "Hello, world!"

    it "should be permitted on a line of its own":
        data = lex_line("    :Very nice.")
        assert data.text == "Very nice."

    it "namespaced elements should not break with text":
        data = lex_line("trees:elm: Awesome sauce.")
        assert data.element == "trees:elm"
        assert data.text == "Awesome sauce."

    it "should be ok to use a colon in text":
        data = lex_line("element: Some text: it's great")
        assert data.text == "Some text: it's great"

    it "should be permitted at the start of a line":
        data = lex_line(":A word from our sponsor.")
        print data
        assert data.text == "A word from our sponsor."
