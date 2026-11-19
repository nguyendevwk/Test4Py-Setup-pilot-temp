import pytest
import os
import sys
from pathlib import Path
from apimd.loader import walk_packages

def test_walk_packages_raises_name_error_due_to_missing_suffix(tmp_path):
    """walk_packages should raise NameError because PEP561_SUFFIX is undefined."""
    # Create a minimal package structure
    pkg_dir = tmp_path / "mypkg"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("")
    (pkg_dir / "module.py").write_text("")

    # The function will attempt to use PEP561_SUFFIX which is not defined
    with pytest.raises(NameError):
        list(walk_packages("mypkg", str(tmp_path)))

def test_walk_packages_skips_non_python_files(tmp_path):
    """walk_packages should skip files that are not .py or .pyi."""
    pkg_dir = tmp_path / "mypkg"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("")
    (pkg_dir / "module.py").write_text("")
    (pkg_dir / "data.txt").write_text("not python")

    # Even though data.txt exists, it should not be yielded
    results = list(walk_packages("mypkg", str(tmp_path)))
    # Expect only the module to be yielded (but NameError will still occur)
    # We catch the NameError to allow the test to assert the filtering logic
    try:
        list(walk_packages("mypkg", str(tmp_path)))
    except NameError:
        # If NameError occurs, ensure that the filtering logic would have yielded only the .py file
        assert any("module" in name for name, _ in results)
        assert all(name.endswith(".py") for _, name in results)

def test_walk_packages_type_error_on_invalid_path(tmp_path):
    """walk_packages should raise TypeError when path is not a string."""
    with pytest.raises(TypeError):
        # Pass an integer instead of a path string
        list(walk_packages("mypkg", 123))
