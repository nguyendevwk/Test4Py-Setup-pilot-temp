import ast
import typed_ast.ast3 as typed_ast
import pytest
from py_backwards.transformers.dict_unpacking import DictUnpackingTransformer

def build_dict(keys, values):
    """Helper to build an ast.Dict node from lists of keys and values."""
    return typed_ast.Dict(keys=keys, values=values)

def test_no_unpacking_returns_original_dict():
    # A dict without any unpacking should be unchanged
    keys = [typed_ast.Num(n=1), typed_ast.Num(n=2)]
    values = [typed_ast.Num(n=10), typed_ast.Num(n=20)]
    node = build_dict(keys, values)

    transformer = DictUnpackingTransformer()
    result = transformer.visit_Dict(node)

    # The result should be the same object (generic_visit returns node)
    assert result is node
    assert isinstance(result, typed_ast.Dict)
    assert [k.n for k in result.keys] == [1, 2]
    assert [v.n for v in result.values] == [10, 20]

def test_unpacking_transforms_to_merge_call():
    # A dict with unpacking: {1: 1, **dict_a}
    keys = [typed_ast.Num(n=1), None]
    values = [typed_ast.Num(n=1), typed_ast.Name(id='dict_a')]
    node = build_dict(keys, values)

    transformer = DictUnpackingTransformer()
    result = transformer.visit_Dict(node)

    # The result should be a Call to _py_backwards_merge_dicts
    assert isinstance(result, typed_ast.Call)
    assert isinstance(result.func, typed_ast.Name)
    assert result.func.id == "_py_backwards_merge_dicts"

    # The argument should be a List containing one Dict and one Call
    assert isinstance(result.args[0], typed_ast.List)
    elts = result.args[0].elts
    assert len(elts) == 2

    # First element is a Dict with the single key/value pair
    first = elts[0]
    assert isinstance(first, typed_ast.Dict)
    assert [k.n for k in first.keys] == [1]
    assert [v.n for v in first.values] == [1]

    # Second element is a Call to dict() with dict_a as argument
    second = elts[1]
    assert isinstance(second, typed_ast.Call)
    assert isinstance(second.func, typed_ast.Name)
    assert second.func.id == "dict"
    assert len(second.args) == 1
    assert isinstance(second.args[0], typed_ast.Name)
    assert second.args[0].id == "dict_a"

def test_multiple_unpackings_and_pairs():
    # A dict with multiple pairs and unpackings: {1:1, **a, 2:2, **b}
    keys = [typed_ast.Num(n=1), None, typed_ast.Num(n=2), None]
    values = [typed_ast.Num(n=1), typed_ast.Name(id='a'),
              typed_ast.Num(n=2), typed_ast.Name(id='b')]
    node = build_dict(keys, values)

    transformer = DictUnpackingTransformer()
    result = transformer.visit_Dict(node)

    # Expect a Call to _py_backwards_merge_dicts with 4 elements
    assert isinstance(result, typed_ast.Call)
    assert isinstance(result.args[0], typed_ast.List)
    elts = result.args[0].elts
    assert len(elts) == 4

    # Check the sequence: Dict, Call, Dict, Call
    assert isinstance(elts[0], typed_ast.Dict)
    assert [k.n for k in elts[0].keys] == [1]
    assert [v.n for v in elts[0].values] == [1]

    assert isinstance(elts[1], typed_ast.Call)
    assert isinstance(elts[1].args[0], typed_ast.Name)
    assert elts[1].args[0].id == "a"

    assert isinstance(elts[2], typed_ast.Dict)
    assert [k.n for k in elts[2].keys] == [2]
    assert [v.n for v in elts[2].values] == [2]

    assert isinstance(elts[3], typed_ast.Call)
    assert isinstance(elts[3].args[0], typed_ast.Name)
    assert elts[3].args[0].id == "b"
