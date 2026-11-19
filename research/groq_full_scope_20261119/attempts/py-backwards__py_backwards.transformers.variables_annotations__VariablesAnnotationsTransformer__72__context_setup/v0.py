import ast
import warnings
import pytest
from py_backwards.transformers.variables_annotations import VariablesAnnotationsTransformer
from py_backwards.types import TransformationResult

def _parse(source: str) -> ast.AST:
    """Parse source using the standard ast module (compatible with typed_ast.ast3)."""
    return ast.parse(source)

def test_transform_with_value(tmp_path):
    source = "a: int = 10\nb: int = 20\n"
    tree = _parse(source)
    result: TransformationResult = VariablesAnnotationsTransformer.transform(tree)

    # tree_changed should be True because annotations were transformed
    assert result.tree_changed is True

    # The resulting tree should contain two Assign nodes with type_comment
    assigns = [node for node in ast.walk(result.tree) if isinstance(node, ast.Assign)]
    assert len(assigns) == 2
    # Check that the first assign corresponds to 'a'
    a_assign = assigns[0]
    assert isinstance(a_assign.targets[0], ast.Name)
    assert a_assign.targets[0].id == "a"
    assert isinstance(a_assign.value, ast.Constant)
    assert a_assign.value.value == 10
    assert a_assign.type_comment == "int"

    # Check that the second assign corresponds to 'b'
    b_assign = assigns[1]
    assert isinstance(b_assign.targets[0], ast.Name)
    assert b_assign.targets[0].id == "b"
    assert isinstance(b_assign.value, ast.Constant)
    assert b_assign.value.value == 20
    assert b_assign.type_comment == "int"

def test_transform_without_value(tmp_path):
    source = "x: str\n"
    tree = _parse(source)
    result: TransformationResult = VariablesAnnotationsTransformer.transform(tree)

    # tree_changed should be True because the annotation was removed
    assert result.tree_changed is True

    # No Assign nodes should remain
    assigns = [node for node in ast.walk(result.tree) if isinstance(node, ast.Assign)]
    assert assigns == []

    # The module body should be empty
    assert isinstance(result.tree, ast.Module)
    assert result.tree.body == []

def test_no_change_when_no_annassign(tmp_path):
    source = "y = 5\nz = 6\n"
    tree = _parse(source)
    result: TransformationResult = VariablesAnnotationsTransformer.transform(tree)

    # tree_changed should be False because there were no AnnAssign nodes
    assert result.tree_changed is False

    # The tree should remain unchanged
    assert ast.dump(result.tree) == ast.dump(tree)
