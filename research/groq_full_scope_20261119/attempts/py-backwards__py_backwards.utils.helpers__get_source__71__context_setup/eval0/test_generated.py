import builtins
import inspect
import types
import pytest
from py_backwards.utils.helpers import get_source

def test_get_source_returns_clean_source():
    def sample_function(x, y=2):
        """Example docstring."""
        return x + y

    source = get_source(sample_function)
    # The returned source should match the original function definition without
    # leading indentation and with the correct signature.
    expected = """def sample_function(x, y=2):
        \"\"\"Example docstring.\"\"\"
        return x + y"""
    assert source == expected

def test_get_source_handles_nested_functions_and_indentation():
    def outer():
        def inner(a, b):
            return a * b
        return inner(3, 4)

    source = get_source(outer)
    # The source should contain the definition of outer and the nested inner
    # function without any leading indentation.
    assert "def outer():" in source
    assert "def inner(a, b):" in source
    assert "return a * b" in source
    # Ensure that the indentation inside the function bodies is preserved.
    lines = source.splitlines()
    assert lines[1].startswith("    \"\"\"") or lines[1].startswith("    return")

def test_get_source_raises_on_builtin_function():
    with pytest.raises(OSError):
        get_source(builtins.len)
