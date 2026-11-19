import ast
import typed_ast.ast3 as typed_ast
import pytest
from py_backwards.transformers.dict_unpacking import DictUnpackingTransformer

def build_dict_node(keys, values):
    """Helper to build a typed_ast.Dict node."""
    return typed_ast.Dict(keys=keys, values=values)

def test_no_unpacking_remains_unchanged():
    """A dict without unpacking should be left untouched."""
    node = build_dict_node(
        keys=[typed_ast.Constant(value=1), typed_ast.Constant(value=2)],
        values=[typed_ast.Constant(value='a'), typed_ast.Constant(value='b')]
    )
    transformer = DictUnpackingTransformer()
    new_node = transformer.visit(node)
    # The node should be the same instance and unchanged
    assert new_node is node
    assert isinstance(new_node, typed_ast.Dict)
    assert [k.value for k in new_node.keys] == [1, 2]
    assert [v.value for v in new_node.values] == ['a', 'b']

def test_single_unpacking_transforms_to_merge_call():
    """A dict with a single unpacking should be transformed into a merge call."""
    node = build_dict_node(
        keys=[typed_ast.Constant(value=1), None],
        values=[typed_ast.Constant(value='a'), typed_ast.Name(id='dict_a')]
    )
    transformer = DictUnpackingTransformer()
    new_node = transformer.visit(node)
    # The result should be a Call to _py_backwards_merge_dicts
    assert isinstance(new_node, typed_ast.Call)
    assert isinstance(new_node.func, typed_ast.Name)
    assert new_node.func.id == '_py_backwards_merge_dicts'
    # The argument list should contain two elements
    assert isinstance(new_node.args[0], typed_ast.List)
    elts = new_node.args[0].elts
    assert len(elts) == 2
    # First element: a Dict with the first key/value
    assert isinstance(elts[0], typed_ast.Dict)
    assert [k.value for k in elts[0].keys] == [1]
    assert [v.value for v in elts[0].values] == ['a']
    # Second element: a Call to dict with the unpacked dict
    assert isinstance(elts[1], typed_ast.Call)
    assert isinstance(elts[1].func, typed_ast.Name)
    assert elts[1].func.id == 'dict'
    assert elts[1].args == [typed_ast.Name(id='dict_a')]
    assert elts[1].keywords == []

def test_multiple_unpackings_grouped_correctly():
    """Multiple unpackings should be grouped into separate calls."""
    node = build_dict_node(
        keys=[
            typed_ast.Constant(value=1), None,
            typed_ast.Constant(value=2), None,
            typed_ast.Constant(value=3)
        ],
        values=[
            typed_ast.Constant(value='a'), typed_ast.Name(id='dict_a'),
            typed_ast.Constant(value='b'), typed_ast.Name(id='dict_b'),
            typed_ast.Constant(value='c')
        ]
    )
    transformer = DictUnpackingTransformer()
    new_node = transformer.visit(node)
    assert isinstance(new_node, typed_ast.Call)
    assert new_node.func.id == '_py_backwards_merge_dicts'
    elts = new_node.args[0].elts
    # Expect three elements: Dict(1:'a'), Call(dict_a), Dict(2:'b'), Call(dict_b), Dict(3:'c')
    # Actually grouping: [Dict(1:'a')], Call(dict_a), [Dict(2:'b')], Call(dict_b), [Dict(3:'c')]
    # So elts length should be 5
    assert len(elts) == 5
    # Check first dict
    assert isinstance(elts[0], typed_ast.Dict)
    assert [k.value for k in elts[0].keys] == [1]
    assert [v.value for v in elts[0].values] == ['a']
    # Check first unpack call
    assert isinstance(elts[1], typed_ast.Call)
    assert elts[1].func.id == 'dict'
    assert elts[1].args == [typed_ast.Name(id='dict_a')]
    # Check second dict
    assert isinstance(elts[2], typed_ast.Dict)
    assert [k.value for k in elts[2].keys] == [2]
    assert [v.value for v in elts[2].values] == ['b']
    # Check second unpack call
    assert isinstance(elts[3], typed_ast.Call)
    assert elts[3].func.id == 'dict'
    assert elts[3].args == [typed_ast.Name(id='dict_b')]
    # Check third dict
    assert isinstance(elts[4], typed_ast.Dict)
    assert [k.value for k in elts[4].keys] == [3]
    assert [v.value for v in elts[4].values] == ['c']
