import ast
import typed_ast.ast3 as typed_ast
import pytest

from py_backwards.transformers.variables_annotations import VariablesAnnotationsTransformer
from py_backwards.types import TransformationResult


def build_tree(source: str) -> typed_ast.AST:
    """Parse source code into a typed_ast AST."""
    return typed_ast.parse(source, mode="exec")


def get_assign_targets(tree: typed_ast.AST):
    """Return a list of target names from Assign nodes in the tree."""
    targets = []
    for node in typed_ast.walk(tree):
        if isinstance(node, typed_ast.Assign):
            for t in node.targets:
                if isinstance(t, typed_ast.Name):
                    targets.append(t.id)
    return targets


def get_assign_values(tree: typed_ast.AST):
    """Return a list of values (as strings) from Assign nodes in the tree."""
    values = []
    for node in typed_ast.walk(tree):
        if isinstance(node, typed_ast.Assign):
            if isinstance(node.value, typed_ast.Constant):
                values.append(node.value.value)
    return values


def test_transformer_removes_annotation_and_keeps_value():
    src = """
a: int = 10
b: str
"""
    tree = build_tree(src)
    result: TransformationResult = VariablesAnnotationsTransformer.transform(tree)

    # The tree should have changed
    assert result.tree_changed is True

    # There should be no AnnAssign nodes left
    ann_assigns = [n for n in typed_ast.walk(result.tree) if isinstance(n, typed_ast.AnnAssign)]
    assert ann_assigns == []

    # There should be one Assign node for 'a' with value 10
    assigns = [n for n in typed_ast.walk(result.tree) if isinstance(n, typed_ast.Assign)]
    assert len(assigns) == 1
    assign = assigns[0]
    assert isinstance(assign.targets[0], typed_ast.Name)
    assert assign.targets[0].id == "a"
    assert isinstance(assign.value, typed_ast.Constant)
    assert assign.value.value == 10

    # The type_comment should be preserved
    assert assign.type_comment == "int"


def test_transformer_removes_annotation_without_value():
    src = """
x: float
"""
    tree = build_tree(src)
    result: TransformationResult = VariablesAnnotationsTransformer.transform(tree)

    # The tree should have changed
    assert result.tree_changed is True

    # No AnnAssign nodes should remain
    ann_assigns = [n for n in typed_ast.walk(result.tree) if isinstance(n, typed_ast.AnnAssign)]
    assert ann_assigns == []

    # No Assign nodes should be added because there was no value
    assigns = [n for n in typed_ast.walk(result.tree) if isinstance(n, typed_ast.Assign)]
    assert assigns == []


def test_transformer_does_not_modify_tree_without_annassign():
    src = """
def foo():
    return 42
"""
    tree = build_tree(src)
    result: TransformationResult = VariablesAnnotationsTransformer.transform(tree)

    # The tree should not have changed
    assert result.tree_changed is False

    # The structure should be identical to the original
    original_code = typed_ast.unparse(tree)
    transformed_code = typed_ast.unparse(result.tree)
    assert original_code == transformed_code
