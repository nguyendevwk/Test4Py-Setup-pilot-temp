import os
import sys
import types
import importlib
import pytest
from pathlib import Path

# Import the target function
from httpie.utils import get_site_paths

# Helper to create a dummy compat module with desired attributes
def _make_compat(is_frozen, min_version, max_version):
    compat = types.SimpleNamespace(
        is_frozen=is_frozen,
        MIN_SUPPORTED_PY_VERSION=min_version,
        MAX_SUPPORTED_PY_VERSION=max_version
    )
    sys.modules['httpie.compat'] = compat
    importlib.reload(importlib.import_module('httpie.utils'))

@pytest.fixture(autouse=True)
def reset_compat(monkeypatch):
    # Ensure httpie.compat is reset after each test
    yield
    if 'httpie.compat' in sys.modules:
        del sys.modules['httpie.compat']

def test_get_site_paths_not_frozen(tmp_path):
    # Simulate non-frozen environment
    _make_compat(is_frozen=False, min_version=[3, 8], max_version=[3, 10])
    # Call the function
    paths = list(get_site_paths(tmp_path))
    # Expect a single path equal to the input
    assert len(paths) == 1
    assert paths[0] == tmp_path

def test_get_site_paths_frozen_boundary(tmp_path):
    # Simulate frozen environment with min and max versions
    _make_compat(is_frozen=True, min_version=[3, 7], max_version=[3, 9])
    paths = list(get_site_paths(tmp_path))
    # Expect three paths with py_version_short suffixes 3.7, 3.8, 3.9
    expected_suffixes = ['3.7', '3.8', '3.9']
    assert len(paths) == len(expected_suffixes)
    for path, suffix in zip(paths, expected_suffixes):
        assert path.name.endswith(suffix)
        # Ensure the path is a subdirectory of the original path
        assert suffix in path.parts

def test_get_site_paths_invalid_path_type(tmp_path):
    # Simulate non-frozen environment
    _make_compat(is_frozen=False, min_version=[3, 8], max_version=[3, 10])
    # Pass an invalid type (e.g., string) to get_site_paths
    with pytest.raises(AttributeError):
        list(get_site_paths(str(tmp_path)))
