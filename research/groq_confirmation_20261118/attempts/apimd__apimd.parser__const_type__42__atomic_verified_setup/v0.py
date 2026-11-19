import pytest
from apimd.parser import const_type
from ast import Constant, Tuple, List, Set, Dict, Call, Name, Attribute, unparse

def test_const_type_basic_constants():
    # Integer constant
    assert const_type(Constant(42)) == "int"
    # String constant
    assert const_type(Constant("hello")) == "str"
    # Boolean constant
    assert const_type(Constant(True)) == "bool"

def test_const_type_collections_and_dicts():
    # Tuple of constants
    assert const_type(Tuple(elts=[Constant(1), Constant(2)])) == "tuple[int]"
    # List of constants
    assert const_type(List(elts=[Constant("a"), Constant("b")])) == "list[str]"
    # Set of constants
    assert const_type(Set(elts=[Constant(3), Constant(4)])) == "set[int]"
    # Dict with constant keys and values
    assert const_type(Dict(keys=[Constant("x")], values=[Constant(10)])) == "dict[str, int]"

def test_const_type_calls_and_unknown():
    # Call to a known type constructor
    assert const_type(Call(func=Name(id="int", ctx=None), args=[], keywords=[])) == "int"
    # Call to an unknown function returns ANY
    assert const_type(Call(func=Name(id="unknown_func", ctx=None), args=[], keywords=[])) == "ANY"
    # Passing a non-ast.expr (e.g., int) falls back to ANY
    assert const_type(1) == "ANY"
