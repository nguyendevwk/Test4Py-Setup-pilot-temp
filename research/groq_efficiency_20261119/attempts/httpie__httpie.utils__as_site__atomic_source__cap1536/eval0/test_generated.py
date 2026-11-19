import sysconfig
from pathlib import Path

import pytest

from httpie.utils import as_site


def test_as_site_default(tmp_path: Path):
    """as_site should return the default site-packages path for the given base."""
    site_path = as_site(tmp_path)
    expected = Path(
        sysconfig.get_path(
            "purelib",
            vars={"base": str(tmp_path)},
        )
    )
    assert site_path == expected
    assert site_path.is_absolute()


def test_as_site_with_extra_vars(tmp_path: Path):
    """as_site should incorporate extra_vars into the path resolution."""
    # Add a custom variable that is used in the format string for purelib
    # (e.g., 'py_version' to force a specific Python version string)
    custom_py_version = "3.9"
    site_path = as_site(tmp_path, py_version=custom_py_version)
    expected = Path(
        sysconfig.get_path(
            "purelib",
            vars={"base": str(tmp_path), "py_version": custom_py_version},
        )
    )
    assert site_path == expected
    # Ensure the custom variable is reflected in the path string
    assert f"python{custom_py_version}" in site_path.as_posix()


def test_as_site_override_base(tmp_path: Path, tmp_path_factory):
    """as_site should allow overriding the base path via extra_vars."""
    # Create a second temporary directory to act as the overridden base
    overridden_base = tmp_path_factory.mktemp("override")
    site_path = as_site(tmp_path, base=str(overridden_base))
    expected = Path(
        sysconfig.get_path(
            "purelib",
            vars={"base": str(overridden_base)},
        )
    )
    assert site_path == expected
    # The resulting path should not contain the original tmp_path
    assert str(tmp_path) not in site_path.as_posix()
