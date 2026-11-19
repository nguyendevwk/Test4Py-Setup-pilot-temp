import ast
import typed_ast.ast3 as typed_ast
import pytest
from py_backwards.transformers.base import BaseNodeTransformer
from py_backwards.types import TransformationResult

# Helper: create a simple AST from source code
def parse_source(src: str) -> typed_ast.AST:
    return typed_ast.parse(src)

# 1. Test that BaseNodeTransformer.transform returns unchanged tree and no changes flag
def test_base_transformer_no_change(tmp_path):
    src = "x = 1\nprint(x)"
    tree = parse_source(src)
    result: TransformationResult = BaseNodeTransformer.transform(tree)
    # The tree should be the same object
    assert result.tree is tree
    # No changes should be reported
    assert result.changed is False
    # Dependencies should be empty list
    assert result.dependencies == []

# 2. Test that a subclass that modifies a node sets the changed flag
def test_subclass_modifies_node(tmp_path):
    class IncrementTransformer(BaseNodeTransformer):
        def visit_Name(self, node: typed_ast.Name):
            # Replace every name with a constant 42
            return typed_ast.Constant(value=42, kind=None)

    src = "a = b + c"
    tree = parse_source(src)
    result: TransformationResult = IncrementTransformer.transform(tree)
    # The tree should be modified
    assert result.changed is True
    # The transformed tree should no longer contain any Name nodes
    names = [n for n in typed_ast.walk(result.tree) if isinstance(n, typed_ast.Name)]
    assert names == []

# 3. Test that dependencies are propagated correctly from subclass
def test_subclass_dependencies(tmp_path):
    class DepTransformer(BaseNodeTransformer):
        dependencies = ["dep1", "dep2"]

    src = "x = 0"
    tree = parse_source(src)
    result: TransformationResult = DepTransformer.transform(tree)
    assert result.dependencies == ["dep1", "dep2"]
