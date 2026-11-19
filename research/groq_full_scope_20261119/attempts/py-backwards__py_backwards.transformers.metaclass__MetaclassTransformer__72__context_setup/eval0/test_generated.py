import pytest
from typed_ast import ast3 as ast
from py_backwards.transformers.metaclass import MetaclassTransformer

def test_metaclass_transformation():
    source = "class A(metaclass=B):\n    pass"
    module = ast.parse(source)
    transformer = MetaclassTransformer()
    transformed = transformer.visit(module)

    # Import from six should be inserted at the top
    first_stmt = transformed.body[0]
    assert isinstance(first_stmt, ast.ImportFrom)
    assert first_stmt.module == "six"

    # The class should have its bases replaced
    class_def = transformed.body[1]
    assert isinstance(class_def, ast.ClassDef)
    assert len(class_def.bases) == 1
    base_call = class_def.bases[0]
    assert isinstance(base_call, ast.Call)
    assert isinstance(base_call.func, ast.Name)
    assert base_call.func.id == "_py_backwards_six_with_metaclass"

    # The original metaclass keyword should be removed
    assert class_def.keywords == []

def test_no_metaclass_keyword():
    source = "class B:\n    pass"
    module = ast.parse(source)
    transformer = MetaclassTransformer()
    transformed = transformer.visit(module)

    # No import should be added
    assert not any(isinstance(stmt, ast.ImportFrom) and stmt.module == "six" for stmt in transformed.body)

    # Class definition should remain unchanged
    class_def = transformed.body[0]
    assert isinstance(class_def, ast.ClassDef)
    assert class_def.bases == []
    assert class_def.keywords == []

def test_multiple_classes_mixed():
    source = (
        "class X(metaclass=Meta):\n    pass\n"
        "class Y:\n    pass\n"
        "class Z(metaclass=Other):\n    pass\n"
    )
    module = ast.parse(source)
    transformer = MetaclassTransformer()
    transformed = transformer.visit(module)

    # Import should be inserted once
    imports = [stmt for stmt in transformed.body if isinstance(stmt, ast.ImportFrom) and stmt.module == "six"]
    assert len(imports) == 1

    # Check each class
    class_defs = [stmt for stmt in transformed.body if isinstance(stmt, ast.ClassDef)]
    assert len(class_defs) == 3

    # X transformed
    x_def = class_defs[0]
    assert isinstance(x_def.bases[0], ast.Call)
    assert x_def.bases[0].func.id == "_py_backwards_six_with_metaclass"
    assert x_def.keywords == []

    # Y unchanged
    y_def = class_defs[1]
    assert y_def.bases == []
    assert y_def.keywords == []

    # Z transformed
    z_def = class_defs[2]
    assert isinstance(z_def.bases[0], ast.Call)
    assert z_def.bases[0].func.id == "_py_backwards_six_with_metaclass"
    assert z_def.keywords == []
