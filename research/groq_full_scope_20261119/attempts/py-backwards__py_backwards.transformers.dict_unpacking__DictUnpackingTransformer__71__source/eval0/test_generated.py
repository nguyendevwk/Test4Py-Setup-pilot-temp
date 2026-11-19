import pytest
from typed_ast import ast3 as ast
from py_backwards.transformers.dict_unpacking import DictUnpackingTransformer

def _get_module(source: str) -> ast.Module:
    """Parse source code into a typed_ast Module node."""
    return ast.parse(source, mode="exec")

def _ast_to_repr(node):
    """Return a simplified representation of an AST node for assertions."""
    if isinstance(node, ast.Module):
        return [_ast_to_repr(n) for n in node.body]
    if isinstance(node, ast.Expr):
        return _ast_to_repr(node.value)
    if isinstance(node, ast.Call):
        return ("Call", node.func.id, [_ast_to_repr(arg) for arg in node.args])
    if isinstance(node, ast.Dict):
        return ("Dict",
                [(_ast_to_repr(k) if k else None) for k in node.keys],
                [(_ast_to_repr(v) if v else None) for v in node.values])
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Constant):
        return node.value
    return type(node).__name__

def test_dict_with_unpacking_transforms_to_merge_call():
    source = "x = {1: 1, **dict_a}"
    module = _get_module(source)
    transformer = DictUnpackingTransformer()
    transformed = transformer.visit(module)
    # The assignment target should be unchanged
    assign = transformed.body[0]
    assert isinstance(assign, ast.Assign)
    # The value should be a Call to _py_backwards_merge_dicts
    call = assign.value
    assert isinstance(call, ast.Call)
    assert call.func.id == "_py_backwards_merge_dicts"
    # The argument list should contain two elements
    lst = call.args[0]
    assert isinstance(lst, ast.List)
    assert len(lst.elts) == 2
    # First element is a Dict with key 1
    first = lst.elts[0]
    assert isinstance(first, ast.Dict)
    assert first.keys[0].value == 1
    assert first.values[0].value == 1
    # Second element is a Call to dict with dict_a
    second = lst.elts[1]
    assert isinstance(second, ast.Call)
    assert second.func.id == "dict"
    assert isinstance(second.args[0], ast.Name)
    assert second.args[0].id == "dict_a"

def test_dict_without_unpacking_remains_unchanged():
    source = "y = {2: 2}"
    module = _get_module(source)
    transformer = DictUnpackingTransformer()
    transformed = transformer.visit(module)
    assign = transformed.body[0]
    assert isinstance(assign, ast.Assign)
    val = assign.value
    # Should still be a Dict node
    assert isinstance(val, ast.Dict)
    assert val.keys[0].value == 2
    assert val.values[0].value == 2

def test_multiple_unpackings_merge_correctly():
    source = "z = {1: 1, **dict_a, **dict_b}"
    module = _get_module(source)
    transformer = DictUnpackingTransformer()
    transformed = transformer.visit(module)
    assign = transformed.body[0]
    call = assign.value
    lst = call.args[0]
    # Expect three elements: first dict, then dict_a, then dict_b
    assert len(lst.elts) == 3
    # First element is a Dict with key 1
    first = lst.elts[0]
    assert isinstance(first, ast.Dict)
    assert first.keys[0].value == 1
    assert first.values[0].value == 1
    # Second element is a Call to dict with dict_a
    second = lst.elts[1]
    assert isinstance(second, ast.Call)
    assert second.func.id == "dict"
    assert second.args[0].id == "dict_a"
    # Third element is a Call to dict with dict_b
    third = lst.elts[2]
    assert isinstance(third, ast.Call)
    assert third.func.id == "dict"
    assert third.args[0].id == "dict_b"
