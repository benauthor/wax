import re
import xml.etree.ElementTree as ET
from pprint import pprint as p
from pprint import pformat as f

whitespace = re.compile('\s+')

class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

    def __repr__(self):
        return f({'b-children': self.children, 'a-el': self.element} )

def count_indent(line):
    match = whitespace.match(line)
    try:
        length = len(match.group(0))
    except AttributeError:
        return 0
    else:
        if length % 4 != 0:
            raise Exception('bad indent')
        # maybe throw error on modulo != 0 ???
        return length / 4


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

root = AttrDict(indent=-1, children=[], name="ROOT", element=ET.Element('ROOT'))

def makenode(line, lineno, prev):
    """tmp. make the object"""
    t = AttrDict()
    t.name = line.strip()
    t.children = []
    t.parent = root
#    t.line = line
    t.lineno = lineno
    t.indent = count_indent(line)
    t.element = ET.Element(t.name)
    return t

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
        prev.children.append(t)
        t.parent = prev
    elif t.indent == prev.indent:
        # if my indent is same as prev, i am a child of whatever prev is a child of
        t.parent = prev.parent
        t.parent.children.append(t)
    else:
        # my indent is smaller than prev.
        t.parent = parent_chain(t.indent, prev)
        t.parent.children.append(t)


prev = root
lineno = 0
for line in e.splitlines():
    lineno += 1
    if line:
        n = makenode(line, lineno, prev)
        sortit(n, prev)
        prev = n

print e
p(root)
