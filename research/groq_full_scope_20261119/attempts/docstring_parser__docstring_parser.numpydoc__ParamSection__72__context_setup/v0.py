import inspect
import pytest
from docstring_parser.numpydoc import ParamSection, DocstringParam

# Test 1: Basic parsing without type, optional or default
def test_parse_item_basic():
    section = ParamSection(title="Parameters", key="parameters")
    key = "my_arg"
    value = "This is a simple argument."
    result = section._parse_item(key, value)
    assert isinstance(result, DocstringParam)
    assert result.arg_name == "my_arg"
    assert result.type_name is None
    assert result.is_optional is None
    assert result.default is None
    assert result.description == "This is a simple argument."
    assert result.args == ["parameters", "my_arg"]

# Test 2: Parsing with type, optional flag and default in type declaration
def test_parse_item_type_optional_default():
    section = ParamSection(title="Parameters", key="parameters")
    key = "count : int, optional, default=10"
    value = "Number of items."
    result = section._parse_item(key, value)
    assert result.arg_name == "count"
    assert result.type_name == "int"
    assert result.is_optional is True
    assert result.default == "10"
    assert result.description == "Number of items."

# Test 3: Default value extracted from description when not in type declaration
def test_parse_item_default_in_description():
    section = ParamSection(title="Parameters", key="parameters")
    key = "threshold : float"
    value = "Threshold value. Defaults to 0.5."
    result = section._parse_item(key, value)
    assert result.arg_name == "threshold"
    assert result.type_name == "float"
    assert result.is_optional is None
    assert result.default == "0.5"
    assert result.description == "Threshold value. Defaults to 0.5."
