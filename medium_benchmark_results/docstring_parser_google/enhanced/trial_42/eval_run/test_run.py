import pytest
from docstring_parser.google import parse

def test_parse_google_style_parses_params_and_returns():
    doc = """Summary.

Args:
    name (str): The name.

Returns:
    bool: The return value.
"""
    parsed = parse(doc)

    # Basic description
    assert parsed.short_description == "Summary."
    assert parsed.description == "Summary."

    # Params
    assert len(parsed.params) == 1
    param = parsed.params[0]
    assert param.arg_name == "name"
    assert param.type_name == "str"
    assert param.description == "The name."
    # Mapping by name
    assert parsed.params_by_name["name"].arg_name == "name"

    # Returns
    ret = parsed.returns
    assert ret is not None
    assert ret.type_name == "bool"
    assert ret.description == "The return value."
