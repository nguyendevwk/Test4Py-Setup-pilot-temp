import os
import sysconfig
from pathlib import Path

import pytest

from httpie.utils import as_site


def test_as_site_returns_site_packages(tmp_path: Path):
    """as_site should return a Path ending with 'site-packages'."""
    result = as_site(tmp_path)
    assert isinstance(result, Path)
    assert result.is_absolute()
    # The purelib path is usually <base>/site-packages
    assert result.name == "site-packages"
    # The parent directory should be the tmp_path we passed
    assert result.parent == tmp_path


def test_as_site_ignores_extra_vars(tmp_path: Path):
    """Passing extra_vars should not alter the computed path."""
    result1 = as_site(tmp_path, foo="bar", baz=123)
    result2 = as_site(tmp_path)
    assert result1 == result2
    # Ensure that the extra vars are not reflected in the path string
    assert "foo" not in str(result1)
    assert "baz" not in str(result1)


def test_as_site_with_non_path_input(tmp_path: Path):
    """as_site should accept any object convertible to str."""
    # Pass a string path
    result_str = as_site(str(tmp_path))
    assert result_str == as_site(tmp_path)

    # Pass an integer (converted to string)
    result_int = as_site(42)
    # The base will be '42', so the path should end with '42/site-packages'
    assert result_int.name == "site-packages"
    assert result_int.parent.name == "42"
