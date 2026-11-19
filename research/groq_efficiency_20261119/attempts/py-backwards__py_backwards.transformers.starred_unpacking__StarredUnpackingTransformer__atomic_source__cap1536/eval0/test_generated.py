import ast
import typed_ast.ast3 as typed_ast
import pytest
from py_backwards.transformers.starred_unpacking import StarredUnpackingTransformer

def _parse_and_transform(source: str) -> ast.AST:
    """Parse source with typed_ast and apply StarredUnpackingTransformer."""
    tree = typed_ast.parse(source)
    transformer = StarredUnpackingTransformer()
    new_tree = transformer.visit(tree)
    assert transformer._tree_changed is True
    return new_tree

def test_list_starred_unpacking():
    src = "[2, *range(10), 1]"
    new_tree = _parse_and_transform(src)
    # The transformed node should be a BinOp of two additions
    # resulting in a list concatenation: [2] + list(range(10)) + [1]
    # Verify the structure by dumping the AST
    dump = ast.dump(new_tree, annotate_fields=True, include_attributes=False)
    assert "BinOp" in dump
    assert "Add()" in dump
    assert "List(elts=[Num(n=2)])" in dump
    assert "Call(func=Name(id='list')" in dump
    assert "Num(n=1)" in dump

def test_call_starred_unpacking():
    src = "print(*range(1), *range(3))"
    new_tree = _parse_and_transform(src)
    # The transformed call should have a single starred argument that is a BinOp
    # representing list(range(1)) + list(range(3))
    dump = ast.dump(new_tree, annotate_fields=True, include_attributes=False)
    assert "Call" in dump
    assert "func=Name(id='print')" in dump
    assert "Starred" in dump
    assert "BinOp" in dump
    assert "Call(func=Name(id='list')" in dump
    assert dump.count("Num(n=1)") == 1
    assert dump.count("Num(n=3)") == 1

def test_no_starred_no_change():
    src = "[1, 2, 3]"
    tree = typed_ast.parse(src)
    transformer = StarredUnpackingTransformer()
    new_tree = transformer.visit(tree)
    # Since there are no starred elements, the tree should remain unchanged
    assert transformer._tree_changed is False
    assert ast.dump(new_tree, annotate_fields=True, include_attributes=False) == \
           ast.dump(tree, annotate_fields=True, include_attributes=False)
