import sysconfig
import pytest
from pathlib import Path
from httpie.utils import as_site

def test_as_site_basic(tmp_path):
    """as_site should return the site-packages path relative to the given base."""
    # Create a temporary directory to act as the base
    base = tmp_path / "myproject"
    base.mkdir()
    # Call as_site with the base directory
    result = as_site(base)
    # The result should be a Path object
    assert isinstance(result, Path)
    # The result should be the same as sysconfig's purelib path with the base overridden
    expected = Path(sysconfig.get_path('purelib', vars={'base': str(base)}))
    assert result == expected
    # The result should be inside the base directory
    assert str(result).startswith(str(base))

def test_as_site_with_extra_vars(tmp_path):
    """as_site should honor extra_vars passed to sysconfig.get_path."""
    base = tmp_path / "project"
    base.mkdir()
    # Use an extra variable to change the layout
    result = as_site(base, layout="lib")
    # The returned path should reflect the 'layout' variable
    expected = Path(sysconfig.get_path('purelib', vars={'base': str(base), 'layout': 'lib'}))
    assert result == expected
    # Ensure that the layout variable actually changed the path
    assert "lib" in str(result)

def test_as_site_invalid_input():
    """Passing a non-Path object should raise a TypeError."""
    with pytest.raises(TypeError):
        as_site(123)  # int is not a valid Path argument
