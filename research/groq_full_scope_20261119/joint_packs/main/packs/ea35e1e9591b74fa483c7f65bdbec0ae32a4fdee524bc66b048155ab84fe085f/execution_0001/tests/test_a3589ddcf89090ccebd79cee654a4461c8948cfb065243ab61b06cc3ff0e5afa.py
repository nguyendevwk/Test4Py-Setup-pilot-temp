import json
import pytest
from pathlib import Path
from collections import OrderedDict
from jinja2 import Environment
from cookiecutter.prompt import prompt_choice_for_config, render_variable

@pytest.fixture
def jinja_env() -> Environment:
    """Provide a simple Jinja2 environment."""
    return Environment()

def test_prompt_choice_for_config_no_input_returns_first(jinja_env):
    """When no_input is True, the function should return the first rendered option."""
    cookiecutter_dict = {"project_name": "Test Project"}
    options = ["{{ cookiecutter.project_name }}", "Other"]
    result = prompt_choice_for_config(
        cookiecutter_dict=cookiecutter_dict,
        env=jinja_env,
        key="project_name",
        options=options,
        no_input=True,
    )
    assert result == "Test Project"

def test_prompt_choice_for_config_no_input_empty_options_raises(jinja_env):
    """If no_input is True and options list is empty, a ValueError should be raised."""
    cookiecutter_dict = {}
    options = []
    with pytest.raises(ValueError, match="The list of choices is empty"):
        prompt_choice_for_config(
            cookiecutter_dict=cookiecutter_dict,
            env=jinja_env,
            key="empty",
            options=options,
            no_input=True,
        )

def test_render_variable_with_nested_structure(jinja_env):
    """render_variable should correctly render nested structures with Jinja2 templates."""
    cookiecutter_dict = {"name": "Alice", "age": 30}
    raw = {
        "greeting": "Hello, {{ cookiecutter.name }}!",
        "details": {
            "age_statement": "You are {{ cookiecutter.age }} years old.",
            "list": ["{{ cookiecutter.name }}", "{{ cookiecutter.age }}"]
        }
    }
    rendered = render_variable(jinja_env, raw, cookiecutter_dict)
    assert isinstance(rendered, dict)
    assert rendered["greeting"] == "Hello, Alice!"
    assert rendered["details"]["age_statement"] == "You are 30 years old."
    assert rendered["details"]["list"] == ["Alice", "30"]
