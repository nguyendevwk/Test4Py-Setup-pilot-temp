import os
import pytest
from apimd.loader import walk_packages, PEP561_SUFFIX

def test_walk_packages_normal(tmp_path):
    # Create a package with a module and a stub package
    pkg_dir = tmp_path / "pkg"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("# init")
    (pkg_dir / "module.py").write_text("x = 1")

    stub_dir = tmp_path / f"pkg{PEP561_SUFFIX}"
    stub_dir.mkdir()
    (stub_dir / "__init__.pyi").write_text("# stub init")

    # Collect results
    results = list(walk_packages("pkg", str(tmp_path)))
    names = {name for name, _ in results}
    paths = {path for _, path in results}

    # Expected names and paths
    expected_names = {"pkg", "pkg.module"}
    expected_paths = {
        str(pkg_dir),
        str(pkg_dir / "module.py"),
        str(stub_dir),
    }

    assert names == expected_names
    assert paths == expected_paths
    # Ensure each path ends with the correct file or directory
    for name, path in results:
        if name == "pkg.module":
            assert path.endswith("module.py")
        else:
            assert path.endswith("__init__.py") or path.endswith("__init__.pyi")

def test_walk_packages_no_files(tmp_path):
    # Create an empty package directory
    empty_dir = tmp_path / "empty_pkg"
    empty_dir.mkdir()
    # No .py or .pyi files inside
    results = list(walk_packages("empty_pkg", str(tmp_path)))
    assert results == []

def test_walk_packages_excludes_invalid(tmp_path):
    # Create a valid package
    valid_dir = tmp_path / "valid_pkg"
    valid_dir.mkdir()
    (valid_dir / "__init__.py").write_text("# init")

    # Create an unrelated file outside the valid prefix
    unrelated_file = tmp_path / "unrelated.py"
    unrelated_file.write_text("print('hello')")

    results = list(walk_packages("valid_pkg", str(tmp_path)))
    # Should only contain the valid package, not the unrelated file
    assert len(results) == 1
    name, path = results[0]
    assert name == "valid_pkg"
    assert path == str(valid_dir)
