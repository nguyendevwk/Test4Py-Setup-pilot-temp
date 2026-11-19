import os
import sys
import importlib
import pytest
from apimd.loader import walk_packages

# Helper to create a package structure
def create_pkg_structure(tmp_path, pkg_name, files):
    pkg_dir = tmp_path / pkg_name
    pkg_dir.mkdir()
    for file in files:
        (pkg_dir / file).write_text("# dummy")
    return pkg_dir

def test_walk_packages_returns_expected_names(tmp_path):
    # Create a package with two modules and an __init__.py
    pkg_dir = create_pkg_structure(tmp_path, "mypkg", ["__init__.py", "module1.py", "sub/__init__.py", "sub/module2.py"])
    # Ensure subdirectory exists
    (pkg_dir / "sub").mkdir()
    # Run walk_packages
    results = list(walk_packages("mypkg", str(tmp_path)))
    # Expected names: mypkg, mypkg.module1, mypkg.sub, mypkg.sub.module2
    expected = {
        ("mypkg", str(pkg_dir)),
        ("mypkg.module1", str(pkg_dir / "module1.py")),
        ("mypkg.sub", str(pkg_dir / "sub")),
        ("mypkg.sub.module2", str(pkg_dir / "sub" / "module2.py")),
    }
    assert set(results) == expected

def test_walk_packages_skips_non_python_files(tmp_path):
    # Create a package with a .txt file
    pkg_dir = create_pkg_structure(tmp_path, "pkg", ["__init__.py", "script.py", "notes.txt"])
    # Run walk_packages
    results = list(walk_packages("pkg", str(tmp_path)))
    # Only python files should be yielded
    assert ("pkg", str(pkg_dir)) in results
    assert ("pkg.script", str(pkg_dir / "script.py")) in results
    # .txt file should not appear
    assert all(name != "pkg.notes" for name, _ in results)

def test_walk_packages_with_nonexistent_path(tmp_path):
    # Provide a path that does not exist
    nonexistent = tmp_path / "does_not_exist"
    # walk_packages should not raise an exception and yield nothing
    results = list(walk_packages("any", str(nonexistent)))
    assert results == []
