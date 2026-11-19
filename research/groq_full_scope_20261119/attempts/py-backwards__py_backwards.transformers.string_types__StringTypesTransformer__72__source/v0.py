import ast as pyast
import typed_ast.ast3 as ast
import pytest

from py_backwards.transformers.string_types import StringTypesTransformer
from py_backwards.types import TransformationResult


def parse_code(code: str) -> ast.AST:
    """Parse source code into a typed_ast AST."""
    return ast.parse(code)


def ast_to_code(tree: ast.AST) -> str:
    """Convert a typed_ast AST back to source code."""
    return pyast.unparse(tree)


def test_replaces_str_with_unicode():
    source = "def f():\n    x = str\n    y = 'hello'\n"
    tree = parse_code(source)
    result: TransformationResult = StringTypesTransformer.transform(tree)

    # The transformer should report a change
    assert result.changed is True

    # The AST should now contain 'unicode' instead of 'str'
    new_source = ast_to_code(result.tree)
    assert "unicode" in new_source
    assert "str" not in new_source
    # Ensure other string literals are untouched
    assert "'hello'" in new_source


def test_no_change_when_no_str():
    source = "def f():\n    x = 42\n    y = 'str'\n"
    tree = parse_code(source)
    result: TransformationResult = StringTypesTransformer.transform(tree)

    # No nodes should have been modified
    assert result.changed is False
    # The source should remain identical
    assert ast_to_code(result.tree) == source


def test_only_replaces_name_str_not_attribute():
    source = "class str:\n    pass\n\ndef f():\n    x = str\n"
    tree = parse_code(source)
    result: TransformationResult = StringTypesTransformer.transform(tree)

    # The class name 'str' should stay unchanged
    new_source = ast_to_code(result.tree)
    assert "class str:" in new_source
    # The variable assignment should be changed
    assert "unicode" in new_source
    assert "x = unicode" in new_source
