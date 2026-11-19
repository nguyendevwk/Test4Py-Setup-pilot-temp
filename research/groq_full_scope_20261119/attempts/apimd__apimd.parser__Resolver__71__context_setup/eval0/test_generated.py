import ast
import pytest
from apimd.parser import Resolver, _m

def test_visit_constant_parses_and_resolves_name():
    # Setup: a constant string that is a valid Python expression "foo"
    const_node = ast.Constant(value="foo")
    resolver = Resolver(root="mymod", alias={})
    # Resolve the constant
    resolved = resolver.visit(const_node)
    # The resolved node should be a Name node with id "foo"
    assert isinstance(resolved, ast.Name)
    assert resolved.id == "foo"
    # Unparse to string to confirm
    assert ast.unparse(resolved) == "foo"

def test_visit_name_resolves_alias_and_typevar():
    # Alias mapping: "mymod.bar" -> "typing.TypeVar('T')"
    alias_map = {"mymod.bar": "typing.TypeVar('T')"}
    resolver = Resolver(root="mymod", alias=alias_map)
    # Create a Name node for "bar"
    name_node = ast.Name(id="bar", ctx=ast.Load())
    # Resolve the name
    resolved = resolver.visit(name_node)
    # Since the alias is a TypeVar, the resolver should return the original node
    assert resolved is name_node
    # Now test a normal alias that is a simple expression
    alias_map["mymod.baz"] = "42"
    resolver = Resolver(root="mymod", alias=alias_map)
    name_node = ast.Name(id="baz", ctx=ast.Load())
    resolved = resolver.visit(name_node)
    # The alias "42" should be parsed and returned as a Constant node
    assert isinstance(resolved, ast.Constant)
    assert resolved.value == 42

def test_visit_subscript_union_and_optional():
    resolver = Resolver(root="mymod", alias={})
    # Union: typing.Union[int, str]
    union_expr = ast.parse("typing.Union[int, str]").body[0].value
    resolved_union = resolver.visit(union_expr)
    # Should be a BinOp with BitOr between int and str
    assert isinstance(resolved_union, ast.BinOp)
    assert isinstance(resolved_union.op, ast.BitOr)
    left, right = resolved_union.left, resolved_union.right
    assert isinstance(left, ast.Name) and left.id == "int"
    assert isinstance(right, ast.Name) and right.id == "str"
    # Optional: typing.Optional[int]
    optional_expr = ast.parse("typing.Optional[int]").body[0].value
    resolved_optional = resolver.visit(optional_expr)
    # Should be a BinOp with BitOr between int and None
    assert isinstance(resolved_optional, ast.BinOp)
    assert isinstance(resolved_optional.op, ast.BitOr)
    assert isinstance(resolved_optional.left, ast.Name) and resolved_optional.left.id == "int"
    assert isinstance(resolved_optional.right, ast.Constant) and resolved_optional.right.value is None
