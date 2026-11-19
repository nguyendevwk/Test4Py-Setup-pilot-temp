import json
import pytest
from pathlib import Path
from jinja2 import Environment
from cookiecutter.prompt import prompt_choice_for_config, render_variable

# Helper to create a minimal cookiecutter dict and Jinja2 environment
@pytest.fixture
def env_and_dict(tmp_path: Path):
    env = Environment()
    cookiecutter_dict = {"project_name": "Test Project"}
    return env, cookiecutter_dict

def test_prompt_choice_for_config_no_input_returns_first_rendered(env_and_dict):
    env, cookiecutter_dict = env_and_dict
    # Options contain Jinja2 expressions that refer to cookiecutter variables
    options = ["{{ cookiecutter.project_name }}", "{{ cookiecutter.project_name | lower }}"]
    result = prompt_choice_for_config(
        cookiecutter_dict,
        env,
        key="project_name",
        options=options,
        no_input=True,
        prompts=None,
        prefix="",
    )
    # The first rendered option should be the original project name
    assert result == "Test Project"

def test_prompt_choice_for_config_no_input_empty_options_raises(env_and_dict):
    env, cookiecutter_dict = env_and_dict
    options = []
    with pytest.raises(ValueError, match="The list of choices is empty"):
        prompt_choice_for_config(
            cookiecutter_dict,
            env,
            key="project_name",
            options=options,
            no_input=True,
            prompts=None,
            prefix="",
        )

def test_render_variable_handles_nested_structures(env_and_dict):
    env, cookiecutter_dict = env_and_dict
    # Nested dict and list with Jinja2 expressions
    raw = {
        "name": "{{ cookiecutter.project_name }}",
        "tags": ["{{ cookiecutter.project_name }}", "demo"],
        "config": {"enabled": True, "path": "{{ cookiecutter.project_name | replace(' ', '_') }}"},
    }
    rendered = render_variable(env, raw, cookiecutter_dict)
    assert isinstance(rendered, dict)
    assert rendered["name"] == "Test Project"
    assert rendered["tags"] == ["Test Project", "demo"]
    assert rendered["config"]["path"] == "Test_Project"
    assert rendered["config"]["enabled"] is True
