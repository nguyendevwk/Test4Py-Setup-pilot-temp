import ast
import pytest
from apimd.parser import Resolver

def apply_transformer(code: str, root: str, alias: dict, self_ty: str = "") -> str:
    """Helper to parse, transform, and unparse a code snippet."""
    tree = ast.parse(code)
    transformer = Resolver(root, alias, self_ty)
    transformed = transformer.visit(tree)
    ast.fix_missing_locations(transformed)
    return ast.unparse(transformed)

def test_visit_constant_parses_and_resolves_name():
    # Constant string that is a valid Python expression (a Name)
    code = "x = 'y'"
    # alias maps 'y' to 'z', so the constant should resolve to Name('z')
    transformed = apply_transformer(code, root="pkg", alias={"y": "z"})
    assert transformed == "x = z"

    # Constant string that is not a valid expression should remain unchanged
    code_invalid = "x = 'not a valid expr'"
    transformed_invalid = apply_transformer(code_invalid, root="pkg", alias={})
    assert transformed_invalid == "x = 'not a valid expr'"

def test_visit_name_resolves_self_and_aliases():
    # self_ty replacement
    code_self = "x: Self = None"
    transformed_self = apply_transformer(code_self, root="pkg", alias={}, self_ty="Self")
    assert transformed_self == "x: Self = None"

    # Alias resolution: 'foo' maps to 'typing.List[int]'
    code_alias = "x: foo = None"
    transformed_alias = apply_transformer(
        code_alias,
        root="pkg",
        alias={"foo": "typing.List[int]"}
    )
    # The alias should be expanded to the actual type
    assert transformed_alias == "x: List[int] = None"

    # Alias that is a TypeVar should not be expanded
    code_typevar = "x: T = None"
    transformed_typevar = apply_transformer(
        code_typevar,
        root="pkg",
        alias={"T": "typing.TypeVar('T')"}
    )
    assert transformed_typevar == "x: T = None"

def test_visit_subscript_handles_union_and_optional_and_pep585():
    # Union via typing.Union
    code_union = "x: typing.Union[int, str] = None"
    transformed_union = apply_transformer(
        code_union,
        root="pkg",
        alias={"typing.Union": "typing.Union"}
    )
    assert transformed_union == "x: int | str = None"

    # Optional via typing.Optional
    code_optional = "x: typing.Optional[int] = None"
    transformed_optional = apply_transformer(
        code_optional,
        root="pkg",
        alias={"typing.Optional": "typing.Optional"}
    )
    assert transformed_optional == "x: int | None = None"

    # Deprecated PEP585 name: 'list' should be replaced with 'List'
    code_pep585 = "x: list[int] = None"
    transformed_pep585 = apply_transformer(
        code_pep585,
        root="pkg",
        alias={}
    )
    assert transformed_pep585 == "x: List[int] = None"
