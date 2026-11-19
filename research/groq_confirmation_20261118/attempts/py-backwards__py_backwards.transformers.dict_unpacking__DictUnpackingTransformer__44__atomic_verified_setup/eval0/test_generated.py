import pytest
import typed_ast.ast3 as ast
from py_backwards.transformers.dict_unpacking import DictUnpackingTransformer

def parse_code(code: str) -> ast.Module:
    """Parse source code into a typed_ast Module node."""
    return ast.parse(code, mode="exec")

def ast_to_source(node: ast.AST) -> str:
    """Convert an AST node back to source code using ast.unparse if available."""
    try:
        import ast as pyast
        return pyast.unparse(node)
    except Exception:
        # Fallback: use typed_ast's unparse if available
        try:
            from typed_ast import ast3
            return ast3.unparse(node)
        except Exception:
            return str(node)

def test_no_unpacking_remains_unchanged():
    code = "d = {1: 2, 3: 4}"
    module = parse_code(code)
    transformer = DictUnpackingTransformer()
    transformed = transformer.visit(module)
    # The dict should remain a Dict node with same keys and values
    assign = transformed.body[0]
    assert isinstance(assign.value, ast.Dict)
    assert [k.value for k in assign.value.keys] == [1, 3]
    assert [v.value for v in assign.value.values] == [2, 4]

def test_single_unpacking_transforms_to_merge_call():
    code = "d = {1: 2, **{'a': 3}}"
    module = parse_code(code)
    transformer = DictUnpackingTransformer()
    transformed = transformer.visit(module)
    assign = transformed.body[0]
    # The value should now be a Call to _py_backwards_merge_dicts
    assert isinstance(assign.value, ast.Call)
    assert isinstance(assign.value.func, ast.Name)
    assert assign.value.func.id == "_py_backwards_merge_dicts"
    # The argument list should contain two elements: a Dict and a Call to dict()
    args = assign.value.args[0].elts
    assert len(args) == 2
    # First element is a Dict with key 1
    first = args[0]
    assert isinstance(first, ast.Dict)
    assert first.keys[0].value == 1
    assert first.values[0].value == 2
    # Second element is a Call to dict() with the unpacked dict
    second = args[1]
    assert isinstance(second, ast.Call)
    assert isinstance(second.func, ast.Name)
    assert second.func.id == "dict"
    # The argument to dict() should be the unpacked dict
    assert len(second.args) == 1
    unpacked = second.args[0]
    assert isinstance(unpacked, ast.Dict)
    assert unpacked.keys[0].s == "a"
    assert unpacked.values[0].value == 3

def test_multiple_unpackings_and_order():
    code = "d = {1: 2, **{'a': 3}, 4: 5, **{'b': 6}}"
    module = parse_code(code)
    transformer = DictUnpackingTransformer()
    transformed = transformer.visit(module)
    assign = transformed.body[0]
    assert isinstance(assign.value, ast.Call)
    args = assign.value.args[0].elts
    # Expect four elements: Dict, Call, Dict, Call
    assert len(args) == 4
    # First dict should contain key 1
    first = args[0]
    assert isinstance(first, ast.Dict)
    assert first.keys[0].value == 1
    assert first.values[0].value == 2
    # Second call should wrap {'a': 3}
    second = args[1]
    assert isinstance(second, ast.Call)
    assert second.func.id == "dict"
    assert second.args[0].keys[0].s == "a"
    assert second.args[0].values[0].value == 3
    # Third dict should contain key 4
    third = args[2]
    assert isinstance(third, ast.Dict)
    assert third.keys[0].value == 4
    assert third.values[0].value == 5
    # Fourth call should wrap {'b': 6}
    fourth = args[3]
    assert isinstance(fourth, ast.Call)
    assert fourth.func.id == "dict"
    assert fourth.args[0].keys[0].s == "b"
    assert fourth.args[0].values[0].value == 6
