import os
import sys
import importlib
import pytest
from apimd.loader import walk_packages, PEP561_SUFFIX

def test_walk_packages_yields_expected_names(tmp_path):
    # Create a package structure:
    # tmp_path/
    #   pkg/
    #     __init__.py
    #     module.py
    #     subpkg/
    #       __init__.py
    #       submodule.py
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    (pkg / "__init__.py").write_text("")
    (pkg / "module.py").write_text("")
    subpkg = pkg / "subpkg"
    subpkg.mkdir()
    (subpkg / "__init__.py").write_text("")
    (subpkg / "submodule.py").write_text("")

    # Walk packages
    results = list(walk_packages("pkg", str(tmp_path)))
    # Expected names: pkg, pkg.module, pkg.subpkg, pkg.subpkg.submodule
    expected = {
        ("pkg", str(pkg)),
        ("pkg.module", str(pkg / "module.py")),
        ("pkg.subpkg", str(subpkg)),
        ("pkg.subpkg.submodule", str(subpkg / "submodule.py")),
    }
    assert set(results) == expected

def test_walk_packages_skips_non_py_files(tmp_path):
    # Create a directory with various files
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    (pkg / "__init__.py").write_text("")
    (pkg / "module.py").write_text("")
    (pkg / "data.txt").write_text("not a python file")
    (pkg / "script.sh").write_text("#!/bin/bash")
    (pkg / "module.pyi").write_text("")

    results = list(walk_packages("pkg", str(tmp_path)))
    # Should only include .py and .pyi files
    names = {name for name, _ in results}
    assert names == {"pkg", "pkg.module", "pkg.module"}  # duplicate due to same name? actually module.py and module.pyi produce same name
    # Ensure data.txt and script.sh are not present
    for _, path in results:
        assert not path.endswith((".txt", ".sh"))

def test_walk_packages_raises_on_nonexistent_path(tmp_path):
    # Provide a path that does not exist
    nonexistent = tmp_path / "does_not_exist"
    with pytest.raises(FileNotFoundError):
        list(walk_packages("pkg", str(nonexistent)))
