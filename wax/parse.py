import re
import xml.etree.ElementTree as ET

import __init__ as wax

from analyze import count_indent

#whitespace = re.compile('\s+')

#class AttrDict(dict):
#    def __init__(self, *args, **kwargs):
#        super(AttrDict, self).__init__(*args, **kwargs)
#        self.__dict__ = self
#
#    def __repr__(self):
#        return f({'b-children': self.children, 'a-el': self.element} )

#def count_indent(line):
#    match = whitespace.match(line)
#    try:
#        length = len(match.group(0))
#    except AttributeError:
#        return 0
#    else:
#            if length % 4 != 0:
#            raise Exception('bad indent')
#        # maybe throw error on modulo != 0 ???
#        return length / 4





def makenode(line, lineno, prev):
    """tmp. make the object"""
    name = line.strip()
    indent, _ = count_indent(line)
    return wax.WaxElement(tag=name, parent=None, line_num=lineno, indent=indent)

def parent_chain(indent, prev):
    """recursively walk the parent chain and return the parent at given indent"""
    if indent == prev.indent:
        return prev.parent
    else:
        return parent_chain(indent, prev.parent)

def sortit(t, prev):
    """given previous, decide what to do."""
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


def parse_lines(iterable):
    root = wax.WaxDocument()
    prev = root
    lineno = 0
    for line in iterable:
        lineno += 1
        if line.strip(): # empty lines are allowed
            n = makenode(line, lineno, prev)
            sortit(n, prev)
            prev = n
    return root

if __name__ == "__main__":
#    try:
#        infile = sys.argv[1]
#    except IndexError:
#        raise IndexError("You need to specify a file")
    e = """
    N
        n
            u
    N
    N

        n
        n
            u
        n
    """

    print e
    document = parse_lines(e.splitlines())
    print list(document.xml())
