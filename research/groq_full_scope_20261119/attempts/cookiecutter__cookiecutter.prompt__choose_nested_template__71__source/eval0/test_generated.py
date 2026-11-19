import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict

import pytest

from cookiecutter.prompt import choose_nested_template


def test_choose_nested_template_new_style_no_input(tmp_path: Path):
    """Test normal selection with new style config and no_input=True."""
    # Create a fake template directory
    template_dir = tmp_path / "my_template"
    template_dir.mkdir()
    # Context with new style config
    context: Dict[str, Any] = {
        "cookiecutter": {
            "templates": {
                "option1": {"path": "my_template"},
                "option2": {"path": "other_template"},
            },
            "__prompts__": {},
        }
    }
    # Call function with no_input=True to avoid prompting
    result = choose_nested_template(context, tmp_path, no_input=True)
    # The result should be the absolute path to my_template
    expected = str((tmp_path / "my_template").resolve())
    assert result == expected
    # Ensure the returned path is not absolute relative to repo_dir
    assert Path(result).is_absolute()
    assert not Path(result).is_absolute() is False  # sanity check


def test_choose_nested_template_old_style_error(tmp_path: Path):
    """Test error when old style config returns an absolute template path."""
    # Create a fake template directory with absolute path
    abs_template = tmp_path / "abs_template"
    abs_template.mkdir()
    # Context with old style config
    context: Dict[str, Any] = {
        "cookiecutter": {
            "template": [
                f"{abs_template} (Absolute path)",
            ],
            "__prompts__": {},
        }
    }
    # The function should raise ValueError because the path is absolute
    with pytest.raises(ValueError, match="Illegal template path"):
        choose_nested_template(context, tmp_path, no_input=True)


def test_choose_nested_template_old_style_success(tmp_path: Path):
    """Test successful selection with old style config and no_input=True."""
    # Create a fake template directory
    template_dir = tmp_path / "old_template"
    template_dir.mkdir()
    # Context with old style config
    context: Dict[str, Any] = {
        "cookiecutter": {
            "template": [
                f"{template_dir} (Old style)",
            ],
            "__prompts__": {},
        }
    }
    # Call function with no_input=True
    result = choose_nested_template(context, tmp_path, no_input=True)
    # The result should be the absolute path to old_template
    expected = str((tmp_path / "old_template").resolve())
    assert result == expected
    # Ensure the returned path is not absolute relative to repo_dir
    assert Path(result).is_absolute()
