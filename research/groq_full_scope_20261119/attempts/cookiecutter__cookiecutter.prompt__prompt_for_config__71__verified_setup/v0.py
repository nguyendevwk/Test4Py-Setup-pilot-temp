import json
import pytest
from collections import OrderedDict

from cookiecutter.prompt import prompt_for_config, UndefinedVariableInTemplate


def test_simple_and_choice_variables_no_input(tmp_path):
    # Context with a simple string, a list choice, and a nested dict
    context = {
        "cookiecutter": {
            "project_name": "demo",
            "license": ["MIT", "Apache-2.0", "GPL-3.0"],
            "author": {"first": "John", "last": "Doe"},
            "__prompts__": {},
        }
    }
    result = prompt_for_config(context, no_input=True)

    # Simple variable should be rendered as is
    assert result["project_name"] == "demo"

    # Choice variable should default to first option when no_input
    assert result["license"] == "MIT"

    # Nested dict should be rendered correctly
    assert result["author"] == {"first": "John", "last": "Doe"}

    # The result should preserve order
    assert list(result.keys()) == ["project_name", "license", "author"]


def test_boolean_variable_no_input_and_user_prompt(tmp_path):
    # Context with a boolean variable
    context = {
        "cookiecutter": {
            "include_tests": True,
            "__prompts__": {},
        }
    }
    # no_input=True should keep the original boolean value
    result_no_input = prompt_for_config(context, no_input=True)
    assert result_no_input["include_tests"] is True

    # When no_input=False, the function would normally prompt the user.
    # Since we cannot simulate interactive input, we test that the function
    # still returns a boolean value (the default) without raising.
    result_prompt = prompt_for_config(context, no_input=False)
    assert isinstance(result_prompt["include_tests"], bool)


def test_undefined_variable_raises_error(tmp_path):
    # Context where a variable references an undefined variable in the template
    context = {
        "cookiecutter": {
            "project_name": "{{ undefined_var }}",
            "__prompts__": {},
        }
    }
    with pytest.raises(UndefinedVariableInTemplate) as excinfo:
        prompt_for_config(context, no_input=True)

    # The exception message should mention the problematic variable
    assert "project_name" in str(excinfo.value)
    # The original context should be preserved in the exception
    assert excinfo.value.context == context
