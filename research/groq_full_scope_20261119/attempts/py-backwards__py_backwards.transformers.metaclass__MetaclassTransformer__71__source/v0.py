import ast
import typed_ast.ast3 as typed_ast
import pytest
from py_backwards.transformers.metaclass import MetaclassTransformer
from py_backwards.utils.snippet import snippet
from py_backwards.utils.tree import unparse

def _transform(source: str) -> str:
    """Helper that parses, transforms, and unparses a source string."""
    tree = snippet(source)
    transformer = MetaclassTransformer()
    transformed = transformer.visit(tree)
    return unparse(transformed)

def test_metaclass_transformation():
    src = """
class A(metaclass=B):
    pass
"""
    result = _transform(src)
    # The transformed class should inherit from the helper function
    assert "class A(_py_backwards_six_with_metaclass(B)):" in result
    # The original metaclass keyword should be removed
    assert "metaclass=" not in result
    # The six import should be added at the top
    assert result.strip().startswith("import six")

def test_no_metaclass_no_change():
    src = """
class C:
    x = 1
"""
    result = _transform(src)
    # No metaclass keyword, so the class should remain unchanged
    assert "class C:" in result
    assert "x = 1" in result
    # No six import should be added
    assert not result.strip().startswith("import six")

def test_multiple_keywords_remains_other_keywords():
    src = """
class D(metaclass=Meta, kw=42):
    pass
"""
    result = _transform(src)
    # Only the first keyword (metaclass) should be removed
    assert "class D(_py_backwards_six_with_metaclass(Meta)):" in result
    # The second keyword should still be present as a keyword argument
    assert "kw=42" in result
    # The metaclass keyword should no longer appear
    assert "metaclass=" not in result
