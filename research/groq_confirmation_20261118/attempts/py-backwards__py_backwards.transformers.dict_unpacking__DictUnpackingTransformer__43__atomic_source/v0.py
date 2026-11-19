import ast
import typed_ast.ast3 as typed_ast
import pytest
from py_backwards.transformers.dict_unpacking import DictUnpackingTransformer

# Helper to create a simple Name node
def name(id_):
    return typed_ast.Name(id=id_, ctx=typed_ast.Load())

def test_visit_dict_with_single_unpacking():
    # Construct a dict: {1: 1, **a}
    node = typed_ast.Dict(
        keys=[typed_ast.Constant(value=1), None],
        values=[typed_ast.Constant(value=1), name('a')]
    )
    transformer = DictUnpackingTransformer()
    result = transformer.visit_Dict(node)

    # The result should be a Call to _py_backwards_merge_dicts
    assert isinstance(result, typed_ast.Call)
    assert isinstance(result.func, typed_ast.Name)
    assert result.func.id == "_py_backwards_merge_dicts"

    # The argument list should contain two elements: a Dict and a Call(dict, [a])
    args = result.args
    assert isinstance(args[0], typed_ast.List)
    elts = args[0].elts
    assert len(elts) == 2

    # First element: a Dict with key 1 and value 1
    first = elts[0]
    assert isinstance(first, typed_ast.Dict)
    assert len(first.keys) == 1
    assert isinstance(first.keys[0], typed_ast.Constant)
    assert first.keys[0].value == 1
    assert isinstance(first.values[0], typed_ast.Constant)
    assert first.values[0].value == 1

    # Second element: a Call to dict with argument a
    second = elts[1]
    assert isinstance(second, typed_ast.Call)
    assert isinstance(second.func, typed_ast.Name)
    assert second.func.id == "dict"
    assert len(second.args) == 1
    assert isinstance(second.args[0], typed_ast.Name)
    assert second.args[0].id == "a"

def test_visit_dict_without_unpacking_returns_original():
    # Construct a dict: {1: 1}
    node = typed_ast.Dict(
        keys=[typed_ast.Constant(value=1)],
        values=[typed_ast.Constant(value=1)]
    )
    transformer = DictUnpackingTransformer()
    result = transformer.visit_Dict(node)

    # Should return the original node unchanged
    assert result is node
    assert isinstance(result, typed_ast.Dict)
    assert len(result.keys) == 1
    assert result.keys[0].value == 1
    assert result.values[0].value == 1

def test_visit_dict_with_multiple_unpackings():
    # Construct a dict: {1: 1, **a, **b, 2: 2}
    node = typed_ast.Dict(
        keys=[
            typed_ast.Constant(value=1),
            None,
            None,
            typed_ast.Constant(value=2)
        ],
        values=[
            typed_ast.Constant(value=1),
            name('a'),
            name('b'),
            typed_ast.Constant(value=2)
        ]
    )
    transformer = DictUnpackingTransformer()
    result = transformer.visit_Dict(node)

    # Should be a Call to _py_backwards_merge_dicts
    assert isinstance(result, typed_ast.Call)
    assert result.func.id == "_py_backwards_merge_dicts"

    # Argument list should contain three elements: Dict, Call(dict, [a]), Call(dict, [b]), Dict
    args = result.args
    assert isinstance(args[0], typed_ast.List)
    elts = args[0].elts
    # Expected groups: [(1,1)], a, b, [(2,2)] -> 4 elements
    assert len(elts) == 4

    # Check first element is Dict {1:1}
    first = elts[0]
    assert isinstance(first, typed_ast.Dict)
    assert first.keys[0].value == 1
    assert first.values[0].value == 1

    # Second element is Call(dict, [a])
    second = elts[1]
    assert isinstance(second, typed_ast.Call)
    assert second.func.id == "dict"
    assert second.args[0].id == "a"

    # Third element is Call(dict, [b])
    third = elts[2]
    assert isinstance(third, typed_ast.Call)
    assert third.func.id == "dict"
    assert third.args[0].id == "b"

    # Fourth element is Dict {2:2}
    fourth = elts[3]
    assert isinstance(fourth, typed_ast.Dict)
    assert fourth.keys[0].value == 2
    assert fourth.values[0].value == 2
