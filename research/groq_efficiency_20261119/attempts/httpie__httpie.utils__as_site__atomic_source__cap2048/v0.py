import sysconfig
import pytest
from pathlib import Path
from httpie.utils import as_site


def test_as_site_basic(tmp_path: Path):
    """as_site should return the expected site-packages path for a given base."""
    base = tmp_path
    result = as_site(base)
    expected = Path(sysconfig.get_path('purelib', vars={'base': str(base)}))
    assert isinstance(result, Path)
    assert result == expected
    assert result.is_absolute()


def test_as_site_with_extra_vars(tmp_path: Path):
    """Passing extra_vars should not alter the computed path unless they affect the format."""
    base = tmp_path
    # Provide an extra variable that is not used in the purelib format
    result = as_site(base, foo='bar')
    expected = Path(sysconfig.get_path('purelib', vars={'base': str(base), 'foo': 'bar'}))
    assert result == expected
    # Ensure that the extra variable is ignored in the path string
    assert 'bar' not in result.as_posix()


def test_as_site_nonexistent_path(tmp_path: Path):
    """as_site should construct a path even if the base directory does not exist."""
    nonexistent = tmp_path / "does_not_exist"
    result = as_site(nonexistent)
    expected = Path(sysconfig.get_path('purelib', vars={'base': str(nonexistent)}))
    assert result == expected
    # The path should not exist on the filesystem
    assert not result.exists()
