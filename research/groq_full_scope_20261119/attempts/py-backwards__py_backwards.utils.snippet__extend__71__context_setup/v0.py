import pytest
import inspect
from typing import Any
from py_backwards.utils.snippet import extend
from typed_ast import ast3 as ast

def test_extend_returns_none_and_does_not_modify_input():
    # Create two simple assignment AST nodes
    assign1 = ast.Assign(targets=[ast.Name(id='x', ctx=ast.Store())], value=ast.Constant(value=1))
    assign2 = ast.Assign(targets=[ast.Name(id='y', ctx=ast.Store())], value=ast.Constant(value=2))
    assignments = [assign1, assign2]
    # Keep a copy for comparison
    original = assignments.copy()
    # Call extend
    result = extend(assignments)
    # extend should return None
    assert result is None
    # The input list should remain unchanged
    assert assignments == original
    # The elements should still be AST Assign nodes
    assert all(isinstance(a, ast.Assign) for a in assignments)

def test_extend_raises_type_error_on_non_iterable():
    # Pass a non-iterable object (e.g., an integer)
    with pytest.raises(TypeError):
        extend(42)

def test_extend_signature_and_docstring():
    # Verify that extend has the expected signature
    sig = inspect.signature(extend)
    assert sig.parameters == {'var': inspect.Parameter('var', inspect.Parameter.POSITIONAL_OR_KEYWORD)}
    # Verify that the return annotation is None
    assert sig.return_annotation is inspect.Signature.empty or sig.return_annotation is None
    # Verify that the docstring contains the word "Extends"
    assert 'Extends' in inspect.getdoc(extend)
