import json
import os
import re
import sys
from pathlib import Path
import pytest
from cookiecutter.prompt import choose_nested_template

def test_choose_nested_template_new_style_no_input(tmp_path):
    # Setup context with new style config
    context = {
        "cookiecutter": {
            "templates": {
                "option1": {"path": "subdir/template1"},
                "option2": {"path": "subdir/template2"},
            },
            "__prompts__": {},
        }
    }
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    # Create dummy template directories
    (repo_dir / "subdir/template1").mkdir(parents=True)
    (repo_dir / "subdir/template2").mkdir(parents=True)

    # Call with no_input=True to avoid interactive prompt
    result = choose_nested_template(context, repo_dir, no_input=True)

    # The function should return the path to the first template
    expected = str((repo_dir / "subdir/template1").resolve())
    assert result == expected

def test_choose_nested_template_old_style_no_input(tmp_path):
    # Setup context with old style config
    context = {
        "cookiecutter": {
            "template": [
                "Template A (subdir/templateA)",
                "Template B (subdir/templateB)",
            ],
            "__prompts__": {},
        }
    }
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    # Create dummy template directories
    (repo_dir / "subdir/templateA").mkdir(parents=True)
    (repo_dir / "subdir/templateB").mkdir(parents=True)

    # Call with no_input=True to avoid interactive prompt
    result = choose_nested_template(context, repo_dir, no_input=True)

    # The function should return the path to the first template
    expected = str((repo_dir / "subdir/templateA").resolve())
    assert result == expected

def test_choose_nested_template_illegal_absolute_path(tmp_path):
    # Setup context with absolute path in config
    context = {
        "cookiecutter": {
            "templates": {
                "option1": {"path": str(tmp_path / "abs_template")},
            },
            "__prompts__": {},
        }
    }
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    # Create dummy absolute template directory
    (tmp_path / "abs_template").mkdir(parents=True)

    # Expect ValueError due to absolute path
    with pytest.raises(ValueError, match="Illegal template path"):
        choose_nested_template(context, repo_dir, no_input=True)
