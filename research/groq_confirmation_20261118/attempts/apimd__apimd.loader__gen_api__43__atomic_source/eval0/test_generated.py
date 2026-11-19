import importlib
import os
import sys
import types
from pathlib import Path

import pytest

from apimd.loader import gen_api


def create_module(tmp_path: Path, module_name: str, content: str) -> Path:
    """Create a temporary Python module in a package."""
    pkg_dir = tmp_path / "pkg"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("")
    mod_path = pkg_dir / f"{module_name}.py"
    mod_path.write_text(content)
    # Ensure the package is importable
    sys.path.insert(0, str(tmp_path))
    return mod_path


def test_gen_api_creates_markdown_and_returns_docs(tmp_path):
    """Normal case: a module exists, API file is created and returned."""
    mod_name = "sample_module"
    mod_content = """
def foo(x):
    \"\"\"Return x squared.\"\"\"
    return x * x
"""
    create_module(tmp_path, mod_name, mod_content)

    # Run gen_api
    docs = gen_api({"Sample Module": mod_name}, prefix=str(tmp_path / "docs"))

    # There should be one doc returned
    assert len(docs) == 1
    doc = docs[0]
    # The doc should contain the function name and its docstring
    assert "foo" in doc
    assert "Return x squared." in doc

    # The markdown file should exist and contain the same content
    md_path = tmp_path / "docs" / f"{mod_name.replace('_', '-')}-api.md"
    assert md_path.is_file()
    md_content = md_path.read_text()
    assert doc == md_content


def test_gen_api_skips_missing_module(tmp_path):
    """If a module cannot be found, it is skipped and no file is created."""
    # No module is created
    docs = gen_api({"Missing": "nonexistent_module"}, prefix=str(tmp_path / "docs"))

    # No docs should be returned
    assert docs == []

    # No docs directory should be created
    assert not (tmp_path / "docs").exists()


def test_gen_api_dry_run_does_not_write_file(tmp_path):
    """Dry run mode should not create files but still return docs."""
    mod_name = "dry_module"
    mod_content = """
def bar():
    pass
"""
    create_module(tmp_path, mod_name, mod_content)

    docs = gen_api(
        {"Dry Module": mod_name},
        prefix=str(tmp_path / "docs"),
        dry=True,
    )

    # Docs should be returned
    assert len(docs) == 1
    # No file should be written
    md_path = tmp_path / "docs" / f"{mod_name.replace('_', '-')}-api.md"
    assert not md_path.exists()
