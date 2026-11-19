import ast as pyast
import typed_ast.ast3 as ast
import pytest

from py_backwards.transformers.string_types import StringTypesTransformer
from py_backwards.types import TransformationResult


def parse_source(source: str) -> ast.AST:
    """Parse source code into a typed_ast.ast3 AST."""
    return ast.parse(source)


def ast_to_source(tree: ast.AST) -> str:
    """Convert an AST back to source code using the standard ast module."""
    return pyast.unparse(tree)


def test_transform_replaces_str_with_unicode():
    source = "x = str('hello')\nprint(str(x))"
    tree = parse_source(source)

    result: TransformationResult = StringTypesTransformer.transform(tree)

    # The tree should have changed
    assert result.changed is True

    # The transformed source should contain 'unicode' instead of 'str'
    transformed_source = ast_to_source(result.tree)
    assert "unicode('hello')" in transformed_source
    assert "print(unicode(x))" in transformed_source
    # Ensure no other 'str' remains
    assert "str(" not in transformed_source


def test_transform_no_change_when_no_str():
    source = "x = 42\nprint(x)"
    tree = parse_source(source)

    result: TransformationResult = StringTypesTransformer.transform(tree)

    # The tree should not have changed
    assert result.changed is False

    # The source should remain identical
    transformed_source = ast_to_source(result.tree)
    assert transformed_source.strip() == source.strip()


def test_transform_does_not_modify_other_names():
    source = "str = 5\nprint(str)\nprint('str')"
    tree = parse_source(source)

    result: TransformationResult = StringTypesTransformer.transform(tree)

    # The tree should have changed because the Name node 'str' in the assignment
    # is replaced, but string literals remain unchanged
    assert result.changed is True

    transformed_source = ast_to_source(result.tree)
    # The variable name should now be 'unicode'
    assert "unicode = 5" in transformed_source
    # The print of the variable should use the new name
    assert "print(unicode)" in transformed_source
    # The string literal should remain unchanged
    assert "print('str')" in transformed_source
