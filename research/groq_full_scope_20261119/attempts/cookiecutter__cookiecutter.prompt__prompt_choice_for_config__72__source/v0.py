import pytest
from collections import OrderedDict
from jinja2 import Environment
from cookiecutter.prompt import prompt_choice_for_config

def test_prompt_choice_returns_first_option_when_no_input():
    """When no_input is True, the function should return the first rendered option."""
    env = Environment()
    cookiecutter_dict = {"name": "Alice"}
    options = ["Option 1", "Option 2"]
    result = prompt_choice_for_config(
        cookiecutter_dict=cookiecutter_dict,
        env=env,
        key="choice",
        options=options,
        no_input=True,
    )
    assert result == "Option 1"

def test_prompt_choice_raises_value_error_on_empty_options():
    """When no_input is True and options list is empty, a ValueError should be raised."""
    env = Environment()
    cookiecutter_dict = {}
    with pytest.raises(ValueError, match="The list of choices is empty"):
        prompt_choice_for_config(
            cookiecutter_dict=cookiecutter_dict,
            env=env,
            key="choice",
            options=[],
            no_input=True,
        )

def test_prompt_choice_renders_variables_in_options():
    """Options containing Jinja2 variables should be rendered correctly before selection."""
    env = Environment()
    cookiecutter_dict = {"project_name": "my_project"}
    options = ["{{ project_name }}", "Other"]
    result = prompt_choice_for_config(
        cookiecutter_dict=cookiecutter_dict,
        env=env,
        key="choice",
        options=options,
        no_input=True,
    )
    assert result == "my_project"
