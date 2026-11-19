import pytest
from typed_ast import ast3 as ast
from py_backwards.transformers.base import BaseImportRewrite


class DummyRewrite(BaseImportRewrite):
    rewrites = [('oldpkg', 'newpkg'), ('oldpkg.sub', 'newpkg.sub')]


def test_get_matched_rewrite():
    tr = DummyRewrite()
    # Exact match
    assert tr._get_matched_rewrite('oldpkg') == ('oldpkg', 'newpkg')
    # Prefix match
    assert tr._get_matched_rewrite('oldpkg.submodule') == ('oldpkg', 'newpkg')
    # No match
    assert tr._get_matched_rewrite('otherpkg') is None
    # None input
    assert tr._get_matched_rewrite(None) is None


def test_visit_import_rewrite(tmp_path):
    tr = DummyRewrite()
    # Build an Import node for oldpkg
    node = ast.Import(names=[ast.alias(name='oldpkg', asname=None)])
    result = tr.visit_Import(node)
    # The result should be a Try node with a new Import inside
    assert isinstance(result, ast.Try)
    # The body of the try should contain the rewritten import
    body_import = result.body[0]
    assert isinstance(body_import, ast.Import)
    assert body_import.names[0].name == 'newpkg'
    # The except part should still be present
    assert len(result.handlers) == 1
    # Ensure the tree changed flag was set
    assert tr._tree_changed is True


def test_visit_import_from_module_rewrite(tmp_path):
    tr = DummyRewrite()
    # Build an ImportFrom node for oldpkg
    node = ast.ImportFrom(module='oldpkg', names=[ast.alias(name='foo', asname=None)], level=0)
    result = tr.visit_ImportFrom(node)
    # The result should be a Try node with a new ImportFrom inside
    assert isinstance(result, ast.Try)
    body_import_from = result.body[0]
    assert isinstance(body_import_from, ast.ImportFrom)
    assert body_import_from.module == 'newpkg'
    # The names should be preserved
    assert len(body_import_from.names) == 1
    assert body_import_from.names[0].name == 'foo'
    # Ensure the tree changed flag was set
    assert tr._tree_changed is True
