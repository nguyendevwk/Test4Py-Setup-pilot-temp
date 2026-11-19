import ast as py_ast
import typed_ast.ast3 as ast
import pytest
from py_backwards.transformers.base import BaseNodeTransformer
from py_backwards.types import TransformationResult

# Helper to create a simple AST node
def make_simple_tree():
    return ast.parse("x = 1")

def test_transform_returns_original_tree_and_no_change():
    tree = make_simple_tree()
    result = BaseNodeTransformer.transform(tree)
    # The returned tree should be the same object
    assert result.tree is tree
    # No changes should be reported
    assert result.changed is False
    # Dependencies list should be empty by default
    assert result.dependencies == []

def test_transform_with_modified_subclass_sets_changed_flag():
    class ModifyingTransformer(BaseNodeTransformer):
        def visit_Assign(self, node):
            # Mark the tree as changed
            self._tree_changed = True
            return node

    tree = make_simple_tree()
    result = ModifyingTransformer.transform(tree)
    assert result.changed is True
    assert result.tree is tree

def test_transform_with_dependency_list():
    class DependentTransformer(BaseNodeTransformer):
        dependencies = ["dep1", "dep2"]

    tree = make_simple_tree()
    result = DependentTransformer.transform(tree)
    assert result.dependencies == ["dep1", "dep2"]
    assert result.changed is False
    assert result.tree is tree
