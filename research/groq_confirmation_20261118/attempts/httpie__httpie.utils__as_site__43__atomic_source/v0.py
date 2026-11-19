import os
import sysconfig
import pytest
from pathlib import Path

from httpie.utils import as_site


def test_as_site_returns_site_packages(tmp_path: Path):
    """as_site should return a Path that ends with 'site-packages'."""
    site = as_site(tmp_path)
    assert isinstance(site, Path)
    # The returned path should be absolute
    assert site.is_absolute()
    # It should end with the standard site-packages directory
    assert site.parts[-1] == "site-packages"
    # The path should be under the temporary directory
    assert str(site).startswith(str(tmp_path))


def test_as_site_with_extra_vars(tmp_path: Path):
    """Passing extra_vars should not alter the base path for purelib."""
    # Use an extra variable that is not used by the purelib format
    site1 = as_site(tmp_path, foo="bar")
    site2 = as_site(tmp_path)
    # Both should be identical
    assert site1 == site2
    # Ensure the extra variable did not affect the result
    assert "bar" not in str(site1)


def test_as_site_invalid_input_raises(tmp_path: Path):
    """as_site should raise a TypeError when given a non-Path argument."""
    with pytest.raises(TypeError):
        as_site("not a Path")
