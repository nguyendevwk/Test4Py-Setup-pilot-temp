import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict

import pytest

from cookiecutter.prompt import choose_nested_template


def test_choose_nested_template_new_style_no_input(tmp_path: Path):
    """When a new‑style template dict is present, no_input=True should pick the first."""
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    # Create a fake template directory
    (repo_dir / "template_a").mkdir()
    # Context with a new‑style templates dict
    context: Dict[str, Any] = {
        "cookiecutter": {
            "templates": {
                "a": {"title": "Template A", "path": "template_a"},
                "b": {"title": "Template B", "path": "template_b"},
            }
        }
    }
    result = choose_nested_template(context, repo_dir, no_input=True)
    expected = str((repo_dir / "template_a").resolve())
    assert result == expected


def test_choose_nested_template_illegal_absolute_path(tmp_path: Path):
    """If the resolved template path is absolute, a ValueError is raised."""
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    # Context with a new‑style templates dict pointing to an absolute path
    context: Dict[str, Any] = {
        "cookiecutter": {
            "templates": {
                "a": {"title": "Template A", "path": "/absolute/path"},
            }
        }
    }
    with pytest.raises(ValueError, match="Illegal template path"):
        choose_nested_template(context, repo_dir, no_input=True)


def test_choose_nested_template_old_style_no_input(tmp_path: Path):
    """When no new‑style templates are present, the old style list is used."""
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    # Create a fake template directory
    (repo_dir / "old_template").mkdir()
    # Context with old‑style template list
    context: Dict[str, Any] = {
        "cookiecutter": {
            "template": [
                "old_template (old_template)",
                "other_template (other_template)",
            ]
        }
    }
    result = choose_nested_template(context, repo_dir, no_input=True)
    expected = str((repo_dir / "old_template").resolve())
    assert result == expected
