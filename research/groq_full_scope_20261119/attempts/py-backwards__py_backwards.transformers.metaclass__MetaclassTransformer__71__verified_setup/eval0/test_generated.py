import pytest
from typed_ast import ast3 as ast
from py_backwards.transformers.metaclass import MetaclassTransformer


def test_metaclass_transformation_inserts_six_import_and_wraps_base():
    # Parse a module with a class that uses a metaclass
    source = """
class A(metaclass=B):
    pass
"""
    module = ast.parse(source)

    transformer = MetaclassTransformer()
    transformed = transformer.visit(module)

    # The first statement should be an import from six
    assert isinstance(transformed.body[0], ast.Import)
    assert transformed.body[0].names[0].name == "six"

    # The class definition should have no keywords
    class_def = transformed.body[1]
    assert isinstance(class_def, ast.ClassDef)
    assert class_def.keywords == []

    # The bases list should contain a call to _py_backwards_six_with_metaclass(B)
    assert len(class_def.bases) == 1
    base_call = class_def.bases[0]
    assert isinstance(base_call, ast.Call)
    assert isinstance(base_call.func, ast.Name)
    assert base_call.func.id == "_py_backwards_six_with_metaclass"
    assert len(base_call.args) == 1
    assert isinstance(base_call.args[0], ast.Name)
    assert base_call.args[0].id == "B"


def test_no_metaclass_class_remains_unchanged():
    # Parse a module with a class that does not use a metaclass
    source = """
class C:
    pass
"""
    module = ast.parse(source)

    transformer = MetaclassTransformer()
    transformed = transformer.visit(module)

    # No import should be inserted
    assert not isinstance(transformed.body[0], ast.Import)

    # The class definition should be unchanged
    class_def = transformed.body[0]
    assert isinstance(class_def, ast.ClassDef)
    assert class_def.keywords == []
    assert class_def.bases == []


def test_multiple_classes_with_and_without_metaclass():
    # Parse a module with two classes, one with metaclass and one without
    source = """
class X(metaclass=Meta):
    pass

class Y:
    pass
"""
    module = ast.parse(source)

    transformer = MetaclassTransformer()
    transformed = transformer.visit(module)

    # The first statement should be the six import
    assert isinstance(transformed.body[0], ast.Import)
    assert transformed.body[0].names[0].name == "six"

    # First class (X) should be transformed
    class_x = transformed.body[1]
    assert isinstance(class_x, ast.ClassDef)
    assert class_x.keywords == []
    assert len(class_x.bases) == 1
    base_call = class_x.bases[0]
    assert isinstance(base_call, ast.Call)
    assert base_call.func.id == "_py_backwards_six_with_metaclass"
    assert base_call.args[0].id == "Meta"

    # Second class (Y) should remain unchanged
    class_y = transformed.body[2]
    assert isinstance(class_y, ast.ClassDef)
    assert class_y.keywords == []
    assert class_y.bases == []
