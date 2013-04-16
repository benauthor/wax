import sys
import re

import __init__ as wax

from analyze import analyze_lines, analyze_file


def makenode(line, lineno, prev):
    """Construct a node.
    """
    indent, _ = line.indent
    attrib = line.attrs
    node = wax.WaxElement(tag=line.element,
                          parent=None,
                          attrib=attrib,
                          line_num=lineno,
                          indent=indent)
    node.text = ''
    if line.text:
        node.text += line.text
    return node


def parent_chain(indent, prev):
    """Recursively walk the parent chain and return the parent at given indent.
    """
    if indent == prev.indent:
        return prev.parent
    else:
        return parent_chain(indent, prev.parent)


def sortit(t, prev):
    """Given previous, decide what to do.
    """
    if t.indent > prev.indent:
        # if my indent is greater than prev, i am a child of prev
        # TODO attributes may be on consecutive lines
        prev.add_child(t)
        t.parent = prev
    elif t.indent == prev.indent:
        # if my indent is same as prev, i am a child of whatever prev is a child of
        t.parent = prev.parent
        t.parent.add_child(t)
    else:
        # my indent is smaller than prev.
        t.parent = parent_chain(t.indent, prev)
        t.parent.add_child(t)


def parse_data(iterable):
    """Take data from an analyze method and make something of it.
    """
    root = wax.WaxDocument()
    prev = root
    lineno = 0
    for line in iterable:
        lineno += 1
        if line.content.strip(): # empty lines are allowed
            n = makenode(line, lineno, prev)
            sortit(n, prev)
            prev = n
    return root


def parse_string(input):
    return parse_data(analyze_lines(input))


def parse_file(infile):
    return parse_data(analyze_file(infile))


if __name__ == "__main__":
    try:
        infile = sys.argv[1]
    except IndexError:
        raise IndexError("You need to specify a file")
    document = parse_file(infile)
    a_string = ''.join(document.xml())
    print a_string

    # TODO proper prettification
    from xml.dom import minidom
    xml = minidom.parseString("<root>%s</root>" % a_string)
    print xml.toprettyxml()

    for i in analyze_file(infile):
        print i
