import json
import pytest
from jinja2 import Environment
from cookiecutter.prompt import render_variable
from cookiecutter.exceptions import UndefinedVariableInTemplate
from jinja2.exceptions import UndefinedError

def test_render_variable_basic_and_nested():
    env = Environment()
    cookiecutter_dict = {"project_name": "Peanut Butter Cookie", "author": "Alice"}
    # Basic string rendering
    raw_str = "{{ cookiecutter.project_name.replace(' ', '_') }}"
    rendered = render_variable(env, raw_str, cookiecutter_dict)
    assert rendered == "Peanut_Butter_Cookie"

    # Nested dict and list rendering
    raw_dict = {
        "repo": "{{ cookiecutter.project_name.replace(' ', '_') }}",
        "contributors": ["{{ cookiecutter.author }}", "Bob"],
        "settings": {"debug": True, "timeout": "{{ 30 + 5 }}"},
    }
    rendered_dict = render_variable(env, raw_dict, cookiecutter_dict)
    assert isinstance(rendered_dict, dict)
    assert rendered_dict["repo"] == "Peanut_Butter_Cookie"
    assert rendered_dict["contributors"] == ["Alice", "Bob"]
    assert rendered_dict["settings"]["debug"] is True
    assert rendered_dict["settings"]["timeout"] == "35"

def test_render_variable_primitive_and_none():
    env = Environment()
    cookiecutter_dict = {}
    # Boolean and None should be returned unchanged
    assert render_variable(env, True, cookiecutter_dict) is True
    assert render_variable(env, False, cookiecutter_dict) is False
    assert render_variable(env, None, cookiecutter_dict) is None

    # Non-string primitive should be converted to string
    assert render_variable(env, 42, cookiecutter_dict) == "42"
    assert render_variable(env, 3.14, cookiecutter_dict) == "3.14"

def test_render_variable_missing_variable_raises():
    env = Environment()
    cookiecutter_dict = {"existing": "value"}
    raw = "{{ cookiecutter.missing_var }}"
    with pytest.raises(UndefinedError):
        render_variable(env, raw, cookiecutter_dict)
