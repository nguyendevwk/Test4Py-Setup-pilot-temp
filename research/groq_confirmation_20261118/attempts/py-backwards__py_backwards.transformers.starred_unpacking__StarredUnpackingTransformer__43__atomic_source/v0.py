import ast
import typed_ast.ast3 as typed_ast
import pytest
from py_backwards.transformers.starred_unpacking import StarredUnpackingTransformer


def _parse_and_transform(code: str) -> typed_ast.AST:
    """Parse the given code with typed_ast and apply the transformer."""
    tree = typed_ast.parse(code)
    transformer = StarredUnpackingTransformer()
    transformed = transformer.visit(tree)
    return transformed


def test_list_with_starred_unpacked_to_binop():
    """A list containing a starred expression should be transformed into a BinOp."""
    code = "[2, *range(10), 1]"
    transformed = _parse_and_transform(code)
    # The top-level node should be a List with a single element: a BinOp
    assert isinstance(transformed.body[0], typed_ast.Expr)
    assert isinstance(transformed.body[0].value, typed_ast.List)
    assert len(transformed.body[0].value.elts) == 1
    binop = transformed.body[0].value.elts[0]
    assert isinstance(binop, typed_ast.BinOp)
    # The left side of the BinOp should be a List([2])
    assert isinstance(binop.left, typed_ast.List)
    assert len(binop.left.elts) == 1
    assert isinstance(binop.left.elts[0], typed_ast.Num) and binop.left.elts[0].n == 2
    # The right side should be a BinOp of list(range(10)) + [1]
    assert isinstance(binop.right, typed_ast.BinOp)
    assert isinstance(binop.right.left, typed_ast.Call)
    assert isinstance(binop.right.right, typed_ast.List)
    assert len(binop.right.right.elts) == 1
    assert isinstance(binop.right.right.elts[0], typed_ast.Num) and binop.right.right.elts[0].n == 1


def test_call_with_starred_arguments_wrapped_in_list():
    """A function call with starred arguments should wrap the arguments in a list and star the result."""
    code = "print(*range(1), *range(3))"
    transformed = _parse_and_transform(code)
    # The top-level node should be an Expr with a Call to print
    assert isinstance(transformed.body[0], typed_ast.Expr)
    call = transformed.body[0].value
    assert isinstance(call, typed_ast.Call)
    assert isinstance(call.func, typed_ast.Name) and call.func.id == "print"
    # After transformation, there should be a single starred argument
    assert len(call.args) == 1
    starred = call.args[0]
    assert isinstance(starred, typed_ast.Starred)
    # The starred value should be a BinOp of two lists
    binop = starred.value
    assert isinstance(binop, typed_ast.BinOp)
    assert isinstance(binop.left, typed_ast.List)
    assert isinstance(binop.right, typed_ast.List)
    # Each list should contain a Call to list(range(...))
    for lst in (binop.left, binop.right):
        assert len(lst.elts) == 1
        call_list = lst.elts[0]
        assert isinstance(call_list, typed_ast.Call)
        assert isinstance(call_list.func, typed_ast.Name) and call_list.func.id == "list"
        assert len(call_list.args) == 1
        assert isinstance(call_list.args[0], typed_ast.Call)
        assert isinstance(call_list.args[0].func, typed_ast.Name) and call_list.args[0].func.id == "range"


def test_no_starred_remains_unchanged():
    """Code without starred expressions should remain unchanged after transformation."""
    code = "[1, 2, 3]\nprint(4, 5)"
    transformed = _parse_and_transform(code)
    # The transformed tree should be identical to the original
    original = typed_ast.parse(code)
    assert ast.dump(transformed) == ast.dump(original)
