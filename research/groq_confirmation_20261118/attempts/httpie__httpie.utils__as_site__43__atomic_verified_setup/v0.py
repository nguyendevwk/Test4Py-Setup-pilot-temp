import sysconfig
import pytest
from pathlib import Path
from httpie.utils import as_site


def test_as_site_returns_expected_path(tmp_path: Path):
    """
    Verify that as_site returns the correct site-packages path for a given base directory.
    """
    # Create a temporary directory to act as the base
    base_dir = tmp_path / "base"
    base_dir.mkdir()

    # Call as_site with the base directory
    result = as_site(base_dir)

    # The expected path is constructed by sysconfig using the 'purelib' template
    expected = Path(sysconfig.get_path('purelib', vars={'base': str(base_dir)}))

    assert result == expected, f"Expected {expected!r}, got {result!r}"


def test_as_site_with_extra_vars(tmp_path: Path):
    """
    Verify that passing extra_vars correctly overrides the default template variables.
    """
    base_dir = tmp_path / "base"
    base_dir.mkdir()

    # Provide an extra variable that changes the template
    result = as_site(base_dir, prefix="custom")

    # The expected path should include the custom prefix
    expected = Path(sysconfig.get_path('purelib', vars={'base': str(base_dir), 'prefix': 'custom'}))

    assert result == expected, f"Expected {expected!r}, got {result!r}"


def test_as_site_invalid_input_raises_type_error():
    """
    Verify that passing a non-Path object raises a TypeError.
    """
    with pytest.raises(TypeError):
        # as_site expects a pathlib.Path; passing a string should raise TypeError
        as_site("not-a-path")
