# coding: spec

from lex import lex_line

describe "element":
    it "should be identified in a line":
        data = lex_line("div")
        assert data["element"] == "div"

    it "should be indentified amongst whitespace":
        data = lex_line("    p    ")
        assert data["element"] == "p"

    it "should be indentified amongst other words":
        data = lex_line("wat is all this junk")
        assert data["element"] == "wat"

    it "namespaced elements should not break":
        data = lex_line("namespaced:thing")
        assert data["element"] == "namespaced:thing"

