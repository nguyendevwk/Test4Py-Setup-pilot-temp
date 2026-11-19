import ast as pyast
import typed_ast.ast3 as ast
import pytest
from py_backwards.transformers.super_without_arguments import SuperWithoutArgumentsTransformer
from py_backwards.exceptions import NodeNotFound
from py_backwards.utils.helpers import warn


def find_super_call(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "super":
            return node
    return None


def test_super_without_arguments_transforms_inside_method(tmp_path):
    src = """
class A:
    def foo(self):
        super()
"""
    tree = ast.parse(src)
    transformer = SuperWithoutArgumentsTransformer()
    transformer.visit(tree)

    call = find_super_call(tree)
    assert call is not None
    assert len(call.args) == 2
    assert isinstance(call.args[0], ast.Name) and call.args[0].id == "A"
    assert isinstance(call.args[1], ast.Name) and call.args[1].id == "self"


def test_super_without_arguments_warns_outside_class(tmp_path, caplog):
    src = """
def bar():
    super()
"""
    tree = ast.parse(src)
    transformer = SuperWithoutArgumentsTransformer()
    transformer.visit(tree)

    call = find_super_call(tree)
    assert call is not None
    # No arguments should be added
    assert len(call.args) == 0
    # Warning should be logged
    assert any("super() outside of class" in rec.message for rec in caplog.records)


def test_super_without_arguments_no_change_when_args_present(tmp_path):
    src = """
class B:
    def baz(self):
        super(1, 2)
"""
    tree = ast.parse(src)
    transformer = SuperWithoutArgumentsTransformer()
    transformer.visit(tree)

    call = find_super_call(tree)
    assert call is not None
    # Arguments should remain unchanged
    assert len(call.args) == 2
    assert isinstance(call.args[0], ast.Num) and call.args[0].n == 1
    assert isinstance(call.args[1], ast.Num) and call.args[1].n == 2
