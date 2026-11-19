import ast
import typed_ast.ast3 as ast3
import pytest
from py_backwards.transformers.string_types import StringTypesTransformer
from py_backwards.types import TransformationResult

def test_transform_replaces_str_with_unicode(tmp_path):
    """Normal case: a module containing a string literal and a variable named str."""
    source = """
def foo():
    s = str("hello")
    return s
"""
    tree = ast3.parse(source)
    result = StringTypesTransformer.transform(tree)
    assert isinstance(result, TransformationResult)
    assert result.changed is True
    # The transformed tree should contain 'unicode' instead of 'str'
    transformed_source = ast.unparse(result.tree)
    assert "unicode(\"hello\")" in transformed_source
    assert "str(\"hello\")" not in transformed_source

def test_transform_no_changes_when_no_str(tmp_path):
    """Boundary case: code without any 'str' identifiers should not be modified."""
    source = """
def bar():
    x = 42
    return x
"""
    tree = ast3.parse(source)
    result = StringTypesTransformer.transform(tree)
    assert isinstance(result, TransformationResult)
    assert result.changed is False
    # The source should remain identical after unparsing
    transformed_source = ast.unparse(result.tree)
    assert transformed_source.strip() == source.strip()

def test_transform_invalid_input_raises_type_error():
    """Error case: passing a non-AST object should raise a TypeError."""
    with pytest.raises(TypeError):
        StringTypesTransformer.transform(None)
