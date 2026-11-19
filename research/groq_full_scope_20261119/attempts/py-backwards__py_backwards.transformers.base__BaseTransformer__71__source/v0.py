import ast
import pytest
from py_backwards.transformers.base import BaseTransformer
from typed_ast import ast3 as typed_ast


def test_abstract_transform_raises_type_error():
    """
    Verify that calling the abstract transform method on a subclass that
    does not implement it raises a TypeError.
    """
    class DummyTransformer(BaseTransformer):
        pass

    # Instantiate the subclass (allowed because abstract methods are not enforced on instantiation)
    transformer = DummyTransformer()
    # Create a simple AST node to pass to the method
    node = typed_ast.parse("x = 1")
    with pytest.raises(TypeError):
        DummyTransformer.transform(node)


def test_subclass_can_implement_transform_and_return_expected_result():
    """
    Verify that a concrete subclass can implement transform and return a
    TransformationResult that contains the expected keys.
    """
    class ConcreteTransformer(BaseTransformer):
        target = "dummy_target"

        @classmethod
        def transform(cls, tree: typed_ast.AST):
            # For testing, simply return a dict with the target and the number of nodes
            node_count = sum(1 for _ in ast.walk(tree))
            return {"target": cls.target, "node_count": node_count}

    # Create a simple AST node
    node = typed_ast.parse("a = 2\nb = 3")
    result = ConcreteTransformer.transform(node)

    assert isinstance(result, dict)
    assert result["target"] == "dummy_target"
    assert result["node_count"] == 4  # Assign, Name, Constant, Module


def test_target_attribute_can_be_overridden_and_accessed():
    """
    Verify that the target attribute can be overridden in a subclass and
    accessed via the class.
    """
    class OverrideTransformer(BaseTransformer):
        target = "overridden"

    assert OverrideTransformer.target == "overridden"
    # Ensure that the base class still has target None
    assert BaseTransformer.target is None
