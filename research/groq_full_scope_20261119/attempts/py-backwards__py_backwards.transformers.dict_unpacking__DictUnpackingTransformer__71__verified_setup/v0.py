import ast as py_ast
import typed_ast.ast3 as ast
import pytest
from py_backwards.transformers.dict_unpacking import DictUnpackingTransformer


def parse_and_transform(code: str) -> ast.Module:
    """Parse source code with typed_ast and apply the transformer."""
    module = ast.parse(code)
    transformer = DictUnpackingTransformer()
    transformed = transformer.visit(module)
    # Ensure the transformer actually changed the tree
    assert transformer._tree_changed
    return transformed


def test_simple_unpacking():
    """A dict with a single unpacking should be merged into a call."""
    code = "{1: 1, **{'a': 2}}"
    transformed = parse_and_transform(code)

    # The top-level node should be a Call to _py_backwards_merge_dicts
    assert isinstance(transformed.body[0], ast.Expr)
    call = transformed.body[0].value
    assert isinstance(call, ast.Call)
    assert isinstance(call.func, ast.Name)
    assert call.func.id == "_py_backwards_merge_dicts"

    # The argument should be a List containing one Dict
    assert len(call.args) == 1
    list_node = call.args[0]
    assert isinstance(list_node, ast.List)
    assert len(list_node.elts) == 1
    dict_node = list_node.elts[0]
    assert isinstance(dict_node, ast.Dict)

    # The dict should contain the original key/value pair
    assert len(dict_node.keys) == 1
    key = dict_node.keys[0]
    value = dict_node.values[0]
    assert isinstance(key, ast.Num) and key.n == 1
    assert isinstance(value, ast.Num) and value.n == 1


def test_no_unpacking():
    """A dict without unpacking should remain unchanged."""
    code = "{'x': 10, 'y': 20}"
    transformed = parse_and_transform(code)

    # The transformer should not modify the dict
    expr = transformed.body[0]
    assert isinstance(expr, ast.Expr)
    dict_node = expr.value
    assert isinstance(dict_node, ast.Dict)

    # Keys and values should match the original
    keys = [k.s if isinstance(k, ast.Str) else k.n for k in dict_node.keys]
    values = [v.n if isinstance(v, ast.Num) else v.s for v in dict_node.values]
    assert keys == ["x", "y"]
    assert values == [10, 20]


def test_multiple_unpackings():
    """A dict with multiple unpackings should merge all parts correctly."""
    code = "{1: 1, **{'a': 2}, **{'b': 3}, 4: 4}"
    transformed = parse_and_transform(code)

    expr = transformed.body[0]
    assert isinstance(expr, ast.Expr)
    call = expr.value
    assert isinstance(call, ast.Call)
    assert call.func.id == "_py_backwards_merge_dicts"

    list_node = call.args[0]
    assert isinstance(list_node, ast.List)
    # Expect three elements: first dict, second dict, third dict
    assert len(list_node.elts) == 3
    for idx, expected in enumerate([{"1": 1}, {"a": 2}, {"b": 3, "4": 4}]):
        dict_node = list_node.elts[idx]
        assert isinstance(dict_node, ast.Dict)
        keys = [k.s if isinstance(k, ast.Str) else k.n for k in dict_node.keys]
        values = [v.n if isinstance(v, ast.Num) else v.s for v in dict_node.values]
        assert dict(zip(keys, values)) == expected
