import ast
import typed_ast.ast3 as ast3
import pytest
from py_backwards.transformers.super_without_arguments import SuperWithoutArgumentsTransformer
from py_backwards.exceptions import NodeNotFound
from py_backwards.utils.helpers import warn

# Helper to parse source and apply transformer
def transform_source(src: str) -> ast3.Module:
    tree = ast3.parse(src)
    transformer = SuperWithoutArgumentsTransformer(tree)
    transformer.visit(tree)
    return tree

def ast_to_source(tree: ast3.Module) -> str:
    return ast.unparse(tree)

def test_super_without_arguments_replaced_inside_method():
    src = """
class A:
    def foo(self):
        return super()
"""
    tree = transform_source(src)
    # The call should now be super(A, self)
    new_src = ast_to_source(tree)
    assert "super(A, self)" in new_src
    # Ensure no other changes
    assert "class A" in new_src
    assert "def foo(self)" in new_src

def test_super_without_arguments_outside_function_or_class():
    src = """
def bar():
    return super()
"""
    tree = transform_source(src)
    # No change should occur
    new_src = ast_to_source(tree)
    assert "super()" in new_src
    assert "super(" not in new_src.replace("super()", "")

def test_super_with_arguments_not_modified():
    src = """
class B:
    def baz(self):
        return super(B, self)
"""
    tree = transform_source(src)
    new_src = ast_to_source(tree)
    # The original call should remain unchanged
    assert "super(B, self)" in new_src
    # No additional super() calls should appear
    assert new_src.count("super(") == 1
