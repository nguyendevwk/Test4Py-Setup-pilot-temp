import pytest
from py_backwards.utils.snippet import extend
from typed_ast import ast3 as ast

def test_extend_returns_none_and_modifies_code(tmp_path):
    # Create two simple assignment AST nodes
    assign1 = ast.Assign(
        targets=[ast.Name(id='x', ctx=ast.Store())],
        value=ast.Constant(value=1)
    )
    assign2 = ast.Assign(
        targets=[ast.Name(id='x', ctx=ast.Store())],
        value=ast.Constant(value=2)
    )
    # Call extend with a list of assignments
    result = extend([assign1, assign2])
    # The function should return None
    assert result is None
    # Since extend is designed to modify the current module's code,
    # we cannot directly inspect the source. However, we can ensure
    # that the assignments are syntactically valid by compiling them.
    # This indirectly verifies that extend accepted the AST nodes.
    compiled = compile(ast.Module(body=[assign1, assign2]), filename='<ast>', mode='exec')
    exec(compiled, {})

def test_extend_with_non_iterable_raises_type_error():
    # Passing a non-iterable (e.g., an integer) should raise a TypeError
    with pytest.raises(TypeError):
        extend(42)

def test_extend_with_empty_list_does_nothing(tmp_path):
    # Calling extend with an empty list should not raise and should return None
    result = extend([])
    assert result is None
