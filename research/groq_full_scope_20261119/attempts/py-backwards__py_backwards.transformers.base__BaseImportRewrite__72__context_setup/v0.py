import ast
import typed_ast.ast3 as typed_ast
import pytest
from py_backwards.transformers.base import BaseImportRewrite, BaseNodeTransformer, import_rewrite
from py_backwards.types import TransformationResult

# Helper transformer that defines specific rewrites
class TestImportRewrite(BaseImportRewrite):
    rewrites = [("oldpkg", "newpkg")]


def test_simple_import_rewrite(tmp_path):
    """Verify that a plain import is rewritten with a try/except wrapper."""
    source = "import oldpkg\n"
    tree = typed_ast.parse(source)
    transformer = TestImportRewrite(tree)
    transformer.visit(tree)

    # The tree should have changed
    assert transformer._tree_changed is True

    # The root should now be a Try node (import_rewrite returns a Try)
    assert isinstance(tree, typed_ast.Try)

    # The body of the Try should contain the original import
    original_import = tree.body[0]
    assert isinstance(original_import, typed_ast.Import)
    assert original_import.names[0].name == "oldpkg"

    # The except handler should contain the rewritten import
    except_handler = tree.handlers[0]
    rewritten_import = except_handler.body[0]
    assert isinstance(rewritten_import, typed_ast.Import)
    assert rewritten_import.names[0].name == "newpkg"


def test_import_from_rewrite(tmp_path):
    """Verify that an import-from statement is rewritten correctly."""
    source = "from oldpkg import foo\n"
    tree = typed_ast.parse(source)
    transformer = TestImportRewrite(tree)
    transformer.visit(tree)

    assert transformer._tree_changed is True
    assert isinstance(tree, typed_ast.Try)

    # Original import-from in the try body
    original_import_from = tree.body[0]
    assert isinstance(original_import_from, typed_ast.ImportFrom)
    assert original_import_from.module == "oldpkg"

    # Except handler contains rewritten import-from
    except_handler = tree.handlers[0]
    rewritten_import_from = except_handler.body[0]
    assert isinstance(rewritten_import_from, typed_ast.ImportFrom)
    assert rewritten_import_from.module == "newpkg"


def test_no_rewrite(tmp_path):
    """Verify that imports not matching rewrites are left untouched."""
    source = "import otherpkg\n"
    tree = typed_ast.parse(source)
    transformer = TestImportRewrite(tree)
    transformer.visit(tree)

    # No changes should have been made
    assert transformer._tree_changed is False
    # The root node remains a Module with a single Import
    assert isinstance(tree, typed_ast.Module)
    assert len(tree.body) == 1
    assert isinstance(tree.body[0], typed_ast.Import)
    assert tree.body[0].names[0].name == "otherpkg"
