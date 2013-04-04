
class Element(object):
    """An abstract representation of a node in the tree
    """
    def __init__(self, indent=0, name='', text='',
                 attrs='', children=[], parent=None, line_num=None):
        self.indent = indent
        self.name = name
        self.text = text #? is a text node a thing?
        self.attrs = attrs
        self.children = children
        self.parent = parent
        self.line_num = line_num

