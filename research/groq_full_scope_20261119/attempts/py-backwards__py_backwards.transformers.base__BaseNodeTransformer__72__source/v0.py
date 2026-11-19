import pytest
import typed_ast.ast3 as ast
from py_backwards.transformers.base import BaseNodeTransformer
from py_backwards.types import TransformationResult


class DummyTransformer(BaseNodeTransformer):
    """A minimal transformer that marks the tree as changed."""
    dependencies = ["dummy_dep"]

    def visit_Module(self, node: ast.Module):
        # Mark the tree as changed and return the node unchanged
        self._tree_changed = True
        return node


def test_transform_no_changes(tmp_path):
    """Transforming a tree that does not modify it should report no changes."""
    source = "x = 1\n"
    tree = ast.parse(source)
    result: TransformationResult = BaseNodeTransformer.transform(tree)
    # The tree should be the same object
    assert result.tree is tree
    # No changes should be reported
    assert result.changed is False
    # Dependencies should be empty for the base class
    assert result.dependencies == []


def test_transform_with_change(tmp_path):
    """A transformer that sets _tree_changed should report a change."""
    source = "x = 1\n"
    tree = ast.parse(source)
    result: TransformationResult = DummyTransformer.transform(tree)
    # The tree should be the same object
    assert result.tree is tree
    # The change flag should be True
    assert result.changed is True
    # Dependencies should be inherited from the subclass
    assert result.dependencies == ["dummy_dep"]


def test_transform_dependencies_inheritance(tmp_path):
    """Dependencies defined in a subclass are returned correctly."""
    class DepTransformer(BaseNodeTransformer):
        dependencies = ["dep1", "dep2"]

        def visit_Module(self, node: ast.Module):
            return node

    source = "y = 2\n"
    tree = ast.parse(source)
    result: TransformationResult = DepTransformer.transform(tree)
    assert result.dependencies == ["dep1", "dep2"]
    assert result.changed is False
