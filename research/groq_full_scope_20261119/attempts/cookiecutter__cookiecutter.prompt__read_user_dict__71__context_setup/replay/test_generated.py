import json
import pytest
from collections import OrderedDict
from cookiecutter.prompt import read_user_dict, process_json, JsonPrompt
from rich.prompt import PromptBase
from cookiecutter.exceptions import UndefinedVariableInTemplate
from rich.prompt import InvalidResponse

# Test that read_user_dict raises TypeError when default_value is not a dict
def test_read_user_dict_invalid_default():
    with pytest.raises(TypeError):
        read_user_dict("my_var", default_value="not a dict")

# Test that process_json correctly parses a JSON string into an OrderedDict
def test_process_json_valid():
    json_str = '{"a": 1, "b": 2}'
    result = process_json(json_str)
    assert isinstance(result, OrderedDict)
    assert result == OrderedDict([("a", 1), ("b", 2)])

# Test that process_json raises InvalidResponse for malformed JSON or non-dict JSON
def test_process_json_invalid():
    # malformed JSON
    with pytest.raises(InvalidResponse):
        process_json('{"a": 1, "b": }')
    # valid JSON but not a dict
    with pytest.raises(InvalidResponse):
        process_json('["a", "b"]')
