import importlib
import os
import sys
import types
from pathlib import Path

import pytest

from apimd.loader import gen_api


@pytest.fixture
def simple_module(tmp_path):
    """Create a simple Python module with a function and a class."""
    mod_dir = tmp_path / "pkg"
    mod_dir.mkdir()
    (mod_dir / "__init__.py").write_text("")
    mod_file = mod_dir / "mymodule.py"
    mod_file.write_text(
        """
def hello(name: str) -> str:
    \"\"\"Return greeting.\"\"\"
    return f"Hello, {name}!"

class Greeter:
    def __init__(self, prefix: str = "Hi"):
        self.prefix = prefix

    def greet(self, name: str) -> str:
        return f"{self.prefix}, {name}!"
"""
    )
    # Ensure the module can be imported
    sys.path.insert(0, str(tmp_path))
    yield mod_file
    sys.path.pop(0)


def test_gen_api_creates_markdown(tmp_path, simple_module):
    """Test that gen_api generates a markdown file with expected content."""
    root_names = {"My Module": "pkg.mymodule"}
    docs = gen_api(root_names, prefix=str(tmp_path / "docs"))
    # One document should be returned
    assert len(docs) == 1
    # The markdown file should exist
    md_file = tmp_path / "docs" / "mymodule-api.md"
    assert md_file.is_file()
    content = md_file.read_text()
    # The file should contain the function signature and class definition
    assert "def hello(name: str) -> str:" in content
    assert "class Greeter:" in content
    # The title should be correct
    assert content.startswith("# My Module API\n\n")


def test_gen_api_skips_missing_module(tmp_path):
    """Test that a non‑existent module is skipped and no file is created."""
    root_names = {"Missing": "nonexistent.module"}
    docs = gen_api(root_names, prefix=str(tmp_path / "docs"))
    # No documents should be returned
    assert docs == []
    # No markdown directory should be created
    assert not (tmp_path / "docs").exists()


def test_gen_api_empty_root_names(tmp_path):
    """Test that an empty root_names dict returns an empty list and creates no files."""
    docs = gen_api({}, prefix=str(tmp_path / "docs"))
    assert docs == []
    # The docs directory should still be created because gen_api creates it if missing
    assert (tmp_path / "docs").is_dir()
