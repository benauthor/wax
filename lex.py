#!/usr/bin/env python
import sys
import re
import itertools

### TODOS:
# + problems detecting attrs with special chars, i.e. tal:define. escaping??
# + probably problems with long pythony attr values
# + what exactly do things return when they are empty/None?


# for matching things
whitespace = re.compile('\s+')
word = re.compile('[\w:]+')
txtdlm = ':'
attrdlm = '\|'
text_str = '(?<=' + txtdlm + ' | ' + txtdlm + ')[\w\W]+'
text = re.compile(text_str)
#text = re.compile('(?<=: | :)[\w\W]+')
attr = re.compile('(?<=\|)[^'+ attrdlm + txtdlm + ']+')

#attribute sugar
SUGAR_MAP = {
        '.': 'class',
        '#': 'id'
    }

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
    plain, _, _ = plain.partition(':')
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
    words = word.findall(line)
    try:
        return words[0]
    except IndexError:
        return None

def get_content(line):
    return line.strip()

def get_attrs(line):
    attrs = attr.findall(line)
    return attrs

def get_text(line):
    match = text.search(line)
    try:
        return match.group(0)
    except AttributeError:
        return None

def lex_line(line):
    data = {}
    line = line.rstrip('\r\n')
    line, _, data['comment'] = line.partition('//')
    data['indent'] = count_indent(line)
    data['element'] = get_element(line)
    data['content'] = get_content(line)
    data['text'] = get_text(line)
    data['attrs'] = get_attrs(line)
    data['sugar'] = get_sugar(line)
    return data

def lex_file(path):
    with open(path) as f:
        for i, line in enumerate(f):
            data = lex_line(line)
            data['line'] = i + 1
            yield data

#TODO catch some syntax errors.

if __name__ == "__main__":
    try:
        infile = sys.argv[1]
    except IndexError:
        raise IndexError("You need to specify a file")

    for i in lex_file(infile):
        print i

