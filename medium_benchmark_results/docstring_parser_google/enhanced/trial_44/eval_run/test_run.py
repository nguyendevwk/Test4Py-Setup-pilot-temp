import pytest
from docstring_parser.google import parse
from docstring_parser.common import DocstringParam, DocstringReturns

def test_parse_basic_docstring():
    text = """Summary.

Args:
    name (str): The name.

Returns:
    bool: The return value.
"""
    doc = parse(text)
    # Basic type check
    assert hasattr(doc, "short_description")
    assert hasattr(doc, "params")
    assert hasattr(doc, "returns")

    # Short description should be the first line
    assert doc.short_description == "Summary."

    # There should be exactly one parameter parsed
    assert len(doc.params) == 1
    param = doc.params[0]
    assert isinstance(param, DocstringParam)
    assert param.arg_name == "name"
    assert param.type_name == "str"
    assert param.description == "The name."

    # The return value should be parsed correctly
    ret = doc.returns
    assert isinstance(ret, DocstringReturns)
    assert ret.type_name == "bool"
    assert ret.description == "The return value."
