import ast
import typed_ast.ast3 as typed_ast
import pytest
from py_backwards.transformers.dict_unpacking import DictUnpackingTransformer
from py_backwards.utils.snippet import snippet

def build_dict_node(pairs):
    """Helper to build a typed_ast.Dict node from a list of (key, value) tuples.
    Keys can be None to represent ** unpacking."""
    keys = []
    values = []
    for k, v in pairs:
        keys.append(k)
        values.append(v)
    return typed_ast.Dict(keys=keys, values=values)

def build_module_from_dict(dict_node):
    """Wrap a dict node in a Module node."""
    return typed_ast.Module(body=[typed_ast.Expr(value=dict_node)], type_ignores=[])

def ast_to_source(node):
    """Convert a typed_ast node to source code using the snippet helper."""
    return snippet(node)

def test_no_unpacking_keeps_dict():
    """A dict without unpacking should remain unchanged."""
    # {1: 2, 3: 4}
    dict_node = build_dict_node([
        (typed_ast.Num(n=1), typed_ast.Num(n=2)),
        (typed_ast.Num(n=3), typed_ast.Num(n=4)),
    ])
    module = build_module_from_dict(dict_node)

    transformer = DictUnpackingTransformer()
    transformed = transformer.visit(module)

    # The transformed node should still be a Dict with same keys/values
    expr = transformed.body[0]
    assert isinstance(expr, typed_ast.Expr)
    assert isinstance(expr.value, typed_ast.Dict)
    assert len(expr.value.keys) == 2
    assert isinstance(expr.value.keys[0], typed_ast.Num)
    assert expr.value.keys[0].n == 1
    assert expr.value.values[0].n == 2

def test_unpacking_merges_dicts():
    """A dict with unpacking should be transformed into a merge call."""
    # {1: 1, **dict_a}
    dict_a = typed_ast.Name(id='dict_a', ctx=typed_ast.Load())
    dict_node = build_dict_node([
        (typed_ast.Num(n=1), typed_ast.Num(n=1)),
        (None, dict_a),  # represents **dict_a
    ])
    module = build_module_from_dict(dict_node)

    transformer = DictUnpackingTransformer()
    transformed = transformer.visit(module)

    # The transformed node should be a Call to _py_backwards_merge_dicts
    expr = transformed.body[0]
    assert isinstance(expr, typed_ast.Expr)
    call = expr.value
    assert isinstance(call, typed_ast.Call)
    assert isinstance(call.func, typed_ast.Name)
    assert call.func.id == '_py_backwards_merge_dicts'
    # The argument should be a List of two elements: a Dict and a Call to dict()
    assert isinstance(call.args[0], typed_ast.List)
    elts = call.args[0].elts
    assert len(elts) == 2
    # First element is a Dict with key 1
    first = elts[0]
    assert isinstance(first, typed_ast.Dict)
    assert first.keys[0].n == 1
    assert first.values[0].n == 1
    # Second element is a Call to dict(dict_a)
    second = elts[1]
    assert isinstance(second, typed_ast.Call)
    assert isinstance(second.func, typed_ast.Name)
    assert second.func.id == 'dict'
    assert isinstance(second.args[0], typed_ast.Name)
    assert second.args[0].id == 'dict_a'

def test_multiple_unpackings_and_order():
    """Multiple unpackings should preserve order and merge correctly."""
    # {1: 1, **dict_a, 2: 2, **dict_b}
    dict_a = typed_ast.Name(id='dict_a', ctx=typed_ast.Load())
    dict_b = typed_ast.Name(id='dict_b', ctx=typed_ast.Load())
    dict_node = build_dict_node([
        (typed_ast.Num(n=1), typed_ast.Num(n=1)),
        (None, dict_a),
        (typed_ast.Num(n=2), typed_ast.Num(n=2)),
        (None, dict_b),
    ])
    module = build_module_from_dict(dict_node)

    transformer = DictUnpackingTransformer()
    transformed = transformer.visit(module)

    expr = transformed.body[0]
    call = expr.value
    elts = call.args[0].elts
    # Expect three elements: Dict(1), Call(dict_a), Dict(2), Call(dict_b)
    assert len(elts) == 4
    # Check order and types
    assert isinstance(elts[0], typed_ast.Dict)
    assert elts[0].keys[0].n == 1
    assert isinstance(elts[1], typed_ast.Call)
    assert elts[1].args[0].id == 'dict_a'
    assert isinstance(elts[2], typed_ast.Dict)
    assert elts[2].keys[0].n == 2
    assert isinstance(elts[3], typed_ast.Call)
    assert elts[3].args[0].id == 'dict_b'
