import importlib
import os
import sys
import types
from pathlib import Path

import pytest

from apimd.loader import gen_api


@pytest.fixture
def simple_module(tmp_path):
    """Create a temporary Python module with a simple function."""
    mod_dir = tmp_path / "simple_pkg"
    mod_dir.mkdir()
    (mod_dir / "__init__.py").write_text("")
    (mod_dir / "utils.py").write_text(
        """
def add(a, b):
    return a + b
"""
    )
    sys.path.insert(0, str(tmp_path))
    yield "simple_pkg.utils"
    sys.path.pop(0)


def test_gen_api_creates_markdown(tmp_path, simple_module):
    """gen_api should create a markdown file with the expected header and content."""
    docs = gen_api({"Simple Utils": simple_module}, prefix=str(tmp_path / "docs"))
    # One document should be returned
    assert len(docs) == 1
    doc = docs[0]
    # Header should match level 1
    assert doc.startswith("# Simple Utils API\n\n")
    # The markdown should contain the function signature
    assert "def add(a, b):" in doc
    # The file should exist
    expected_file = tmp_path / "docs" / "simple-pkg-utils-api.md"
    assert expected_file.is_file()
    # File content should match the returned doc
    assert expected_file.read_text() == doc


def test_gen_api_skips_missing_module(tmp_path):
    """If a module cannot be found, gen_api should skip it and not create a file."""
    docs = gen_api({"Missing": "nonexistent.module"}, prefix=str(tmp_path / "docs"))
    # No documents should be returned
    assert docs == []
    # No files should be created
    assert not (tmp_path / "docs").exists()


def test_gen_api_with_custom_level_and_dry(tmp_path, simple_module):
    """gen_api should respect custom level and dry flag (no file creation)."""
    docs = gen_api(
        {"Custom": simple_module},
        prefix=str(tmp_path / "docs"),
        level=3,
        dry=True,
    )
    # One document should be returned
    assert len(docs) == 1
    doc = docs[0]
    # Header should use level 3
    assert doc.startswith("### Custom API\n\n")
    # No file should be written because dry=True
    expected_file = tmp_path / "docs" / "simple-pkg-utils-api.md"
    assert not expected_file.exists()
