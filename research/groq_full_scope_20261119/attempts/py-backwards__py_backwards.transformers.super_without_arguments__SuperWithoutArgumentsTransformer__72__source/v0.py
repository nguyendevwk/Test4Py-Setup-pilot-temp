import ast
import typed_ast.ast3 as ast3
import warnings
import pytest
from py_backwards.transformers.super_without_arguments import SuperWithoutArgumentsTransformer
from py_backwards.exceptions import NodeNotFound

def _parse_and_transform(source: str) -> ast3.Module:
    """Parse source with typed_ast and apply the transformer."""
    tree = ast3.parse(source)
    transformer = SuperWithoutArgumentsTransformer()
    transformer._tree = tree
    transformer.visit(tree)
    return tree

def test_super_inside_method_replaces_args():
    src = """
class A:
    def foo(self):
        return super()
"""
    tree = _parse_and_transform(src)
    # Find the Call node
    call_node = None
    for node in ast3.walk(tree):
        if isinstance(node, ast3.Call) and isinstance(node.func, ast3.Name) and node.func.id == 'super':
            call_node = node
            break
    assert call_node is not None, "super() call not found"
    # After transformation, args should be [Name('A'), Name('self')]
    assert len(call_node.args) == 2
    assert isinstance(call_node.args[0], ast3.Name) and call_node.args[0].id == 'A'
    assert isinstance(call_node.args[1], ast3.Name) and call_node.args[1].id == 'self'

def test_super_outside_function_warns(caplog):
    src = """
class A:
    return super()
"""
    tree = ast3.parse(src)
    transformer = SuperWithoutArgumentsTransformer()
    transformer._tree = tree
    with caplog.at_level("WARNING"):
        transformer.visit(tree)
    # Expect a warning about super() outside of function
    assert any("super() outside of function" in rec.message for rec in caplog.records)

def test_super_outside_class_warns(caplog):
    src = """
def foo():
    return super()
"""
    tree = ast3.parse(src)
    transformer = SuperWithoutArgumentsTransformer()
    transformer._tree = tree
    with caplog.at_level("WARNING"):
        transformer.visit(tree)
    # Expect a warning about super() outside of class
    assert any("super() outside of class" in rec.message for rec in caplog.records)
