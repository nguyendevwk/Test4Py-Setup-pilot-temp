import re
import pytest
from docstring_parser.numpydoc import ParamSection
from docstring_parser.numpydoc.common import DocstringParam

# Helper to create a ParamSection instance
def make_section():
    return ParamSection(title="Params", key="params")

def test_parse_basic_parameter():
    """Test parsing of a simple parameter without type or default."""
    section = make_section()
    key = "my_arg"
    value = "This is a simple argument."
    result = section._parse_item(key, value)

    assert isinstance(result, DocstringParam)
    assert result.arg_name == "my_arg"
    assert result.type_name is None
    assert result.is_optional is False
    assert result.default is None
    assert result.description == "This is a simple argument."
    # args should contain the section key and the argument name
    assert result.args == ["params", "my_arg"]

def test_parse_optional_with_default_and_type():
    """Test parsing of an optional parameter with type and default in the key."""
    section = make_section()
    key = "opt_arg : int, optional = 42"
    value = "An optional integer argument."
    result = section._parse_item(key, value)

    assert result.arg_name == "opt_arg"
    assert result.type_name == "int"
    assert result.is_optional is True
    assert result.default == "42"
    assert result.description == "An optional integer argument."

def test_parse_default_in_description():
    """Test that a default value specified only in the description is captured."""
    section = make_section()
    key = "flag : bool"
    value = "A flag that defaults to True if not provided. Default: True"
    result = section._parse_item(key, value)

    assert result.arg_name == "flag"
    assert result.type_name == "bool"
    assert result.is_optional is False
    assert result.default == "True"
    assert result.description == "A flag that defaults to True if not provided. Default: True"
