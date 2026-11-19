import importlib
import os
import sys
from pathlib import Path

import pytest

from apimd.loader import gen_api


@pytest.fixture
def module_dir(tmp_path):
    """Create a temporary directory with a simple Python module."""
    mod_dir = tmp_path / "pkg"
    mod_dir.mkdir()
    (mod_dir / "__init__.py").write_text("")
    (mod_dir / "mymodule.py").write_text(
        """
def hello():
    return "world"
"""
    )
    # Make the directory importable
    sys.path.insert(0, str(mod_dir))
    yield mod_dir
    sys.path.pop(0)


def test_gen_api_creates_markdown_file(module_dir, tmp_path):
    """Normal generation: a markdown file is created with expected content."""
    root_names = {"My Module": "mymodule"}
    prefix = tmp_path / "docs"
    docs = gen_api(root_names, prefix=str(prefix), level=2, dry=False)

    # One document should be returned
    assert len(docs) == 1
    doc = docs[0]
    # Header should match level
    assert doc.startswith("## My Module API\n\n")
    # The module's function should appear in the doc
    assert "def hello" in doc

    # File should exist
    expected_file = prefix / "mymodule-api.md"
    assert expected_file.is_file()
    file_content = expected_file.read_text()
    assert file_content == doc


def test_gen_api_dry_run(module_dir, tmp_path):
    """Dry run: no files are written, but docs are returned."""
    root_names = {"My Module": "mymodule"}
    prefix = tmp_path / "docs"
    docs = gen_api(root_names, prefix=str(prefix), level=1, dry=True)

    # One document should be returned
    assert len(docs) == 1
    doc = docs[0]
    assert doc.startswith("# My Module API\n\n")

    # No file should be created
    expected_file = prefix / "mymodule-api.md"
    assert not expected_file.exists()


def test_gen_api_missing_module(tmp_path):
    """If a module cannot be found, it is skipped and no file is created."""
    root_names = {"Missing": "nonexistent_module"}
    prefix = tmp_path / "docs"
    docs = gen_api(root_names, prefix=str(prefix), level=1, dry=False)

    # No documents should be returned
    assert docs == []

    # No file should be created
    expected_file = prefix / "nonexistent_module-api.md"
    assert not expected_file.exists()
