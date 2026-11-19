import ast
import pytest
from typed_ast import ast3 as typed_ast
from py_backwards.utils.snippet import extend_tree, find, get_non_exp_parent_and_index, replace_at

def build_tree(source: str) -> typed_ast.AST:
    """Parse source code into a typed_ast AST."""
    return typed_ast.parse(source)

def test_extend_tree_replaces_call_with_variable():
    # Source contains a call to extend that should be replaced by a variable.
    src = """
def foo():
    x = extend(y)
"""
    tree = build_tree(src)
    # Prepare variables mapping: 'y' should be replaced by a string literal.
    variables = {'y': typed_ast.Str(s='replaced')}
    extend_tree(tree, variables)

    # After transformation, the call should be replaced by the string literal.
    # Find the assignment target and value.
    assign = find(tree, typed_ast.Assign)[0]
    assert isinstance(assign.value, typed_ast.Str)
    assert assign.value.s == 'replaced'

def test_extend_tree_no_effect_when_no_extend_call():
    # Source without any extend calls should remain unchanged.
    src = """
def bar():
    a = 1
    b = 2
"""
    tree = build_tree(src)
    variables = {'x': typed_ast.Str(s='unused')}
    extend_tree(tree, variables)

    # The tree should still contain the original assignments.
    assigns = find(tree, typed_ast.Assign)
    assert len(assigns) == 2
    assert isinstance(assigns[0].value, typed_ast.Num)
    assert assigns[0].value.n == 1

def test_extend_tree_raises_key_error_for_missing_variable():
    # Source contains an extend call with an argument not present in variables.
    src = """
def baz():
    z = extend(missing)
"""
    tree = build_tree(src)
    variables = {}  # empty mapping

    with pytest.raises(KeyError):
        extend_tree(tree, variables)
