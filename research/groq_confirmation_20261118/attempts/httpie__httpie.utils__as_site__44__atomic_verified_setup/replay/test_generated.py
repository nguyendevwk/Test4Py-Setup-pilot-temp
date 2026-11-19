import sysconfig
import pytest
from pathlib import Path
from httpie.utils import as_site


def test_as_site_returns_site_packages_in_tmp(tmp_path: Path) -> None:
    """as_site should return a Path ending with 'site-packages' inside the given base."""
    result = as_site(tmp_path)
    assert isinstance(result, Path)
    assert result.is_absolute()
    assert result.parts[-1] == "site-packages"
    # The path should be under the temporary directory
    assert result.parts[:len(tmp_path.parts)] == tmp_path.parts


def test_as_site_overrides_base_with_extra_vars(tmp_path: Path) -> None:
    """Passing a 'base' in extra_vars should override the original path."""
    # Create a second temporary directory to act as the overridden base
    override = tmp_path / "override"
    override.mkdir()
    result = as_site(tmp_path, base=str(override))
    # The returned path should now be under the override directory
    assert result.parts[:len(override.parts)] == override.parts
    assert result.parts[-1] == "site-packages"


def test_as_site_with_nonexistent_path(tmp_path: Path) -> None:
    """as_site should not raise an error even if the provided Path does not exist."""
    non_existent = tmp_path / "does_not_exist"
    # Ensure the path does not exist
    assert not non_existent.exists()
    result = as_site(non_existent)
    # The function should still return a Path object pointing to the expected location
    assert isinstance(result, Path)
    assert result.parts[-1] == "site-packages"
    # The returned path should be under the non-existent path
    assert result.parts[:len(non_existent.parts)] == non_existent.parts
