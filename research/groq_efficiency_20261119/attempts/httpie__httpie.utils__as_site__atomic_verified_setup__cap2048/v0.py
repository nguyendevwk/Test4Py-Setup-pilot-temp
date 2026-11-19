import sysconfig
import pytest
from pathlib import Path
from httpie.utils import as_site


def test_as_site_returns_expected_path(tmp_path: Path):
    """as_site should return the site-packages path for the given base."""
    result = as_site(tmp_path)
    expected = Path(sysconfig.get_path('purelib', vars={'base': str(tmp_path)}))
    assert result == expected
    assert result.is_absolute()


def test_as_site_with_extra_vars_overrides_base(tmp_path: Path):
    """Passing extra_vars should override the base used by sysconfig.get_path."""
    new_base = tmp_path / "custom"
    result = as_site(tmp_path, base=str(new_base))
    expected = Path(sysconfig.get_path('purelib', vars={'base': str(new_base)}))
    assert result == expected
    assert str(new_base) in str(result)


def test_as_site_raises_on_invalid_var(tmp_path: Path):
    """Providing an unknown variable to sysconfig.get_path should raise KeyError."""
    with pytest.raises(KeyError):
        # 'invalid' is not a recognized variable for the 'purelib' path
        as_site(tmp_path, invalid="value")
