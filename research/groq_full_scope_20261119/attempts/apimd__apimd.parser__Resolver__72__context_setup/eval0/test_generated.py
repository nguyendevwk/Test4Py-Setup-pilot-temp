import ast
import pytest
from apimd.parser import Resolver, _m

# Helper to transform source code using Resolver
def transform(source: str, root: str, alias: dict[str, str], self_ty: str = "") -> str:
    tree = ast.parse(source)
    resolver = Resolver(root, alias, self_ty)
    transformed = resolver.visit(tree)
    ast.fix_missing_locations(transformed)
    return ast.unparse(transformed)

def test_constant_string_evaluation(tmp_path):
    # A string constant that is a valid expression should be replaced
    src = "x = '1 + 2'"
    result = transform(src, root="mymod", alias={}, self_ty="")
    assert result.strip() == "x = 3"

    # A string constant that is not a valid expression remains unchanged
    src = "y = 'invalid expression'"
    result = transform(src, root="mymod", alias={}, self_ty="")
    assert result.strip() == "y = 'invalid expression'"

def test_name_alias_and_self_resolution(tmp_path):
    # Alias mapping replaces a name with a new expression
    src = "a = foo"
    alias = {"mymod.foo": "bar + 1"}
    result = transform(src, root="mymod", alias=alias, self_ty="")
    assert result.strip() == "a = bar + 1"

    # self_ty replacement turns the identifier into 'Self'
    src = "b = self_ty"
    result = transform(src, root="mymod", alias={}, self_ty="self_ty")
    assert result.strip() == "b = Self"

def test_subscript_pep585_and_optional(tmp_path):
    # PEP585 deprecated name should be replaced with the modern equivalent
    src = "c: typing.List[int]"
    alias = {"mymod.typing.List": "typing.List"}
    result = transform(src, root="mymod", alias=alias, self_ty="")
    assert "typing.List[int]" in result  # unchanged because alias maps to same

    # Optional conversion: typing.Optional[int] -> int | None
    src = "d: typing.Optional[int]"
    alias = {"mymod.typing.Optional": "typing.Optional"}
    result = transform(src, root="mymod", alias=alias, self_ty="")
    assert "int | None" in result

    # Union conversion: typing.Union[int, str] -> int | str
    src = "e: typing.Union[int, str]"
    alias = {"mymod.typing.Union": "typing.Union"}
    result = transform(src, root="mymod", alias=alias, self_ty="")
    assert "int | str" in result
