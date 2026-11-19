import json
import os
import re
import sys
import pytest
from collections import OrderedDict
from pathlib import Path
from typing import Any
from jinja2 import Environment
from cookiecutter.prompt import prompt_choice_for_config, render_variable

# Helper to create a minimal environment
def make_env(context: dict[str, Any]) -> Environment:
    env = Environment()
    env.globals.update(context)
    return env

def test_prompt_choice_for_config_no_input_returns_first_option(tmp_path: Path):
    # Setup
    cookiecutter_dict = {"project_name": "demo"}
    env = make_env(cookiecutter_dict)
    key = "project_name"
    options = ["demo", "test"]
    # Execute
    result = prompt_choice_for_config(
        cookiecutter_dict=cookiecutter_dict,
        env=env,
        key=key,
        options=options,
        no_input=True,
        prompts=None,
        prefix="",
    )
    # Assert
    assert result == "demo"

def test_prompt_choice_for_config_no_input_empty_options_raises():
    # Setup
    cookiecutter_dict = {}
    env = make_env(cookiecutter_dict)
    key = "empty"
    options = []
    # Execute & Assert
    with pytest.raises(ValueError, match="The list of choices is empty"):
        prompt_choice_for_config(
            cookiecutter_dict=cookiecutter_dict,
            env=env,
            key=key,
            options=options,
            no_input=True,
            prompts=None,
            prefix="",
        )

def test_prompt_choice_for_config_renders_template_options(tmp_path: Path):
    # Setup
    cookiecutter_dict = {"lang": "Python"}
    env = make_env(cookiecutter_dict)
    key = "lang"
    options = ["{{ lang }}", "JavaScript"]
    # Execute
    result = prompt_choice_for_config(
        cookiecutter_dict=cookiecutter_dict,
        env=env,
        key=key,
        options=options,
        no_input=True,
        prompts=None,
        prefix="",
    )
    # Assert
    assert result == "Python"
