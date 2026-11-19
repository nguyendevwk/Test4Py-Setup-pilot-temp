import ast
import typed_ast.ast3 as typed_ast
import pytest
from py_backwards.utils.snippet import VariablesReplacer


def _parse(source: str) -> typed_ast.Module:
    """Parse source code into a typed_ast Module."""
    return typed_ast.parse(source)


def _get_name(node: typed_ast.Module, attr: str) -> str:
    """Return the first occurrence of a Name node's id in the AST."""
    for n in typed_ast.walk(node):
        if isinstance(n, typed_ast.Name):
            return n.id
    raise AssertionError(f"No Name node found for attribute {attr}")


def _get_arg(node: typed_ast.Module, arg_name: str) -> str:
    """Return the first occurrence of an arg node's arg in the AST."""
    for n in typed_ast.walk(node):
        if isinstance(n, typed_ast.arg) and n.arg == arg_name:
            return n.arg
    raise AssertionError(f"No arg node found for argument {arg_name}")


def _get_import_from_module(node: typed_ast.Module) -> str:
    """Return the module string of the first ImportFrom node."""
    for n in typed_ast.walk(node):
        if isinstance(n, typed_ast.ImportFrom):
            return n.module
    raise AssertionError("No ImportFrom node found")


def test_replace_name_and_arg():
    source = """
def foo(x):
    y = x + 1
    return y
"""
    tree = _parse(source)
    # Map variable names to new unique names
    mapping = {"x": "x_unique", "y": "y_unique", "foo": "foo_unique"}
    VariablesReplacer.replace(tree, mapping)

    # Verify that function name, argument name, and variable names are replaced
    assert _get_name(tree, "foo") == "foo_unique"
    assert _get_arg(tree, "x") == "x_unique"
    # The variable 'y' appears twice: once as target of assignment, once as return value
    # The first occurrence should be replaced in the assignment target
    names = [n.id for n in typed_ast.walk(tree) if isinstance(n, typed_ast.Name)]
    assert "y_unique" in names
    assert "y" not in names


def test_replace_import_from_module_parts():
    source = """
from mypkg.submodule import MyClass as MC
"""
    tree = _parse(source)
    mapping = {"mypkg": "pkg", "submodule": "sub", "MyClass": "Cls"}
    VariablesReplacer.replace(tree, mapping)

    # The module string should be updated to 'pkg.sub'
    assert _get_import_from_module(tree) == "pkg.sub"
    # The alias name should be updated to 'Cls'
    for n in typed_ast.walk(tree):
        if isinstance(n, typed_ast.alias):
            assert n.name == "Cls"
            assert n.asname == "MC"  # asname unchanged


def test_no_replacement_for_unmatched_types():
    source = """
class MyClass:
    def method(self, param):
        return param
"""
    tree = _parse(source)
    # Provide a mapping where the value is a different AST node type
    # For example, map 'MyClass' to a FunctionDef node (should not replace)
    dummy_func = typed_ast.FunctionDef(name="dummy", args=typed_ast.arguments(args=[]), body=[], decorator_list=[])
    mapping = {"MyClass": dummy_func, "method": "method_unique"}
    VariablesReplacer.replace(tree, mapping)

    # Class name should remain unchanged because mapping value is not a string or same type
    class_names = [n.name for n in typed_ast.walk(tree) if isinstance(n, typed_ast.ClassDef)]
    assert "MyClass" in class_names
    # Method name should be replaced because mapping value is a string
    method_names = [n.name for n in typed_ast.walk(tree) if isinstance(n, typed_ast.FunctionDef)]
    assert "method_unique" in method_names
    assert "method" not in method_names
