import sysconfig
import pytest
from pathlib import Path
from httpie.utils import as_site


def test_as_site_returns_path_with_given_base(tmp_path: Path):
    """as_site should return a Path that starts with the provided base."""
    result = as_site(tmp_path)
    assert isinstance(result, Path)
    # The returned path should be under the temporary directory
    assert result.as_posix().startswith(tmp_path.as_posix())
    # It should end with the standard site-packages suffix
    assert result.name == "site-packages"


def test_as_site_respects_extra_vars_overrides(tmp_path: Path):
    """Providing extra_vars should override the base used by sysconfig."""
    override = tmp_path / "override"
    override.mkdir()
    result = as_site(tmp_path, base=str(override))
    assert isinstance(result, Path)
    # The result should now start with the overridden base
    assert result.as_posix().startswith(override.as_posix())
    assert result.name == "site-packages"


def test_as_site_with_nonexistent_base(tmp_path: Path):
    """as_site should not raise when the base directory does not exist."""
    nonexistent = tmp_path / "does_not_exist"
    # Ensure the directory does not exist
    assert not nonexistent.exists()
    result = as_site(nonexistent)
    assert isinstance(result, Path)
    # The returned path should still be under the nonexistent directory
    assert result.as_posix().startswith(nonexistent.as_posix())
    assert result.name == "site-packages"
