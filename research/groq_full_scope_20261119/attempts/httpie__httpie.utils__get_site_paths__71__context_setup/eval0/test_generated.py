import pytest
from pathlib import Path
from httpie.utils import get_site_paths, as_site

def test_get_site_paths_returns_expected_path(tmp_path: Path):
    """
    Normal case: get_site_paths should yield a single Path that is the
    purelib directory under the supplied base path.
    """
    # Call the function with a temporary directory
    result = list(get_site_paths(tmp_path))
    assert len(result) == 1, "Expected exactly one path when not frozen"
    site_path = result[0]
    # The returned path should be a subpath of the temporary directory
    assert site_path.is_absolute()
    assert str(site_path).startswith(str(tmp_path))
    # The returned path should be the purelib directory for the base
    expected = as_site(tmp_path)
    assert site_path == expected, "Returned path does not match as_site output"

def test_get_site_paths_with_non_path_argument_raises():
    """
    Error case: passing a non-Path argument should raise a TypeError
    because as_site expects a Path instance.
    """
    with pytest.raises(TypeError):
        # Passing an integer will cause as_site to fail
        list(get_site_paths(42))

def test_get_site_paths_with_empty_path(tmp_path: Path):
    """
    Boundary case: passing an empty Path (Path('')) should still produce a
    valid purelib path under the current working directory.
    """
    empty_path = Path('')
    result = list(get_site_paths(empty_path))
    assert len(result) == 1
    site_path = result[0]
    # The path should be under the current working directory
    cwd = Path.cwd()
    assert str(site_path).startswith(str(cwd))
    # It should match the as_site output for the empty path
    expected = as_site(empty_path)
    assert site_path == expected
