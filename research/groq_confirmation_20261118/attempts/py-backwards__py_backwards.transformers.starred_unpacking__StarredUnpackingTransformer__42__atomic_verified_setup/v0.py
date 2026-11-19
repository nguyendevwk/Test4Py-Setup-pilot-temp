import ast as pyast
import typed_ast.ast3 as ast
import pytest
from py_backwards.transformers.starred_unpacking import StarredUnpackingTransformer

def _parse_and_transform(code: str) -> ast.AST:
    """Parse Python code with typed_ast and apply the transformer."""
    tree = ast.parse(code)
    transformer = StarredUnpackingTransformer()
    transformer.visit(tree)
    return tree

def _ast_dump(node: ast.AST) -> str:
    """Return a deterministic string representation of an AST node."""
    return ast.dump(node, annotate_fields=True, include_attributes=False)

def test_list_with_starred_unpacking():
    code = "[2, *range(10), 1]"
    tree = _parse_and_transform(code)
    # The root should be a Module containing a single Expr with a BinOp
    expr = tree.body[0].value
    assert isinstance(expr, ast.BinOp)
    # Left side should be a BinOp of [2] + list(range(10))
    left = expr.left
    assert isinstance(left, ast.BinOp)
    assert isinstance(left.left, ast.List)
    assert isinstance(left.right, ast.Call)
    assert left.right.func.id == "list"
    # Right side should be [1]
    assert isinstance(expr.right, ast.List)
    # Verify the structure matches expected
    expected = (
        "BinOp(left=BinOp(left=List(elts=[Constant(value=2)]), "
        "right=Call(func=Name(id='list'), args=[Call(func=Name(id='range'), "
        "args=[Constant(value=10)], keywords=[])]), op=Add()), "
        "right=List(elts=[Constant(value=1)]), op=Add())"
    )
    assert _ast_dump(expr) == expected

def test_call_with_starred_unpacking():
    code = "print(*range(1), *range(3))"
    tree = _parse_and_transform(code)
    # The root should be a Module containing a single Expr with a Call
    call = tree.body[0].value
    assert isinstance(call, ast.Call)
    # The function should be Name 'print'
    assert isinstance(call.func, ast.Name)
    assert call.func.id == "print"
    # The args should be a single Starred wrapping a BinOp
    assert len(call.args) == 1
    starred = call.args[0]
    assert isinstance(starred, ast.Starred)
    binop = starred.value
    assert isinstance(binop, ast.BinOp)
    # Left side: list(range(1))
    assert isinstance(binop.left, ast.Call)
    assert binop.left.func.id == "list"
    # Right side: list(range(3))
    assert isinstance(binop.right, ast.Call)
    assert binop.right.func.id == "list"
    # Verify the structure matches expected
    expected = (
        "Call(func=Name(id='print'), args=[Starred(value=BinOp("
        "left=Call(func=Name(id='list'), args=[Call(func=Name(id='range'), "
        "args=[Constant(value=1)], keywords=[])]), "
        "right=Call(func=Name(id='list'), args=[Call(func=Name(id='range'), "
        "args=[Constant(value=3)], keywords=[])]), op=Add())], "
        "keywords=[])"
    )
    assert _ast_dump(call) == expected

def test_no_starred_elements_remain_unchanged():
    code = "[1, 2, 3]"
    tree = _parse_and_transform(code)
    # The root should be a Module containing a single Expr with a List
    expr = tree.body[0].value
    assert isinstance(expr, ast.List)
    # The list should contain three Constant nodes
    elts = expr.elts
    assert len(elts) == 3
    assert all(isinstance(e, ast.Constant) for e in elts)
    assert [e.value for e in elts] == [1, 2, 3]
    # Ensure the transformer did not modify the tree
    assert not hasattr(tree, "_tree_changed") or not tree._tree_changed
