import pytest
import typed_ast.ast3 as ast
from py_backwards.transformers.base import BaseTransformer
from py_backwards.types import TransformationResult


def test_base_transformer_abstract_method():
    """BaseTransformer.transform is abstract and cannot be called directly."""
    with pytest.raises(TypeError):
        BaseTransformer.transform(ast.parse("x = 1"))


def test_subclass_implementation_returns_expected_result(tmp_path):
    """A concrete subclass correctly implements transform and returns a TransformationResult."""
    class DummyTransformer(BaseTransformer):
        target = "dummy"

        @classmethod
        def transform(cls, tree: ast.AST) -> TransformationResult:
            # Return a simple result containing the original tree and a dummy mapping
            return {"original": tree, "mapping": {"x": "y"}}

    tree = ast.parse("x = 1")
    result = DummyTransformer.transform(tree)
    assert isinstance(result, dict)
    assert result["original"] is tree
    assert result["mapping"] == {"x": "y"}


def test_transformer_with_invalid_input_raises_type_error():
    """transform should raise a TypeError when called with a non-AST argument."""
    class DummyTransformer(BaseTransformer):
        target = "dummy"

        @classmethod
        def transform(cls, tree: ast.AST) -> TransformationResult:
            return {"original": tree, "mapping": {}}

    with pytest.raises(TypeError):
        DummyTransformer.transform("not an AST")
