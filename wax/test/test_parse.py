# coding: spec
#
#from wax.analyze import analyze_lines
#from wax.parse import cluster, group_by_indent, group_recursive
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
