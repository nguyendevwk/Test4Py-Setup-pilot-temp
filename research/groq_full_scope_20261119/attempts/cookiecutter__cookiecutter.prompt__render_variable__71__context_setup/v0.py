import pytest
from jinja2 import Environment
from cookiecutter.prompt import render_variable

def test_render_variable_basic_string_and_dict():
    env = Environment()
    context = {"project_name": "Peanut Butter Cookie"}
    raw = "{{ cookiecutter.project_name.replace(' ', '_') }}"
    # Basic string rendering
    assert render_variable(env, raw, context) == "Peanut_Butter_Cookie"

    # Nested dict rendering
    raw_dict = {
        "repo_name": "{{ cookiecutter.project_name.replace(' ', '_') }}",
        "description": "A cookie project"
    }
    rendered = render_variable(env, raw_dict, context)
    assert isinstance(rendered, dict)
    assert rendered["repo_name"] == "Peanut_Butter_Cookie"
    assert rendered["description"] == "A cookie project"

def test_render_variable_list_and_non_string_types():
    env = Environment()
    context = {"project_name": "Test Project"}
    raw_list = [
        "{{ cookiecutter.project_name }}",
        42,
        True,
        {"nested": "{{ cookiecutter.project_name }}"}
    ]
    rendered = render_variable(env, raw_list, context)
    assert isinstance(rendered, list)
    assert rendered[0] == "Test Project"
    assert rendered[1] == 42
    assert rendered[2] is True
    assert isinstance(rendered[3], dict)
    assert rendered[3]["nested"] == "Test Project"

def test_render_variable_undefined_variable_raises():
    env = Environment()
    context = {"existing": "value"}
    raw = "{{ cookiecutter.nonexistent }}"
    with pytest.raises(Exception) as excinfo:
        render_variable(env, raw, context)
    # The exception should be a Jinja2 UndefinedError or a subclass
    assert hasattr(excinfo.value, "__class__")
    assert "nonexistent" in str(excinfo.value)
