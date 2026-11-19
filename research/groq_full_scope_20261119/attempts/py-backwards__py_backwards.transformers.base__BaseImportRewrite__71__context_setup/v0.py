import ast
import typed_ast.ast3 as typed_ast
import pytest
from py_backwards.transformers.base import BaseImportRewrite, TransformationResult

# Helper to parse source into typed_ast AST
def parse_source(src: str):
    return typed_ast.parse(src)

# Subclass with specific rewrites for testing
class TestImportRewrite(BaseImportRewrite):
    rewrites = [("oldpkg", "newpkg")]

def test_import_rewrite_changes_module_and_maintains_alias():
    src = "import oldpkg.submodule as sm"
    tree = parse_source(src)
    result = TestImportRewrite.transform(tree)
    # Tree should have changed
    assert result.changed is True
    # The root should be a Try node
    assert isinstance(result.tree.body[0], typed_ast.Try)
    # Inside the Try, the first statement is the original import
    original_import = result.tree.body[0].body[0]
    assert isinstance(original_import, typed_ast.Import)
    assert original_import.names[0].name == "oldpkg.submodule"
    # The second statement is the rewritten import
    rewritten_import = result.tree.body[0].orelse[0]
    assert isinstance(rewritten_import, typed_ast.Import)
    assert rewritten_import.names[0].name == "newpkg.submodule"
    # Alias should be preserved
    assert rewritten_import.names[0].asname == "sm"

def test_import_from_module_rewrite():
    src = "from oldpkg import module"
    tree = parse_source(src)
    result = TestImportRewrite.transform(tree)
    assert result.changed is True
    assert isinstance(result.tree.body[0], typed_ast.Try)
    # Original import
    original = result.tree.body[0].body[0]
    assert isinstance(original, typed_ast.ImportFrom)
    assert original.module == "oldpkg"
    # Rewritten import
    rewritten = result.tree.body[0].orelse[0]
    assert isinstance(rewritten, typed_ast.ImportFrom)
    assert rewritten.module == "newpkg"
    assert rewritten.names[0].name == "module"

def test_import_from_names_rewrite():
    src = "from oldpkg import a, b as bb, c"
    tree = parse_source(src)
    result = TestImportRewrite.transform(tree)
    assert result.changed is True
    assert isinstance(result.tree.body[0], typed_ast.Try)
    # The rewritten part should contain two ImportFrom nodes
    rewritten_parts = result.tree.body[0].orelse
    # There should be two ImportFrom nodes: one for a, one for b
    assert len(rewritten_parts) == 2
    modules = {node.module for node in rewritten_parts}
    # Both should be rewritten to newpkg
    assert modules == {"newpkg"}
    # Check that aliases are preserved
    names = [node.names[0].name for node in rewritten_parts]
    asnames = [node.names[0].asname for node in rewritten_parts]
    assert set(names) == {"a", "b"}
    assert set(asnames) == {"a", "bb"}
