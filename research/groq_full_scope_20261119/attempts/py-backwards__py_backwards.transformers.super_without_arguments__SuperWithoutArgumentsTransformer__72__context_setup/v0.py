import sys
import io
import typed_ast.ast3 as ast
import pytest

from py_backwards.transformers.super_without_arguments import SuperWithoutArgumentsTransformer


def find_call_node(tree):
    """Return the first ast.Call node in the tree."""
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            return node
    return None


def test_super_inside_class_method_transforms_correctly():
    source = """
class MyClass:
    def method(self):
        super()
"""
    tree = ast.parse(source)
    transformer = SuperWithoutArgumentsTransformer()
    transformer.visit(tree)

    call_node = find_call_node(tree)
    assert call_node is not None
    # After transformation, super() should have two arguments: class name and self
    assert len(call_node.args) == 2
    assert isinstance(call_node.args[0], ast.Name)
    assert isinstance(call_node.args[1], ast.Name)
    assert call_node.args[0].id == "MyClass"
    assert call_node.args[1].id == "self"


def test_super_outside_function_no_change_and_warning(capfd):
    source = """
class MyClass:
    super()
"""
    tree = ast.parse(source)
    transformer = SuperWithoutArgumentsTransformer()
    transformer.visit(tree)

    call_node = find_call_node(tree)
    assert call_node is not None
    # No arguments should be added because super() is outside a function
    assert len(call_node.args) == 0

    # Capture warning output
    out, err = capfd.readouterr()
    assert "super() outside of function" in err


def test_super_outside_class_no_change_and_warning(capfd):
    source = """
def func():
    super()
"""
    tree = ast.parse(source)
    transformer = SuperWithoutArgumentsTransformer()
    transformer.visit(tree)

    call_node = find_call_node(tree)
    assert call_node is not None
    # No arguments should be added because super() is outside a class
    assert len(call_node.args) == 0

    # Capture warning output
    out, err = capfd.readouterr()
    assert "super() outside of class" in err
