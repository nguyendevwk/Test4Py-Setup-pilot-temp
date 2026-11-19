import json
import os
import re
import sys
from pathlib import Path

import pytest

from cookiecutter.prompt import choose_nested_template


def test_choose_nested_template_new_style(tmp_path):
    """Test new style template selection with a config dict."""
    # Create a fake template file in the repo
    template_file = tmp_path / "nested" / "template1"
    template_file.parent.mkdir(parents=True)
    template_file.touch()

    context = {
        "cookiecutter": {
            "__prompts__": {},
            "templates": {
                "option1": {"path": "nested/template1"},
                "option2": {"path": "nested/template2"},
            },
        }
    }

    # No input: should pick the first key in the dict
    result = choose_nested_template(context, tmp_path, no_input=True)
    expected = str((tmp_path / "nested/template1").resolve())
    assert result == expected
    assert Path(result).exists()


def test_choose_nested_template_old_style(tmp_path):
    """Test old style template selection with a list of strings."""
    # Create a fake template file in the repo
    template_file = tmp_path / "nested" / "template2"
    template_file.parent.mkdir(parents=True)
    template_file.touch()

    context = {
        "cookiecutter": {
            "__prompts__": {},
            "template": [
                "optionA (nested/template2)",
                "optionB (nested/template3)",
            ],
        }
    }

    # No input: should pick the first option
    result = choose_nested_template(context, tmp_path, no_input=True)
    expected = str((tmp_path / "nested/template2").resolve())
    assert result == expected
    assert Path(result).exists()


def test_choose_nested_template_illegal_path(tmp_path):
    """Test that an absolute template path raises ValueError."""
    # Create a fake template file in the repo
    template_file = tmp_path / "nested" / "template1"
    template_file.parent.mkdir(parents=True)
    template_file.touch()

    context = {
        "cookiecutter": {
            "__prompts__": {},
            "templates": {
                "option1": {"path": str(template_file.resolve())},  # absolute path
            },
        }
    }

    with pytest.raises(ValueError, match="Illegal template path"):
        choose_nested_template(context, tmp_path, no_input=True)
