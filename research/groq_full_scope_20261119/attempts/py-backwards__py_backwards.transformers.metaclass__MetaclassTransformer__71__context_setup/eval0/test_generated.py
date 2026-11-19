import pytest
import typed_ast.ast3 as ast
from py_backwards.transformers.metaclass import MetaclassTransformer


def test_metaclass_transformation_inserts_import_and_replaces_bases(tmp_path):
    source = "class A(metaclass=B):\n    pass"
    tree = ast.parse(source)
    transformer = MetaclassTransformer()
    transformed = transformer.visit(tree)

    # Import should be inserted at the top
    first_stmt = transformed.body[0]
    assert isinstance(first_stmt, ast.ImportFrom)
    assert first_stmt.module == "six"
    assert first_stmt.names[0].name == "with_metaclass"

    # Class definition should have no keywords
    class_def = transformed.body[1]
    assert isinstance(class_def, ast.ClassDef)
    assert class_def.keywords == []

    # Base should be a call to _py_backwards_six_with_metaclass
    base_call = class_def.bases[0]
    assert isinstance(base_call, ast.Call)
    assert isinstance(base_call.func, ast.Name)
    assert base_call.func.id == "_py_backwards_six_with_metaclass"
    # The first argument of the call should be the original metaclass
    assert isinstance(base_call.args[0], ast.Name)
    assert base_call.args[0].id == "B"


def test_class_without_metaclass_keyword_remains_unchanged(tmp_path):
    source = "class C:\n    pass"
    tree = ast.parse(source)
    transformer = MetaclassTransformer()
    transformed = transformer.visit(tree)

    # No import should be added
    assert not isinstance(transformed.body[0], ast.ImportFrom)

    # Class definition should be unchanged
    class_def = transformed.body[0]
    assert isinstance(class_def, ast.ClassDef)
    assert class_def.bases == []
    assert class_def.keywords == []


def test_multiple_keywords_only_first_processed_and_all_removed(tmp_path):
    source = "class D(metaclass=E, foo=1):\n    pass"
    tree = ast.parse(source)
    transformer = MetaclassTransformer()
    transformed = transformer.visit(tree)

    class_def = transformed.body[0]
    # After transformation, all keywords should be removed
    assert class_def.keywords == []

    # Base should be replaced by the metaclass call
    base_call = class_def.bases[0]
    assert isinstance(base_call, ast.Call)
    assert isinstance(base_call.func, ast.Name)
    assert base_call.func.id == "_py_backwards_six_with_metaclass"
    # The first argument should be the original metaclass
    assert isinstance(base_call.args[0], ast.Name)
    assert base_call.args[0].id == "E"
