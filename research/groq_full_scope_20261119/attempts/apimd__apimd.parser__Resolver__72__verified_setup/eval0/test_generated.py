import ast
import pytest
from apimd.parser import Resolver, PEP585


def test_visit_constant_parses_and_resolves_string():
    # A string constant that is a valid expression should be parsed and visited.
    node = ast.parse("'x + 1'").body[0].value  # Constant node
    resolver = Resolver(root="mymod", alias={}, self_ty="")
    new_node = resolver.visit(node)
    # The result should be an expression node representing the parsed expression.
    assert isinstance(new_node, ast.BinOp)
    assert isinstance(new_node.left, ast.Name)
    assert new_node.left.id == "x"
    assert isinstance(new_node.right, ast.Constant)
    assert new_node.right.value == 1

    # A string that is not a valid expression should be left unchanged.
    bad_node = ast.parse("'not a valid expression'").body[0].value
    new_bad = resolver.visit(bad_node)
    assert new_bad is bad_node  # unchanged


def test_visit_name_resolves_alias_and_self():
    # Alias mapping should replace names with the parsed expression.
    alias = {"mymod.foo": "typing.List[int]"}
    resolver = Resolver(root="mymod", alias=alias, self_ty="T")
    name_node = ast.Name(id="foo", ctx=ast.Load())
    new_node = resolver.visit(name_node)
    # The alias expression is a Subscript; after visiting it should be a Subscript node.
    assert isinstance(new_node, ast.Subscript)
    assert isinstance(new_node.value, ast.Name)
    assert new_node.value.id == "List"

    # Self type should be replaced with 'Self'.
    self_node = ast.Name(id="T", ctx=ast.Load())
    new_self = resolver.visit(self_node)
    assert isinstance(new_self, ast.Name)
    assert new_self.id == "Self"


def test_visit_subscript_pep585_and_union_optional():
    resolver = Resolver(root="mymod", alias={}, self_ty="")

    # typing.Union -> BitOr chain
    union_node = ast.parse("typing.Union[int, str]").body[0].value
    new_union = resolver.visit(union_node)
    assert isinstance(new_union, ast.BinOp)
    assert isinstance(new_union.op, ast.BitOr)
    # The left side should be the first element, right side the second
    assert isinstance(new_union.left, ast.Name)
    assert new_union.left.id == "int"
    assert isinstance(new_union.right, ast.Name)
    assert new_union.right.id == "str"

    # typing.Optional -> Union with None
    opt_node = ast.parse("typing.Optional[int]").body[0].value
    new_opt = resolver.visit(opt_node)
    assert isinstance(new_opt, ast.BinOp)
    assert isinstance(new_opt.op, ast.BitOr)
    assert isinstance(new_opt.left, ast.Name)
    assert new_opt.left.id == "int"
    assert isinstance(new_opt.right, ast.Constant)
    assert new_opt.right.value is None

    # PEP585 deprecated name mapping
    # Pick a key from PEP585, e.g., 'typing.List' -> 'list'
    for old, new in PEP585.items():
        if old.startswith("typing."):
            name = old.split(".", 1)[1]
            sub_node = ast.parse(f"{old}[int]").body[0].value
            new_sub = resolver.visit(sub_node)
            assert isinstance(new_sub, ast.Subscript)
            assert isinstance(new_sub.value, ast.Name)
            assert new_sub.value.id == new
            break
