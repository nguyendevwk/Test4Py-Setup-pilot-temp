import ast
import typed_ast.ast3 as typed_ast
import pytest
from py_backwards.transformers.dict_unpacking import DictUnpackingTransformer

def transform_source(src: str) -> typed_ast.Module:
    """Parse source with typed_ast, apply transformer, and return the transformed AST."""
    module = typed_ast.parse(src)
    transformer = DictUnpackingTransformer()
    return transformer.visit(module)

def test_no_unpacking_remains_dict():
    src = "d = {1: 2, 3: 4}"
    mod = transform_source(src)
    # Find the assignment target dict
    assign = mod.body[0]
    assert isinstance(assign, typed_ast.Assign)
    dict_node = assign.value
    assert isinstance(dict_node, typed_ast.Dict)
    # Keys and values should be unchanged
    keys = [k.value for k in dict_node.keys]
    values = [v.value for v in dict_node.values]
    assert keys == [1, 3]
    assert values == [2, 4]

def test_unpacking_transforms_to_merge_call():
    src = "d = {1: 2, **{'a': 3}, 4: 5}"
    mod = transform_source(src)
    assign = mod.body[0]
    assert isinstance(assign, typed_ast.Assign)
    call = assign.value
    # The top-level node should be a Call to _py_backwards_merge_dicts
    assert isinstance(call, typed_ast.Call)
    assert isinstance(call.func, typed_ast.Name)
    assert call.func.id == "_py_backwards_merge_dicts"
    # The argument should be a List of two elements: a Dict and a Call to dict()
    args = call.args
    assert len(args) == 1
    lst = args[0]
    assert isinstance(lst, typed_ast.List)
    assert len(lst.elts) == 2
    # First element: a Dict with key 1 and value 2
    first = lst.elts[0]
    assert isinstance(first, typed_ast.Dict)
    assert [k.value for k in first.keys] == [1]
    assert [v.value for v in first.values] == [2]
    # Second element: a Call to dict() with the unpacked dict as argument
    second = lst.elts[1]
    assert isinstance(second, typed_ast.Call)
    assert isinstance(second.func, typed_ast.Name)
    assert second.func.id == "dict"
    assert len(second.args) == 1
    inner_dict = second.args[0]
    assert isinstance(inner_dict, typed_ast.Dict)
    assert [k.value for k in inner_dict.keys] == ["a"]
    assert [v.value for v in inner_dict.values] == [3]

def test_multiple_unpackings_and_boundary_cases():
    src = "d = {**{'x': 1}, **{'y': 2}, 3: 4}"
    mod = transform_source(src)
    assign = mod.body[0]
    call = assign.value
    # Should merge three dicts: two unpacked and one literal
    lst = call.args[0]
    assert isinstance(lst, typed_ast.List)
    assert len(lst.elts) == 3
    # Check each element is a Call to dict() wrapping the unpacked dict
    for i, key in enumerate(["x", "y"]):
        elem = lst.elts[i]
        assert isinstance(elem, typed_ast.Call)
        assert elem.func.id == "dict"
        inner = elem.args[0]
        assert isinstance(inner, typed_ast.Dict)
        assert inner.keys[0].value == key
        assert inner.values[0].value == i + 1
    # Last element is the literal dict
    last = lst.elts[2]
    assert isinstance(last, typed_ast.Dict)
    assert last.keys[0].value == 3
    assert last.values[0].value == 4
