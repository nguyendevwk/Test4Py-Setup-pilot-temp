import pytest
from apimd.parser import const_type
from ast import Constant, Tuple, List, Set, Dict, Call, Name, Attribute, parse

def test_const_type_basic_constants():
    # Integer constant
    node_int = Constant(value=42)
    assert const_type(node_int) == 'int'

    # String constant
    node_str = Constant(value="hello")
    assert const_type(node_str) == 'str'

    # Boolean constant
    node_bool = Constant(value=True)
    assert const_type(node_bool) == 'bool'

def test_const_type_collections_and_dicts():
    # List of integers
    node_list = List(elts=[Constant(value=1), Constant(value=2)])
    assert const_type(node_list) == 'listint'

    # Tuple of mixed types
    node_tuple = Tuple(elts=[Constant(value=1), Constant(value="a")])
    assert const_type(node_tuple) == 'tupleintstr'

    # Set of floats
    node_set = Set(elts=[Constant(value=1.5), Constant(value=2.5)])
    assert const_type(node_set) == 'setfloat'

    # Dict with string keys and integer values
    node_dict = Dict(keys=[Constant(value="x"), Constant(value="y")],
                     values=[Constant(value=10), Constant(value=20)])
    assert const_type(node_dict) == 'dictstrint'

def test_const_type_call_and_unknown():
    # Call to built-in type constructor
    node_call_int = Call(func=Name(id='int', ctx=None), args=[], keywords=[])
    assert const_type(node_call_int) == 'int'

    # Call to a non-PEP585 type
    node_call_custom = Call(func=Name(id='CustomType', ctx=None), args=[], keywords=[])
    assert const_type(node_call_custom) == 'ANY'

    # Node that is not handled by const_type
    node_unhandled = parse("x + y").body[0].value  # BinOp node
    assert const_type(node_unhandled) == 'ANY'
