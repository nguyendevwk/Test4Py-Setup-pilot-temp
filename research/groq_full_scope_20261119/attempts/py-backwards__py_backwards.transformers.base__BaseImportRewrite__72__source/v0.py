import pytest
from typed_ast import ast3 as ast
from py_backwards.transformers.base import BaseImportRewrite
from py_backwards.transformers import import_rewrite

class DummyRewrite(BaseImportRewrite):
    rewrites = [('oldpkg', 'newpkg')]

def test_visit_import_rewrites_module_name():
    transformer = DummyRewrite()
    node = ast.Import(names=[ast.alias(name='oldpkg', asname=None)])
    result = transformer.visit_Import(node)
    # The result should be a Try node wrapping the rewritten import
    assert isinstance(result, ast.Try)
    # The rewritten import should have the new module name
    new_import = result.body[0]
    assert isinstance(new_import, ast.Import)
    assert new_import.names[0].name == 'newpkg'
    # The alias should be preserved
    assert new_import.names[0].asname is None
    # The transformer should mark the tree as changed
    assert transformer._tree_changed is True

def test_visit_importfrom_rewrites_module_name():
    transformer = DummyRewrite()
    node = ast.ImportFrom(module='oldpkg.sub', names=[ast.alias(name='func', asname=None)], level=0)
    result = transformer.visit_ImportFrom(node)
    # The result should be a Try node wrapping the rewritten import-from
    assert isinstance(result, ast.Try)
    new_import_from = result.body[0]
    assert isinstance(new_import_from, ast.ImportFrom)
    # The module should be rewritten
    assert new_import_from.module == 'newpkg.sub'
    # Names should be unchanged
    assert len(new_import_from.names) == 1
    assert new_import_from.names[0].name == 'func'
    assert transformer._tree_changed is True

def test_visit_importfrom_rewrites_specific_name():
    transformer = DummyRewrite()
    node = ast.ImportFrom(module='oldpkg', names=[
        ast.alias(name='func', asname=None),
        ast.alias(name='other', asname=None)
    ], level=0)
    result = transformer.visit_ImportFrom(node)
    # Only 'func' should be rewritten because full name matches rewrite
    assert isinstance(result, ast.Try)
    new_import_froms = result.body
    # Two ImportFrom nodes should be produced: one for rewritten, one for unchanged
    assert len(new_import_froms) == 2
    rewritten = next((n for n in new_import_froms if n.module == 'newpkg'), None)
    unchanged = next((n for n in new_import_froms if n.module == 'oldpkg'), None)
    assert rewritten is not None
    assert unchanged is not None
    # Rewritten node should contain only the rewritten name
    assert len(rewritten.names) == 1
    assert rewritten.names[0].name == 'func'
    # Unchanged node should contain the other name
    assert len(unchanged.names) == 1
    assert unchanged.names[0].name == 'other'
    assert transformer._tree_changed is True
