import builtins
import importlib
import sys
import types
import os
import re
import logging
import pytest

from apimd.loader import loader, walk_packages, _read, _load_module, PEP561_SUFFIX
from apimd.parser import Parser

# Helper to create a simple package structure
def create_pkg(tmp_path, pkg_name, files):
    pkg_path = tmp_path / pkg_name
    pkg_path.mkdir()
    for fname, content in files.items():
        (pkg_path / fname).write_text(content)
    return pkg_path

def test_loader_parses_python_file(tmp_path):
    """Loader should parse a normal .py file and return compiled output containing the module name."""
    pkg = create_pkg(tmp_path, "mypkg", {"__init__.py": "x = 1\n"})
    out = loader(str(pkg), str(tmp_path), link=False, level=0, toc=False)
    assert isinstance(out, str)
    assert "mypkg" in out
    # Ensure that the content of the file was read
    assert "x = 1" in _read(str(pkg / "__init__.py"))

def test_loader_handles_stub_only(tmp_path):
    """Loader should process a package that only contains a .pyi stub and still return output."""
    pkg = create_pkg(tmp_path, "stubpkg", {"__init__.pyi": "def foo() -> int: ...\n"})
    out = loader(str(pkg), str(tmp_path), link=False, level=0, toc=False)
    assert isinstance(out, str)
    assert "stubpkg" in out
    # The stub file should be read
    assert "def foo" in _read(str(pkg / "__init__.pyi"))

def test_walk_packages_filters_non_package_files(tmp_path):
    """walk_packages should ignore files outside the package and non-.py/.pyi files."""
    pkg = create_pkg(tmp_path, "mypkg", {
        "__init__.py": "pass\n",
        "module.py": "pass\n",
        "not_a_pkg.txt": "ignore\n",
        "sub/__init__.py": "pass\n",
    })
    # Create a subdirectory that is not a package
    (pkg / "sub").mkdir()
    (pkg / "sub" / "file.py").write_text("pass\n")
    names = list(walk_packages("mypkg", str(tmp_path)))
    # Should include mypkg, mypkg.module, mypkg.sub
    expected = {"mypkg", "mypkg.module", "mypkg.sub"}
    assert set(name for name, _ in names) == expected
    # Ensure that non-package file is not yielded
    assert all("not_a_pkg" not in name for name, _ in names)
