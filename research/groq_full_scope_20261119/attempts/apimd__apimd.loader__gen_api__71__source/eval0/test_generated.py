import importlib.util
import os
import sys
from pathlib import Path

import pytest

from apimd.loader import gen_api


def _create_module(tmp_path: Path, name: str, content: str) -> Path:
    """Create a Python module file in tmp_path and return its path."""
    module_path = tmp_path / f"{name}.py"
    module_path.write_text(content)
    return module_path


def test_gen_api_creates_markdown(tmp_path):
    """Normal case: a valid module is loaded and a markdown file is written."""
    # Create a simple module with one function
    mod_name = "sample_module"
    mod_content = """
def hello(name: str) -> str:
    return f"Hello, {name}"
"""
    _create_module(tmp_path, mod_name, mod_content)

    # Ensure the module can be found
    sys.path.insert(0, str(tmp_path))

    # Run gen_api
    docs = gen_api({"Sample": mod_name}, prefix=str(tmp_path / "docs"))

    # Verify that a markdown file was created
    md_path = tmp_path / "docs" / f"{mod_name.replace('_', '-')}-api.md"
    assert md_path.is_file(), "Markdown file was not created"

    # Verify the content of the markdown file
    md_text = md_path.read_text()
    assert "# Sample API" in md_text
    assert "def hello(name: str) -> str:" in md_text

    # Verify that the returned docs list contains the same content
    assert docs == [md_text]


def test_gen_api_skips_missing_module(tmp_path):
    """Boundary case: a non‑existent module is skipped and no file is written."""
    # Run gen_api with a module that does not exist
    docs = gen_api({"Missing": "nonexistent_module"}, prefix=str(tmp_path / "docs"))

    # No docs should be returned
    assert docs == []

    # No markdown file should be created
    md_path = tmp_path / "docs" / "nonexistent-module-api.md"
    assert not md_path.exists(), "Markdown file should not exist for missing module"


def test_gen_api_dry_run(tmp_path):
    """Error/edge case: dry run mode should not write files but still return docs."""
    # Create a module
    mod_name = "dry_module"
    mod_content = """
def add(a: int, b: int) -> int:
    return a + b
"""
    _create_module(tmp_path, mod_name, mod_content)

    # Ensure the module can be found
    sys.path.insert(0, str(tmp_path))

    # Run gen_api in dry mode
    docs = gen_api({"Dry": mod_name}, prefix=str(tmp_path / "docs"), dry=True)

    # No markdown file should be written
    md_path = tmp_path / "docs" / f"{mod_name.replace('_', '-')}-api.md"
    assert not md_path.exists(), "Markdown file should not be written in dry mode"

    # Docs should still contain the generated content
    assert docs, "Docs should not be empty in dry mode"
    assert "def add(a: int, b: int) -> int:" in docs[0]
