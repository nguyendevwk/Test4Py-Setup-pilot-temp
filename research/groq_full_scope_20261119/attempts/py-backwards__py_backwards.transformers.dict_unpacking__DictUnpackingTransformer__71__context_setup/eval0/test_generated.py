import ast
import typed_ast.ast3 as typed_ast
import pytest
from py_backwards.transformers.dict_unpacking import DictUnpackingTransformer

def build_dict_node(keys, values):
    """Helper to create a typed_ast.Dict node from lists of keys and values."""
    return typed_ast.Dict(
        keys=[k if k is not None else None for k in keys],
        values=values
    )

def unparse(node):
    """Return a string representation of the AST node for easier comparison."""
    return ast.unparse(node) if hasattr(ast, "unparse") else typed_ast.dump(node)

def test_normal_dict_unpacking():
    """A dict with a single unpacking should be transformed into a merge call."""
    # {1: 1, **{'a': 2}}
    dict_node = build_dict_node(
        keys=[typed_ast.Num(n=1), None],
        values=[typed_ast.Num(n=1), typed_ast.Dict(keys=[typed_ast.Str(s='a')], values=[typed_ast.Num(n=2)])]
    )
    transformer = DictUnpackingTransformer()
    transformed = transformer.visit(dict_node)
    # The result should be a Call to _py_backwards_merge_dicts
    assert isinstance(transformed, typed_ast.Call)
    assert isinstance(transformed.func, typed_ast.Name)
    assert transformed.func.id == "_py_backwards_merge_dicts"
    # The argument should be a List containing a Dict and a Call to dict()
    assert isinstance(transformed.args[0], typed_ast.List)
    elts = transformed.args[0].elts
    # First element: a Dict with key 1
    assert isinstance(elts[0], typed_ast.Dict)
    assert elts[0].keys[0].n == 1
    assert elts[0].values[0].n == 1
    # Second element: a Call to dict() with the unpacked dict
    assert isinstance(elts[1], typed_ast.Call)
    assert isinstance(elts[1].func, typed_ast.Name)
    assert elts[1].func.id == "dict"
    assert elts[1].args[0].keys[0].s == "a"
    assert elts[1].args[0].values[0].n == 2

def test_dict_without_unpacking():
    """A dict without unpacking should remain unchanged."""
    dict_node = build_dict_node(
        keys=[typed_ast.Num(n=1), typed_ast.Num(n=2)],
        values=[typed_ast.Num(n=10), typed_ast.Num(n=20)]
    )
    transformer = DictUnpackingTransformer()
    transformed = transformer.visit(dict_node)
    # Should be a Dict node unchanged
    assert isinstance(transformed, typed_ast.Dict)
    assert [k.n for k in transformed.keys] == [1, 2]
    assert [v.n for v in transformed.values] == [10, 20]

def test_multiple_unpackings_and_groups():
    """A dict with multiple unpackings and groups should produce correct merge structure."""
    # {1: 1, **{'a': 2}, 3: 3, **{'b': 4}}
    dict_node = build_dict_node(
        keys=[
            typed_ast.Num(n=1), None, typed_ast.Num(n=3), None
        ],
        values=[
            typed_ast.Num(n=1),
            typed_ast.Dict(keys=[typed_ast.Str(s='a')], values=[typed_ast.Num(n=2)]),
            typed_ast.Num(n=3),
            typed_ast.Dict(keys=[typed_ast.Str(s='b')], values=[typed_ast.Num(n=4)])
        ]
    )
    transformer = DictUnpackingTransformer()
    transformed = transformer.visit(dict_node)
    # Should be a Call to _py_backwards_merge_dicts
    assert isinstance(transformed, typed_ast.Call)
    assert transformed.func.id == "_py_backwards_merge_dicts"
    # The list should contain 4 elements: Dict, Call, Dict, Call
    elts = transformed.args[0].elts
    assert len(elts) == 4
    # Check first Dict
    assert isinstance(elts[0], typed_ast.Dict)
    assert elts[0].keys[0].n == 1
    assert elts[0].values[0].n == 1
    # Check first Call
    assert isinstance(elts[1], typed_ast.Call)
    assert elts[1].args[0].keys[0].s == "a"
    assert elts[1].args[0].values[0].n == 2
    # Check second Dict
    assert isinstance(elts[2], typed_ast.Dict)
    assert elts[2].keys[0].n == 3
    assert elts[2].values[0].n == 3
    # Check second Call
    assert isinstance(elts[3], typed_ast.Call)
    assert elts[3].args[0].keys[0].s == "b"
    assert elts[3].args[0].values[0].n == 4
