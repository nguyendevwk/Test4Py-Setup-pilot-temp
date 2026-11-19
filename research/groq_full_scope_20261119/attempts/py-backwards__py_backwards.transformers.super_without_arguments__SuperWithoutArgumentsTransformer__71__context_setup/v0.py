import ast as pyast
import typed_ast.ast3 as ast
import pytest

from py_backwards.transformers.super_without_arguments import SuperWithoutArgumentsTransformer


def _find_super_call(tree):
    """Return the first Call node whose func is a Name with id 'super'."""
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "super":
            return node
    return None


def test_super_inside_method_replaced(tmp_path):
    source = """
class MyClass:
    def method(self):
        super()
"""
    tree = ast.parse(source)
    transformer = SuperWithoutArgumentsTransformer(tree)
    transformer.visit(tree)

    call_node = _find_super_call(tree)
    assert call_node is not None
    # After transformation, super() should have two arguments: class name and first arg of method
    assert len(call_node.args) == 2
    assert isinstance(call_node.args[0], ast.Name) and call_node.args[0].id == "MyClass"
    assert isinstance(call_node.args[1], ast.Name) and call_node.args[1].id == "self"


def test_super_outside_function_no_change(tmp_path, caplog):
    source = """
class MyClass:
    super()
"""
    tree = ast.parse(source)
    transformer = SuperWithoutArgumentsTransformer(tree)
    transformer.visit(tree)

    call_node = _find_super_call(tree)
    assert call_node is not None
    # No arguments should be added because super() is outside a function
    assert len(call_node.args) == 0
    # Warning should be logged
    assert any("super() outside of function" in rec.message for rec in caplog.records)


def test_super_outside_class_no_change(tmp_path, caplog):
    source = """
def func():
    super()
"""
    tree = ast.parse(source)
    transformer = SuperWithoutArgumentsTransformer(tree)
    transformer.visit(tree)

    call_node = _find_super_call(tree)
    assert call_node is not None
    # No arguments should be added because super() is outside a class
    assert len(call_node.args) == 0
    # Warning should be logged
    assert any("super() outside of class" in rec.message for rec in caplog.records)
