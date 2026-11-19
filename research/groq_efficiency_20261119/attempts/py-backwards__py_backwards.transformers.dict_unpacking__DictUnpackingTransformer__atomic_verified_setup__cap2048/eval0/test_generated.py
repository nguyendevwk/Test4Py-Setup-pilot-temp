import ast
import typed_ast.ast3 as typed_ast
import pytest
from py_backwards.transformers.dict_unpacking import DictUnpackingTransformer

def _transform(source: str) -> typed_ast.Module:
    """Parse source, apply DictUnpackingTransformer, and return the transformed AST."""
    tree = typed_ast.parse(source)
    transformer = DictUnpackingTransformer()
    return transformer.visit(tree)

def test_no_unpacking_remains_dict():
    source = "d = {1: 2, 3: 4}"
    transformed = _transform(source)
    # Find the assignment target dict node
    assign = transformed.body[0]
    assert isinstance(assign, typed_ast.Assign)
    dict_node = assign.value
    assert isinstance(dict_node, typed_ast.Dict)
    # Keys and values should be unchanged
    keys = [k.n for k in dict_node.keys]
    values = [v.n for v in dict_node.values]
    assert keys == [1, 3]
    assert values == [2, 4]

def test_single_unpacking_merges_dicts():
    source = "d = {1: 2, **{'a': 3}}"
    transformed = _transform(source)
    assign = transformed.body[0]
    assert isinstance(assign, typed_ast.Assign)
    call = assign.value
    # Should be a call to _py_backwards_merge_dicts
    assert isinstance(call, typed_ast.Call)
    assert isinstance(call.func, typed_ast.Name)
    assert call.func.id == "_py_backwards_merge_dicts"
    # The argument should be a list of two elements: a Dict and a Call to dict()
    list_arg = call.args[0]
    assert isinstance(list_arg, typed_ast.List)
    elts = list_arg.elts
    assert len(elts) == 2
    # First element is a Dict with key 1
    first = elts[0]
    assert isinstance(first, typed_ast.Dict)
    assert first.keys[0].n == 1
    assert first.values[0].n == 2
    # Second element is a Call to dict()
    second = elts[1]
    assert isinstance(second, typed_ast.Call)
    assert isinstance(second.func, typed_ast.Name)
    assert second.func.id == "dict"
    # The argument to dict() should be the unpacked dict
    assert second.args[0].keys[0].s == "a"
    assert second.args[0].values[0].n == 3

def test_multiple_unpackings_and_groups():
    source = "d = {1: 2, **{'a': 3}, 4: 5, **{'b': 6}, 7: 8}"
    transformed = _transform(source)
    assign = transformed.body[0]
    call = assign.value
    list_arg = call.args[0]
    elts = list_arg.elts
    # Expect 4 elements: Dict, Call, Dict, Call
    assert len(elts) == 4
    # First dict should contain 1:2
    first = elts[0]
    assert isinstance(first, typed_ast.Dict)
    assert first.keys[0].n == 1
    assert first.values[0].n == 2
    # Second call should be dict({'a':3})
    second = elts[1]
    assert isinstance(second, typed_ast.Call)
    assert second.args[0].keys[0].s == "a"
    assert second.args[0].values[0].n == 3
    # Third dict should contain 4:5 and 7:8
    third = elts[2]
    assert isinstance(third, typed_ast.Dict)
    keys = [k.n for k in third.keys]
    values = [v.n for v in third.values]
    assert keys == [4, 7]
    assert values == [5, 8]
    # Fourth call should be dict({'b':6})
    fourth = elts[3]
    assert isinstance(fourth, typed_ast.Call)
    assert fourth.args[0].keys[0].s == "b"
    assert fourth.args[0].values[0].n == 6
