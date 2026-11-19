import re
import pytest
from docstring_parser.numpydoc import ParamSection
from docstring_parser.common import DocstringParam

# Helper to create a ParamSection instance (the base class expects title and key)
def make_section():
    return ParamSection(title="dummy", key="dummy")

def test_parse_item_with_type_and_optional():
    """Test parsing of a key with type, optional flag and default in type."""
    section = make_section()
    key = "x : int, optional = 5"
    value = "An integer parameter."
    param = section._parse_item(key, value)

    assert isinstance(param, DocstringParam)
    assert param.arg_name == "x"
    assert param.type_name == "int"
    assert param.is_optional is True
    assert param.default == "5"
    assert param.description == "An integer parameter."
    # args should contain the section key and the argument name
    assert param.args == ["dummy", "x"]

def test_parse_item_with_default_in_description():
    """Test that a default value specified in the description is captured."""
    section = make_section()
    key = "y : float"
    value = "A float parameter. Default is 0.0."
    param = section._parse_item(key, value)

    assert param.arg_name == "y"
    assert param.type_name == "float"
    assert param.is_optional is False
    assert param.default == "0.0"
    assert param.description == "A float parameter. Default is 0.0."

def test_parse_item_without_type_and_optional():
    """Test parsing when no type or optional flag is present."""
    section = make_section()
    key = "z"
    value = "A parameter with no type."
    param = section._parse_item(key, value)

    assert param.arg_name == "z"
    assert param.type_name is None
    assert param.is_optional is False
    assert param.default is None
    assert param.description == "A parameter with no type."
    assert param.args == ["dummy", "z"]
