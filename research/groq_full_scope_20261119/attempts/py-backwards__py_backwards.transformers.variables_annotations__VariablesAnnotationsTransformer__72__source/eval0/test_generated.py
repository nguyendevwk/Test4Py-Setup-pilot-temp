import pytest
from typed_ast import ast3 as ast
from py_backwards.transformers.variables_annotations import VariablesAnnotationsTransformer
from py_backwards.types import TransformationResult

def test_annotation_with_value_replaced_by_assign():
    code = "a: int = 10\n"
    tree = ast.parse(code, mode="exec")
    result: TransformationResult = VariablesAnnotationsTransformer.transform(tree)

    # Tree should have changed
    assert result.tree_changed is True

    # Only one statement in the module body
    assert len(result.tree.body) == 1
    stmt = result.tree.body[0]
    assert isinstance(stmt, ast.Assign)

    # Target should be the name 'a'
    assert isinstance(stmt.targets[0], ast.Name)
    assert stmt.targets[0].id == "a"

    # Value should be the constant 10
    assert isinstance(stmt.value, ast.Constant)
    assert stmt.value.value == 10

    # Type comment should be preserved
    assert stmt.type_comment == "int"

def test_annotation_without_value_is_removed():
    code = "b: int\n"
    tree = ast.parse(code, mode="exec")
    result: TransformationResult = VariablesAnnotationsTransformer.transform(tree)

    # Tree should have changed
    assert result.tree_changed is True

    # Body should be empty after removal
    assert len(result.tree.body) == 0

def test_annotation_inside_function_body():
    code = """\
def f():
    x: str = 'hi'
"""
    tree = ast.parse(code, mode="exec")
    result: TransformationResult = VariablesAnnotationsTransformer.transform(tree)

    # Tree should have changed
    assert result.tree_changed is True

    # Function definition should be present
    assert len(result.tree.body) == 1
    func = result.tree.body[0]
    assert isinstance(func, ast.FunctionDef)

    # Function body should contain one Assign statement
    assert len(func.body) == 1
    stmt = func.body[0]
    assert isinstance(stmt, ast.Assign)

    # Target should be the name 'x'
    assert isinstance(stmt.targets[0], ast.Name)
    assert stmt.targets[0].id == "x"

    # Value should be the constant 'hi'
    assert isinstance(stmt.value, ast.Constant)
    assert stmt.value.value == "hi"

    # Type comment should be preserved
    assert stmt.type_comment == "str"
