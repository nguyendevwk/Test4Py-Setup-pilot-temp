import re
import pytest
from inspect import cleandoc
from docstring_parser.numpydoc import ParamSection
from docstring_parser.common import DocstringParam

# Helper regex patterns from the module (re-exported for clarity)
PARAM_KEY_REGEX = re.compile(r"(?P<name>\w+)(?::\s*(?P<type>.+))?")
PARAM_OPTIONAL_REGEX = re.compile(r"(?P<type>.+)\s*,\s*optional")
PARAM_DEFAULT_REGEX = re.compile(r"(?P<type>.+)\s*=\s*(?P<value>.+)")
PARAM_DEFAULT_REGEX_IN_DESC = re.compile(r"(?P<value>.+?)\s*\(default\s*=\s*(?P<value>.+?)\)")

def test_parse_item_basic():
    """Test parsing of a simple parameter without type or default."""
    section = ParamSection()
    key = "param1"
    value = "This is a simple parameter."
    result = section._parse_item(key, value)
    assert isinstance(result, DocstringParam)
    assert result.arg_name == "param1"
    assert result.type_name is None
    assert result.is_optional is None
    assert result.default is None
    assert result.description == "This is a simple parameter."

def test_parse_item_optional_with_default():
    """Test parsing of a parameter marked optional with a default in the type."""
    section = ParamSection()
    key = "param2 : int, optional = 42"
    value = "An integer parameter with a default."
    result = section._parse_item(key, value)
    assert result.arg_name == "param2"
    assert result.type_name == "int"
    assert result.is_optional is True
    assert result.default == "42"
    assert result.description == "An integer parameter with a default."

def test_parse_item_default_in_description():
    """Test parsing when the default is only present in the description."""
    section = ParamSection()
    key = "param3 : str"
    value = cleandoc("""
        A string parameter.
        (default = 'hello')
    """)
    result = section._parse_item(key, value)
    assert result.arg_name == "param3"
    assert result.type_name == "str"
    assert result.is_optional is None
    assert result.default == "'hello'"
    assert result.description == "A string parameter.\n(default = 'hello')"
