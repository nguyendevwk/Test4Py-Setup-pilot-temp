import inspect
import textwrap
import pytest
from py_backwards.utils.helpers import get_source


def test_get_source_removes_common_padding():
    """get_source should strip the common indentation from the function source."""
    def sample_function():
        """A simple function."""
        return 42

    source = get_source(sample_function)
    # The returned source should start at column 0 and contain the function definition
    assert source.startswith("def sample_function():")
    # The docstring should be indented correctly
    assert '"""A simple function."""' in source
    # The return statement should be indented by one level
    assert "return 42" in source
    # No leading whitespace should remain
    assert not source.startswith("    ")


def test_get_source_handles_nested_functions():
    """get_source should correctly handle nested functions and preserve relative indentation."""
    def outer():
        def inner():
            return "inner"
        return inner()

    source = get_source(outer)
    # The outer function definition should start at column 0
    assert source.startswith("def outer():")
    # The inner function should be indented by one level relative to outer
    assert "def inner():" in source
    # The return inside inner should be indented correctly
    assert "return \"inner\"" in source
    # No extra indentation should be present at the start of any line
    assert all(not line.startswith("    ") for line in source.splitlines() if line.strip())


def test_get_source_raises_on_non_callable():
    """get_source should raise a TypeError when called with a non-callable object."""
    with pytest.raises(TypeError):
        get_source(42)  # non-callable argument
