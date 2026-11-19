import os
import sys
import importlib.util
import importlib.machinery
import importlib
import types
import pytest
from apimd.loader import loader
from apimd.logger import logger

# Helper to create a simple package structure
def create_pkg(tmp_path, pkg_name, files):
    pkg_path = tmp_path / pkg_name
    pkg_path.mkdir()
    (pkg_path / "__init__.py").write_text("")
    for fname, content in files.items():
        (pkg_path / fname).write_text(content)
    return pkg_path

def test_loader_parses_python_module(tmp_path):
    # Create a package with a single .py module
    create_pkg(tmp_path, "mypkg", {"mod.py": "x = 42\n"})
    # Ensure the package is importable
    sys.path.insert(0, str(tmp_path))
    try:
        result = loader(str(tmp_path), str(tmp_path), link=False, level=0, toc=False)
        # The compiled output should contain the module name
        assert "mypkg.mod" in result
        # The module should be importable
        mod = importlib.import_module("mypkg.mod")
        assert mod.x == 42
    finally:
        sys.path.pop(0)

def test_loader_parses_stub_only(tmp_path, caplog):
    # Create a package with only a .pyi stub
    create_pkg(tmp_path, "stubpkg", {"stub.pyi": "def foo() -> int: ...\n"})
    sys.path.insert(0, str(tmp_path))
    try:
        caplog.set_level(logger.level)
        result = loader(str(tmp_path), str(tmp_path), link=False, level=0, toc=False)
        # The compiled output should still contain the module name
        assert "stubpkg.stub" in result
        # No import should succeed because there's no .py file
        with pytest.raises(ImportError):
            importlib.import_module("stubpkg.stub")
    finally:
        sys.path.pop(0)

def test_loader_skips_missing_source(tmp_path, caplog):
    # Create a package with a .py file that references a missing module
    create_pkg(tmp_path, "brokenpkg", {"broken.py": "import nonexistent\n"})
    sys.path.insert(0, str(tmp_path))
    try:
        caplog.set_level(logger.level)
        result = loader(str(tmp_path), str(tmp_path), link=False, level=0, toc=False)
        # The compiled output should still contain the module name
        assert "brokenpkg.broken" in result
        # Importing should raise ImportError due to missing dependency
        with pytest.raises(ImportError):
            importlib.import_module("brokenpkg.broken")
    finally:
        sys.path.pop(0)
