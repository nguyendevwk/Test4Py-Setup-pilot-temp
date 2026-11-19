import json
import os
import re
from pathlib import Path

import pytest

from cookiecutter.prompt import choose_nested_template


@pytest.fixture
def repo_dir(tmp_path):
    """Create a temporary repository directory with a dummy template folder."""
    (tmp_path / "templates" / "basic").mkdir(parents=True)
    return tmp_path


def test_choose_nested_template_new_style(repo_dir):
    """Test that the function selects the first template when no_input=True."""
    context = {
        "cookiecutter": {
            "template": [
                "basic (templates/basic)",
                "advanced (templates/advanced)",
            ]
        }
    }
    # Create the advanced template directory to ensure path resolution works
    (repo_dir / "templates" / "advanced").mkdir(parents=True)

    result = choose_nested_template(context, repo_dir, no_input=True)
    expected = str((repo_dir / "templates" / "basic").resolve())
    assert result == expected


def test_choose_nested_template_old_style_with_prompts(repo_dir):
    """Test that the function correctly parses the template path from the
    prompt string when __prompts__ are present."""
    context = {
        "cookiecutter": {
            "__prompts__": {"template": "Select a template"},
            "template": [
                "basic (templates/basic)",
                "advanced (templates/advanced)",
            ],
        }
    }
    # Ensure the selected template exists
    (repo_dir / "templates" / "advanced").mkdir(parents=True)

    result = choose_nested_template(context, repo_dir, no_input=True)
    expected = str((repo_dir / "templates" / "advanced").resolve())
    assert result == expected


def test_choose_nested_template_illegal_path(repo_dir):
    """Test that an absolute path in the template string raises ValueError."""
    context = {
        "cookiecutter": {
            "template": [
                f"/absolute/path/to/template (templates/basic)",
            ]
        }
    }
    with pytest.raises(ValueError, match="Illegal template path"):
        choose_nested_template(context, repo_dir, no_input=True)
