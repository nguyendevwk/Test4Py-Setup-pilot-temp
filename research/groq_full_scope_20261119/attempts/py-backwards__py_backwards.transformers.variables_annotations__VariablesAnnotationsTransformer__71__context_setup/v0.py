import ast as pyast
import typed_ast.ast3 as ast
import pytest

from py_backwards.transformers.variables_annotations import VariablesAnnotationsTransformer
from py_backwards.types import TransformationResult


def test_transform_simple_annotation_with_value():
    source = "a: int = 10\nb: int\n"
    tree = ast.parse(source)
    result: TransformationResult = VariablesAnnotationsTransformer.transform(tree)

    # The transformation should have changed the tree
    assert result.changed is True

    # The resulting module should have two statements:
    # 1. a = 10  (annotation removed, value kept)
    # 2. b (annotation removed, no value)
    assert isinstance(result.tree, ast.Module)
    assert len(result.tree.body) == 2

    # First statement should be an Assign node
    first = result.tree.body[0]
    assert isinstance(first, ast.Assign)
    assert isinstance(first.targets[0], ast.Name)
    assert first.targets[0].id == "a"
    assert isinstance(first.value, ast.Num) or isinstance(first.value, ast.Constant)
    assert first.value.n == 10

    # Second statement should be an Expr node containing a Name (since no value)
    second = result.tree.body[1]
    assert isinstance(second, ast.Expr)
    assert isinstance(second.value, ast.Name)
    assert second.value.id == "b"


def test_transform_no_annotations_no_change():
    source = "x = 5\nprint(x)\n"
    tree = ast.parse(source)
    result: TransformationResult = VariablesAnnotationsTransformer.transform(tree)

    # No annotation nodes, so tree should remain unchanged
    assert result.changed is False
    assert isinstance(result.tree, ast.Module)
    assert len(result.tree.body) == 2
    assert isinstance(result.tree.body[0], ast.Assign)
    assert isinstance(result.tree.body[1], ast.Expr)


def test_transform_annotation_outside_body_warns_and_skips(tmp_path, capsys):
    # Create a function with an annotation at module level (outside body)
    source = "a: int = 1\n\ndef f():\n    pass\n"
    tree = ast.parse(source)
    result: TransformationResult = VariablesAnnotationsTransformer.transform(tree)

    # The annotation outside the function body should be skipped
    # The tree should still contain the annotation node
    assert result.changed is True
    assert isinstance(result.tree, ast.Module)
    # The first statement should still be an AnnAssign
    first = result.tree.body[0]
    assert isinstance(first, ast.AnnAssign)
    assert first.target.id == "a"
    assert first.value.n == 1

    # Capture the warning output
    captured = capsys.readouterr()
    assert "Assignment outside of body" in captured.err
