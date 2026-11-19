import json
import pytest
from collections import OrderedDict

from cookiecutter.prompt import prompt_for_config, UndefinedVariableInTemplate


def test_simple_and_rendered_variables(tmp_path):
    """Verify that simple string and boolean variables are rendered correctly
    and that Jinja2 expressions are evaluated using the current context."""
    context = {
        "cookiecutter": {
            "project_name": "My Project",
            "repo_name": "{{ cookiecutter.project_name.replace(' ', '_') }}",
            "include_docs": True,
            "_private": "secret",
            "__prompt__": "This should not be prompted",
        }
    }
    result = prompt_for_config(context, no_input=True)
    assert isinstance(result, OrderedDict)
    # Simple string rendered correctly
    assert result["project_name"] == "My Project"
    # Jinja2 expression evaluated
    assert result["repo_name"] == "My_Project"
    # Boolean preserved
    assert result["include_docs"] is True
    # Private key preserved unchanged
    assert result["_private"] == "secret"
    # No prompt key remains untouched
    assert result["__prompt__"] == "This should not be prompted"


def test_choice_variable_returns_first_option(tmp_path):
    """When no_input is True, a choice variable should return the first
    rendered option without prompting."""
    context = {
        "cookiecutter": {
            "license": ["MIT", "Apache-2.0", "GPL-3.0"],
            "project_name": "Test",
        }
    }
    result = prompt_for_config(context, no_input=True)
    assert result["license"] == "MIT"
    # Ensure other variables are still processed
    assert result["project_name"] == "Test"


def test_empty_choice_raises_value_error(tmp_path):
    """prompt_choice_for_config should raise ValueError when the options list
    is empty and no_input is True."""
    context = {
        "cookiecutter": {
            "empty_choice": [],
            "project_name": "Test",
        }
    }
    with pytest.raises(ValueError, match="The list of choices is empty"):
        prompt_for_config(context, no_input=True)
