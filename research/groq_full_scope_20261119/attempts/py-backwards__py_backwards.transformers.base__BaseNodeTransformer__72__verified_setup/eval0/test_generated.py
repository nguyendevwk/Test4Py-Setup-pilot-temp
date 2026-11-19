import pytest
import typed_ast.ast3 as ast
from py_backwards.transformers.base import BaseNodeTransformer
from py_backwards.types import TransformationResult


class DummyTransformer(BaseNodeTransformer):
    dependencies = ["dummy_dep"]

    def visit_Name(self, node):
        # Mark that a change would occur if we visit a Name node
        self._tree_changed = True
        return node


def test_transform_changes_flag_and_dependencies(tmp_path):
    # Create a simple AST containing a Name node
    source = "x = 1"
    tree = ast.parse(source)
    result: TransformationResult = DummyTransformer.transform(tree)

    # The result should contain the original tree
    assert result.tree is tree
    # Since the transformer visits a Name node, _tree_changed should be True
    assert result.changed is True
    # Dependencies should match the subclass definition
    assert result.dependencies == ["dummy_dep"]


def test_transform_no_changes(tmp_path):
    # Create an AST that does not contain any Name nodes
    source = "pass"
    tree = ast.parse(source)
    result: TransformationResult = DummyTransformer.transform(tree)

    # No Name node visited, so changed flag remains False
    assert result.changed is False
    # Dependencies remain as defined
    assert result.dependencies == ["dummy_dep"]


def test_transform_invalid_input_raises():
    # Passing a non-AST object should raise an AttributeError during visit
    with pytest.raises(AttributeError):
        DummyTransformer.transform(42)
