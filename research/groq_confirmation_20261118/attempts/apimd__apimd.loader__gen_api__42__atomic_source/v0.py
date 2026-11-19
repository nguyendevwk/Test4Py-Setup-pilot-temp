import importlib.util
import os
import sys
import types
from pathlib import Path

import pytest

from apimd.loader import gen_api


def _create_module(tmp_path: Path, module_name: str, code: str) -> Path:
    """Create a Python module file under tmp_path and return its path."""
    module_path = tmp_path / f"{module_name}.py"
    module_path.write_text(code)
    return module_path


def _import_module_from_path(module_name: str, module_path: Path) -> types.ModuleType:
    """Import a module from a given file path."""
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_gen_api_creates_markdown(tmp_path):
    """Normal case: a simple module with a function should produce a markdown file."""
    # Create a simple module
    mod_code = """
def hello(name: str) -> str:
    \"\"\"Return greeting.\"\"\"
    return f"Hello, {name}!"
"""
    mod_path = _create_module(tmp_path, "greet", mod_code)

    # Ensure module is importable
    _import_module_from_path("greet", mod_path)

    # Run gen_api
    docs = gen_api({"Greeting": "greet"}, pwd=str(tmp_path), prefix=str(tmp_path / "docs"))

    # There should be one doc returned
    assert len(docs) == 1
    doc = docs[0]
    # The markdown should contain the function signature
    assert "def hello(name: str) -> str:" in doc
    # The file should be created
    md_file = tmp_path / "docs" / "greet-api.md"
    assert md_file.is_file()
    content = md_file.read_text()
    assert content == doc


def test_gen_api_empty_root_names(tmp_path):
    """Boundary case: empty root_names should return an empty list and create no files."""
    docs = gen_api({}, pwd=str(tmp_path), prefix=str(tmp_path / "docs"))
    assert docs == []
    # No docs directory should be created because nothing was written
    assert not (tmp_path / "docs").exists()


def test_gen_api_missing_module(tmp_path):
    """Error case: a non-existent module name should be skipped and not produce a file."""
    # Create a dummy module that will be referenced
    _create_module(tmp_path, "existing", "def foo(): pass")

    # Run gen_api with one existing and one missing module
    docs = gen_api(
        {"Existing": "existing", "Missing": "nonexistent"},
        pwd=str(tmp_path),
        prefix=str(tmp_path / "docs"),
    )

    # Only the existing module should produce a doc
    assert len(docs) == 1
    assert "def foo()" in docs[0]
    # Only one file should exist
    md_file = tmp_path / "docs" / "existing-api.md"
    assert md_file.is_file()
    # The missing module should not create a file
    assert not (tmp_path / "docs" / "nonexistent-api.md").exists()
