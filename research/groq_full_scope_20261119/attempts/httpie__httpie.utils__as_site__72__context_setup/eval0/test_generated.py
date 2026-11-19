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
    # Ensure the returned path is under the overridden base
    assert str(site_path).startswith(str(new_base))

def test_as_site_accepts_non_path_input_and_raises_on_invalid_type(tmp_path: Path):
    """as_site should accept a Path object but raise a TypeError when given an invalid type."""
    # Valid input: Path object
    assert isinstance(as_site(tmp_path), Path)
    # Invalid input: integer (will be converted to string but still works)
    assert isinstance(as_site(123), Path)
    # Invalid input: None should raise a TypeError because sysconfig.get_path expects a string
    with pytest.raises(TypeError):
        as_site(None)
