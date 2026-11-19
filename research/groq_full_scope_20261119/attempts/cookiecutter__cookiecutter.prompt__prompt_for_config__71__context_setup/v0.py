import json
import pytest
from collections import OrderedDict

from cookiecutter.prompt import (
    prompt_for_config,
    prompt_choice_for_config,
    UndefinedVariableInTemplate,
)


def test_prompt_for_config_simple_and_dict(monkeypatch):
    """
    Verify that prompt_for_config correctly renders simple values and
    dictionary values when no_input=True.
    """
    context = {
        "cookiecutter": {
            "project_name": "My Project",
            "repo_name": "{{ cookiecutter.project_name.replace(' ', '_') }}",
            "config": {"key1": "value1", "key2": "{{ cookiecutter.project_name }}"},
            "__prompts__": {},
        }
    }

    result = prompt_for_config(context, no_input=True)

    assert isinstance(result, OrderedDict)
    # Simple string rendered correctly
    assert result["project_name"] == "My Project"
    # Jinja2 expression rendered
    assert result["repo_name"] == "My_Project"
    # Dictionary rendered recursively
    assert result["config"] == {"key1": "value1", "key2": "My Project"}


def test_prompt_choice_for_config_returns_first_when_no_input():
    """
    When no_input=True, prompt_choice_for_config should return the first
    rendered option without prompting the user.
    """
    context = {
        "cookiecutter": {
            "project_name": "Test",
            "__prompts__": {},
        }
    }
    env = context["cookiecutter"]["__prompts__"]  # dummy env for rendering
    # Use a simple list of raw values
    options = ["option1", "{{ cookiecutter.project_name }}"]
    # Render options manually
    rendered = [prompt_choice_for_config.__globals__["render_variable"](
        prompt_choice_for_config.__globals__["create_env_with_context"](context),
        opt,
        {}
    ) for opt in options]
    # The first option should be returned
    assert prompt_choice_for_config({}, None, "choice", options, True) == rendered[0]


def test_prompt_choice_for_config_raises_on_empty_list():
    """
    prompt_choice_for_config should raise ValueError when the options list
    is empty and no_input is True.
    """
    with pytest.raises(ValueError, match="empty"):
        prompt_choice_for_config({}, None, "choice", [], True)
