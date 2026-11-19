import json
import pytest
from jinja2 import Environment
from cookiecutter.prompt import render_variable

def test_render_variable_basic_and_nested():
    env = Environment()
    context = {"project_name": "Peanut Butter Cookie", "author": "Alice"}
    raw = {
        "repo_name": "{{ cookiecutter.project_name.replace(' ', '_') }}",
        "description": "Project by {{ cookiecutter.author }}",
        "features": ["{{ cookiecutter.project_name }}", "{{ cookiecutter.author }}"],
    }
    result = render_variable(env, raw, context)
    assert isinstance(result, dict)
    assert result["repo_name"] == "Peanut_Butter_Cookie"
    assert result["description"] == "Project by Alice"
    assert result["features"] == ["Peanut Butter Cookie", "Alice"]

def test_render_variable_primitive_and_none():
    env = Environment()
    context = {"value": 42}
    assert render_variable(env, None, context) is None
    assert render_variable(env, True, context) is True
    assert render_variable(env, 3.14, context) == "3.14"
    assert render_variable(env, "Hello {{ cookiecutter.value }}", context) == "Hello 42"

def test_render_variable_undefined_variable_raises():
    env = Environment()
    context = {"existing": "yes"}
    raw = "Missing: {{ cookiecutter.nonexistent }}"
    with pytest.raises(Exception) as excinfo:
        render_variable(env, raw, context)
    assert "nonexistent" in str(excinfo.value)
