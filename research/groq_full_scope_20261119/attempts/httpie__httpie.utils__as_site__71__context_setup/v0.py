import sysconfig
import pytest
from pathlib import Path
from httpie.utils import as_site


def test_as_site_basic(tmp_path: Path):
    """as_site should return a Path that starts with the supplied base directory."""
    result = as_site(tmp_path)
    assert isinstance(result, Path)
    # The returned path should be inside the temporary directory
    assert result.is_absolute()
    assert str(result).startswith(str(tmp_path))
    # It should be the purelib path relative to the base
    expected_suffix = sysconfig.get_path('purelib', vars={'base': str(tmp_path)})
    assert str(result) == expected_suffix


def test_as_site_override_base(tmp_path: Path):
    """Passing a 'base' in extra_vars should override the supplied path."""
    # Create a second temporary directory
    other = tmp_path / "other"
    other.mkdir()
    # Override base with the other directory
    result = as_site(tmp_path, base=str(other))
    expected_suffix = sysconfig.get_path('purelib', vars={'base': str(other)})
    assert str(result) == expected_suffix
    # Ensure it does not start with the original tmp_path
    assert not str(result).startswith(str(tmp_path))
    assert str(result).startswith(str(other))


def test_as_site_with_non_path_input(tmp_path: Path):
    """as_site should accept a string path and convert it to a Path internally."""
    path_str = str(tmp_path)
    result = as_site(path_str)
    expected_suffix = sysconfig.get_path('purelib', vars={'base': path_str})
    assert str(result) == expected_suffix
    assert isinstance(result, Path)
