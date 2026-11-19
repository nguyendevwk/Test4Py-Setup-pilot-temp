import ast
import pytest
from py_backwards.utils.snippet import extend

def test_extend_returns_none_and_does_not_modify_input():
    # Create a list of assignment AST nodes
    assignments = [
        ast.Assign(targets=[ast.Name(id='x', ctx=ast.Store())], value=ast.Constant(value=1)),
        ast.Assign(targets=[ast.Name(id='y', ctx=ast.Store())], value=ast.Constant(value=2)),
    ]
    # Call extend and ensure it returns None
    result = extend(assignments)
    assert result is None
    # Ensure the input list is unchanged
    assert assignments[0].value.value == 1
    assert assignments[1].value.value == 2

def test_extend_raises_type_error_for_non_iterable():
    # Pass a non-iterable object to extend
    with pytest.raises(TypeError):
        extend(42)

def test_extend_handles_empty_assignment_list():
    # Passing an empty list should not raise an exception
    empty_assignments = []
    result = extend(empty_assignments)
    assert result is None
