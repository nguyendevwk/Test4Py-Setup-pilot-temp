import ast
import pytest
from apimd.parser import Resolver

def _transform(code: str, root: str = "", alias: dict = None, self_ty: str = "") -> ast.AST:
    """Parse code, apply Resolver, and return the transformed AST."""
    alias = alias or {}
    tree = ast.parse(code)
    resolver = Resolver(root=root, alias=alias, self_ty=self_ty)
    return resolver.visit(tree)

def test_visit_constant_resolves_name(tmp_path):
    # Create a constant string that is a valid name and should be resolved
    code = "x = 'y'"
    # Alias 'y' to 'z' so that the constant should resolve to Name('z')
    alias = {"y": "z"}
    transformed = _transform(code, alias=alias)
    # Find the assignment target and value
    assign = transformed.body[0]
    assert isinstance(assign, ast.Assign)
    assert isinstance(assign.value, ast.Name)
    assert assign.value.id == "z"

def test_visit_name_alias_and_self(tmp_path):
    # Test that a name matching self_ty is replaced with 'Self'
    code = "x = a"
    alias = {"a": "b"}
    transformed = _transform(code, alias=alias, self_ty="a")
    assign = transformed.body[0]
    # Since 'a' is self_ty, it should become Name('Self')
    assert isinstance(assign.value, ast.Name)
    assert assign.value.id == "Self"

    # Test that a name not in alias remains unchanged
    code2 = "x = c"
    transformed2 = _transform(code2, alias=alias)
    assign2 = transformed2.body[0]
    assert isinstance(assign2.value, ast.Name)
    assert assign2.value.id == "c"

def test_visit_subscript_union_and_optional(tmp_path):
    # Test Union conversion: Union[int, str] -> int | str
    code = "x: Union[int, str] = None"
    alias = {"Union": "typing.Union"}
    transformed = _transform(code, alias=alias)
    ann = transformed.body[0].annotation
    # Should be a BinOp with BitOr between int and str
    assert isinstance(ann, ast.BinOp)
    assert isinstance(ann.op, ast.BitOr)
    assert isinstance(ann.left, ast.Name) and ann.left.id == "int"
    assert isinstance(ann.right, ast.Name) and ann.right.id == "str"

    # Test Optional conversion: Optional[int] -> int | None
    code_opt = "y: Optional[int] = None"
    alias_opt = {"Optional": "typing.Optional"}
    transformed_opt = _transform(code_opt, alias=alias_opt)
    ann_opt = transformed_opt.body[0].annotation
    assert isinstance(ann_opt, ast.BinOp)
    assert isinstance(ann_opt.op, ast.BitOr)
    assert isinstance(ann_opt.left, ast.Name) and ann_opt.left.id == "int"
    assert isinstance(ann_opt.right, ast.Constant) and ann_opt.right.value is None
