import os
import sys
import sysconfig
import pytest
from pathlib import Path
from httpie.utils import get_site_paths, as_site
import httpie.compat

# Test 1: Normal behavior when the application is not frozen.
def test_get_site_paths_non_frozen(tmp_path: Path):
    # Ensure the environment is not frozen
    httpie.compat.is_frozen = False
    # Call the function with a temporary path
    paths = list(get_site_paths(tmp_path))
    # It should yield exactly one path
    assert len(paths) == 1
    # The yielded path should be the site-packages path for the given base
    expected = as_site(tmp_path)
    assert paths[0] == expected
    # The path should exist (even if empty) and be a directory
    assert paths[0].is_dir()

# Test 2: Error handling when an invalid type is passed.
def test_get_site_paths_invalid_argument():
    # Passing a string instead of a Path should raise a TypeError
    with pytest.raises(TypeError):
        list(get_site_paths("not-a-path"))

# Test 3: Behavior when the application is frozen.
def test_get_site_paths_frozen(tmp_path: Path, monkeypatch):
    # Patch the compatibility module to simulate a frozen environment
    monkeypatch.setattr(httpie.compat, "is_frozen", True)
    # Define supported Python versions for the test
    monkeypatch.setattr(httpie.compat, "MIN_SUPPORTED_PY_VERSION", [3, 8])
    monkeypatch.setattr(httpie.compat, "MAX_SUPPORTED_PY_VERSION", [3, 10])
    # Call the function
    paths = list(get_site_paths(tmp_path))
    # It should yield one path per supported minor version
    assert len(paths) == 3
    # Verify that each yielded path corresponds to the correct Python version
    expected_versions = ["3.8", "3.9", "3.10"]
    for path, version in zip(paths, expected_versions):
        # The path should contain the version string
        assert version in str(path)
        # The path should be a directory
        assert path.is_dir()
