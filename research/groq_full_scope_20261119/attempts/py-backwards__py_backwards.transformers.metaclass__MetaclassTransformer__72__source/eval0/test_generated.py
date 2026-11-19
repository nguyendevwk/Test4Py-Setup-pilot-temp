import ast
import pytest
from typed_ast import ast3 as typed_ast
from py_backwards.transformers.metaclass import MetaclassTransformer
from py_backwards.utils.snippet import snippet

def _parse_and_transform(source: str) -> typed_ast.Module:
    """Parse source with typed_ast and apply MetaclassTransformer."""
    tree = typed_ast.parse(source)
    transformer = MetaclassTransformer()
    transformed = transformer.visit(tree)
    return transformed

def test_metaclass_transformation_inserts_six_and_wraps_base():
    source = """
class A(metaclass=B):
    pass
"""
    transformed = _parse_and_transform(source)
    # The first statement should be the six import
    assert isinstance(transformed.body[0], typed_ast.Import)
    assert transformed.body[0].names[0].name == "six"

    # Find the class definition
    class_def = next(node for node in transformed.body if isinstance(node, typed_ast.ClassDef))
    # After transformation, no keywords should remain
    assert class_def.keywords == []

    # The bases list should contain a single Call to _py_backwards_six_with_metaclass
    assert len(class_def.bases) == 1
    base_call = class_def.bases[0]
    assert isinstance(base_call, typed_ast.Call)
    assert isinstance(base_call.func, typed_ast.Name)
    assert base_call.func.id == "_py_backwards_six_with_metaclass"
    # The argument to the call should be the original metaclass B
    assert isinstance(base_call.args[0], typed_ast.Name)
    assert base_call.args[0].id == "B"

def test_class_without_metaclass_remains_unchanged():
    source = """
class C:
    x = 1
"""
    transformed = _parse_and_transform(source)
    # No six import should be added
    assert not any(isinstance(node, typed_ast.Import) for node in transformed.body)

    class_def = next(node for node in transformed.body if isinstance(node, typed_ast.ClassDef))
    # Base list should be unchanged (empty)
    assert class_def.bases == []
    # Keywords should be unchanged (empty)
    assert class_def.keywords == []

def test_metaclass_keyword_not_named_metaclass_is_also_transformed():
    source = """
class D(foo=Bar):
    pass
"""
    transformed = _parse_and_transform(source)
    # The transformer will treat the first keyword as metaclass regardless of name
    class_def = next(node for node in transformed.body if isinstance(node, typed_ast.ClassDef))
    # Keywords should be cleared
    assert class_def.keywords == []

    # Base should be wrapped
    assert len(class_def.bases) == 1
    base_call = class_def.bases[0]
    assert isinstance(base_call, typed_ast.Call)
    assert isinstance(base_call.func, typed_ast.Name)
    assert base_call.func.id == "_py_backwards_six_with_metaclass"
    # The argument should be the value of the keyword (Bar)
    assert isinstance(base_call.args[0], typed_ast.Name)
    assert base_call.args[0].id == "Bar"
