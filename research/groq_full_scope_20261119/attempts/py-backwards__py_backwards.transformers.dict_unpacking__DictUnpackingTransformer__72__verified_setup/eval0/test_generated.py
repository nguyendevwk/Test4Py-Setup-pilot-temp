import ast
import typed_ast.ast3 as typed_ast
import pytest
from py_backwards.transformers.dict_unpacking import DictUnpackingTransformer


def _parse_and_transform(source: str):
    """Parse source with typed_ast and apply DictUnpackingTransformer."""
    tree = typed_ast.parse(source)
    transformer = DictUnpackingTransformer()
    transformed = transformer.visit(tree)
    return transformed, transformer


def test_single_unpacking():
    source = "x = {1: 1, **d}"
    transformed, transformer = _parse_and_transform(source)

    # The assignment target should be unchanged
    assign = transformed.body[0]
    assert isinstance(assign, typed_ast.Assign)

    # The value should be a Call to _py_backwards_merge_dicts
    call = assign.value
    assert isinstance(call, typed_ast.Call)
    assert isinstance(call.func, typed_ast.Name)
    assert call.func.id == "_py_backwards_merge_dicts"

    # The argument should be a List of two elements
    args_list = call.args[0]
    assert isinstance(args_list, typed_ast.List)
    assert len(args_list.elts) == 2

    # First element: a Dict with key 1 and value 1
    first = args_list.elts[0]
    assert isinstance(first, typed_ast.Dict)
    assert len(first.keys) == 1
    assert isinstance(first.keys[0], typed_ast.Num)
    assert first.keys[0].n == 1
    assert isinstance(first.values[0], typed_ast.Num)
    assert first.values[0].n == 1

    # Second element: a Call to dict() with the unpacked dict
    second = args_list.elts[1]
    assert isinstance(second, typed_ast.Call)
    assert isinstance(second.func, typed_ast.Name)
    assert second.func.id == "dict"
    assert len(second.args) == 1
    assert isinstance(second.args[0], typed_ast.Name)
    assert second.args[0].id == "d"

    # The transformer should have marked the tree as changed
    assert transformer._tree_changed is True


def test_multiple_unpacking():
    source = "y = {**a, 2: 2, **b}"
    transformed, transformer = _parse_and_transform(source)

    assign = transformed.body[0]
    call = assign.value
    args_list = call.args[0]
    assert len(args_list.elts) == 3

    # First element: unpacked a
    first = args_list.elts[0]
    assert isinstance(first, typed_ast.Call)
    assert first.func.id == "dict"
    assert first.args[0].id == "a"

    # Second element: dict with key 2
    second = args_list.elts[1]
    assert isinstance(second, typed_ast.Dict)
    assert second.keys[0].n == 2
    assert second.values[0].n == 2

    # Third element: unpacked b
    third = args_list.elts[2]
    assert isinstance(third, typed_ast.Call)
    assert third.func.id == "dict"
    assert third.args[0].id == "b"

    assert transformer._tree_changed is True


def test_no_unpacking():
    source = "z = {3: 3}"
    transformed, transformer = _parse_and_transform(source)

    assign = transformed.body[0]
    value = assign.value
    # Should remain a plain Dict node
    assert isinstance(value, typed_ast.Dict)
    assert len(value.keys) == 1
    assert value.keys[0].n == 3
    assert value.values[0].n == 3

    # Transformer should not mark the tree as changed
    assert transformer._tree_changed is False
