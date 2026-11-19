import ast
import typed_ast.ast3 as typed_ast
import pytest
from py_backwards.utils.snippet import VariablesReplacer

def parse_code(code: str):
    """Parse source code into a typed_ast module node."""
    return typed_ast.parse(code)

def get_name_ids(module):
    """Return a list of all Name.id values in the module."""
    return [node.id for node in typed_ast.walk(module) if isinstance(node, typed_ast.Name)]

def get_function_names(module):
    """Return a list of all FunctionDef.name values in the module."""
    return [node.name for node in typed_ast.walk(module) if isinstance(node, typed_ast.FunctionDef)]

def get_import_from_modules(module):
    """Return a list of all ImportFrom.module values in the module."""
    return [node.module for node in typed_ast.walk(module) if isinstance(node, typed_ast.ImportFrom)]

def get_alias_names(module):
    """Return a list of all alias.name values in the module."""
    return [node.name for node in typed_ast.walk(module) if isinstance(node, typed_ast.alias)]

def get_except_names(module):
    """Return a list of all ExceptHandler.name values in the module."""
    return [node.name for node in typed_ast.walk(module) if isinstance(node, typed_ast.ExceptHandler)]

def test_name_and_function_replacement(tmp_path):
    code = """
def foo(x):
    y = x + 1
    return y
"""
    tree = parse_code(code)
    variables = {"foo": "bar", "x": "z", "y": "w"}
    VariablesReplacer.replace(tree, variables)

    # Check function name replaced
    assert get_function_names(tree) == ["bar"]

    # Check variable names replaced
    assert get_name_ids(tree) == ["z", "w", "z", "w"]

def test_import_and_alias_replacement(tmp_path):
    code = """
from module.sub import foo as bar
import module.sub as mod
"""
    tree = parse_code(code)
    variables = {"module": "pkg", "sub": "inner", "foo": "baz", "bar": "qux", "mod": "m"}
    VariablesReplacer.replace(tree, variables)

    # Check ImportFrom module replaced
    assert get_import_from_modules(tree) == ["pkg.inner"]

    # Check alias names replaced
    assert get_alias_names(tree) == ["pkg.inner.baz", "pkg.inner"]

def test_except_handler_and_attribute_replacement(tmp_path):
    code = """
try:
    pass
except ValueError as err:
    print(err)
"""
    tree = parse_code(code)
    variables = {"ValueError": "CustomError", "err": "error", "print": "log"}
    VariablesReplacer.replace(tree, variables)

    # Check except handler name replaced
    assert get_except_names(tree) == ["error"]

    # Check attribute names (print is a Name, not Attribute, so test Name replacement)
    assert get_name_ids(tree) == ["log", "error"]
