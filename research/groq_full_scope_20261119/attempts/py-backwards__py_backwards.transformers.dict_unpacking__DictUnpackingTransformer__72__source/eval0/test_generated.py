import ast
import typed_ast.ast3 as ast3
import pytest
from py_backwards.transformers.dict_unpacking import DictUnpackingTransformer

def test_split_by_None_basic():
    transformer = DictUnpackingTransformer()
    # Construct pairs: key, value
    pairs = [(ast3.Constant(value=1), ast3.Constant(value=2)),
             (None, ast3.Name(id='dict_a')),
             (ast3.Constant(value=3), ast3.Constant(value=4))]
    splitted = transformer._split_by_None(pairs)
    # Expect three groups: first list, then unpack group, then second list
    assert isinstance(splitted, list)
    assert len(splitted) == 3
    assert splitted[0] == [(ast3.Constant(value=1), ast3.Constant(value=2))]
    assert splitted[1] == ast3.Name(id='dict_a')
    assert splitted[2] == [(ast3.Constant(value=3), ast3.Constant(value=4))]

def test_prepare_splitted_and_merge():
    transformer = DictUnpackingTransformer()
    # Prepare a splitted list with a dict and a call
    splitted = [
        [(ast3.Constant(value='a'), ast3.Constant(value=1))],
        ast3.Name(id='dict_b'),
        [(ast3.Constant(value='c'), ast3.Constant(value=3))]
    ]
    prepared = list(transformer._prepare_splitted(splitted))
    # First group -> ast.Dict
    assert isinstance(prepared[0], ast3.Dict)
    assert prepared[0].keys[0].value == 'a'
    assert prepared[0].values[0].value == 1
    # Second group -> ast.Call to dict()
    assert isinstance(prepared[1], ast3.Call)
    assert isinstance(prepared[1].func, ast3.Name)
    assert prepared[1].func.id == 'dict'
    # Third group -> ast.Dict
    assert isinstance(prepared[2], ast3.Dict)
    assert prepared[2].keys[0].value == 'c'
    assert prepared[2].values[0].value == 3
    # Merge into a call
    merged = transformer._merge_dicts(prepared)
    assert isinstance(merged, ast3.Call)
    assert isinstance(merged.func, ast3.Name)
    assert merged.func.id == '_py_backwards_merge_dicts'
    # The argument should be a list containing the three prepared nodes
    assert isinstance(merged.args[0], ast3.List)
    assert len(merged.args[0].elts) == 3

def test_visit_Dict_with_unpacking():
    transformer = DictUnpackingTransformer()
    # Build a dict node: {1: 2, **dict_x, 3: 4}
    dict_node = ast3.Dict(
        keys=[
            ast3.Constant(value=1),
            None,
            ast3.Constant(value=3)
        ],
        values=[
            ast3.Constant(value=2),
            ast3.Name(id='dict_x'),
            ast3.Constant(value=4)
        ]
    )
    result = transformer.visit_Dict(dict_node)
    # Result should be a Call to _py_backwards_merge_dicts
    assert isinstance(result, ast3.Call)
    assert isinstance(result.func, ast3.Name)
    assert result.func.id == '_py_backwards_merge_dicts'
    # The list argument should contain three elements: two dicts and one call
    list_arg = result.args[0]
    assert isinstance(list_arg, ast3.List)
    assert len(list_arg.elts) == 3
    # First element: dict with key 1
    first = list_arg.elts[0]
    assert isinstance(first, ast3.Dict)
    assert first.keys[0].value == 1
    assert first.values[0].value == 2
    # Second element: call to dict() with dict_x
    second = list_arg.elts[1]
    assert isinstance(second, ast3.Call)
    assert isinstance(second.func, ast3.Name)
    assert second.func.id == 'dict'
    assert second.args[0] == ast3.Name(id='dict_x')
    # Third element: dict with key 3
    third = list_arg.elts[2]
    assert isinstance(third, ast3.Dict)
    assert third.keys[0].value == 3
    assert third.values[0].value == 4
