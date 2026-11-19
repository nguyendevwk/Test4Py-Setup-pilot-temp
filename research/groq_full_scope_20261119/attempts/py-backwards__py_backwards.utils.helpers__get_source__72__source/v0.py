import inspect
import textwrap
import pytest
from py_backwards.utils.helpers import get_source


def test_get_source_removes_common_padding():
    """get_source should strip the common indentation from the function source."""
    def sample_function():
        """Example docstring."""
        x = 1
        return x

    source = get_source(sample_function)
    # The returned source should start at column 0 and match the original function body
    expected = textwrap.dedent(inspect.getsource(sample_function))
    assert source == expected


def test_get_source_handles_nested_functions():
    """get_source should correctly handle functions defined inside other functions."""
    def outer():
        def inner():
            return "inner"
        return inner()

    source = get_source(outer)
    # The source should contain the inner function definition without extra indentation
    assert "def inner()" in source
    assert source.startswith("def outer():")


def test_get_source_raises_on_non_callable():
    """get_source should raise a TypeError when passed a non-callable object."""
    with pytest.raises(TypeError):
        get_source(42)
