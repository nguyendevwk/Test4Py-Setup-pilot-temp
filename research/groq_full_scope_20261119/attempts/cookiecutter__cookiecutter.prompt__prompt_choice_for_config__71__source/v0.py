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

from cookiecutter.prompt import prompt_choice_for_config
from cookiecutter.utils import create_env_with_context

def test_prompt_choice_for_config_returns_first_option(tmp_path):
    """When no_input is True, the function should return the first rendered option."""
    # Prepare a simple cookiecutter dict and options
    cookiecutter_dict = {"project_name": "demo"}
    env = Environment()
    options = ["{{ project_name }}", "other"]
    # Call the function with no_input=True
    result = prompt_choice_for_config(
        cookiecutter_dict=cookiecutter_dict,
        env=env,
        key="project_name",
        options=options,
        no_input=True,
        prompts=None,
        prefix="",
    )
    # The first option should be rendered to "demo"
    assert result == "demo"

def test_prompt_choice_for_config_empty_options_raises(tmp_path):
    """When no_input is True and options list is empty, a ValueError should be raised."""
    cookiecutter_dict = {}
    env = Environment()
    options = []
    with pytest.raises(ValueError, match="The list of choices is empty"):
        prompt_choice_for_config(
            cookiecutter_dict=cookiecutter_dict,
            env=env,
            key="dummy",
            options=options,
            no_input=True,
            prompts=None,
            prefix="",
        )

def test_prompt_choice_for_config_renders_template_options(tmp_path):
    """Options containing Jinja2 expressions should be rendered correctly."""
    cookiecutter_dict = {"name": "Alice", "age": 30}
    env = Environment()
    options = ["{{ name }} is {{ age }} years old", "Unknown"]
    # Use no_input to avoid interactive prompt
    result = prompt_choice_for_config(
        cookiecutter_dict=cookiecutter_dict,
        env=env,
        key="name",
        options=options,
        no_input=True,
        prompts=None,
        prefix="",
    )
    assert result == "Alice is 30 years old"
