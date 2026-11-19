import json
import pytest
from jinja2 import Environment
from cookiecutter.prompt import render_variable

def test_render_variable_basic_string(tmp_path):
    """Test rendering of a simple string template with a variable."""
    env = Environment()
    cookiecutter_dict = {"project_name": "Peanut Butter Cookie"}
    raw = "{{ cookiecutter.project_name.replace(' ', '_') }}"
    result = render_variable(env, raw, cookiecutter_dict)
    assert result == "Peanut_Butter_Cookie"

def test_render_variable_nested_structures(tmp_path):
    """Test rendering when raw is a nested dict and list."""
    env = Environment()
    cookiecutter_dict = {"project_name": "Test Project", "author": "Alice"}
    raw = {
        "repo": "{{ cookiecutter.project_name.replace(' ', '-') }}",
        "contributors": [
            "{{ cookiecutter.author }}",
            "Bob"
        ],
        "settings": {
            "debug": True,
            "max_items": 10
        }
    }
    result = render_variable(env, raw, cookiecutter_dict)
    expected = {
        "repo": "Test-Project",
        "contributors": ["Alice", "Bob"],
        "settings": {"debug": True, "max_items": 10}
    }
    assert result == expected

def test_render_variable_undefined_variable_raises(tmp_path):
    """Test that an undefined variable in the template raises UndefinedError."""
    env = Environment()
    cookiecutter_dict = {"project_name": "Demo"}
    raw = "{{ cookiecutter.undefined_var }}"
    with pytest.raises(Exception) as excinfo:
        render_variable(env, raw, cookiecutter_dict)
    assert "undefined" in str(excinfo.value).lower()
