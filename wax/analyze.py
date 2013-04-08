#!/usr/bin/env python
import sys
import re
import itertools

### TODOS:
# + problems detecting attrs with special chars, i.e. tal:define. escaping??
# + probably problems with long pythony attr values
# + what exactly do things return when they are empty/None?

# Delimiters
COMMENTDLM = '//'
TXTDLM = ':'

# for matching things
whitespace = re.compile('\s+')
#word = re.compile('\w+')
word = re.compile('\w[\w:]*\w|\w')
#firstword = re.compile('^\w[\w:]*\w|^\w')
attrdlm = '\|'
text_str = '(?<=' + TXTDLM + ' | ' + TXTDLM + ')[\w\W]+'
text = re.compile(text_str)
#text = re.compile('(?<=: | :)[\w\W]+')
attr = re.compile('(?<=\|)[^'+ attrdlm + TXTDLM + ']+')

#attribute sugar
SUGAR_MAP = {
        '.': 'class',
        '#': 'id'
    }

class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

def splitted(s, sep):
    # splits each in a list of strings on sep, then re-adds the sep onto the
    # right-hand thing, then flattens the whole list.
    split = [i.split(sep) for i in s]
    result = []
    for part in split:
        result.append([part[0]] + [sep + i for i in part[1:]])
    return list(itertools.chain.from_iterable(result))


def get_sugar(line):
    plain = line.lstrip()
    plain, _, _ = plain.partition(TXTDLM)
    plain, _, _ = plain.partition('|')
    parts = reduce(splitted, SUGAR_MAP.keys(), [plain])
    try:
        return [p for p in parts if p[0] in SUGAR_MAP.keys()]
    except IndexError:
        return []

def count_indent(line):
    match = whitespace.match(line)
    try:
        length = len(match.group(0))
    except AttributeError:
        return (0, 0)
    else:
        # maybe throw error on modulo != 0 ???
        return (length / 4, length % 4)

def get_element(line):
    match = word.match(line)
    try:
        element = match.group(0)
    except AttributeError:
        return None
    else:
        return element

def get_content(line):
    return line.strip()

def get_attrs(line):
    attrs = attr.findall(line)
    return attrs

def get_text(line):
    try:
        if line[0] == TXTDLM:
            return line[1:]
    except IndexError:
        return None

    match = text.search(line)
    try:
        return match.group(0)
    except AttributeError:
        return None
    # do we need a final return none?

def analyze_line(line):
    data = AttrDict()
    data['raw'] = line
    # chomp the newlines
    line = line.rstrip('\r\n')
    line, _, data['comment'] = line.partition(COMMENTDLM)
    data['indent'] = count_indent(line)
    # now we are done with the whitespace
    line = line.strip()
    data['element'] = get_element(line)
    data['content'] = get_content(line)
    data['text'] = get_text(line)
    data['attrs'] = get_attrs(line)
    data['sugar'] = get_sugar(line)
    data['children'] = []
    return data

def analyze_lines(text):
    for line in iter(text.splitlines()):
        yield analyze_line(line)

def analyze_file(path):
    with open(path) as f:
        for i, line in enumerate(f):
            data = analyze_line(line)
            data['line'] = i + 1
            yield data

#TODO catch some syntax errors.

#TODO the following will not be necessary later
if __name__ == "__main__":
    try:
        infile = sys.argv[1]
    except IndexError:
        raise IndexError("You need to specify a file")

    for i in analyze_file(infile):
        print i

