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
    # Ensure no remaining 'str' identifiers
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
    source = "str_value = 'test'\nprint(str_value)\nstr = 5"
    tree = parse_source(source)

    result: TransformationResult = StringTypesTransformer.transform(tree)

    # Only the identifier 'str' used as a type should be changed
    transformed_source = ast_to_source(result.tree)
    # The variable name 'str_value' should remain unchanged
    assert "str_value" in transformed_source
    # The assignment to str should remain unchanged
    assert "str = 5" in transformed_source
    # No 'unicode' should appear because no type usage
    assert "unicode" not in transformed_source
