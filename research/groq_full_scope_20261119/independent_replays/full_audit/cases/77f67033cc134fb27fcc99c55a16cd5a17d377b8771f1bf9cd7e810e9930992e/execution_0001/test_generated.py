import ast
import pytest
from apimd.parser import const_type, ANY

def test_const_type_with_constant_and_sequence():
    # Constant node
    node_const = ast.Constant(value=42)
    assert const_type(node_const) == "int"

    # List of constants with same type
    node_list = ast.List(elts=[ast.Constant(value=1), ast.Constant(value=2)], ctx=ast.Load())
    assert const_type(node_list) == "list[int]"

    # Tuple of constants with mixed types -> Any
    node_tuple = ast.Tuple(elts=[ast.Constant(value=1), ast.Constant(value="a")], ctx=ast.Load())
    assert const_type(node_tuple) == "tuple[Any]"

def test_const_type_with_dict_and_call():
    # Dict with constant keys and values of same type
    node_dict = ast.Dict(
        keys=[ast.Constant(value="x"), ast.Constant(value="y")],
        values=[ast.Constant(value=3), ast.Constant(value=4)]
    )
    assert const_type(node_dict) == "dict[str, int]"

    # Call to a known type constructor
    node_call = ast.Call(func=ast.Name(id="int", ctx=ast.Load()), args=[ast.Constant(value="5")], keywords=[])
    assert const_type(node_call) == "int"

    # Call to an unknown function returns ANY
    node_call_unknown = ast.Call(func=ast.Name(id="unknown_func", ctx=ast.Load()), args=[], keywords=[])
    assert const_type(node_call_unknown) == ANY

def test_const_type_with_invalid_and_boundary_inputs():
    # Passing a node that is not an expr (e.g., an ast.Module) should fall back to ANY
    node_module = ast.Module(body=[])
    assert const_type(node_module) == ANY

    # Passing a Call with a non-name function (e.g., a lambda) returns ANY
    node_lambda_call = ast.Call(func=ast.Lambda(args=ast.arguments(posonlyargs=[], args=[], vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[]), body=ast.Constant(value=1)), args=[], keywords=[])
    assert const_type(node_lambda_call) == ANY
