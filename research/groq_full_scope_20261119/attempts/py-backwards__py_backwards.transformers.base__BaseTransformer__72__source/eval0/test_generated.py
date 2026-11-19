import pytest
import ast
from typed_ast import ast3 as typed_ast
from py_backwards.transformers.base import BaseTransformer
from py_backwards.types import TransformationResult

# Test 1: Ensure the abstract BaseTransformer cannot be used directly
def test_base_transformer_abstract():
    with pytest.raises(TypeError):
        BaseTransformer.transform(typed_ast.Module(body=[]))

# Test 2: Subclass implements transform and returns expected structure
def test_subclass_transform_returns_tuple():
    class DummyTransformer(BaseTransformer):
        target = None

        @classmethod
        def transform(cls, tree: typed_ast.AST) -> TransformationResult:
            # Return a tuple of (new_tree, mapping)
            return (tree, {})

    module = typed_ast.Module(body=[])
    result = DummyTransformer.transform(module)
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert result[0] is module
    assert isinstance(result[1], dict)

# Test 3: Subclass transform must accept only ast.AST instances
def test_subclass_transform_type_check(tmp_path):
    class StrictTransformer(BaseTransformer):
        target = None

        @classmethod
        def transform(cls, tree: typed_ast.AST) -> TransformationResult:
            if not isinstance(tree, typed_ast.AST):
                raise TypeError("Expected typed_ast.AST")
            return (tree, {})

    module = typed_ast.Module(body=[])
    # Valid call
    result = StrictTransformer.transform(module)
    assert result[0] is module

    # Invalid call should raise TypeError
    with pytest.raises(TypeError, match="Expected typed_ast.AST"):
        StrictTransformer.transform(42)
