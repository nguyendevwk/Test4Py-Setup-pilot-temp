import ast as pyast
import typed_ast.ast3 as ast
import pytest

from py_backwards.transformers.variables_annotations import VariablesAnnotationsTransformer
from py_backwards.types import TransformationResult


def parse_source(src: str) -> ast.AST:
    """Parse source code into a typed_ast AST."""
    return ast.parse(src, mode="exec")


def ast_to_source(node: ast.AST) -> str:
    """Convert a typed_ast AST back to source code."""
    return pyast.unparse(node)  # uses standard ast.unparse


def test_transform_with_value(tmp_path):
    src = "a: int = 10\nb: int = 20\n"
    tree = parse_source(src)
    result: TransformationResult = VariablesAnnotationsTransformer.transform(tree)

    # The tree should have changed
    assert result.tree_changed is True

    # The resulting source should contain plain assignments without annotations
    new_src = ast_to_source(result.tree)
    assert "a = 10" in new_src
    assert "b = 20" in new_src
    assert ": int" not in new_src


def test_transform_without_value(tmp_path):
    src = "x: str\n"
    tree = parse_source(src)
    result: TransformationResult = VariablesAnnotationsTransformer.transform(tree)

    # The tree should have changed (the AnnAssign removed)
    assert result.tree_changed is True

    # The resulting source should not contain the variable declaration
    new_src = ast_to_source(result.tree)
    assert "x:" not in new_src
    assert new_src.strip() == ""  # only a newline remains


def test_no_annotations_remain_unchanged(tmp_path):
    src = "y = 5\nz = 6\n"
    tree = parse_source(src)
    result: TransformationResult = VariablesAnnotationsTransformer.transform(tree)

    # No annotations, so tree should not change
    assert result.tree_changed is False

    # The source should be identical
    new_src = ast_to_source(result.tree)
    assert new_src == src
