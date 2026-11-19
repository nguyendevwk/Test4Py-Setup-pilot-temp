import os
import sys
import importlib.util
import types
import pytest
from apimd.loader import gen_api, _site_path, _write, loader, _load_module, _read, walk_packages

# Helper to create a minimal package in a temporary directory
def create_pkg(tmp_path, pkg_name, module_name, content):
    pkg_dir = tmp_path / pkg_name
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("")
    (pkg_dir / f"{module_name}.py").write_text(content)
    return pkg_dir

def test_gen_api_creates_markdown(tmp_path):
    # Create a simple package with one module
    pkg_dir = create_pkg(tmp_path, "mypkg", "mymod", "def foo():\n    '''Foo docstring.'''\n    pass")
    # Ensure the package is importable
    sys.path.insert(0, str(tmp_path))
    try:
        docs = gen_api({"MyPkg": "mypkg"}, prefix=str(tmp_path / "docs"))
        # One markdown file should be created
        md_path = tmp_path / "docs" / "mypkg-api.md"
        assert md_path.is_file()
        # The content should contain the module docstring
        md_text = md_path.read_text()
        assert "Foo docstring." in md_text
        # The returned docs list should contain the same content
        assert docs[0] == md_text
    finally:
        sys.path.pop(0)

def test_gen_api_dry_run_returns_docs(tmp_path):
    # Create a package with a module that has no docstring
    pkg_dir = create_pkg(tmp_path, "emptypkg", "empty", "def bar():\n    pass")
    sys.path.insert(0, str(tmp_path))
    try:
        docs = gen_api({"EmptyPkg": "emptypkg"}, prefix=str(tmp_path / "docs"), dry=True)
        # No file should be written
        assert not (tmp_path / "docs" / "emptypkg-api.md").exists()
        # The docs list should contain the generated markdown (without file)
        assert len(docs) == 1
        assert "# EmptyPkg API" in docs[0]
    finally:
        sys.path.pop(0)

def test_loader_skips_nonexistent_module(tmp_path):
    # Create a package with a module that imports a missing dependency
    pkg_dir = create_pkg(tmp_path, "badpkg", "badmod", "import nonexistent\n\ndef baz():\n    '''Baz docstring.'''\n    pass")
    sys.path.insert(0, str(tmp_path))
    try:
        # loader should skip the module due to ImportError and return empty string
        doc = loader("badpkg", _site_path("badpkg"), link=True, level=1, toc=False)
        assert doc == ""
    finally:
        sys.path.pop(0)
