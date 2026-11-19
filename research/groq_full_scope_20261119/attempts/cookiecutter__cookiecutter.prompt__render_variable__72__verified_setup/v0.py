import json
import os
import re
import sys
from collections import OrderedDict
from collections.abc import Iterator
from itertools import starmap
from pathlib import Path
from typing import TYPE_CHECKING, Any, TypeAlias
from jinja2 import Environment
import pytest
from cookiecutter.prompt import render_variable

def test_render_variable_basic_and_none_and_bool():
    env = Environment()
    cookiecutter_dict = {"project_name": "Peanut Butter Cookie"}
    # Basic string rendering
    raw = "{{ cookiecutter.project_name.replace(' ', '_') }}"
    rendered = render_variable(env, raw, cookiecutter_dict)
    assert rendered == "Peanut_Butter_Cookie"

    # None returns None
    assert render_variable(env, None, cookiecutter_dict) is None

    # Boolean returns same boolean
    assert render_variable(env, True, cookiecutter_dict) is True
    assert render_variable(env, False, cookiecutter_dict) is False

def test_render_variable_nested_structures():
    env = Environment()
    cookiecutter_dict = {"project_name": "Peanut Butter Cookie"}
    raw = {
        "repo_name": "{{ cookiecutter.project_name.replace(' ', '_') }}",
        "tags": ["{{ cookiecutter.project_name }}", "test"],
        "config": {"enabled": True, "value": "{{ cookiecutter.project_name }}"},
    }
    rendered = render_variable(env, raw, cookiecutter_dict)
    assert isinstance(rendered, dict)
    assert rendered["repo_name"] == "Peanut_Butter_Cookie"
    assert rendered["tags"] == ["Peanut Butter Cookie", "test"]
    assert rendered["config"]["enabled"] is True
    assert rendered["config"]["value"] == "Peanut Butter Cookie"

def test_render_variable_undefined_variable_raises():
    env = Environment()
    cookiecutter_dict = {"project_name": "Peanut Butter Cookie"}
    raw = "{{ cookiecutter.undefined_var }}"
    with pytest.raises(Exception) as excinfo:
        render_variable(env, raw, cookiecutter_dict)
    # The exception should be a Jinja2 UndefinedError
    assert "undefined" in str(excinfo.value).lower()
