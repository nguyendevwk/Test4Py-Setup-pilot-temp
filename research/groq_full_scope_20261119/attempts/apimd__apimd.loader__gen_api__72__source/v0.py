import importlib
import sys
import types
import os
import pathlib
import pytest

from apimd.loader import gen_api

# Helper to create a temporary package with a simple module
def create_pkg(tmp_path, pkg_name, module_name, content):
    pkg_dir = tmp_path / pkg_name
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("")
    mod_file = pkg_dir / f"{module_name}.py"
    mod_file.write_text(content)
    return pkg_dir

def test_gen_api_creates_markdown(tmp_path):
    # Create a simple package with a module that defines a function
    pkg_dir = create_pkg(tmp_path, "demo_pkg", "mymod", "def hello():\n    return 'hi'\n")
    # Ensure the package is importable
    sys.path.insert(0, str(tmp_path))
    try:
        docs = gen_api({"Demo": "demo_pkg.mymod"}, prefix=str(tmp_path / "docs"))
    finally:
        sys.path.pop(0)

    # There should be one document returned
    assert len(docs) == 1
    doc = docs[0]
    # The document should start with a level-1 header
    assert doc.startswith("# Demo API\n\n")
    # The module's docstring (none) and function signature should appear
    assert "def hello()" in doc
    # The output file should exist
    out_file = tmp_path / "docs" / "demo-pkg-mymod-api.md"
    assert out_file.is_file()
    # The file content should match the returned doc
    assert out_file.read_text() == doc

def test_gen_api_skips_missing_module(tmp_path):
    # No package created for 'missing_pkg'
    sys.path.insert(0, str(tmp_path))
    try:
        docs = gen_api({"Missing": "missing_pkg.nonexistent"}, prefix=str(tmp_path / "docs"))
    finally:
        sys.path.pop(0)

    # No documents should be returned
    assert docs == []
    # The docs directory should still be created but empty
    docs_dir = tmp_path / "docs"
    assert docs_dir.is_dir()
    assert not any(docs_dir.iterdir())

def test_gen_api_dry_run(tmp_path, caplog):
    # Create a package with a module containing a class
    pkg_dir = create_pkg(tmp_path, "dry_pkg", "mod", "class Foo:\n    pass\n")
    sys.path.insert(0, str(tmp_path))
    try:
        docs = gen_api({"Dry": "dry_pkg.mod"}, prefix=str(tmp_path / "docs"), dry=True)
    finally:
        sys.path.pop(0)

    # One document should be returned
    assert len(docs) == 1
    doc = docs[0]
    # The document should contain the class definition
    assert "class Foo" in doc
    # No file should be written
    out_file = tmp_path / "docs" / "dry-pkg-mod-api.md"
    assert not out_file.exists()
    # The dry flag should have logged the document content
    assert any("class Foo" in record.message for record in caplog.records)
