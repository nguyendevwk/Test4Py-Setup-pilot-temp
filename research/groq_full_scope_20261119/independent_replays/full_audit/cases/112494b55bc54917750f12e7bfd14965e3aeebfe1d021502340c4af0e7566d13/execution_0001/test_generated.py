import inspect
import textwrap
import pytest
from py_backwards.utils.helpers import get_source


def test_get_source_removes_common_padding():
    """get_source should strip the common indentation from the function source."""
    def sample_function():
        """A simple function."""
        x = 1
        return x

    source = get_source(sample_function)
    # The returned source should start at column 0 and preserve internal indentation
    assert source.startswith("def sample_function():")
    assert "\n    x = 1" in source
    assert "\n    return x" in source
    # Ensure no leading spaces on the first line
    assert source.splitlines()[0].startswith("def")


def test_get_source_handles_nested_functions():
    """Nested functions should have their indentation correctly adjusted."""
    def outer():
        def inner():
            return "inner"
        return inner()

    source = get_source(outer)
    # The outer function definition should start at column 0
    assert source.splitlines()[0].startswith("def outer():")
    # The inner function should be indented relative to outer
    assert "\n    def inner():" in source
    assert "\n        return \"inner\"" in source


def test_get_source_raises_on_non_callable():
    """Passing a non-callable to get_source should raise a TypeError."""
    with pytest.raises(TypeError):
        get_source(42)
