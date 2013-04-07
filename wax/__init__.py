#USEFUL NOTE: http://www.packtpub.com/article/writing-a-package-in-python

import xml.etree.ElementTree

import analyze
import parse

class WaxElement(xml.etree.ElementTree.Element):
    """An abstract representation of a node in the tree
    """
    def __init__(self, indent=0, tag='', attrib={}, parent=None, line_num=None):
        self.indent = indent
        self.parent = parent
        self.line_num = line_num
        super(WaxElement, self).__init__(tag, attrib)

