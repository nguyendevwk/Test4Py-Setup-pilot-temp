import ast
import typed_ast.ast3 as typed_ast
import inspect
import sys
import io

from py_backwards.transformers.super_without_arguments import SuperWithoutArgumentsTransformer
from py_backwards.exceptions import NodeNotFound

def parse_and_transform(code: str) -> typed_ast.Module:
    """Parse code with typed_ast and apply the transformer."""
    tree = typed_ast.parse(code)
    transformer = SuperWithoutArgumentsTransformer()
    transformer.visit(tree)
    return tree

def get_call_node(tree: typed_ast.Module) -> typed_ast.Call:
    """Return the first Call node found in the tree."""
    for node in ast.walk(tree):
        if isinstance(node, typed_ast.Call):
            return node
    raise AssertionError("No Call node found")

def test_super_replaced_inside_method(tmp_path):
    code = """
class MyClass:
    def method(self):
        super()
"""
    tree = parse_and_transform(code)
    call_node = get_call_node(tree)
    # After transformation, args should be [Name('MyClass'), Name('self')]
    assert isinstance(call_node.args[0], typed_ast.Name)
    assert call_node.args[0].id == "MyClass"
    assert isinstance(call_node.args[1], typed_ast.Name)
    assert call_node.args[1].id == "self"

def test_super_outside_function_warns_and_unchanged(tmp_path, capsys):
    code = """
class MyClass:
    super()
"""
    tree = parse_and_transform(code)
    call_node = get_call_node(tree)
    # The call should remain unchanged (no args)
    assert call_node.args == []
    # Capture warning output
    captured = capsys.readouterr()
    assert "super() outside of function" in captured.out

def test_super_outside_class_warns_and_unchanged(tmp_path, capsys):
    code = """
def func():
    super()
"""
    tree = parse_and_transform(code)
    call_node = get_call_node(tree)
    # The call should remain unchanged (no args)
    assert call_node.args == []
    # Capture warning output
    captured = capsys.readouterr()
    assert "super() outside of class" in captured.out
