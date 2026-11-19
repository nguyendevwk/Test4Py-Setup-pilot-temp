import ast
import typed_ast.ast3 as typed_ast
import pytest
from py_backwards.transformers.starred_unpacking import StarredUnpackingTransformer

def _parse_and_transform(code: str, node_type: type):
    """Parse `code` into an AST node of type `node_type` and apply the transformer."""
    tree = typed_ast.parse(code)
    # Find the first node of the requested type
    target_node = None
    for node in ast.walk(tree):
        if isinstance(node, node_type):
            target_node = node
            break
    assert target_node is not None, f"Could not find node of type {node_type.__name__}"
    transformer = StarredUnpackingTransformer()
    transformed = transformer.visit(target_node)
    return transformed, transformer._tree_changed

def test_list_with_starred_unpacking():
    code = "[2, *range(10), 1]"
    transformed, changed = _parse_and_transform(code, typed_ast.List)
    # The transformed node should be a BinOp representing addition of lists
    assert isinstance(transformed, typed_ast.BinOp)
    # The left side should be a BinOp (2 + list(range(10)))
    assert isinstance(transformed.left, typed_ast.BinOp)
    # The right side should be a List containing the element 1
    assert isinstance(transformed.right, typed_ast.List)
    # Ensure the tree was marked as changed
    assert changed is True

def test_call_with_starred_unpacking():
    code = "print(*range(1), *range(3))"
    transformed, changed = _parse_and_transform(code, typed_ast.Call)
    # After transformation, the call should have a single Starred argument
    assert len(transformed.args) == 1
    assert isinstance(transformed.args[0], typed_ast.Starred)
    # The starred value should be a BinOp adding two list calls
    starred_val = transformed.args[0].value
    assert isinstance(starred_val, typed_ast.BinOp)
    # Ensure the tree was marked as changed
    assert changed is True

def test_non_starred_list_remains_unchanged():
    code = "[1, 2, 3]"
    transformed, changed = _parse_and_transform(code, typed_ast.List)
    # The node should be unchanged (same type and elements)
    assert isinstance(transformed, typed_ast.List)
    assert [e.value for e in transformed.elts] == [1, 2, 3]
    # The transformer should not mark the tree as changed
    assert changed is False
