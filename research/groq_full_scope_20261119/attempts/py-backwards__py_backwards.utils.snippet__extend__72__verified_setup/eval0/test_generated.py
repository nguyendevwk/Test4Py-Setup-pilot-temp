import ast
import pytest
from py_backwards.utils.snippet import extend

def test_extend_returns_none_with_empty_list(tmp_path):
    """Calling extend with an empty list should return None and not raise."""
    result = extend([])
    assert result is None

def test_extend_returns_none_with_non_iterable(tmp_path):
    """Calling extend with a non-iterable should return None and not raise."""
    result = extend(42)
    assert result is None

def test_extend_returns_none_with_assign_list(tmp_path):
    """Calling extend with a list of ast.Assign nodes should return None."""
    assign1 = ast.Assign(targets=[ast.Name(id='x', ctx=ast.Store())], value=ast.Constant(value=1))
    assign2 = ast.Assign(targets=[ast.Name(id='x', ctx=ast.Store())], value=ast.Constant(value=2))
    result = extend([assign1, assign2])
    assert result is None
