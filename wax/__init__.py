#USEFUL NOTE: http://www.packtpub.com/article/writing-a-package-in-python

import xml.etree.ElementTree as ET

import config
import analyze
import parse


class WaxDocument(object):
    def __init__(self, children=[], indent=-1):
        self.children=[]
        self.indent=-1

    def xml(self):
        for child in self.children:
            yield ET.tostring(child)

    def add_child(self, item):
        self.children.append(item)


class WaxElement(ET.Element):
    """An abstract representation of a node in the tree
    """
    def __init__(self, indent=0, tag='', attrib={}, parent=None, line_num=None):
        super(WaxElement, self).__init__(tag, attrib)
        self.indent = indent
        self.parent = parent
        self.line_num = line_num

    def add_child(self, item):
        self.append(item)

    def xml(self):
        return ET.tostring(self)

    def wax(self):
        indent = ' ' * config.SPACES_PER_INDENT * self.indent
        return "{indent}{tag}".format(indent=indent,
                                      tag=self.tag)

