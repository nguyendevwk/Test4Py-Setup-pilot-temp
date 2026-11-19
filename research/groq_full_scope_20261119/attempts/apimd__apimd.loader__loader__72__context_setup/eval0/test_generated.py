import os
import sys
import importlib
import importlib.util
import importlib.machinery
import types
import pytest

# Import the target function and helper classes from the package
from apimd.loader import loader, Parser, walk_packages, PEP561_SUFFIX

def test_loader_parses_py_and_pyi(tmp_path):
    """
    Create a simple package with both .py and .pyi files.
    The loader should parse the .py file and ignore the .pyi for pure Python modules.
    The resulting documentation string should contain the module name.
    """
    # Create package structure
    pkg_dir = tmp_path / "mypkg"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("")
    (pkg_dir / "module.py").write_text("def foo():\n    '''Foo docstring.'''\n    pass\n")
    (pkg_dir / "module.pyi").write_text("def foo() -> None: ...\n")

    # Ensure the package is importable
    sys.path.insert(0, str(tmp_path))
    try:
        # Run loader
        result = loader("mypkg", str(tmp_path), link=False, level=1, toc=False)
    finally:
        sys.path.pop(0)

    # The result should contain the module name and its docstring
    assert "module" in result
    assert "Foo docstring." in result

def test_loader_skips_pure_py_when_present(tmp_path):
    """
    Create a package with a .py file and a .pyi stub.
    The loader should parse the .py file and not attempt to load the stub as a separate module.
    """
    pkg_dir = tmp_path / "mypkg2"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("")
    (pkg_dir / "mod.py").write_text("def bar():\n    '''Bar docstring.'''\n    pass\n")
    (pkg_dir / "mod.pyi").write_text("def bar() -> None: ...\n")

    sys.path.insert(0, str(tmp_path))
    try:
        result = loader("mypkg2", str(tmp_path), link=False, level=1, toc=False)
    finally:
        sys.path.pop(0)

    # The result should contain the module name only once
    assert result.count("mod") == 1
    assert "Bar docstring." in result

def test_loader_warns_when_no_module(tmp_path, caplog):
    """
    Create a package with only a .pyi stub and no .py or extension module.
    The loader should log a warning but still return documentation containing the module name.
    """
    pkg_dir = tmp_path / "mypkg3"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("")
    (pkg_dir / "stub.pyi").write_text("def baz() -> None: ...\n")

    sys.path.insert(0, str(tmp_path))
    try:
        caplog.set_level("WARNING")
        result = loader("mypkg3", str(tmp_path), link=False, level=1, toc=False)
    finally:
        sys.path.pop(0)

    # A warning should have been logged about missing module
    assert any("no module for stub" in rec.message for rec in caplog.records)
    # The documentation should still contain the module name
    assert "stub" in result
