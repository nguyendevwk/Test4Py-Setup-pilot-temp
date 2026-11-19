import inspect
import pytest
from docstring_parser.numpydoc import RaisesSection
from docstring_parser.numpydoc.common import DocstringRaises

def test_parse_item_normal():
    """Normal case: non‑empty key and value."""
    section = RaisesSection(title="Raises", key="raises")
    result = section._parse_item("ValueError", "An error occurs")
    assert isinstance(result, DocstringRaises)
    assert result.args == ["raises", "ValueError"]
    assert result.description == "An error occurs"
    assert result.type_name == "ValueError"

def test_parse_item_empty_key():
    """Key is empty string: type_name should be None."""
    section = RaisesSection(title="Raises", key="raises")
    result = section._parse_item("", "No type specified")
    assert isinstance(result, DocstringRaises)
    assert result.args == ["raises", ""]
    assert result.description == "No type specified"
    assert result.type_name is None

def test_parse_item_whitespace_value():
    """Value with only whitespace should be cleaned to None."""
    section = RaisesSection(title="Raises", key="raises")
    result = section._parse_item("RuntimeError", "   \n  ")
    assert isinstance(result, DocstringRaises)
    assert result.args == ["raises", "RuntimeError"]
    assert result.description is None
    assert result.type_name == "RuntimeError"
