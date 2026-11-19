import pytest
from docstring_parser.rest import parse

def test_parse_rest_docstring_extracts_expected_elements():
    docstring = """
    Short description.

    Long description continues here.

    :param x: description of x
    :param y: description of y
    :return: result
    :raises ValueError: if error
    """
    parsed = parse(docstring)

    # Short description
    assert parsed.short_description == "Short description."

    # Long description contains the expected text
    assert "Long description continues here." in parsed.long_description

    # Parameters
    assert len(parsed.params) == 2
    param_names = {p.name for p in parsed.params}
    assert param_names == {"x", "y"}
    param_descs = {p.name: p.description for p in parsed.params}
    assert param_descs["x"] == "description of x"
    assert param_descs["y"] == "description of y"

    # Return description
    assert parsed.returns is not None
    assert parsed.returns.description == "result"

    # Raises
    assert len(parsed.raises) == 1
    raise_entry = parsed.raises[0]
    assert raise_entry.type == "ValueError"
    assert raise_entry.description == "if error"
