import pytest
from docstring_parser.rest import parse

def test_parse_rest_docstring_parses_sections_correctly():
    docstring = """Short description.

Long description continues here.

:param x: description of x
:type x: int
:param y: description of y
:type y: str
:return: result
:rtype: bool
"""
    parsed = parse(docstring)

    assert parsed.short_description == "Short description."
    assert "Long description continues here." in parsed.long_description

    assert len(parsed.params) == 2
    param_x = next(p for p in parsed.params if p.name == "x")
    assert param_x.type_name == "int"
    assert param_x.description == "description of x"

    param_y = next(p for p in parsed.params if p.name == "y")
    assert param_y.type_name == "str"
    assert param_y.description == "description of y"

    assert parsed.returns is not None
    assert parsed.returns.type_name == "bool"
    assert parsed.returns.description == "result"
