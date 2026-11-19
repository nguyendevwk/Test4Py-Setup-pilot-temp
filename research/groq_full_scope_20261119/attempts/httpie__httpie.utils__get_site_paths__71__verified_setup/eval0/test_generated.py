import pathlib
import pytest
from httpie.utils import get_site_paths

@pytest.fixture
def compat_module(monkeypatch):
    """Provide a fake httpie.compat module with controlled attributes."""
    class FakeCompat:
        MIN_SUPPORTED_PY_VERSION = [3, 6]
        MAX_SUPPORTED_PY_VERSION = [3, 8]
        is_frozen = False
    monkeypatch.setitem(
        sys.modules, 'httpie.compat', FakeCompat()
    )
    return FakeCompat

def test_get_site_paths_non_frozen(tmp_path, compat_module):
    """When the application is not frozen, only the original path is yielded."""
    compat_module.is_frozen = False
    result = list(get_site_paths(tmp_path))
    assert result == [tmp_path]
    assert all(isinstance(p, pathlib.Path) for p in result)

def test_get_site_paths_frozen_range(tmp_path, compat_module):
    """When frozen, yield paths for each supported minor version."""
    compat_module.is_frozen = True
    compat_module.MIN_SUPPORTED_PY_VERSION = [3, 6]
    compat_module.MAX_SUPPORTED_PY_VERSION = [3, 8]
    result = list(get_site_paths(tmp_path))
    expected = [
        tmp_path / 'site-packages' / 'py3.6',
        tmp_path / 'site-packages' / 'py3.7',
        tmp_path / 'site-packages' / 'py3.8',
    ]
    assert result == expected

def test_get_site_paths_frozen_boundary(tmp_path, compat_module):
    """When MIN and MAX are equal, only one path is yielded."""
    compat_module.is_frozen = True
    compat_module.MIN_SUPPORTED_PY_VERSION = [3, 9]
    compat_module.MAX_SUPPORTED_PY_VERSION = [3, 9]
    result = list(get_site_paths(tmp_path))
    expected = [tmp_path / 'site-packages' / 'py3.9']
    assert result == expected
