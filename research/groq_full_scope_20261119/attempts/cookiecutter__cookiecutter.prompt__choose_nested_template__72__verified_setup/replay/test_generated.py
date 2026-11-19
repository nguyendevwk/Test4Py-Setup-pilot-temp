import json
import os
import re
import sys
from pathlib import Path
import pytest
from cookiecutter.prompt import choose_nested_template

@pytest.fixture
def repo_dir(tmp_path):
    """Create a temporary repository directory with a dummy template."""
    repo = tmp_path / "repo"
    repo.mkdir()
    # create a nested template directory
    (repo / "templates" / "basic").mkdir(parents=True)
    return repo

def test_choose_nested_template_new_style_no_input(repo_dir):
    """Test selection with new style config and no user input."""
    context = {
        "cookiecutter": {
            "templates": {
                "basic": {"path": "templates/basic"},
                "advanced": {"path": "templates/advanced"},
            },
            "__prompts__": {},
        }
    }
    # Force selection of 'basic' by setting no_input True
    result = choose_nested_template(context, repo_dir, no_input=True)
    expected = str((repo_dir / "templates/basic").resolve())
    assert result == expected

def test_choose_nested_template_old_style_no_input(repo_dir):
    """Test selection with old style config and no user input."""
    # Create a dummy template file to match regex
    (repo_dir / "old_template").write_text("content")
    context = {
        "cookiecutter": {
            "template": [
                "old_template (old_template)",
                "unused (unused)",
            ],
            "__prompts__": {},
        }
    }
    result = choose_nested_template(context, repo_dir, no_input=True)
    expected = str((repo_dir / "old_template").resolve())
    assert result == expected

def test_choose_nested_template_illegal_path_raises(repo_dir):
    """Test that an absolute template path raises ValueError."""
    context = {
        "cookiecutter": {
            "templates": {
                "bad": {"path": str(Path("/absolute/path"))},
            },
            "__prompts__": {},
        }
    }
    with pytest.raises(ValueError, match="Illegal template path"):
        choose_nested_template(context, repo_dir, no_input=True)
