# coding: spec

from parse import cluster 

describe "cluster":
    it "groups things":
        groups = list(cluster(iter([1,1,1,2,2,2])))
        assert groups == [[1,1,1],[2,2,2]]

    it "can use an arbitrary function":
        groups = list(cluster(iter([1,1,1,2,2,2,1,1,1]), lambda x, y: x > y))
        assert groups == [[1,1,1,2,2,2],[1,1,1]]
