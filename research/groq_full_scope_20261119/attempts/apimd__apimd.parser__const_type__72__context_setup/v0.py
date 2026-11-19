import ast
import pytest
from apimd.parser import const_type, ANY

def test_const_type_with_simple_constants():
    # Integer constant
    node_int = ast.Constant(value=42)
    assert const_type(node_int) == "int"

    # String constant
    node_str = ast.Constant(value="hello")
    assert const_type(node_str) == "str"

    # Boolean constant
    node_bool = ast.Constant(value=True)
    assert const_type(node_bool) == "bool"

def test_const_type_with_collections_and_calls():
    # List of integers
    node_list = ast.List(elts=[ast.Constant(value=1), ast.Constant(value=2)], ctx=ast.Load())
    assert const_type(node_list) == "list[int]"

    # Tuple of mixed types should fallback to Any
    node_tuple = ast.Tuple(elts=[ast.Constant(value=1), ast.Constant(value="a")], ctx=ast.Load())
    assert const_type(node_tuple) == "tuple[Any]"

    # Dict with homogeneous key/value types
    node_dict = ast.Dict(
        keys=[ast.Constant(value="x"), ast.Constant(value="y")],
        values=[ast.Constant(value=10), ast.Constant(value=20)]
    )
    assert const_type(node_dict) == "dict[str, int]"

    # Call to a known type constructor
    node_call = ast.Call(func=ast.Name(id="int", ctx=ast.Load()), args=[ast.Constant(value="123")], keywords=[])
    assert const_type(node_call) == "int"

def test_const_type_with_non_constant_and_mixed_elements():
    # Expression that is not a constant or collection
    node_expr = ast.BinOp(left=ast.Constant(value=1), op=ast.Add(), right=ast.Constant(value=2))
    assert const_type(node_expr) == ANY

    # List containing a non-constant element
    node_mixed = ast.List(elts=[ast.Constant(value=1), ast.Name(id="x", ctx=ast.Load())], ctx=ast.Load())
    assert const_type(node_mixed) == ANY

    # Dict with a non-constant key
    node_dict_nonconst = ast.Dict(
        keys=[ast.Name(id="k", ctx=ast.Load()), ast.Constant(value="y")],
        values=[ast.Constant(value=10), ast.Constant(value=20)]
    )
    assert const_type(node_dict_nonconst) == ANY
