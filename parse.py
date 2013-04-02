import sys

from operator import add

from itertools import ifilter
from lex import lex_file, lex_lines

def cluster(iterable, func=lambda x, y: x != y):
    """Take an iterable and yield groups according to a rule.

    The function is applied to each consecutive pair of items in the iterable
    in turn; when it returns true the accumulated group is yielded.
    """
    def next_or_none(iterable):
        try:
            return iterable.next()
        except StopIteration:
            return None

    group = []
    lookahead = next_or_none(iterable)
    while lookahead:
        token = lookahead
        lookahead = next_or_none(iterable)
        group.append(token)
        if func(token, lookahead):
            yield group
            group = []

def has_element(data):
    return data.element

def has_text(data):
    return data.text

def is_empty(data):
    return not data.content

def group_by_indent(data, indent):
    def compare(x,y):
        try:
            return y.indent == indent
        except:
            return True
    for i in cluster(ifilter(lambda x: x.content, data), compare):
        yield i

def group_recursive(data, indent=(0,0)):
    for j in group_by_indent(data, indent):
        if len(j) > 1:
            j[0].children = j[1:]
            print j
#        for i in j: 
#            group_recursive(i, tuple(map(add, indent, (1,0))))
#            print (i.indent, i.element, i.children)

if __name__ == "__main__":
    pass
#    try:
#        infile = sys.argv[1]
#    except IndexError:
#        raise IndexError("You need to specify a file")

#    for i in lex_file(infile):
#        print i
#        if not is_empty(i):
#            if has_element(i):
#                print ('ELEMENT', i.element)
#            if has_text(i):
#                print ('TEXT', i.text)
