import sysconfig
import pytest
from pathlib import Path
from httpie.utils import as_site

def test_as_site_returns_site_packages(tmp_path: Path):
    """as_site should return a Path ending with 'site-packages' relative to the given base."""
    result = as_site(tmp_path)
    assert isinstance(result, Path)
    # The default purelib path template ends with "site-packages"
    assert result.name == "site-packages"
    # The parent directory should be the tmp_path we provided
    assert result.parent == tmp_path

def test_as_site_with_extra_vars(tmp_path: Path):
    """Passing extra_vars should not alter the base directory but can be used to override other parts of the path."""
    # Use a custom variable that is not part of the default template
    result = as_site(tmp_path, custom="value")
    assert isinstance(result, Path)
    assert result.name == "site-packages"
    assert result.parent == tmp_path
    # The custom variable should be ignored for the purelib path
    assert "value" not in str(result)

def test_as_site_invalid_input_raises_type_error():
    """as_site should raise a TypeError when the first argument is not a Path instance."""
    with pytest.raises(TypeError):
        as_site("not-a-path")
