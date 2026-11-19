import importlib
import os
import sys
import types
import tempfile
import shutil
from pathlib import Path

import pytest

from apimd.loader import gen_api


def _create_module(tmp_path: Path, name: str, content: str):
    """Create a simple module file under tmp_path."""
    module_path = tmp_path / f"{name}.py"
    module_path.write_text(content)
    return module_path


def test_gen_api_creates_markdown(tmp_path):
    """Normal case: a module with a simple function should produce a markdown file."""
    # Create a temporary module
    mod_name = "sample_module"
    _create_module(tmp_path, mod_name, "def foo():\n    return 42\n")

    # Ensure the module is importable
    sys.path.insert(0, str(tmp_path))
    try:
        # Call gen_api
        docs = gen_api({"Sample": mod_name}, prefix=str(tmp_path / "docs"))
    finally:
        sys.path.pop(0)

    # Verify that a markdown file was created
    md_path = tmp_path / "docs" / f"{mod_name.replace('_', '-')}-api.md"
    assert md_path.is_file()
    content = md_path.read_text()
    # The content should contain the function signature
    assert "def foo()" in content
    # The title should be present
    assert "# Sample API" in content
    # The returned docs list should contain the same content
    assert docs[0] == content


def test_gen_api_missing_module(tmp_path):
    """If a module cannot be found, it should be skipped and not produce a file."""
    # No module created
    mod_name = "nonexistent_module"
    # Call gen_api
    docs = gen_api({"Missing": mod_name}, prefix=str(tmp_path / "docs"))
    # No docs should be returned
    assert docs == []
    # No markdown file should exist
    md_path = tmp_path / "docs" / f"{mod_name.replace('_', '-')}-api.md"
    assert not md_path.exists()


def test_gen_api_dry_run(tmp_path):
    """Dry run should not write files but still return the generated docs."""
    # Create a temporary module
    mod_name = "dry_module"
    _create_module(tmp_path, mod_name, "def bar(x):\n    return x * 2\n")

    # Ensure the module is importable
    sys.path.insert(0, str(tmp_path))
    try:
        docs = gen_api({"Dry": mod_name}, prefix=str(tmp_path / "docs"), dry=True)
    finally:
        sys.path.pop(0)

    # No markdown file should be written
    md_path = tmp_path / "docs" / f"{mod_name.replace('_', '-')}-api.md"
    assert not md_path.exists()
    # The docs list should contain the generated content
    assert len(docs) == 1
    assert "def bar(x)" in docs[0]
    assert "# Dry API" in docs[0]
