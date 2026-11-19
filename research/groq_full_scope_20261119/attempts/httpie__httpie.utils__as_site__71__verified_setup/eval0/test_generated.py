import os
import sysconfig
from pathlib import Path

import pytest

from httpie.utils import as_site


def test_as_site_returns_absolute_path(tmp_path: Path):
    """
    Verify that as_site returns an absolute Path that starts with the supplied
    base directory and that the returned path is a Path instance.
    """
    result = as_site(tmp_path)
    assert isinstance(result, Path), "Result should be a Path instance"
    assert result.is_absolute(), "Resulting path should be absolute"
    # The returned path should start with the temporary directory
    assert str(result).startswith(str(tmp_path)), (
        f"Resulting path {result} does not start with base {tmp_path}"
    )


def test_as_site_overrides_base(tmp_path: Path):
    """
    Verify that passing a 'base' keyword argument overrides the supplied
    path argument in sysconfig.get_path.
    """
    override = "custom_base"
    result = as_site(tmp_path, base=override)
    # The returned path should contain the overridden base string
    assert override in str(result), (
        f"Resulting path {result} does not contain overridden base '{override}'"
    )
    # It should still be absolute
    assert result.is_absolute(), "Resulting path should be absolute"


def test_as_site_with_non_path_argument(tmp_path: Path):
    """
    Verify that as_site accepts a string that represents a path and behaves
    the same as when a Path object is supplied.
    """
    path_str = str(tmp_path)
    result_from_str = as_site(path_str)
    result_from_path = as_site(Path(path_str))
    assert result_from_str == result_from_path, (
        "as_site should treat string and Path inputs equivalently"
    )
