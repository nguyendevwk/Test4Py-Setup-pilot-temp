import importlib.util
import os
import sys
import types
from pathlib import Path

import pytest

from apimd.loader import gen_api


def _create_module(tmp_path: Path, name: str, content: str) -> Path:
    """Create a Python module file in tmp_path and return its path."""
    module_path = tmp_path / f"{name}.py"
    module_path.write_text(content)
    return module_path


def test_gen_api_creates_markdown(tmp_path: Path):
    """Normal case: a valid module is found and a markdown file is written."""
    # Create a simple module with a function
    mod_name = "sample_module"
    _create_module(tmp_path, mod_name, "def foo():\n    return 42\n")

    # Run gen_api with the temporary directory as pwd
    docs = gen_api(
        root_names={mod_name: mod_name},
        pwd=str(tmp_path),
        prefix=str(tmp_path / "docs"),
        dry=False,
    )

    # Verify that one document was returned
    assert len(docs) == 1
    doc = docs[0]
    # Header should be present
    assert doc.startswith("# Sample Module API\n\n")
    # The function definition should appear in the doc
    assert "def foo()" in doc

    # Verify that the markdown file was created
    md_path = tmp_path / "docs" / f"{mod_name.replace('_', '-')}-api.md"
    assert md_path.is_file()
    # File content should match the returned doc
    assert md_path.read_text() == doc


def test_gen_api_dry_run(tmp_path: Path):
    """Dry run: no files are written, but docs are returned."""
    # Create a simple module
    mod_name = "dry_module"
    _create_module(tmp_path, mod_name, "def bar():\n    return 'bar'\n")

    # Run gen_api with dry=True
    docs = gen_api(
        root_names={mod_name: mod_name},
        pwd=str(tmp_path),
        prefix=str(tmp_path / "docs"),
        dry=True,
    )

    # Verify that one document was returned
    assert len(docs) == 1
    doc = docs[0]
    assert doc.startswith("# Dry Module API\n\n")
    assert "def bar()" in doc

    # Verify that no markdown file was created
    md_path = tmp_path / "docs" / f"{mod_name.replace('_', '-')}-api.md"
    assert not md_path.exists()


def test_gen_api_missing_module(tmp_path: Path):
    """Error case: a non‑existent module is skipped and no docs are returned."""
    # No module file is created
    mod_name = "nonexistent_module"

    # Run gen_api
    docs = gen_api(
        root_names={mod_name: mod_name},
        pwd=str(tmp_path),
        prefix=str(tmp_path / "docs"),
        dry=False,
    )

    # No documents should be returned
    assert docs == []

    # No markdown directory should be created
    docs_dir = tmp_path / "docs"
    assert not docs_dir.exists()
