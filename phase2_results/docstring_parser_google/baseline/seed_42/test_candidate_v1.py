import pytest
from docstring_parser import parse, Docstring, Param, Return, Raise

def test_parse_google_style_docstring_parses_sections():
    docstring_text = """Short description.

Long description continues here.

Args:
    x: description of x.
    y: description of y.

Returns:
    int: The result.

Raises:
    ValueError: If something.
"""
    parsed = parse(docstring_text)

    assert isinstance(parsed, Docstring)
    assert parsed.short_description == "Short description."
    assert parsed.long_description == "Long description continues here."

    assert len(parsed.params) == 2
    param_names = [p.name for p in parsed.params]
    assert param_names == ["x", "y"]
    param_descriptions = [p.description for p in parsed.params]
    assert param_descriptions == ["description of x.", "description of y."]

    assert isinstance(parsed.returns, Return)
    assert parsed.returns.type == "int"
    assert parsed.returns.description == "The result."

    assert len(parsed.raises) == 1
    raise_obj = parsed.raises[0]
    assert isinstance(raise_obj, Raise)
    assert raise_obj.type == "ValueError"
    assert raise_obj.description == "If something."
