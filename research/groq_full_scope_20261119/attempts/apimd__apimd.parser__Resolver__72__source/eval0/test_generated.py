import ast
import pytest
from apimd.parser import Resolver

# Helper to apply the resolver to an AST node
def resolve(node, root="mymodule", alias=None, self_ty=""):
    if alias is None:
        alias = {}
    resolver = Resolver(root, alias, self_ty)
    return resolver.visit(node)

def test_visit_constant_parses_and_resolves_string():
    # A constant string that is a valid expression should be parsed and resolved
    node = ast.Constant(value="1 + 2")
    resolved = resolve(node)
    # The resolved node should be a BinOp representing 1 + 2
    assert isinstance(resolved, ast.BinOp)
    assert isinstance(resolved.left, ast.Constant) and resolved.left.value == 1
    assert isinstance(resolved.right, ast.Constant) and resolved.right.value == 2
    assert isinstance(resolved.op, ast.Add)

def test_visit_name_replaces_alias_and_self():
    # Alias mapping for a name that should be replaced
    alias = {"mymodule.foo": "typing.List[int]"}
    # The resolver should replace 'foo' with the parsed expression
    node = ast.Name(id="foo", ctx=ast.Load())
    resolved = resolve(node, root="mymodule", alias=alias)
    # After resolution, the node should be a Subscript representing List[int]
    assert isinstance(resolved, ast.Subscript)
    assert isinstance(resolved.value, ast.Name) and resolved.value.id == "List"
    assert isinstance(resolved.slice, ast.Index)
    assert isinstance(resolved.slice.value, ast.Constant) and resolved.slice.value.value == 1

    # Self type replacement
    node_self = ast.Name(id="T", ctx=ast.Load())
    resolved_self = resolve(node_self, root="mymodule", alias={}, self_ty="T")
    assert isinstance(resolved_self, ast.Name) and resolved_self.id == "Self"

def test_visit_subscript_converts_union_and_optional():
    # Union conversion: typing.Union[int, str] -> int | str
    node_union = ast.Subscript(
        value=ast.Name(id="Union", ctx=ast.Load()),
        slice=ast.Tuple(elts=[ast.Constant(value=1), ast.Constant(value=2)], ctx=ast.Load()),
        ctx=ast.Load()
    )
    resolved_union = resolve(node_union, root="mymodule", alias={"mymodule.Union": "typing.Union"})
    assert isinstance(resolved_union, ast.BinOp)
    assert isinstance(resolved_union.op, ast.BitOr)
    assert isinstance(resolved_union.left, ast.Constant) and resolved_union.left.value == 1
    assert isinstance(resolved_union.right, ast.Constant) and resolved_union.right.value == 2

    # Optional conversion: typing.Optional[int] -> int | None
    node_opt = ast.Subscript(
        value=ast.Name(id="Optional", ctx=ast.Load()),
        slice=ast.Constant(value=1),
        ctx=ast.Load()
    )
    resolved_opt = resolve(node_opt, root="mymodule", alias={"mymodule.Optional": "typing.Optional"})
    assert isinstance(resolved_opt, ast.BinOp)
    assert isinstance(resolved_opt.op, ast.BitOr)
    assert isinstance(resolved_opt.left, ast.Constant) and resolved_opt.left.value == 1
    assert isinstance(resolved_opt.right, ast.Constant) and resolved_opt.right.value is None
