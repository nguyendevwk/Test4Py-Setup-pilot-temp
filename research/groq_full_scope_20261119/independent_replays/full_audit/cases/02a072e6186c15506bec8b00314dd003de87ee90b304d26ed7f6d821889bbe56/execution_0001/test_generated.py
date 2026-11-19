import json
import pytest
from collections import OrderedDict
from cookiecutter.prompt import prompt_for_config
from cookiecutter.exceptions import UndefinedVariableInTemplate

# Test 1: Normal rendering with no_input=True
def test_prompt_for_config_no_input_simple(tmp_path):
    context = {
        "cookiecutter": {
            "project_name": "demo",
            "author": "Alice",
            "license": "MIT",
            "_private": "secret",
            "__raw": {"key": "value"},
            "nested": {"inner": "{{ cookiecutter.project_name }}"},
        }
    }
    result = prompt_for_config(context, no_input=True)
    assert isinstance(result, OrderedDict)
    # Simple string
    assert result["project_name"] == "demo"
    # Boolean default
    assert result["author"] == "Alice"
    # Raw dict rendered
    assert result["__raw"] == {"key": "value"}
    # Nested dict uses rendered value
    assert result["nested"] == {"inner": "demo"}
    # Private key preserved
    assert result["_private"] == "secret"

# Test 2: Rendering with nested references and dicts
def test_prompt_for_config_nested_dicts(tmp_path):
    context = {
        "cookiecutter": {
            "project_name": "awesome",
            "description": "A project called {{ cookiecutter.project_name }}",
            "config": {
                "name": "{{ cookiecutter.project_name }}",
                "desc": "{{ cookiecutter.description }}",
            },
        }
    }
    result = prompt_for_config(context, no_input=True)
    assert result["project_name"] == "awesome"
    assert result["description"] == "A project called awesome"
    assert result["config"] == {"name": "awesome", "desc": "A project called awesome"}

# Test 3: Undefined variable raises UndefinedVariableInTemplate
def test_prompt_for_config_undefined_variable(tmp_path):
    context = {
        "cookiecutter": {
            "project_name": "{{ missing_var }}",
        }
    }
    with pytest.raises(UndefinedVariableInTemplate) as excinfo:
        prompt_for_config(context, no_input=True)
    assert "Unable to render variable 'project_name'" in str(excinfo.value)
