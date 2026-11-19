import pytest
import typed_ast.ast3 as ast
from py_backwards.transformers.base import BaseTransformer
from py_backwards.types import TransformationResult

class DummyTransformer(BaseTransformer):
    target = None

    @classmethod
    def transform(cls, tree: ast.AST) -> TransformationResult:
        return ("transformed", tree)

def test_base_transformer_abstract():
    """Calling the abstract transform on BaseTransformer should raise TypeError."""
    with pytest.raises(TypeError):
        BaseTransformer.transform(ast.Module(body=[]))

def test_dummy_transformer_returns_expected():
    """DummyTransformer should return a tuple with a string and the original AST."""
    module = ast.Module(body=[])
    result = DummyTransformer.transform(module)
    assert isinstance(result, tuple)
    assert result[0] == "transformed"
    assert result[1] is module

def test_transformer_with_invalid_input_raises():
    """Passing an object that is not an ast.AST should raise a TypeError."""
    with pytest.raises(TypeError):
        DummyTransformer.transform("not an AST")
