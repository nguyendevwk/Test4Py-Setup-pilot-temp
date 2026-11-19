import pytest
from docstring_parser.google import parse
from docstring_parser import Docstring, Param, Return, Raise

def test_parse_google_style_docstring_parses_sections_correctly():
    docstring = """This is a short description.

This is a longer description that spans multiple lines.

Args:
    x: The first argument.
    y: The second argument.

Returns:
    The result.

Raises:
    ValueError: If something goes wrong."""
    parsed = parse(docstring)
    assert isinstance(parsed, Docstring)
    assert parsed.short_description == "This is a short description."
    assert parsed.long_description == "This is a longer description that spans multiple lines."
    assert len(parsed.params) == 2
    x_param, y_param = parsed.params
    assert x_param.name == "x"
    assert x_param.description == "The first argument."
    assert y_param.name == "y"
    assert y_param.description == "The second argument."
    assert parsed.returns is not None
    assert parsed.returns.type_name is None
    assert parsed.returns.description == "The result."
    assert len(parsed.raises) == 1
    raise_obj = parsed.raises[0]
    assert raise_obj.type_name == "ValueError"
    assert raise_obj.description == "If something goes wrong."
