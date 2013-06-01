#coding: spec

from wax.parse import parse_string

describe "elements":
    it "can make a node":
        result = parse_string('foo')
        assert result.all_the_xml() == "<foo />"

    it "can make a sequence of nodes":
        input = """
foo
bar
"""
        result = parse_string(input)
        assert result.all_the_xml() == "<foo /><bar />"

    it "can nest nodes":
        input = """
foo
    bar
"""
        result = parse_string(input)
        assert result.all_the_xml() == "<foo><bar /></foo>"

    it "can group things correctly":
        input = """
a
    b
c
    d
    e
        f
    g
"""
        result = parse_string(input)
        assert result.all_the_xml() == "<a><b /></a><c><d /><e><f /></e><g /></c>"

    it "ignores empty lines":
        input = """
x

y
    
    z
"""
        result = parse_string(input)
        assert result.all_the_xml() == "<x /><y><z /></y>"


describe "attributes":
    it "can put attributes on an element":
        result = parse_string("foo|bar baz")
        assert result.all_the_xml() == '<foo bar="baz" />'

    it "can come on a subsequent line":
        input = """
foo
    |bar baz
"""
        result = parse_string(input)
        assert result.all_the_xml() == '<foo bar="baz" />'

    it "can have several attributes":
        input = """
foo|bar baz|biff bam bap
    |chip chop
"""
        result = parse_string(input)
        assert result.all_the_xml() == '<foo bar="baz" biff="bam bap" chip="chop" />'


describe "sugar":
    """Sugar: the idea is to make life easier by making common tasks
    extremely easy. i.e. div.my-class and div#my-id shorthand
    and maybe the doctype stuff too.
    """
    it "has some sugar to make life easier":
        assert False


#describe "text":

describe "comments":
    it "ignores double slash comments":
        result = parse_string("beans//nomore")
        assert result.all_the_xml() == "<beans />"
    #it "preserves some different kind of comment":
    #   ideas: //! or <! or just !
    #   <foo><!-- wowee --></foo>
#describe "sortit":
#
#describe "cluster":
#    it "groups things":
#        groups = list(cluster(iter([1,1,1,2,2,2])))
#        assert groups == [[1,1,1],[2,2,2]]
#
#    it "can use an arbitrary function":
#        groups = list(cluster(iter([1,1,1,2,2,2,1,1,1]), lambda x, y: x > y))
#        assert groups == [[1,1,1,2,2,2],[1,1,1]]
#
#
#describe "group by indent":
#    it "separates nodes on a level":
#        input = """
#p
#p
#
#p
#"""
#        result = list(group_by_indent(analyze_lines(input), (0, 0)))
#        assert len(result) == 3
#
#    it "groups child nodes with parents":
#        input = """
#parent
#    child
#parent
#    child
#    child
#    child
#
#parent
#    child
#"""
#        result = list(group_by_indent(analyze_lines(input), (0, 0)))
#        assert len(result) == 3
#
#    it "groups n levels deep":
#        input = """
#parent
#    child
#        sub
#parent
#    child
#        sub
#            sub
#"""
#        result = list(group_by_indent(analyze_lines(input), (0, 0)))
#        assert len(result) == 2
#
#    it "groups recursively":
#        input = """
#parent
#    child
#        sub
#"""
#        group_recursive(analyze_lines(input))
#
#        assert False
