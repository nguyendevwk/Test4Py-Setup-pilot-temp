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

# Helper to create a temporary package structure
def create_pkg(tmp_path, name, files):
    pkg_dir = tmp_path / name
    pkg_dir.mkdir()
    for fname, content in files.items():
        (pkg_dir / fname).write_text(content)
    # create __init__.py to make it a package
    (pkg_dir / "__init__.py").write_text("")
    return pkg_dir

def test_loader_parses_python_module(tmp_path):
    # Create a simple package with one .py module
    pkg_dir = create_pkg(tmp_path, "mypkg", {"mod.py": "x = 42"})
    # Run loader
    result = loader(str(pkg_dir), str(pkg_dir), link=False, level=0, toc=False)
    # The compiled output should contain the module name
    assert "mypkg.mod" in result
    # It should also contain the code we wrote
    assert "x = 42" in result

def test_loader_parses_stub_and_skips_py(tmp_path):
    # Create a package with a .pyi stub but no .py
    pkg_dir = create_pkg(tmp_path, "stubpkg", {"mod.pyi": "def foo() -> int: ..."})
    result = loader(str(pkg_dir), str(pkg_dir), link=False, level=0, toc=False)
    # Should contain the module name and the stub signature
    assert "stubpkg.mod" in result
    assert "def foo() -> int" in result

def test_loader_returns_empty_for_no_modules(tmp_path):
    # Create an empty package
    pkg_dir = create_pkg(tmp_path, "emptypkg", {})
    result = loader(str(pkg_dir), str(pkg_dir), link=False, level=0, toc=False)
    # No modules to parse, result should be empty string
    assert result == ""
