import inspect
import pytest
from docstring_parser.numpydoc import ParamSection, DocstringParam

def test_parse_item_with_type_and_optional():
    section = ParamSection(title="Parameters", key="parameters")
    # key with type and optional flag
    key = "x : int, optional"
    value = "The x coordinate."
    result = section._parse_item(key, value)
    assert isinstance(result, DocstringParam)
    assert result.arg_name == "x"
    assert result.type_name == "int"
    assert result.is_optional is True
    assert result.default is None
    assert result.description == "The x coordinate."
    assert result.args == ["parameters", "x"]

def test_parse_item_with_default_in_type_and_description():
    section = ParamSection(title="Parameters", key="parameters")
    # key with type and default value
    key = "y : float = 0.0"
    value = "The y coordinate. Defaults to 0.0."
    result = section._parse_item(key, value)
    assert result.arg_name == "y"
    assert result.type_name == "float"
    assert result.is_optional is True
    assert result.default == "0.0"
    # default should be taken from type, not description
    assert "Defaults to 0.0" not in result.description
    assert result.description == "The y coordinate."

def test_parse_item_with_default_in_description_only():
    section = ParamSection(title="Parameters", key="parameters")
    # key without default, but description contains default
    key = "z : str"
    value = "The z coordinate. Defaults to 'center'."
    result = section._parse_item(key, value)
    assert result.arg_name == "z"
    assert result.type_name == "str"
    assert result.is_optional is False
    assert result.default == "'center'"
    assert result.description == "The z coordinate. Defaults to 'center'."
