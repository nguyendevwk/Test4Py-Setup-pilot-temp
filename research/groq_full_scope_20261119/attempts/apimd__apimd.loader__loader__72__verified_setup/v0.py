import os
import sys
import importlib.util
import importlib.machinery
import pytest
from apimd.loader import loader

@pytest.fixture
def simple_package(tmp_path):
    """Create a minimal package with a .py and a .pyi file."""
    pkg_dir = tmp_path / "mypkg"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("")
    (pkg_dir / "module.py").write_text("def hello():\n    return 'world'")
    (pkg_dir / "module.pyi").write_text("def hello() -> str: ...")
    return pkg_dir

def test_loader_parses_python_and_stub(simple_package, tmp_path):
    """Loader should parse both .py and .pyi files and return a string containing the module name."""
    # Ensure the temporary directory is on sys.path so that walk_packages can find it
    sys.path.insert(0, str(tmp_path))
    try:
        result = loader(str(simple_package), str(tmp_path), link=False, level=0, toc=False)
    finally:
        sys.path.pop(0)

    # The result should contain the fully qualified name of the module
    assert "mypkg.module" in result
    # The result should include the stub signature
    assert "def hello() -> str" in result
    # The result should include the actual implementation
    assert "def hello()" in result
    # The result should not contain the import statement for the module itself
    assert "import mypkg.module" not in result

def test_loader_returns_empty_when_no_packages(tmp_path):
    """Loader should return an empty string when there are no packages to load."""
    # Create an empty directory
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    sys.path.insert(0, str(tmp_path))
    try:
        result = loader(str(empty_dir), str(tmp_path), link=False, level=0, toc=False)
    finally:
        sys.path.pop(0)
    assert result == ""

def test_loader_skips_pure_python_modules(tmp_path):
    """Loader should skip pure .py modules if a .pyi exists for the same module."""
    pkg_dir = tmp_path / "pkg"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("")
    # Create a module with both .py and .pyi
    (pkg_dir / "mod.py").write_text("def foo():\n    return 1")
    (pkg_dir / "mod.pyi").write_text("def foo() -> int: ...")
    sys.path.insert(0, str(tmp_path))
    try:
        result = loader(str(pkg_dir), str(tmp_path), link=False, level=0, toc=False)
    finally:
        sys.path.pop(0)
    # The pure .py module should be skipped, so only the stub should appear
    assert "def foo() -> int" in result
    assert "def foo()" not in result
