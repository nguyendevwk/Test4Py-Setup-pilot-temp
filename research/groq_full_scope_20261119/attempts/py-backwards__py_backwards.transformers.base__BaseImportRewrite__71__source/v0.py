import ast
import typed_ast.ast3 as typed_ast
import pytest
from py_backwards.transformers.base import BaseImportRewrite
from py_backwards.utils.snippet import import_rewrite


class DummyRewrite(BaseImportRewrite):
    rewrites = [("oldpkg", "newpkg")]


def parse_code(code: str):
    """Parse code into a typed_ast module and return the first statement."""
    module = typed_ast.parse(code)
    return module.body[0]


def test_visit_import_rewrites_to_try():
    """Import of a matched module should be replaced with a Try node."""
    node = parse_code("import oldpkg")
    transformer = DummyRewrite()
    result = transformer.visit_Import(node)
    assert isinstance(result, typed_ast.Try)
    # The body of the Try should contain the new import
    new_import = result.body[0]
    assert isinstance(new_import, typed_ast.Import)
    assert new_import.names[0].name == "newpkg"


def test_visit_importfrom_module_rewrites():
    """ImportFrom of a matched module should be replaced with a Try node."""
    node = parse_code("from oldpkg import foo")
    transformer = DummyRewrite()
    result = transformer.visit_ImportFrom(node)
    assert isinstance(result, typed_ast.Try)
    new_import_from = result.body[0]
    assert isinstance(new_import_from, typed_ast.ImportFrom)
    assert new_import_from.module == "newpkg"
    assert new_import_from.names[0].name == "foo"


def test_visit_importfrom_names_rewrites():
    """ImportFrom with partially matched names should replace only those names."""
    node = parse_code("from oldpkg import foo, bar, baz")
    transformer = DummyRewrite()
    result = transformer.visit_ImportFrom(node)
    assert isinstance(result, typed_ast.Try)
    # The Try body should contain two ImportFrom nodes: one for the module rename,
    # one for the names that matched
    bodies = result.body
    # The first body is the module rename
    assert bodies[0].module == "newpkg"
    # The second body contains the renamed names
    renamed_names = bodies[1].names
    # Only 'foo' and 'bar' should be renamed to newpkg.foo and newpkg.bar
    renamed_set = {alias.name for alias in renamed_names}
    assert renamed_set == {"foo", "bar"}
    # The original 'baz' should remain unchanged
    assert bodies[2].module == "oldpkg"
    assert bodies[2].names[0].name == "baz"
