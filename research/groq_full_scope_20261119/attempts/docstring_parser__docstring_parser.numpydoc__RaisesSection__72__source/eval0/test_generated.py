import pytest
from docstring_parser.numpydoc import RaisesSection
from docstring_parser.common import DocstringRaises


def test_parse_item_normal():
    """Normal case: key and value are non‑empty strings."""
    section = RaisesSection()
    result = section._parse_item("ValueError", "Raised when input is invalid.")
    assert isinstance(result, DocstringRaises)
    assert result.args == ["RaisesSection", "ValueError"]
    assert result.description == "Raised when input is invalid."
    assert result.type_name == "ValueError"


def test_parse_item_empty_key():
    """Boundary case: key is an empty string."""
    section = RaisesSection()
    result = section._parse_item("", "No exception type specified.")
    assert isinstance(result, DocstringRaises)
    assert result.args == ["RaisesSection", ""]
    assert result.description == "No exception type specified."
    assert result.type_name is None


def test_parse_item_invalid_key_type():
    """Error case: key is not a string, should raise TypeError."""
    section = RaisesSection()
    with pytest.raises(TypeError):
        section._parse_item(None, "Some description")
