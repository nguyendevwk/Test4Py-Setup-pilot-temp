import json
import pytest
from collections import OrderedDict

from cookiecutter.prompt import prompt_for_config, UndefinedVariableInTemplate


def test_prompt_for_config_no_input_renders_all_values(tmp_path):
    """
    When no_input=True, prompt_for_config should return an OrderedDict
    with all values rendered from the context without any user interaction.
    """
    context = {
        "cookiecutter": {
            "project_name": "TestProject",
            "author_name": "Alice",
            "use_feature_x": True,
            "license": ["MIT", "Apache-2.0", "GPL-3.0"],
            "_private_key": "secret",
            "__rendered": "{{ project_name }}_{{ author_name }}",
            "nested_dict": {"inner": "{{ project_name }}"},
        }
    }

    result = prompt_for_config(context, no_input=True)

    # The result should be an OrderedDict preserving insertion order
    assert isinstance(result, OrderedDict)

    # All keys from the original context should be present
    expected_keys = [
        "project_name",
        "author_name",
        "use_feature_x",
        "license",
        "_private_key",
        "__rendered",
        "nested_dict",
    ]
    assert list(result.keys()) == expected_keys

    # Values should be rendered correctly
    assert result["project_name"] == "TestProject"
    assert result["author_name"] == "Alice"
    assert result["use_feature_x"] is True
    # For list choices, the default is the first element when no_input=True
    assert result["license"] == "MIT"
    assert result["_private_key"] == "secret"
    assert result["__rendered"] == "TestProject_Alice"
    assert result["nested_dict"] == {"inner": "TestProject"}


def test_prompt_for_config_preserves_private_keys(tmp_path):
    """
    Keys starting with a single underscore should be preserved as-is
    and not be prompted for.
    """
    context = {
        "cookiecutter": {
            "_config_path": "/etc/config",
            "project_name": "Demo",
            "__prompt": "{{ project_name }}",
        }
    }

    result = prompt_for_config(context, no_input=True)

    assert "_config_path" in result
    assert result["_config_path"] == "/etc/config"
    assert result["project_name"] == "Demo"
    assert result["__prompt"] == "Demo"


def test_prompt_for_config_raises_on_undefined_variable():
    """
    If a template variable cannot be rendered because it references an
    undefined variable, UndefinedVariableInTemplate should be raised.
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
    # The original context should be available in the exception
    assert excinfo.value.context == context
