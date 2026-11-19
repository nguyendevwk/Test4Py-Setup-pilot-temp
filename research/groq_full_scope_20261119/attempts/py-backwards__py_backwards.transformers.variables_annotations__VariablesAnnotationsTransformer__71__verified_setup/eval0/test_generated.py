import ast
import typed_ast.ast3 as typed_ast
import pytest

from py_backwards.transformers.variables_annotations import VariablesAnnotationsTransformer
from py_backwards.types import TransformationResult


def test_transform_with_value_and_type_comment():
    source = "a: int = 10\nb: int\n"
    tree = typed_ast.parse(source)
    result: TransformationResult = VariablesAnnotationsTransformer.transform(tree)

    # The tree should have changed
    assert result.tree_changed is True

    # After transformation, only the assignment for `a` should remain
    assert len(result.tree.body) == 1
    node = result.tree.body[0]
    assert isinstance(node, typed_ast.Assign)
    # The target should be the name `a`
    assert isinstance(node.targets[0], typed_ast.Name)
    assert node.targets[0].id == "a"
    # The value should be the constant 10
    assert isinstance(node.value, typed_ast.Constant)
    assert node.value.value == 10
    # The type comment should be preserved
    assert node.type_comment == "int"


def test_transform_without_value():
    source = "x: str\n"
    tree = typed_ast.parse(source)
    result: TransformationResult = VariablesAnnotationsTransformer.transform(tree)

    # The tree should have changed
    assert result.tree_changed is True

    # After transformation, the annotated assignment without a value should be removed
    assert len(result.tree.body) == 0


def test_transform_multiple_annotations():
    source = "a: int = 1\nb: int = 2\nc: int\n"
    tree = typed_ast.parse(source)
    result: TransformationResult = VariablesAnnotationsTransformer.transform(tree)

    # The tree should have changed
    assert result.tree_changed is True

    # After transformation, only the assignments for `a` and `b` should remain
    assert len(result.tree.body) == 2
    targets = {node.targets[0].id for node in result.tree.body if isinstance(node, typed_ast.Assign)}
    assert targets == {"a", "b"}

    # Ensure that the assignment for `c` was removed
    for node in result.tree.body:
        assert not (isinstance(node, typed_ast.Assign) and node.targets[0].id == "c")
