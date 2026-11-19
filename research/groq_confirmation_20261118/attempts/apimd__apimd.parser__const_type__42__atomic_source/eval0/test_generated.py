import pytest
from apimd.parser import const_type, ANY
from ast import Constant, List, Tuple, Dict, Call, Name, Attribute, unparse

def test_const_type_with_simple_constants():
    # Integer constant
    node_int = Constant(value=42)
    assert const_type(node_int) == "int"

    # String constant
    node_str = Constant(value="hello")
    assert const_type(node_str) == "str"

    # Boolean constant
    node_bool = Constant(value=True)
    assert const_type(node_bool) == "bool"

def test_const_type_with_collections_and_calls():
    # List of constants
    node_list = List(elts=[Constant(value=1), Constant(value=2)])
    assert const_type(node_list) == "list[int]"

    # Tuple of mixed constants
    node_tuple = Tuple(elts=[Constant(value=1), Constant(value="a")])
    assert const_type(node_tuple) == "tuple[int, str]"

    # Dict with constant keys and values
    node_dict = Dict(keys=[Constant(value="x")], values=[Constant(value=3)])
    assert const_type(node_dict) == "dict[str, int]"

    # Call to a known type constructor
    node_call = Call(func=Name(id="int", ctx=unparse), args=[], keywords=[])
    assert const_type(node_call) == "int"

    # Call to an unknown function should return ANY
    node_unknown = Call(func=Name(id="unknown_func", ctx=unparse), args=[], keywords=[])
    assert const_type(node_unknown) == ANY

def test_const_type_with_unhandled_node_types():
    # Import node should not be handled and return ANY
    from ast import Import
    node_import = Import(names=[])
    assert const_type(node_import) == ANY

    # Delete node should not be handled and return ANY
    from ast import Delete
    node_delete = Delete(targets=[])
    assert const_type(node_delete) == ANY
