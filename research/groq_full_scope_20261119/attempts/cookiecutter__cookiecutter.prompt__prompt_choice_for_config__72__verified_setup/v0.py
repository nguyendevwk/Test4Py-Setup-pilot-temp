import json
import os
import re
import sys
from collections import OrderedDict
from collections.abc import Iterator
from itertools import starmap
from pathlib import Path
from typing import TYPE_CHECKING, Any, TypeAlias
from jinja2 import Environment, FileSystemLoader
import pytest

from cookiecutter.prompt import prompt_choice_for_config, render_variable
from cookiecutter.utils import create_env_with_context

def test_prompt_choice_for_config_no_input_returns_first(tmp_path):
    # Setup a minimal environment and cookiecutter dict
    env = Environment(loader=FileSystemLoader(tmp_path))
    cookiecutter_dict = {"project_name": "demo"}
    options = ["{{ project_name }}", "other"]
    # No input: should return the first rendered option
    result = prompt_choice_for_config(
        cookiecutter_dict=cookiecutter_dict,
        env=env,
        key="project_name",
        options=options,
        no_input=True,
        prompts=None,
        prefix="",
    )
    assert result == "demo"

def test_prompt_choice_for_config_empty_options_raises(tmp_path):
    env = Environment(loader=FileSystemLoader(tmp_path))
    cookiecutter_dict = {}
    options = []
    with pytest.raises(ValueError, match="The list of choices is empty"):
        prompt_choice_for_config(
            cookiecutter_dict=cookiecutter_dict,
            env=env,
            key="empty",
            options=options,
            no_input=True,
            prompts=None,
            prefix="",
        )

def test_prompt_choice_for_config_rendering(tmp_path):
    # Create a template file that uses a variable
    (tmp_path / "template.txt").write_text("Hello {{ name }}")
    env = Environment(loader=FileSystemLoader(tmp_path))
    cookiecutter_dict = {"name": "Alice"}
    options = ["{{ name }}", "Bob"]
    # No input: should render the first option using the env
    result = prompt_choice_for_config(
        cookiecutter_dict=cookiecutter_dict,
        env=env,
        key="name",
        options=options,
        no_input=True,
        prompts=None,
        prefix="",
    )
    assert result == "Alice"
