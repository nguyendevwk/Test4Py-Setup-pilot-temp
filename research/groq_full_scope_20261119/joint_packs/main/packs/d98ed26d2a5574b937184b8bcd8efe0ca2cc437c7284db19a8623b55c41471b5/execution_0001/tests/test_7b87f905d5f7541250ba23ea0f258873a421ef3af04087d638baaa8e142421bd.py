import ast as py_ast
import typed_ast.ast3 as ast
import pytest

from py_backwards.utils.snippet import extend_tree


def test_extend_tree_replaces_call_with_variable(tmp_path):
    # Source code containing an extend call
    src = "extend(x)"
    tree = ast.parse(src)

    # Variable mapping: replace the call with a new Name node 'y'
    new_node = ast.Name(id="y", ctx=ast.Load())
    variables = {"x": new_node}

    # Apply extend_tree
    extend_tree(tree, variables)

    # After replacement, the body should contain a single Name node 'y'
    assert len(tree.body) == 1
    assert isinstance(tree.body[0], ast.Name)
    assert tree.body[0].id == "y"


def test_extend_tree_no_call_unchanged(tmp_path):
    # Source code without an extend call
    src = "print('hello')"
    tree = ast.parse(src)

    # Copy of original tree for comparison
    original_body = list(tree.body)

    # Apply extend_tree with empty variables
    extend_tree(tree, {})

    # Tree should remain unchanged
    assert len(tree.body) == len(original_body)
    assert all(
        type(a) == type(b) and getattr(a, "id", None) == getattr(b, "id", None)
        for a, b in zip(tree.body, original_body)
    )


def test_extend_tree_missing_variable_raises_key_error(tmp_path):
    # Source code with an extend call referencing 'z'
    src = "extend(z)"
    tree = ast.parse(src)

    # Empty variables dict; should raise KeyError when accessing variables['z']
    with pytest.raises(KeyError):
        extend_tree(tree, {})
