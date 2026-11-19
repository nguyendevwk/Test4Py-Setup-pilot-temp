import ast
import typed_ast.ast3 as ast3
import pytest
from py_backwards.utils.snippet import VariablesReplacer

def test_name_and_attribute_replacement(tmp_path):
    code = """
def foo(x):
    y = x + 1
    return y
"""
    tree = ast3.parse(code)
    # Replace variable names: x -> a, y -> b
    replacer = VariablesReplacer({"x": "a", "y": "b"})
    VariablesReplacer.replace(tree, replacer._variables)
    # Verify that the function name remains unchanged
    assert isinstance(tree.body[0], ast3.FunctionDef)
    assert tree.body[0].name == "foo"
    # Verify that the argument name is replaced
    assert tree.body[0].args.args[0].arg == "a"
    # Verify that the assignment target is replaced
    assign = tree.body[0].body[0]
    assert isinstance(assign, ast3.Assign)
    assert assign.targets[0].id == "b"
    # Verify that the return value is replaced
    ret = tree.body[0].body[1]
    assert isinstance(ret, ast3.Return)
    assert ret.value.id == "b"

def test_import_from_and_alias_replacement(tmp_path):
    code = """
from module.sub import foo as bar
"""
    tree = ast3.parse(code)
    # Replace module parts and alias
    replacer = VariablesReplacer({"module": "mod", "foo": "baz", "bar": "qux"})
    VariablesReplacer.replace(tree, replacer._variables)
    imp = tree.body[0]
    assert isinstance(imp, ast3.ImportFrom)
    # Module should be replaced
    assert imp.module == "mod.sub"
    # Alias name should be replaced
    alias = imp.names[0]
    assert alias.name == "baz"
    assert alias.asname == "qux"

def test_except_handler_and_keyword_replacement(tmp_path):
    code = """
try:
    pass
except ValueError as e:
    print(e)
"""
    tree = ast3.parse(code)
    replacer = VariablesReplacer({"e": "exc", "print": "output"})
    VariablesReplacer.replace(tree, replacer._variables)
    handler = tree.body[0].handlers[0]
    assert handler.type.id == "ValueError"
    # Name in except handler should be replaced
    assert handler.name == "exc"
    # Keyword argument in print should be replaced
    call = handler.body[0]
    assert isinstance(call, ast3.Expr)
    assert isinstance(call.value, ast3.Call)
    assert call.value.func.id == "output"
    assert call.value.args[0].id == "exc"
