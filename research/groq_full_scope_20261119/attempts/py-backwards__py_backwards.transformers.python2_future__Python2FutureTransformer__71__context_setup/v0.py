import pytest
from typed_ast import ast3 as ast
from py_backwards.transformers.python2_future import Python2FutureTransformer


def test_adds_future_imports_to_nonempty_module(tmp_path):
    # Create a simple module with one function
    source = "def foo():\n    return 1\n"
    tree = ast.parse(source, filename="<ast>")
    transformer = Python2FutureTransformer()
    transformed = transformer.visit(tree)

    # The first four nodes should be ImportFrom from __future__
    imports = transformed.body[:4]
    expected_names = [
        ("absolute_import", 0),
        ("division", 0),
        ("print_function", 0),
        ("unicode_literals", 0),
    ]
    for node, (name, level) in zip(imports, expected_names):
        assert isinstance(node, ast.ImportFrom)
        assert node.module == "__future__"
        assert node.level == level
        assert len(node.names) == 1
        assert node.names[0].name == name

    # The original function should remain unchanged after the imports
    assert isinstance(transformed.body[4], ast.FunctionDef)
    assert transformed.body[4].name == "foo"


def test_empty_module_still_has_future_imports(tmp_path):
    # Empty module
    source = ""
    tree = ast.parse(source, filename="<ast>")
    transformer = Python2FutureTransformer()
    transformed = transformer.visit(tree)

    # All nodes should be the future imports
    assert len(transformed.body) == 4
    for node in transformed.body:
        assert isinstance(node, ast.ImportFrom)
        assert node.module == "__future__"


def test_tree_changed_flag_set_on_visit(tmp_path):
    source = "x = 1"
    tree = ast.parse(source, filename="<ast>")
    transformer = Python2FutureTransformer()
    # Before visiting, flag should be False
    assert not getattr(transformer, "_tree_changed", False)
    transformer.visit(tree)
    # After visiting, flag should be True
    assert transformer._tree_changed is True
