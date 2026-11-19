import pytest
from typing import List
from typed_ast import ast3 as ast
from py_backwards.transformers.dict_unpacking import DictUnpackingTransformer

def _make_dict(keys: List[ast.expr], values: List[ast.expr]) -> ast.Dict:
    return ast.Dict(keys=keys, values=values)

def _make_call(func_name: str, args: List[ast.expr]) -> ast.Call:
    return ast.Call(func=ast.Name(id=func_name, ctx=ast.Load()), args=args, keywords=[])

def _make_dict_call(arg: ast.expr) -> ast.Call:
    return ast.Call(func=ast.Name(id='dict', ctx=ast.Load()), args=[arg], keywords=[])

def _make_dict_node(pairs: List[tuple]) -> ast.Dict:
    keys, values = zip(*pairs) if pairs else ([], [])
    return _make_dict(list(keys), list(values))

def _make_unpacking(value: ast.expr) -> tuple:
    return (None, value)

def _ast_dump(node):
    return ast.dump(node, annotate_fields=True, include_attributes=False)

def test_no_unpacking_remains_unchanged():
    # {1: 1, 2: 2}
    node = _make_dict_node([(ast.Num(n=1), ast.Num(n=1)), (ast.Num(n=2), ast.Num(n=2))])
    transformer = DictUnpackingTransformer()
    result = transformer.visit_Dict(node)
    assert isinstance(result, ast.Dict)
    assert _ast_dump(result) == _ast_dump(node)

def test_single_unpacking_merges_correctly():
    # {1: 1, **d}
    d = ast.Name(id='d', ctx=ast.Load())
    node = _make_dict_node([(ast.Num(n=1), ast.Num(n=1)), _make_unpacking(d)])
    transformer = DictUnpackingTransformer()
    result = transformer.visit_Dict(node)
    # Expected: _py_backwards_merge_dicts([{'1': 1}, dict(d)])
    expected = _make_call(
        '_py_backwards_merge_dicts',
        [ast.List(elts=[
            ast.Dict(keys=[ast.Num(n=1)], values=[ast.Num(n=1)]),
            _make_dict_call(d)
        ], ctx=ast.Load())]
    )
    assert isinstance(result, ast.Call)
    assert _ast_dump(result) == _ast_dump(expected)

def test_multiple_unpackings_and_pairs():
    # {**a, 2: 2, **b}
    a = ast.Name(id='a', ctx=ast.Load())
    b = ast.Name(id='b', ctx=ast.Load())
    node = _make_dict_node([
        _make_unpacking(a),
        (ast.Num(n=2), ast.Num(n=2)),
        _make_unpacking(b)
    ])
    transformer = DictUnpackingTransformer()
    result = transformer.visit_Dict(node)
    # Expected: _py_backwards_merge_dicts([dict(a), {'2': 2}, dict(b)])
    expected = _make_call(
        '_py_backwards_merge_dicts',
        [ast.List(elts=[
            _make_dict_call(a),
            ast.Dict(keys=[ast.Num(n=2)], values=[ast.Num(n=2)]),
            _make_dict_call(b)
        ], ctx=ast.Load())]
    )
    assert isinstance(result, ast.Call)
    assert _ast_dump(result) == _ast_dump(expected)
