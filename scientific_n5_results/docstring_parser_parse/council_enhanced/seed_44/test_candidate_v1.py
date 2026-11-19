import pytest
from docstring_parser.parser import parse, DocstringStyle
from docstring_parser.parsers import BaseParser, GoogleParser
from docstring_parser.common import Docstring

def test_parse_behavior():
    doc = """Summary line.

:param name: param desc
:type name: str
:returns: return desc
"""
    # 1. Parse with style string
    d1 = parse(doc, style="google")
    assert isinstance(d1, Docstring)
    assert d1.style == DocstringStyle.GOOGLE
    assert d1.short_description == "Summary line."
    assert len(d1.params) == 1
    assert d1.params[0].arg_name == "name"

    # 2. Parse with BaseParser instance
    parser = GoogleParser()
    d2 = parse(doc, style=parser)
    assert d2.style == DocstringStyle.GOOGLE

    # 3. Passing sections with a BaseParser raises ValueError
    with pytest.raises(ValueError):
        parse(doc, style=parser, sections=[("dummy", "section")])

    # 4. Auto detection infers the style
    d3 = parse(doc, style=DocstringStyle.AUTO)
    assert d3.style == DocstringStyle.GOOGLE
