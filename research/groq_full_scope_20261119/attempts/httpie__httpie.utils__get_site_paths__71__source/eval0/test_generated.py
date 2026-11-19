import os
import sys
import types
import pytest
from pathlib import Path

# Import the target function
from httpie.utils import get_site_paths

# Helper to create a fake compat module
def _make_fake_compat(is_frozen, min_py, max_py):
    fake = types.SimpleNamespace(
        is_frozen=is_frozen,
        MIN_SUPPORTED_PY_VERSION=min_py,
        MAX_SUPPORTED_PY_VERSION=max_py,
    )
    return fake

# Helper to patch httpie.compat
@pytest.fixture
def patch_compat(monkeypatch):
    def _patch(is_frozen, min_py, max_py):
        fake = _make_fake_compat(is_frozen, min_py, max_py)
        monkeypatch.setitem(sys.modules, 'httpie.compat', fake)
    return _patch

def test_get_site_paths_not_frozen(tmp_path, patch_compat):
    # Arrange: not frozen, any version values are irrelevant
    patch_compat(is_frozen=False, min_py=[3, 8], max_py=[3, 10])
    # Act
    paths = list(get_site_paths(tmp_path))
    # Assert: only one path, same as input
    assert len(paths) == 1
    assert paths[0] == tmp_path

def test_get_site_paths_frozen_version_range(tmp_path, patch_compat):
    # Arrange: frozen with min 3.7, max 3.9
    patch_compat(is_frozen=True, min_py=[3, 7], max_py=[3, 9])
    # Act
    paths = list(get_site_paths(tmp_path))
    # Assert: three paths, one per minor version
    expected = [
        tmp_path / 'site-packages' / 'py3.7',
        tmp_path / 'site-packages' / 'py3.8',
        tmp_path / 'site-packages' / 'py3.9',
    ]
    assert paths == expected

def test_get_site_paths_invalid_path_type(tmp_path, patch_compat):
    # Arrange: not frozen
    patch_compat(is_frozen=False, min_py=[3, 8], max_py=[3, 10])
    # Act & Assert: passing a string should raise TypeError
    with pytest.raises(TypeError):
        list(get_site_paths(str(tmp_path)))
