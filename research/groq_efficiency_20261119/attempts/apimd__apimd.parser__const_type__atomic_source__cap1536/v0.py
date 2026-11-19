import pytest
from apimd.parser import const_type
from ast import Constant, Tuple, List, Set, Dict, Call, Name, Attribute, parse

def test_constant_and_sequence_types():
    # Constant node
    assert const_type(Constant(value=42)) == "int"
    # Tuple node
    tuple_node = Tuple(elts=[Constant(value=1), Constant(value=2)])
    assert const_type(tuple_node) == "tuple[int]"
    # List node
    list_node = List(elts=[Constant(value="a"), Constant(value="b")])
    assert const_type(list_node) == "list[str]"
    # Set node
    set_node = Set(elts=[Constant(value=3), Constant(value=4)])
    assert const_type(set_node) == "set[int]"

def test_dict_and_call_types():
    # Dict node
    dict_node = Dict(keys=[Constant(value="x"), Constant(value="y")],
                     values=[Constant(value=1), Constant(value=2)])
    assert const_type(dict_node) == "dict[str, int]"
    # Call node with builtin type
    call_node = Call(func=Name(id="int", ctx=None), args=[], keywords=[])
    assert const_type(call_node) == "int"
    # Call node with PEP585 type
    # e.g., list[int] is represented as a Call to Attribute
    call_node_pep = Call(func=Attribute(value=Name(id="list", ctx=None), attr="int", ctx=None),
                         args=[], keywords=[])
    assert const_type(call_node_pep) == "list"

def test_unknown_and_default_behavior():
    # Unknown node type should return ANY
    class UnknownNode:  # simple dummy node
        pass
    assert const_type(UnknownNode()) == "ANY"
    # Call node with unknown function name
    call_node_unknown = Call(func=Name(id="unknown_func", ctx=None), args=[], keywords=[])
    assert const_type(call_node_unknown) == "ANY"
