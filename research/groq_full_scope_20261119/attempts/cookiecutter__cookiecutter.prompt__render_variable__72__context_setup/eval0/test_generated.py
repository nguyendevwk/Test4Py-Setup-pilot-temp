import pytest
from jinja2 import Environment
from cookiecutter.prompt import render_variable
from cookiecutter.exceptions import UndefinedVariableInTemplate
from jinja2.exceptions import UndefinedError

def test_render_variable_basic_and_nested(tmp_path):
    env = Environment()
    context = {"project_name": "Peanut Butter Cookie"}
    raw = "{{ cookiecutter.project_name.replace(' ', '_') }}"
    # Basic string rendering
    assert render_variable(env, raw, context) == "Peanut_Butter_Cookie"

    # Nested dict and list rendering
    raw_dict = {
        "repo": "{{ cookiecutter.project_name.replace(' ', '-') }}",
        "tags": ["{{ cookiecutter.project_name }}", "demo"]
    }
    rendered = render_variable(env, raw_dict, context)
    assert isinstance(rendered, dict)
    assert rendered["repo"] == "Peanut-Butter-Cookie"
    assert rendered["tags"] == ["Peanut Butter Cookie", "demo"]

def test_render_variable_primitive_and_none():
    env = Environment()
    context = {}
    # Boolean and None should be returned unchanged
    assert render_variable(env, True, context) is True
    assert render_variable(env, False, context) is False
    assert render_variable(env, None, context) is None

def test_render_variable_undefined_variable_raises():
    env = Environment()
    context = {}
    raw = "{{ undefined_var }}"
    with pytest.raises(UndefinedError):
        render_variable(env, raw, context)
