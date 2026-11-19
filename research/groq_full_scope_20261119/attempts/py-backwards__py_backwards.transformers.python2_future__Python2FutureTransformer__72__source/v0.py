import ast
import pytest
from py_backwards.transformers.python2_future import Python2FutureTransformer
from py_backwards.utils.snippet import snippet

def test_future_imports_added_to_simple_module():
    code = "x = 1\nprint(x)"
    tree = snippet(code)
    transformer = Python2FutureTransformer()
    new_tree = transformer.visit(tree)
    # The first four nodes should be the future imports
    import_names = ["absolute_import", "division", "print_function", "unicode_literals"]
    for i, name in enumerate(import_names):
        node = new_tree.body[i]
        assert isinstance(node, ast.ImportFrom)
        assert node.module == "__future__"
        assert node.names[0].name == name
    # The rest of the body should remain unchanged
    assert isinstance(new_tree.body[-1], ast.Expr)
    assert isinstance(new_tree.body[-1].value, ast.Call)
    assert transformer._tree_changed is True

def test_future_imports_added_to_empty_module():
    code = ""
    tree = snippet(code)
    transformer = Python2FutureTransformer()
    new_tree = transformer.visit(tree)
    # Body should contain only the future imports
    assert len(new_tree.body) == 4
    import_names = ["absolute_import", "division", "print_function", "unicode_literals"]
    for i, name in enumerate(import_names):
        node = new_tree.body[i]
        assert isinstance(node, ast.ImportFrom)
        assert node.module == "__future__"
        assert node.names[0].name == name
    assert transformer._tree_changed is True

def test_future_imports_do_not_duplicate_if_present():
    code = (
        "from __future__ import division\n"
        "x = 2\n"
    )
    tree = snippet(code)
    transformer = Python2FutureTransformer()
    new_tree = transformer.visit(tree)
    # The first import should still be division, but all four should appear
    import_names = ["absolute_import", "division", "print_function", "unicode_literals"]
    for i, name in enumerate(import_names):
        node = new_tree.body[i]
        assert isinstance(node, ast.ImportFrom)
        assert node.module == "__future__"
        assert node.names[0].name == name
    # The original division import should not be duplicated
    assert len([n for n in new_tree.body if isinstance(n, ast.ImportFrom) and n.module == "__future__"]) == 4
    assert transformer._tree_changed is True
