import pytest
import typed_ast.ast3 as ast
from py_backwards.transformers.dict_unpacking import DictUnpackingTransformer
from py_backwards.utils.tree import insert_at

# Helper to create a Dict node with optional unpacking
def make_dict_node(pairs):
    keys = []
    values = []
    for key, value in pairs:
        keys.append(key)
        values.append(value)
    return ast.Dict(keys=keys, values=values)

# Helper to create a Name node
def name(id_):
    return ast.Name(id=id_, ctx=ast.Load())

# Helper to create a Call node
def call(func, args=None, keywords=None):
    return ast.Call(func=func, args=args or [], keywords=keywords or [])

# Helper to create a List node
def list_node(elts):
    return ast.List(elts=elts, ctx=ast.Load())

# Helper to create a Module node
def module(body):
    return ast.Module(body=body, type_ignores=[])

# Test 1: Normal dict without unpacking remains unchanged
def test_no_unpacking_remains():
    d = make_dict_node([(name('a'), name('b'))])
    mod = module([d])
    transformer = DictUnpackingTransformer()
    new_mod = transformer.visit(mod)
    # The dict node should be unchanged
    assert isinstance(new_mod.body[0], ast.Dict)
    assert len(new_mod.body[0].keys) == 1
    assert isinstance(new_mod.body[0].keys[0], ast.Name)
    assert new_mod.body[0].keys[0].id == 'a'
    assert isinstance(new_mod.body[0].values[0], ast.Name)
    assert new_mod.body[0].values[0].id == 'b'

# Test 2: Dict with a single unpacking transforms to merge call
def test_single_unpacking_transforms():
    d = make_dict_node([(None, name('a'))])  # represents {**a}
    mod = module([d])
    transformer = DictUnpackingTransformer()
    new_mod = transformer.visit(mod)
    # The body should now be a Call to _py_backwards_merge_dicts
    assert isinstance(new_mod.body[0], ast.Call)
    assert isinstance(new_mod.body[0].func, ast.Name)
    assert new_mod.body[0].func.id == '_py_backwards_merge_dicts'
    # The argument should be a List containing the unpacked dict
    assert isinstance(new_mod.body[0].args[0], ast.List)
    assert len(new_mod.body[0].args[0].elts) == 1
    assert isinstance(new_mod.body[0].args[0].elts[0], ast.Name)
    assert new_mod.body[0].args[0].elts[0].id == 'a'

# Test 3: Dict with multiple groups and unpacking merges correctly
def test_multiple_groups_and_unpacking():
    # {1: 1, **a, 2: 2, **b}
    d = make_dict_node([
        (name('1'), name('1')),
        (None, name('a')),
        (name('2'), name('2')),
        (None, name('b'))
    ])
    mod = module([d])
    transformer = DictUnpackingTransformer()
    new_mod = transformer.visit(mod)
    # Should be a Call to _py_backwards_merge_dicts with 3 elements
    assert isinstance(new_mod.body[0], ast.Call)
    assert new_mod.body[0].func.id == '_py_backwards_merge_dicts'
    lst = new_mod.body[0].args[0]
    assert isinstance(lst, ast.List)
    assert len(lst.elts) == 3
    # First element: Dict with key 1
    assert isinstance(lst.elts[0], ast.Dict)
    assert lst.elts[0].keys[0].id == '1'
    # Second element: Call to dict(a)
    assert isinstance(lst.elts[1], ast.Call)
    assert lst.elts[1].func.id == 'dict'
    assert isinstance(lst.elts[1].args[0], ast.Name)
    assert lst.elts[1].args[0].id == 'a'
    # Third element: Dict with key 2
    assert isinstance(lst.elts[2], ast.Dict)
    assert lst.elts[2].keys[0].id == '2'
