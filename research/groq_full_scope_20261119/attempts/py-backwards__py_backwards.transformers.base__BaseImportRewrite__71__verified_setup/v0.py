import ast
import typed_ast.ast3 as typed_ast
import pytest
from py_backwards.transformers.base import BaseImportRewrite
from py_backwards.utils.snippet import snippet

# Helper to parse source with typed_ast
def parse_source(src: str):
    return typed_ast.parse(src, mode="exec")

class DummyRewrite(BaseImportRewrite):
    rewrites = [("oldpkg", "newpkg")]

def test_get_matched_rewrite():
    tr = DummyRewrite()
    # Exact match
    assert tr._get_matched_rewrite("oldpkg") == ("oldpkg", "newpkg")
    # Submodule match
    assert tr._get_matched_rewrite("oldpkg.sub") == ("oldpkg", "newpkg")
    # No match
    assert tr._get_matched_rewrite("otherpkg") is None
    # None input
    assert tr._get_matched_rewrite(None) is None

def test_visit_import_rewrite(tmp_path):
    src = "import oldpkg\n"
    tree = parse_source(src)
    tr = DummyRewrite()
    tr.visit(tree)
    # The import should be replaced by a Try node
    assert isinstance(tree.body[0], typed_ast.Try)
    # The body of the Try should contain the new import
    new_import = tree.body[0].body[0]
    assert isinstance(new_import, typed_ast.Import)
    assert new_import.names[0].name == "newpkg"

def test_visit_importfrom_names_rewrite(tmp_path):
    src = "from oldpkg import foo, bar\n"
    tree = parse_source(src)
    tr = DummyRewrite()
    tr.visit(tree)
    # Should produce a Try node
    assert isinstance(tree.body[0], typed_ast.Try)
    # The new imports should be split into separate ImportFrom nodes
    new_imports = tree.body[0].body
    names = {node.names[0].name for node in new_imports}
    assert names == {"foo", "bar"}
    # Each ImportFrom should have module 'newpkg'
    for node in new_imports:
        assert isinstance(node, typed_ast.ImportFrom)
        assert node.module == "newpkg"
