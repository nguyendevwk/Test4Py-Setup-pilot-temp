import ast
import typed_ast.ast3 as ast3
import pytest
from py_backwards.utils.snippet import VariablesReplacer


def test_name_and_attribute_replacement():
    source = """
def foo(x):
    y = x + 1
    return y
"""
    tree = ast3.parse(source)
    vars_map = {"foo": "bar", "x": "z", "y": "w"}
    VariablesReplacer.replace(tree, vars_map)
    # Verify function name replaced
    func = next(node for node in ast3.walk(tree) if isinstance(node, ast3.FunctionDef))
    assert func.name == "bar"
    # Verify argument name replaced
    arg = func.args.args[0]
    assert arg.arg == "z"
    # Verify variable usage replaced
    assign = next(node for node in ast3.walk(tree) if isinstance(node, ast3.Assign))
    target = assign.targets[0]
    assert isinstance(target, ast3.Name) and target.id == "w"
    value = assign.value
    assert isinstance(value, ast3.BinOp)
    left = value.left
    assert isinstance(left, ast3.Name) and left.id == "z"


def test_import_from_and_alias_replacement():
    source = "from module.sub import foo as bar"
    tree = ast3.parse(source)
    vars_map = {"module": "pkg", "sub": "mod", "foo": "baz", "bar": "qux"}
    VariablesReplacer.replace(tree, vars_map)
    import_node = next(node for node in ast3.walk(tree) if isinstance(node, ast3.ImportFrom))
    assert import_node.module == "pkg.mod"
    alias = import_node.names[0]
    assert alias.name == "baz"
    assert alias.asname == "qux"


def test_unmapped_variables_remain_unchanged():
    source = "a = 1\nb = a + 2"
    tree = ast3.parse(source)
    vars_map = {"a": "x"}  # 'b' not mapped
    VariablesReplacer.replace(tree, vars_map)
    assign_a = next(node for node in ast3.walk(tree) if isinstance(node, ast3.Assign) and node.targets[0].id == "x")
    assign_b = next(node for node in ast3.walk(tree) if isinstance(node, ast3.Assign) and node.targets[0].id == "b")
    assert assign_a is not None
    assert assign_b is not None
    # Ensure 'b' remains unchanged
    assert assign_b.targets[0].id == "b"
    # Ensure 'a' replaced with 'x'
    assert assign_a.targets[0].id == "x"
