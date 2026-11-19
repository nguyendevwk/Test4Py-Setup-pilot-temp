import sysconfig
import pytest
from pathlib import Path
from httpie.utils import as_site

def test_as_site_default(tmp_path):
    """as_site should append 'site-packages' to the given path."""
    result = as_site(tmp_path)
    expected = tmp_path / "site-packages"
    assert result == expected, f"Expected {expected}, got {result}"
    # Ensure the result is a Path instance
    assert isinstance(result, Path)

def test_as_site_override_base(tmp_path):
    """as_site should respect overridden 'base' in extra_vars."""
    override = Path("/tmp")
    result = as_site(tmp_path, base=str(override))
    expected = override / "site-packages"
    assert result == expected, f"Expected {expected}, got {result}"
    # The original tmp_path should remain unchanged
    assert tmp_path / "site-packages" != result

def test_as_site_nonexistent_directory(tmp_path):
    """as_site should work even if the directory does not exist."""
    non_existent = tmp_path / "does_not_exist"
    result = as_site(non_existent)
    expected = non_existent / "site-packages"
    assert result == expected, f"Expected {expected}, got {result}"
    # The path should not be created automatically
    assert not non_existent.exists()
