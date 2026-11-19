import pytest
from py_backwards.utils.helpers import get_source

def test_get_source_returns_clean_source():
    def sample_function(x, y):
        """Example docstring."""
        return x + y

    source = get_source(sample_function)
    # The returned source should match the original definition without leading indentation
    expected = """def sample_function(x, y):
    \"\"\"Example docstring.\"\"\"
    return x + y"""
    assert source == expected

def test_get_source_handles_nested_functions():
    def outer(a):
        def inner(b):
            return a * b
        return inner(5)

    source = get_source(outer)
    # The source should include the nested function definition correctly indented
    assert "def inner(b):" in source
    assert "return a * b" in source
    # Leading indentation should be stripped
    assert source.startswith("def outer(a):")

def test_get_source_raises_on_non_callable():
    with pytest.raises(TypeError):
        get_source(42)
