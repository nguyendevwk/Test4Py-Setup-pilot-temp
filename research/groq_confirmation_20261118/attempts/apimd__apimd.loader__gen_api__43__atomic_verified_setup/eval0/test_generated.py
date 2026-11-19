import importlib
import sys
import types
from pathlib import Path
import pytest

from apimd.loader import gen_api


def create_module(tmp_path, module_name, content=""):
    """Create a simple module file under tmp_path."""
    module_path = tmp_path / f"{module_name}.py"
    module_path.write_text(content)
    return module_path


def test_gen_api_creates_markdown(tmp_path):
    """Normal case: a valid module is processed and a markdown file is created."""
    # Create a simple module with a docstring
    mod_name = "sample_module"
    create_module(tmp_path, mod_name, '"""Sample module docstring."""\n\ndef foo():\n    pass')
    # Run gen_api
    docs = gen_api({"Sample": mod_name}, prefix=str(tmp_path), link=False, level=2, toc=False, dry=False)
    # Verify that one document is returned
    assert len(docs) == 1
    doc = docs[0]
    # The document should start with a level-2 header
    assert doc.startswith("## Sample API\n\n")
    # The markdown file should exist
    md_file = tmp_path / f"{mod_name.replace('_', '-')}-api.md"
    assert md_file.is_file()
    # The file content should match the returned document
    assert md_file.read_text() == doc


def test_gen_api_skips_missing_module(tmp_path):
    """Boundary case: a non‑existent module is skipped and no file is created."""
    # Run gen_api with a module that does not exist
    docs = gen_api({"Missing": "nonexistent_module"}, prefix=str(tmp_path), dry=False)
    # No documents should be returned
    assert docs == []
    # No markdown file should be present
    md_file = tmp_path / "nonexistent-module-api.md"
    assert not md_file.exists()


def test_gen_api_with_pwd(tmp_path):
    """Error/edge case: providing a pwd that contains a package allows import."""
    # Create a package with an __init__.py and a module
    pkg_dir = tmp_path / "mypkg"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("")
    create_module(pkg_dir, "inner", '"""Inner module."""')
    # Ensure the package is importable via pwd
    docs = gen_api({"Inner": "mypkg.inner"}, pwd=str(pkg_dir), prefix=str(tmp_path), dry=False)
    # Document should be generated
    assert len(docs) == 1
    # Verify that the module was imported from the pwd path
    mod = importlib.import_module("mypkg.inner")
    assert isinstance(mod, types.ModuleType)
    # The markdown file should exist
    md_file = tmp_path / "mypkg-inner-api.md"
    assert md_file.is_file()
