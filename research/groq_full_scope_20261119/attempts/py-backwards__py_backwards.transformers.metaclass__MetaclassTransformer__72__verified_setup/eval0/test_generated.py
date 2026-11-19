import ast
import typed_ast.ast3 as typed_ast
import pytest

from py_backwards.transformers.metaclass import MetaclassTransformer
from py_backwards.utils.snippet import snippet
from py_backwards.utils.tree import insert_at


def test_metaclass_transformation_inserts_six_import_and_modifies_bases(tmp_path):
    source = """
class A(metaclass=B):
    pass
"""
    module = snippet(source)
    transformer = MetaclassTransformer()
    transformed = transformer.visit(module)

    # The first statement should be the six import
    assert isinstance(transformed.body[0], typed_ast.Import)
    assert any(alias.name == "six" for alias in transformed.body[0].names)

    # The class should have a new base: _py_backwards_six_with_metaclass(B)
    class_node = transformed.body[1]
    assert isinstance(class_node, typed_ast.ClassDef)
    assert len(class_node.bases) == 1
    base = class_node.bases[0]
    assert isinstance(base, typed_ast.Call)
    assert isinstance(base.func, typed_ast.Attribute)
    assert base.func.attr == "with_metaclass"
    assert base.func.value.id == "_py_backwards_six"

    # The metaclass keyword should be removed
    assert not class_node.keywords


def test_class_without_metaclass_remains_unchanged(tmp_path):
    source = """
class C:
    pass
"""
    module = snippet(source)
    transformer = MetaclassTransformer()
    transformed = transformer.visit(module)

    # No six import should be added
    assert not any(isinstance(stmt, typed_ast.Import) for stmt in transformed.body)

    # The class should be unchanged
    class_node = transformed.body[0]
    assert isinstance(class_node, typed_ast.ClassDef)
    assert class_node.name == "C"
    assert not class_node.keywords
    assert len(class_node.bases) == 0


def test_multiple_classes_with_and_without_metaclass(tmp_path):
    source = """
class X(metaclass=Meta):
    pass

class Y:
    pass
"""
    module = snippet(source)
    transformer = MetaclassTransformer()
    transformed = transformer.visit(module)

    # Six import should be inserted once
    imports = [stmt for stmt in transformed.body if isinstance(stmt, typed_ast.Import)]
    assert len(imports) == 1
    assert any(alias.name == "six" for alias in imports[0].names)

    # First class X should have transformed base
    class_x = transformed.body[1]
    assert isinstance(class_x, typed_ast.ClassDef)
    assert class_x.name == "X"
    assert len(class_x.bases) == 1
    base = class_x.bases[0]
    assert isinstance(base, typed_ast.Call)
    assert base.func.attr == "with_metaclass"

    # Second class Y should remain unchanged
    class_y = transformed.body[2]
    assert isinstance(class_y, typed_ast.ClassDef)
    assert class_y.name == "Y"
    assert len(class_y.bases) == 0
