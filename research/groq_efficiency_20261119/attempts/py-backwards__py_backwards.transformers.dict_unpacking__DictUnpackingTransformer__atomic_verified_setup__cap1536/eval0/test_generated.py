import ast
import typed_ast.ast3 as typed_ast
import pytest

from py_backwards.transformers.dict_unpacking import DictUnpackingTransformer


def _parse_and_transform(code: str) -> typed_ast.Module:
    """Parse source code into a typed_ast.Module and apply the transformer."""
    tree = typed_ast.parse(code)
    transformer = DictUnpackingTransformer()
    transformed = transformer.visit(tree)
    return transformed


def test_no_unpacking_remains_dict():
    """When a dict has no unpacking, it should stay unchanged."""
    code = "x = {1: 1, 2: 2}"
    transformed = _parse_and_transform(code)
    # The assignment target should be a dict node
    assign = transformed.body[0]
    assert isinstance(assign, typed_ast.Assign)
    dict_node = assign.value
    assert isinstance(dict_node, typed_ast.Dict)
    # Keys and values should match the original
    keys = [k.n for k in dict_node.keys]
    values = [v.n for v in dict_node.values]
    assert keys == [1, 2]
    assert values == [1, 2]


def test_single_unpacking_transforms_to_merge_call():
    """A dict with a single unpacking should be replaced by a merge call."""
    code = "x = {1: 1, **{'a': 2}}"
    transformed = _parse_and_transform(code)
    assign = transformed.body[0]
    assert isinstance(assign, typed_ast.Assign)
    call = assign.value
    # The top-level node should be a Call to _py_backwards_merge_dicts
    assert isinstance(call, typed_ast.Call)
    assert isinstance(call.func, typed_ast.Name)
    assert call.func.id == "_py_backwards_merge_dicts"
    # The argument should be a list containing one dict and one call
    list_node = call.args[0]
    assert isinstance(list_node, typed_ast.List)
    elts = list_node.elts
    # First element: a dict with key 1
    assert isinstance(elts[0], typed_ast.Dict)
    assert elts[0].keys[0].n == 1
    assert elts[0].values[0].n == 1
    # Second element: a call to dict() with the unpacked dict
    assert isinstance(elts[1], typed_ast.Call)
    assert isinstance(elts[1].func, typed_ast.Name)
    assert elts[1].func.id == "dict"
    # The argument to dict() should be the unpacked dict
    unpacked_dict = elts[1].args[0]
    assert isinstance(unpacked_dict, typed_ast.Dict)
    assert unpacked_dict.keys[0].s == "a"
    assert unpacked_dict.values[0].n == 2


def test_multiple_unpackings_grouped_correctly():
    """Multiple unpackings should be grouped into separate calls."""
    code = "x = {1: 1, **{'a': 2}, 3: 3, **{'b': 4}, 5: 5}"
    transformed = _parse_and_transform(code)
    assign = transformed.body[0]
    call = assign.value
    list_node = call.args[0]
    elts = list_node.elts
    # Expect three elements: dict, call, dict, call, dict
    assert len(elts) == 5
    # First dict: {1:1}
    assert isinstance(elts[0], typed_ast.Dict)
    assert elts[0].keys[0].n == 1
    # Second call: dict({'a':2})
    assert isinstance(elts[1], typed_ast.Call)
    assert isinstance(elts[1].args[0], typed_ast.Dict)
    assert elts[1].args[0].keys[0].s == "a"
    # Third dict: {3:3}
    assert isinstance(elts[2], typed_ast.Dict)
    assert elts[2].keys[0].n == 3
    # Fourth call: dict({'b':4})
    assert isinstance(elts[3], typed_ast.Call)
    assert isinstance(elts[3].args[0], typed_ast.Dict)
    assert elts[3].args[0].keys[0].s == "b"
    # Fifth dict: {5:5}
    assert isinstance(elts[4], typed_ast.Dict)
    assert elts[4].keys[0].n == 5
