import os
import sys
import importlib
import importlib.util
import importlib.machinery
import importlib.abc
import importlib
import types
import pytest
from apimd.loader import loader

# Helper to create a simple package structure
def create_package(tmp_path, name, files):
    pkg_path = tmp_path / name
    pkg_path.mkdir()
    (pkg_path / "__init__.py").write_text("")
    for fname, content in files.items():
        (pkg_path / fname).write_text(content)
    return str(pkg_path)

def test_loader_parses_python_module(tmp_path):
    """Loader should parse a normal .py module and return a non‑empty string."""
    pkg = create_package(tmp_path, "mypkg", {"module.py": "def foo(): return 42"})
    result = loader(pkg, os.getcwd(), link=False, level=0, toc=False)
    assert isinstance(result, str)
    assert result.strip() != ""

def test_loader_parses_stub_only(tmp_path):
    """Loader should still compile when only a .pyi stub is present."""
    pkg = create_package(tmp_path, "stubpkg", {"module.pyi": "def bar() -> int: ..."})
    result = loader(pkg, os.getcwd(), link=False, level=0, toc=False)
    assert isinstance(result, str)
    assert result.strip() != ""

def test_loader_handles_missing_files(tmp_path):
    """Loader should not raise when the root directory is empty or missing."""
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    result = loader(str(empty_dir), os.getcwd(), link=False, level=0, toc=False)
    assert isinstance(result, str)
    # The result may be empty but should not raise an exception
    assert result == "" or result.strip() != ""
