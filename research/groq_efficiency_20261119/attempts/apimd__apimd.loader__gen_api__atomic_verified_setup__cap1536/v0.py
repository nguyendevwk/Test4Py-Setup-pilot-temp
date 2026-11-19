import sys
import os
import importlib.util
import importlib.machinery
import importlib
import types
import pathlib
import pytest

from apimd.loader import gen_api

@pytest.fixture
def temp_module(tmp_path):
    """Create a temporary Python module with a simple function."""
    mod_dir = tmp_path / "mymodule"
    mod_dir.mkdir()
    mod_file = mod_dir / "example.py"
    mod_file.write_text(
        """
def hello():
    return "world"
"""
    )
    # Add the module directory to sys.path so it can be found
    sys.path.insert(0, str(mod_dir))
    yield "example"
    # Clean up sys.path
    sys.path.remove(str(mod_dir))

def test_gen_api_creates_markdown_file(tmp_path, temp_module):
    """Normal case: a module is found and a markdown file is written."""
    prefix = tmp_path / "docs"
    docs = gen_api({"Example": temp_module}, prefix=str(prefix))
    # One document should be returned
    assert len(docs) == 1
    # The markdown file should exist
    expected_file = prefix / f"{temp_module.replace('_', '-')}-api.md"
    assert expected_file.is_file()
    # The content should start with a level 1 header
    content = expected_file.read_text()
    assert content.startswith("# Example API\n\n")
    # The content should contain the function definition
    assert "def hello" in content

def test_gen_api_skips_missing_module(tmp_path):
    """If a module cannot be found, it is skipped and no file is created."""
    prefix = tmp_path / "docs"
    docs = gen_api({"Missing": "nonexistent_module"}, prefix=str(prefix))
    # No documents should be returned
    assert docs == []
    # No markdown file should exist
    assert not (prefix / "nonexistent-module-api.md").exists()

def test_gen_api_dry_run(tmp_path, temp_module):
    """Dry run should not create files but return the document content."""
    prefix = tmp_path / "docs"
    docs = gen_api({"Example": temp_module}, prefix=str(prefix), dry=True)
    # One document should be returned
    assert len(docs) == 1
    # No markdown file should be created
    expected_file = prefix / f"{temp_module.replace('_', '-')}-api.md"
    assert not expected_file.exists()
    # The returned document should contain the function definition
    assert "def hello" in docs[0]
