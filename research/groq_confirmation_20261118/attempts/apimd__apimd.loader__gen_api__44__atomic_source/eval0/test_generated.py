import importlib
import os
import sys
import types
from pathlib import Path

import pytest

from apimd.loader import gen_api


def _create_module(tmp_path: Path, name: str, code: str) -> Path:
    """Create a simple module file under tmp_path."""
    module_path = tmp_path / f"{name}.py"
    module_path.write_text(code)
    return module_path


def test_gen_api_creates_markdown(tmp_path: Path):
    """Normal case: a valid module is found and a markdown file is written."""
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
    docs = gen_api({"Sample": mod_name}, prefix=str(tmp_path / "docs"))

    # One document should be returned
    assert len(docs) == 1
    doc = docs[0]
    # The document should start with a level-1 header
    assert doc.startswith("# Sample API\n\n")
    # The markdown file should exist
    md_path = tmp_path / "docs" / f"{mod_name.replace('_', '-')}-api.md"
    assert md_path.is_file()
    # The file content should match the returned doc
    assert md_path.read_text() == doc


def test_gen_api_skips_missing_module(tmp_path: Path):
    """When a module cannot be found, it is skipped and no file is created."""
    # No module created
    mod_name = "nonexistent_module"

    # Run gen_api
    docs = gen_api({"Missing": mod_name}, prefix=str(tmp_path / "docs"))

    # No documents should be returned
    assert docs == []
    # No markdown directory should be created
    assert not (tmp_path / "docs").exists()


def test_gen_api_dry_run(tmp_path: Path):
    """Dry run should not create files but return the generated docs."""
    # Create a simple module
    mod_name = "dry_module"
    _create_module(tmp_path, mod_name, "x = 1\n")

    # Run gen_api with dry=True
    docs = gen_api({"Dry": mod_name}, prefix=str(tmp_path / "docs"), dry=True)

    # One document should be returned
    assert len(docs) == 1
    doc = docs[0]
    # The markdown directory should not exist
    assert not (tmp_path / "docs").exists()
    # The document should contain the module's content
    assert "x = 1" in doc
