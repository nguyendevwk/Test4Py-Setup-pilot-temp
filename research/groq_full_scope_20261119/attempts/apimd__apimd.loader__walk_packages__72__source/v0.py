import os
import sys
import pytest
from apimd.loader import walk_packages

# Helper to create a file with optional content
def create_file(path, content=""):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def test_walk_packages_normal(tmp_path):
    """
    Verify that walk_packages yields correct module names for a
    typical package layout with .py and .pyi files.
    """
    # Create a package structure:
    # tmp_path/
    #   pkg/
    #     __init__.py
    #     module.py
    #     subpkg/
    #       __init__.py
    #       submodule.py
    #   other.py
    pkg_dir = tmp_path / "pkg"
    subpkg_dir = pkg_dir / "subpkg"
    create_file(pkg_dir / "__init__.py")
    create_file(pkg_dir / "module.py")
    create_file(subpkg_dir / "__init__.py")
    create_file(subpkg_dir / "submodule.py")
    create_file(tmp_path / "other.py")

    # Run walk_packages on the top-level package
    results = list(walk_packages("pkg", str(tmp_path)))
    # Expected module names
    expected = {
        ("pkg", str(pkg_dir)),
        ("pkg.module", str(pkg_dir / "module.py")),
        ("pkg.subpkg", str(subpkg_dir)),
        ("pkg.subpkg.submodule", str(subpkg_dir / "submodule.py")),
    }
    assert set(results) == expected

def test_walk_packages_ignores_non_python(tmp_path):
    """
    Verify that files not ending with .py or .pyi are ignored.
    """
    # Create a package with a non-Python file
    pkg_dir = tmp_path / "pkg"
    create_file(pkg_dir / "__init__.py")
    create_file(pkg_dir / "data.txt")
    create_file(pkg_dir / "script.sh")

    results = list(walk_packages("pkg", str(tmp_path)))
    # Only the __init__ should be yielded
    assert results == [("pkg", str(pkg_dir))]

def test_walk_packages_no_py_files(tmp_path):
    """
    Verify that walk_packages yields nothing when there are no .py/.pyi files
    inside the package directory.
    """
    # Create an empty package directory
    pkg_dir = tmp_path / "empty_pkg"
    os.makedirs(pkg_dir, exist_ok=True)

    results = list(walk_packages("empty_pkg", str(tmp_path)))
    # No modules should be found
    assert results == []
