import pytest
from docstring_parser.google import parse

def test_parse_google_style_docstring_parses_sections_correctly():
    docstring = """This is a test docstring.

Args:
    x (int): The first argument.
    y (str): The second argument.

Returns:
    bool: True if successful.

Raises:
    ValueError: If something goes wrong."""
    doc = parse(docstring)

    # Description
    assert doc.description.strip() == "This is a test docstring."

    # Params
    assert len(doc.params) == 2
    param_names = [p.name for p in doc.params]
    assert param_names == ["x", "y"]
    param_types = [p.type_name for p in doc.params]
    assert param_types == ["int", "str"]
    param_descs = [p.description.strip() for p in doc.params]
    assert param_descs == ["The first argument.", "The second argument."]

    # Returns
    assert len(doc.returns) == 1
    ret = doc.returns[0]
    assert ret.type_name == "bool"
    assert ret.description.strip() == "True if successful."

    # Raises
    assert len(doc.raises) == 1
    r = doc.raises[0]
    assert r.exception_type == "ValueError"
    assert r.description.strip() == "If something goes wrong."
