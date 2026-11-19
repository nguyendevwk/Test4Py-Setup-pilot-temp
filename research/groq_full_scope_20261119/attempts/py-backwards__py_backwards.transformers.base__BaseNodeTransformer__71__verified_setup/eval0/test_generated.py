import pytest
import typed_ast.ast3 as ast
from py_backwards.transformers.base import BaseNodeTransformer
from py_backwards.types import TransformationResult


class DummyTransformer(BaseNodeTransformer):
    """A minimal transformer that marks the tree as changed when visiting an Assign node."""
    def visit_Assign(self, node: ast.Assign):
        self._tree_changed = True
        return node


def test_transform_changes_flag(tmp_path):
    """Verify that visiting an Assign node sets the changed flag."""
    source = "x = 1\n"
    tree = ast.parse(source)
    result: TransformationResult = DummyTransformer.transform(tree)
    assert result.changed is True
    assert result.dependencies == []  # no dependencies declared
    # The tree should remain structurally identical
    assert isinstance(result.tree, ast.Module)
    assert len(result.tree.body) == 1
    assert isinstance(result.tree.body[0], ast.Assign)


def test_transform_no_change(tmp_path):
    """Verify that when no relevant nodes are visited, the changed flag remains False."""
    class NoChangeTransformer(BaseNodeTransformer):
        def visit_Expr(self, node: ast.Expr):
            return node

    source = "print('hello')\n"
    tree = ast.parse(source)
    result: TransformationResult = NoChangeTransformer.transform(tree)
    assert result.changed is False
    assert result.dependencies == []
    assert isinstance(result.tree, ast.Module)
    assert len(result.tree.body) == 1
    assert isinstance(result.tree.body[0], ast.Expr)


def test_transform_invalid_input():
    """Passing a non-AST object should raise a TypeError during visit."""
    with pytest.raises(TypeError):
        DummyTransformer.transform(None)
