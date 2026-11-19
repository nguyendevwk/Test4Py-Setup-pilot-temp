import os
import sys
import importlib.util
import pytest
from apimd.loader import walk_packages

# Helper to create a file with optional content
def create_file(path, content=""):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def test_walk_packages_yields_expected_names(tmp_path):
    """
    Verify that walk_packages yields the correct dotted names and paths
    for a simple package structure with .py and .pyi files.
    """
    # Create a package structure
    pkg_dir = tmp_path / "mypkg"
    pkg_dir.mkdir()
    create_file(pkg_dir / "__init__.py")
    create_file(pkg_dir / "module.py")
    create_file(pkg_dir / "sub" / "__init__.py")
    create_file(pkg_dir / "sub" / "submodule.pyi")

    # Run walk_packages
    results = list(walk_packages("mypkg", str(tmp_path)))
    # Expected names: mypkg, mypkg.module, mypkg.sub, mypkg.sub.submodule
    expected = {
        ("mypkg", str(pkg_dir)),
        ("mypkg.module", str(pkg_dir / "module.py")),
        ("mypkg.sub", str(pkg_dir / "sub" / "__init__.py")),
        ("mypkg.sub.submodule", str(pkg_dir / "sub" / "submodule.pyi")),
    }
    assert set(results) == expected

def test_walk_packages_skips_non_python_files(tmp_path):
    """
    Verify that walk_packages skips files that are not .py or .pyi.
    """
    pkg_dir = tmp_path / "pkg"
    pkg_dir.mkdir()
    create_file(pkg_dir / "script.sh")
    create_file(pkg_dir / "data.txt")
    create_file(pkg_dir / "module.py")

    results = list(walk_packages("pkg", str(tmp_path)))
    # Only the .py file should be yielded
    assert results == [("pkg.module", str(pkg_dir / "module.py"))]

def test_walk_packages_no_matching_files(tmp_path):
    """
    Verify that walk_packages yields nothing when there are no matching files.
    """
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    # No .py or .pyi files inside
    results = list(walk_packages("empty", str(tmp_path)))
    assert results == []
