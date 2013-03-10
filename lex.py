import re

# for matching things
whitespace = re.compile('\s+')
word = re.compile('\w+')
txtdlm = ':'
text_str = '(?<=' + txtdlm + ' | ' + txtdlm + ')[\w\W]+'
text = re.compile(text_str)
#text = re.compile('(?<=: | :)[\w\W]+')
attr = re.compile('(?<=\| )[\w\W]+')

def count_indent(line):
    match = whitespace.match(line)
    try:
        length = len(match.group(0))
    except AttributeError:
        return 0
    else:
        # maybe throw error on modulo != 0
        # if length % 4 != 0:
        #     raise Exception('funny indent')
        return length/4

def get_element(line):
    words = word.findall(line)
    try:
        return words[0]
    except IndexError:
        return None

def get_content(line):
    return line.strip()

def get_attrs(line):
    pass

def get_text(line):
    match = text.search(line)
    try:
        return match.group(0)
    except AttributeError:
        return None


infile = "in.wax"
with open(infile) as f:
    for i, line in enumerate(f):
        data = {}
        data['line'] = i + 1
        data['indent'] = count_indent(line)
        data['element'] = get_element(line)
        data['content'] = get_content(line)
        data['text'] = get_text(line)
        print data

