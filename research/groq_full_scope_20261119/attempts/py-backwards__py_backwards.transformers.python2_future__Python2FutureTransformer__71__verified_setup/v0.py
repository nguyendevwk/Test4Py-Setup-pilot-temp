import pytest
import typed_ast.ast3 as ast
from py_backwards.transformers.python2_future import Python2FutureTransformer


def _parse_code(code: str) -> ast.Module:
    """Parse source code into a typed_ast Module node."""
    return ast.parse(code, mode="exec")


def test_adds_future_imports():
    """The transformer should prepend the four __future__ imports."""
    transformer = Python2FutureTransformer()
    module = _parse_code("")  # empty module
    transformed = transformer.visit_Module(module)

    # The first four nodes should be ImportFrom from "__future__"
    expected_names = [
        "absolute_import",
        "division",
        "print_function",
        "unicode_literals",
    ]
    actual_names = [
        node.names[0].name for node in transformed.body[:4]
    ]
    assert actual_names == expected_names
    # The rest of the body should remain unchanged (empty)
    assert len(transformed.body) == 4


def test_tree_changed_flag():
    """The transformer should set the _tree_changed flag when visiting a module."""
    transformer = Python2FutureTransformer()
    module = _parse_code("x = 1")
    transformer.visit_Module(module)
    assert transformer._tree_changed is True


def test_preserves_existing_body():
    """Existing module body should be preserved after adding imports."""
    code = "def foo():\n    return 42\n"
    transformer = Python2FutureTransformer()
    module = _parse_code(code)
    transformed = transformer.visit_Module(module)

    # After the four imports, the original function definition should follow
    assert isinstance(transformed.body[4], ast.FunctionDef)
    assert transformed.body[4].name == "foo"
    # The function body should contain a single Return node
    assert isinstance(transformed.body[4].body[0], ast.Return)
    assert transformed.body[4].body[0].value.n == 42
