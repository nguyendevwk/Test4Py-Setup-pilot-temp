import importlib
import os
import sys
import types
from pathlib import Path

import pytest

from apimd.loader import gen_api


def _create_module(tmp_path: Path, name: str, content: str) -> Path:
    """Create a temporary Python module file."""
    module_path = tmp_path / f"{name}.py"
    module_path.write_text(content)
    return module_path


def test_gen_api_creates_markdown(tmp_path):
    """Normal case: a valid module is loaded and a markdown file is written."""
    # Create a simple module with a function
    mod_name = "sample_module"
    _create_module(tmp_path, mod_name, "def hello():\n    return 'hi'\n")

    # Ensure the module can be imported
    sys.path.insert(0, str(tmp_path))
    try:
        importlib.invalidate_caches()
        importlib.import_module(mod_name)
    finally:
        sys.path.pop(0)

    # Run gen_api
    docs = gen_api({"Sample": mod_name}, pwd=str(tmp_path), prefix=str(tmp_path / "docs"), dry=False)

    # Verify that one document was returned
    assert len(docs) == 1
    doc = docs[0]
    # The document should start with a level 1 header
    assert doc.startswith("# Sample API\n\n")
    # The document should contain the function signature
    assert "def hello()" in doc

    # Verify that the markdown file was created
    md_path = tmp_path / "docs" / f"{mod_name.replace('_', '-')}-api.md"
    assert md_path.is_file()
    assert md_path.read_text() == doc


def test_gen_api_skips_missing_module(tmp_path):
    """Error case: a non‑existent module is skipped and no docs are returned."""
    # Run gen_api with a module that does not exist
    docs = gen_api({"Missing": "nonexistent_module"}, prefix=str(tmp_path / "docs"), dry=False)

    # No documents should be returned
    assert docs == []

    # No markdown file should be created
    md_path = tmp_path / "docs" / "nonexistent-module-api.md"
    assert not md_path.exists()


def test_gen_api_prefix_already_exists(tmp_path):
    """Boundary case: the prefix directory already exists; gen_api should not fail."""
    # Create the prefix directory beforehand
    prefix_dir = tmp_path / "existing_docs"
    prefix_dir.mkdir()

    # Create a simple module
    mod_name = "another_module"
    _create_module(tmp_path, mod_name, "def add(a, b):\n    return a + b\n")

    # Ensure the module can be imported
    sys.path.insert(0, str(tmp_path))
    try:
        importlib.invalidate_caches()
        importlib.import_module(mod_name)
    finally:
        sys.path.pop(0)

    # Run gen_api
    docs = gen_api({"Another": mod_name}, prefix=str(prefix_dir), dry=False)

    # Verify that one document was returned
    assert len(docs) == 1

    # Verify that the markdown file was written into the existing directory
    md_path = prefix_dir / f"{mod_name.replace('_', '-')}-api.md"
    assert md_path.is_file()
    assert md_path.read_text() == docs[0]
