import sysconfig
import pytest
from pathlib import Path
from httpie.utils import as_site


def test_as_site_returns_expected_path(tmp_path: Path):
    """as_site should return the purelib path for the given base directory."""
    expected = Path(sysconfig.get_path('purelib', vars={'base': str(tmp_path)}))
    result = as_site(tmp_path)
    assert result == expected
    assert isinstance(result, Path)


def test_as_site_handles_trailing_slash(tmp_path: Path):
    """as_site should correctly handle a Path that ends with a slash."""
    # Create a subdirectory to ensure the path is not the root of tmp_path
    sub = tmp_path / "subdir"
    sub.mkdir()
    # Add a trailing slash by converting to string and back to Path
    path_with_slash = Path(str(sub) + "/")
    expected = Path(sysconfig.get_path('purelib', vars={'base': str(sub)}))
    result = as_site(path_with_slash)
    assert result == expected
    assert result == Path(expected)  # ensure Path equality works


def test_as_site_ignores_extra_vars(tmp_path: Path):
    """as_site should ignore extra_vars that do not affect the 'base' key."""
    # Pass an extra variable that is not used by sysconfig.get_path
    result = as_site(tmp_path, foo="bar")
    expected = Path(sysconfig.get_path('purelib', vars={'base': str(tmp_path)}))
    assert result == expected
    # Ensure the extra variable did not alter the result
    assert result == expected
