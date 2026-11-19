import pytest
from docstring_parser.numpydoc import ParamSection
from docstring_parser.common import DocstringParam

class DummyParamSection(ParamSection):
    def __init__(self, key: str):
        self.key = key

def test_parse_simple_param():
    section = DummyParamSection("param1")
    key = "x : int"
    value = "An integer value."
    result = section._parse_item(key, value)
    assert isinstance(result, DocstringParam)
    assert result.args == ["param1", "x"]
    assert result.arg_name == "x"
    assert result.type_name == "int"
    assert result.is_optional is False
    assert result.default is None
    assert result.description == "An integer value."

def test_parse_optional_with_default_in_type():
    section = DummyParamSection("param2")
    key = "y : str, optional = 'default'"
    value = "A string with a default."
    result = section._parse_item(key, value)
    assert result.arg_name == "y"
    assert result.type_name == "str"
    assert result.is_optional is True
    assert result.default == "'default'"
    assert result.description == "A string with a default."

def test_parse_default_in_description():
    section = DummyParamSection("param3")
    key = "z : float"
    value = "A float value. Default: 3.14"
    result = section._parse_item(key, value)
    assert result.arg_name == "z"
    assert result.type_name == "float"
    assert result.is_optional is False
    assert result.default == "3.14"
    assert result.description == "A float value. Default: 3.14"
