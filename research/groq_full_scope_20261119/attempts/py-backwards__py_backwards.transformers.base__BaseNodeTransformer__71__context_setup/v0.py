import ast as py_ast
import typed_ast.ast3 as ast
import pytest
from py_backwards.transformers.base import BaseNodeTransformer
from py_backwards.types import TransformationResult

# Helper to create a simple AST from source code
def parse_source(src: str) -> ast.AST:
    return ast.parse(src)

def test_transform_no_changes():
    """BaseNodeTransformer.transform should return unchanged tree and flag False."""
    src = "x = 1"
    tree = parse_source(src)
    result: TransformationResult = BaseNodeTransformer.transform(tree)
    # The tree returned should be the same object
    assert result.tree is tree
    # No changes should be detected
    assert result.changed is False
    # Dependencies list should be empty by default
    assert result.dependencies == []

def test_transform_with_subclass_modification():
    """Subclass that modifies the tree should set changed flag True."""
    class IncrementTransformer(BaseNodeTransformer):
        def visit_Name(self, node: ast.Name):
            # Replace any name 'x' with 'y'
            if node.id == "x":
                new_node = ast.Name(id="y", ctx=node.ctx)
                self._tree_changed = True
                return new_node
            return node

    src = "x = 1"
    tree = parse_source(src)
    result: TransformationResult = IncrementTransformer.transform(tree)
    # The tree should be modified
    assert result.changed is True
    # The modified tree should reflect the change
    new_src = ast.unparse(result.tree)
    assert new_src == "y = 1"

def test_transform_with_multiple_nodes_and_dependencies():
    """Ensure that dependencies are propagated and multiple nodes are processed."""
    class DummyTransformer(BaseNodeTransformer):
        dependencies = ["dummy_dep"]

        def visit_Num(self, node: ast.Num):
            # Increment all numeric literals
            new_node = ast.Num(n=node.n + 1)
            self._tree_changed = True
            return new_node

    src = "a = 2\nb = 3"
    tree = parse_source(src)
    result: TransformationResult = DummyTransformer.transform(tree)
    # Changed flag should be True
    assert result.changed is True
    # Dependencies should be propagated
    assert result.dependencies == ["dummy_dep"]
    # Verify that all numbers were incremented
    new_src = ast.unparse(result.tree)
    assert new_src == "a = 3\nb = 4"
