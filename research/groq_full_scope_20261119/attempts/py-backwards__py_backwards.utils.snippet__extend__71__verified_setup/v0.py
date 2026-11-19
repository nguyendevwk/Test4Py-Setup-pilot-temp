import ast
import builtins
import sys
import types
import pytest

from py_backwards.utils.snippet import extend


def test_extend_returns_none_and_does_not_modify_input():
    """extend should return None and leave the input list unchanged."""
    assignments = [
        ast.parse("x = 1").body[0],
        ast.parse("x = 2").body[0],
    ]
    original = assignments.copy()
    result = extend(assignments)
    assert result is None
    assert assignments == original, "extend should not modify the input list"


def test_extend_with_empty_list_does_nothing():
    """extend should handle an empty list gracefully."""
    empty = []
    result = extend(empty)
    assert result is None
    assert empty == [], "extend should not alter an empty list"


def test_extend_with_non_iterable_raises_type_error():
    """extend should raise a TypeError when given a non-iterable argument."""
    with pytest.raises(TypeError):
        extend(42)
