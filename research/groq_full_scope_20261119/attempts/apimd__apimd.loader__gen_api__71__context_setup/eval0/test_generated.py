import sys
import os
import importlib
import pytest
from apimd.loader import gen_api, _site_path

# Helper to create a minimal package with a single module
def create_pkg(tmp_path, name, content=""):
    pkg_dir = tmp_path / name
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("")
    (pkg_dir / "module.py").write_text(content)
    return pkg_dir

def test_gen_api_writes_markdown(tmp_path, caplog):
    # Create a simple package with a docstring
    pkg_dir = create_pkg(tmp_path, "demo_pkg", '"""Demo package docstring."""')
    sys.path.insert(0, str(tmp_path))
    try:
        docs = gen_api({"Demo": "demo_pkg"}, prefix=str(tmp_path / "docs"))
        # One markdown file should be created
        md_path = tmp_path / "docs" / "demo-pkg-api.md"
        assert md_path.is_file()
        content = md_path.read_text()
        # The content should contain the title and the docstring
        assert "# Demo API" in content
        assert "Demo package docstring." in content
        # gen_api returns the compiled docs
        assert len(docs) == 1
        assert "Demo package docstring." in docs[0]
    finally:
        sys.path.pop(0)

def test_gen_api_dry_run(tmp_path, caplog):
    # Create a package with a simple function
    pkg_dir = create_pkg(tmp_path, "dry_pkg", "def foo():\n    '''Foo docstring.'''\n    pass")
    sys.path.insert(0, str(tmp_path))
    try:
        docs = gen_api({"Dry": "dry_pkg"}, prefix=str(tmp_path / "docs"), dry=True)
        # No file should be written
        assert not (tmp_path / "docs" / "dry-pkg-api.md").exists()
        # The returned docs should contain the function docstring
        assert any("Foo docstring." in d for d in docs)
    finally:
        sys.path.pop(0)

def test_gen_api_missing_package(tmp_path, caplog):
    # Call with a non-existent package name
    with caplog.at_level("WARNING"):
        docs = gen_api({"Missing": "nonexistent_pkg"}, prefix=str(tmp_path / "docs"))
    # No docs should be returned
    assert docs == []
    # Warning should be logged
    assert any("can not be found" in rec.message for rec in caplog.records)
