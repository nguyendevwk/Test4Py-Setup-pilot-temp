import ast
import pytest
from py_backwards.transformers.base import BaseTransformer
from typed_ast import ast3 as typed_ast
from py_backwards.types import TransformationResult


def test_base_transformer_abstract_method_raises():
    """Calling the abstract transform on BaseTransformer should raise TypeError."""
    with pytest.raises(TypeError):
        BaseTransformer.transform(typed_ast.Module(body=[]))


def test_subclass_implements_transform_returns_expected():
    """A concrete subclass must implement transform and return a TransformationResult."""
    class DummyTransformer(BaseTransformer):
        target = None

        @classmethod
        def transform(cls, tree: typed_ast.AST) -> TransformationResult:
            # Return a simple tuple as a mock result
            return ("ok", tree)

    # Create a minimal AST node
    node = typed_ast.Module(body=[typed_ast.Expr(value=typed_ast.Constant(value=42))])
    result = DummyTransformer.transform(node)
    assert isinstance(result, tuple)
    assert result[0] == "ok"
    assert result[1] is node


def test_transform_with_invalid_input_raises():
    """Passing an invalid type to transform should raise a TypeError."""
    class DummyTransformer(BaseTransformer):
        target = None

        @classmethod
        def transform(cls, tree: typed_ast.AST) -> TransformationResult:
            if not isinstance(tree, typed_ast.AST):
                raise TypeError("Expected an AST node")
            return ("ok", tree)

    with pytest.raises(TypeError, match="Expected an AST node"):
        DummyTransformer.transform("not an AST")
