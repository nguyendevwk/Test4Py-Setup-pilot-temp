import ast
import typed_ast.ast3 as ast3
import pytest
from py_backwards.utils.snippet import VariablesReplacer

# Helper to parse source into an AST module
def parse_source(src: str) -> ast3.Module:
    return ast3.parse(src)

def ast_to_source(node: ast3.AST) -> str:
    return ast.unparse(node) if hasattr(ast, "unparse") else ast3.dump(node)

def test_replace_name_and_attribute():
    src = """
x = 1
def foo():
    return x
obj.attr = x
"""
    tree = parse_source(src)
    # Replace variable 'x' with 'y' and attribute 'attr' with 'baz'
    variables = {"x": "y", "attr": "baz"}
    VariablesReplacer.replace(tree, variables)

    # After replacement, the source should contain 'y' instead of 'x'
    new_src = ast_to_source(tree)
    assert "y = 1" in new_src
    assert "return y" in new_src
    assert "obj.baz = y" in new_src
    # Ensure original names are not present
    assert "x" not in new_src
    assert "attr" not in new_src

def test_replace_function_and_class_names():
    src = """
class MyClass:
    def method(self):
        pass

def my_func():
    pass
"""
    tree = parse_source(src)
    variables = {"MyClass": "RenamedClass", "my_func": "renamed_func"}
    VariablesReplacer.replace(tree, variables)

    new_src = ast_to_source(tree)
    assert "class RenamedClass:" in new_src
    assert "def renamed_func()" in new_src
    # Ensure old names are absent
    assert "MyClass" not in new_src
    assert "my_func" not in new_src

def test_replace_import_from_and_alias():
    src = """
from module.sub import foo as bar
from other import baz
"""
    tree = parse_source(src)
    variables = {"module.sub": "new.module", "foo": "qux", "bar": "alias", "other": "other_mod", "baz": "quux"}
    VariablesReplacer.replace(tree, variables)

    new_src = ast_to_source(tree)
    # Check that module path and names are replaced
    assert "from new.module import qux as alias" in new_src
    assert "from other_mod import quux" in new_src
    # Ensure original identifiers are not present
    assert "module.sub" not in new_src
    assert "foo" not in new_src
    assert "bar" not in new_src
    assert "other" not in new_src
    assert "baz" not in new_src
