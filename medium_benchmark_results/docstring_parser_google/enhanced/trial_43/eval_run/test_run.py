import pytest
from docstring_parser.google import parse
from docstring_parser.common import Kind

def test_parse_google_style_docstring_parses_correctly():
    text = """Summary.

Args:
    name (str): The name.

Returns:
    bool: The return value.
"""
    doc = parse(text)
    # Basic Docstring attributes
    assert isinstance(doc, type(parse(text)))  # Docstring instance
    assert doc.short_description == "Summary."
    assert doc.long_description is None
    assert doc.description == "Summary."

    # Params
    assert len(doc.params) == 1
    param = doc.params[0]
    assert isinstance(param, type(doc.params[0]))
    assert param.arg_name == "name"
    assert param.type_name == "str"
    assert param.description == "The name."
    assert param.kind is Kind.PARAM

    # Returns
    ret = doc.returns
    assert ret is not None
    assert ret.description == "The return value."
    assert ret.type_name == "bool"
    assert ret.kind is Kind.RETURNS
