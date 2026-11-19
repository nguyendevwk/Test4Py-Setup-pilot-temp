import json
import pytest
from collections import OrderedDict

from cookiecutter.prompt import prompt_for_config
from cookiecutter.exceptions import UndefinedVariableInTemplate
from cookiecutter.utils import create_env_with_context


def test_prompt_for_config_simple_and_boolean_no_input(tmp_path):
    """
    Verify that simple string and boolean variables are rendered correctly
    when no user input is requested.
    """
    context = {
        "cookiecutter": {
            "project_name": "demo",
            "use_feature": True,
            "_private": "secret",
            "__rendered": "{{ cookiecutter.project_name }}",
        }
    }
    result = prompt_for_config(context, no_input=True)

    # Simple string should be rendered unchanged
    assert result["project_name"] == "demo"
    # Boolean should be rendered as True
    assert result["use_feature"] is True
    # Private key should be preserved
    assert result["_private"] == "secret"
    # Rendered key should resolve the template
    assert result["__rendered"] == "demo"
    # The result should be an OrderedDict preserving insertion order
    assert isinstance(result, OrderedDict)
    assert list(result.keys()) == [
        "project_name",
        "use_feature",
        "_private",
        "__rendered",
    ]


def test_prompt_for_config_choice_and_dict_no_input(tmp_path):
    """
    Verify that choice variables and dictionary variables are rendered
    correctly when no user input is requested.
    """
    context = {
        "cookiecutter": {
            "language": ["python", "javascript"],
            "config": {"debug": False, "timeout": 30},
            "__choice_rendered": "{{ cookiecutter.language }}",
        }
    }
    result = prompt_for_config(context, no_input=True)

    # Choice variable should default to the first option
    assert result["language"] == "python"
    # Dictionary variable should be rendered as a dict
    assert result["config"] == {"debug": False, "timeout": 30}
    # Rendered choice should reflect the chosen value
    assert result["__choice_rendered"] == "python"


def test_prompt_for_config_undefined_variable_raises(tmp_path):
    """
    Verify that an undefined variable in a template raises
    UndefinedVariableInTemplate with the correct message.
    """
    context = {
        "cookiecutter": {
            "project_name": "{{ undefined_var }}",
        }
    }
    with pytest.raises(UndefinedVariableInTemplate) as excinfo:
        prompt_for_config(context, no_input=True)

    # The exception message should mention the problematic key
    assert "project_name" in str(excinfo.value)
    # The original UndefinedError should be the cause
    assert isinstance(excinfo.value.__cause__, Exception)
