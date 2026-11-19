import importlib
import os
import sys
import types
from pathlib import Path

import pytest

from apimd.loader import gen_api


def test_gen_api_creates_markdown(tmp_path):
    # Create a simple module with a function
    pkg_dir = tmp_path / "mypkg"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("")
    mod_file = pkg_dir / "mymodule.py"
    mod_file.write_text(
        """
def hello():
    \"\"\"Say hello\"\"\"
    return "hello"
"""
    )
    # Ensure the package is importable
    sys.path.insert(0, str(tmp_path))
    try:
        docs = gen_api({"My Module": "mypkg.mymodule"}, prefix=str(tmp_path / "docs"))
    finally:
        sys.path.pop(0)

    # One markdown file should be created
    md_path = tmp_path / "docs" / "mymodule-api.md"
    assert md_path.is_file()
    content = md_path.read_text()
    # The content should contain the function signature and docstring
    assert "def hello()" in content
    assert "Say hello" in content
    # The returned docs list should contain the same content
    assert docs == [content]


def test_gen_api_skips_missing_module(tmp_path):
    # No module exists
    docs = gen_api({"Missing": "nonexistent.module"}, prefix=str(tmp_path / "docs"))
    # No markdown file should be created
    md_path = tmp_path / "docs" / "nonexistent-module-api.md"
    assert not md_path.exists()
    # The docs list should be empty
    assert docs == []


def test_gen_api_dry_run(tmp_path):
    # Create a module
    pkg_dir = tmp_path / "pkg"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("")
    (pkg_dir / "mod.py").write_text(
        """
def foo():
    \"\"\"Foo function\"\"\"
    pass
"""
    )
    sys.path.insert(0, str(tmp_path))
    try:
        docs = gen_api({"Pkg": "pkg.mod"}, prefix=str(tmp_path / "docs"), dry=True)
    finally:
        sys.path.pop(0)

    # No file should be written
    md_path = tmp_path / "docs" / "mod-api.md"
    assert not md_path.exists()
    # The docs list should still contain the generated content
    assert len(docs) == 1
    assert "def foo()" in docs[0]
    assert "Foo function" in docs[0]
