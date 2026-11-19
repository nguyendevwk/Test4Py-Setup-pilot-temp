import pytest
from py_backwards.transformers.base import BaseTransformer
from typed_ast import ast3 as ast
from py_backwards.types import CompilationTarget, TransformationResult

# Dummy subclass that implements the abstract method
class DummyTransformer(BaseTransformer):
    target = CompilationTarget.PYTHON_3_8

    @classmethod
    def transform(cls, tree: ast.AST) -> TransformationResult:
        # Return a simple TransformationResult for testing
        return TransformationResult(
            transformed=tree,
            diagnostics=[],
            errors=[]
        )

def test_abstract_method_enforcement():
    """BaseTransformer.transform must be overridden; calling it directly raises TypeError."""
    with pytest.raises(TypeError):
        BaseTransformer.transform(ast.Module(body=[]))

def test_subclass_implementation_returns_expected():
    """Subclass implements transform and returns a TransformationResult with the same tree."""
    module = ast.Module(body=[ast.Pass()])
    result = DummyTransformer.transform(module)
    assert isinstance(result, TransformationResult)
    assert result.transformed is module
    assert result.diagnostics == []
    assert result.errors == []

def test_transform_with_invalid_input_raises_type_error():
    """transform should raise TypeError when called with an object that is not an ast.AST."""
    with pytest.raises(TypeError):
        DummyTransformer.transform("not an AST node")
