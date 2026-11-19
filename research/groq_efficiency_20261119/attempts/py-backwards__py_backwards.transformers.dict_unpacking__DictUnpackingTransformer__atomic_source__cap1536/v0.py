import pytest
from typed_ast import ast3 as ast
from py_backwards.transformers.dict_unpacking import DictUnpackingTransformer

def build_module(source: str) -> ast.Module:
    """Parse source code into a typed_ast Module node."""
    return ast.parse(source, mode="exec")

def ast_to_source(node: ast.AST) -> str:
    """Convert a typed_ast node back to source code using ast.unparse if available."""
    try:
        return ast.unparse(node)  # Python 3.9+
    except AttributeError:
        # Fallback: use ast.dump for structural comparison
        return ast.dump(node)

def test_no_unpacking_remains_dict():
    source = "x = {1: 2, 3: 4}"
    module = build_module(source)
    transformer = DictUnpackingTransformer()
    transformed = transformer.visit(module)
    # The assignment should remain unchanged
    assign = transformed.body[0]
    assert isinstance(assign, ast.Assign)
    dict_node = assign.value
    assert isinstance(dict_node, ast.Dict)
    assert dict_node.keys == [ast.Num(n=1), ast.Num(n=3)]
    assert dict_node.values == [ast.Num(n=2), ast.Num(n=4)]
    # No tree change flag should be set
    assert not getattr(transformer, "_tree_changed", False)

def test_unpacking_transforms_to_merge_call():
    source = "y = {1: 2, **{'a': 3}}"
    module = build_module(source)
    transformer = DictUnpackingTransformer()
    transformed = transformer.visit(module)
    assign = transformed.body[0]
    assert isinstance(assign, ast.Assign)
    call = assign.value
    # Should be a call to _py_backwards_merge_dicts
    assert isinstance(call, ast.Call)
    assert isinstance(call.func, ast.Name)
    assert call.func.id == "_py_backwards_merge_dicts"
    # The argument should be a list containing one dict and one call to dict()
    assert isinstance(call.args[0], ast.List)
    elts = call.args[0].elts
    assert len(elts) == 2
    # First element: a dict with key 1
    first = elts[0]
    assert isinstance(first, ast.Dict)
    assert first.keys == [ast.Num(n=1)]
    assert first.values == [ast.Num(n=2)]
    # Second element: a call to dict() with the unpacked dict
    second = elts[1]
    assert isinstance(second, ast.Call)
    assert isinstance(second.func, ast.Name)
    assert second.func.id == "dict"
    # The argument to dict() should be the unpacked dict
    assert second.args == [ast.Dict(keys=[ast.Str(s='a')], values=[ast.Num(n=3)])]
    # Tree change flag should be set
    assert getattr(transformer, "_tree_changed", False)

def test_multiple_unpackings_and_order():
    source = "z = {1: 2, **{'a': 3}, 4: 5, **{'b': 6}}"
    module = build_module(source)
    transformer = DictUnpackingTransformer()
    transformed = transformer.visit(module)
    assign = transformed.body[0]
    call = assign.value
    # The merge call should contain four elements: dict, dict, dict, dict
    elts = call.args[0].elts
    assert len(elts) == 4
    # Check order and contents
    # 1st dict: {1: 2}
    first = elts[0]
    assert isinstance(first, ast.Dict)
    assert first.keys == [ast.Num(n=1)]
    assert first.values == [ast.Num(n=2)]
    # 2nd dict: {'a': 3}
    second = elts[1]
    assert isinstance(second, ast.Dict)
    assert second.keys == [ast.Str(s='a')]
    assert second.values == [ast.Num(n=3)]
    # 3rd dict: {4: 5}
    third = elts[2]
    assert isinstance(third, ast.Dict)
    assert third.keys == [ast.Num(n=4)]
    assert third.values == [ast.Num(n=5)]
    # 4th dict: {'b': 6}
    fourth = elts[3]
    assert isinstance(fourth, ast.Dict)
    assert fourth.keys == [ast.Str(s='b')]
    assert fourth.values == [ast.Num(n=6)]
    # Tree change flag should be set
    assert getattr(transformer, "_tree_changed", False)
