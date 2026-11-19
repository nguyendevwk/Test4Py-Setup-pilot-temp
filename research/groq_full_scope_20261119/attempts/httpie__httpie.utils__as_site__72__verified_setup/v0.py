import sysconfig
import pytest
from pathlib import Path
from httpie.utils import as_site

def test_as_site_returns_site_packages_path(tmp_path: Path):
    """as_site should return the site-packages path derived from the given base path."""
    site_path = as_site(tmp_path)
    expected = Path(sysconfig.get_path('purelib', vars={'base': str(tmp_path)}))
    assert site_path == expected
    # The returned path should be a subpath of the base path
    assert str(site_path).startswith(str(tmp_path))

def test_as_site_with_extra_vars_overrides_base(tmp_path: Path):
    """Passing an extra 'base' variable should override the original path."""
    new_base = tmp_path / "custom"
    site_path = as_site(tmp_path, base=str(new_base))
    expected = Path(sysconfig.get_path('purelib', vars={'base': str(new_base)}))
    assert site_path == expected
    # Ensure the original tmp_path is not part of the result
    assert str(site_path) != str(tmp_path)

def test_as_site_with_non_path_argument(tmp_path: Path):
    """as_site accepts a Path-like object; passing a string should still work."""
    site_path = as_site(str(tmp_path))
    expected = Path(sysconfig.get_path('purelib', vars={'base': str(tmp_path)}))
    assert site_path == expected
