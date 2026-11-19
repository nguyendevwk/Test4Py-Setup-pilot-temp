import ast as pyast
import typed_ast.ast3 as ast
import pytest
from py_backwards.transformers.starred_unpacking import StarredUnpackingTransformer

def _parse(code: str) -> ast.AST:
    """Parse source code into a typed_ast AST."""
    return ast.parse(code)

def _ast_dump(node: ast.AST) -> str:
    """Return a canonical string representation of an AST node."""
    return ast.dump(node, annotate_fields=True, include_attributes=False)

def test_list_with_starred_unpacking():
    """Verify that a list containing a starred expression is transformed into a sum of lists."""
    code = "[2, *range(10), 1]"
    tree = _parse(code)
    transformer = StarredUnpackingTransformer()
    transformer.visit(tree)
    # The resulting node should be a BinOp representing [2] + list(range(10)) + [1]
    expected = pyast.parse("[2] + list(range(10)) + [1]").body[0].value
    assert _ast_dump(tree.body[0].value) == _ast_dump(expected)

def test_call_with_multiple_starred_arguments():
    """Verify that a function call with multiple starred arguments is transformed correctly."""
    code = "print(*range(1), *range(3))"
    tree = _parse(code)
    transformer = StarredUnpackingTransformer()
    transformer.visit(tree)
    # The resulting call should have a single starred argument: list(range(1)) + list(range(3))
    expected_call = pyast.parse("print(*(list(range(1)) + list(range(3))))").body[0].value
    assert _ast_dump(tree.body[0].value) == _ast_dump(expected_call)

def test_no_starred_no_change():
    """Ensure that nodes without starred expressions remain unchanged."""
    code = "[1, 2, 3]"
    tree = _parse(code)
    transformer = StarredUnpackingTransformer()
    transformer.visit(tree)
    # The AST should be identical to the original
    original = pyast.parse(code).body[0].value
    assert _ast_dump(tree.body[0].value) == _ast_dump(original)
