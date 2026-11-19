import inspect
import pytest
from docstring_parser.numpydoc import RaisesSection
from docstring_parser.numpydoc.common import DocstringRaises

def test_parse_item_normal():
    section = RaisesSection(title="Raises", key="raises")
    # normal key and value
    result = section._parse_item("ValueError", "  An error occurs when input is invalid.  ")
    assert isinstance(result, DocstringRaises)
    assert result.args == ["raises", "ValueError"]
    assert result.description == "An error occurs when input is invalid."
    assert result.type_name == "ValueError"

def test_parse_item_empty_key_and_value():
    section = RaisesSection(title="Raises", key="raises")
    # empty key and empty value
    result = section._parse_item("", "")
    assert isinstance(result, DocstringRaises)
    assert result.args == ["raises", ""]
    # description should be None because value is empty after stripping
    assert result.description is None
    # type_name should be None because key length is 0
    assert result.type_name is None

def test_parse_item_multiline_value_and_whitespace():
    section = RaisesSection(title="Raises", key="raises")
    multiline_value = """
        First line of description.
        Second line continues here.
    """
    # inspect.cleandoc removes common indentation
    cleaned = inspect.cleandoc(multiline_value)
    result = section._parse_item("RuntimeError", cleaned)
    expected_description = "First line of description.\nSecond line continues here."
    assert result.description == expected_description
    assert result.type_name == "RuntimeError"
