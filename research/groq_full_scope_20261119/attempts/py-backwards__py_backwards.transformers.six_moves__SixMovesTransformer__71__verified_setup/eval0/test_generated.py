import ast
import typed_ast.ast3 as typed_ast
import pytest

from py_backwards.transformers.six_moves import SixMovesTransformer


def _parse_and_transform(source: str) -> typed_ast.Module:
    """Parse source with typed_ast and apply SixMovesTransformer."""
    tree = typed_ast.parse(source)
    transformer = SixMovesTransformer()
    transformer.visit(tree)
    return tree


def _get_import_from_modules(tree: typed_ast.Module):
    """Return a list of module names from ImportFrom nodes in the tree."""
    return [
        node.module
        for node in ast.walk(tree)
        if isinstance(node, typed_ast.ImportFrom)
    ]


def test_rewrites_moved_module_import():
    """
    Verify that an import of a module that has moved to six.moves
    is rewritten to use six.moves.<module>.
    """
    source = "from cStringIO import StringIO\n"
    tree = _parse_and_transform(source)
    modules = _get_import_from_modules(tree)
    assert modules == ["six.moves.cStringIO"]


def test_no_rewrite_for_non_moved_module():
    """
    Verify that imports of modules that are not moved remain unchanged.
    """
    source = "from collections import defaultdict\n"
    tree = _parse_and_transform(source)
    modules = _get_import_from_modules(tree)
    assert modules == ["collections"]


def test_rewrite_with_alias_and_multiple_imports():
    """
    Verify that multiple imports from the same moved module are all rewritten,
    and that aliasing is preserved.
    """
    source = (
        "from cStringIO import StringIO as SI\n"
        "from cStringIO import BytesIO\n"
    )
    tree = _parse_and_transform(source)
    modules = _get_import_from_modules(tree)
    assert modules == ["six.moves.cStringIO", "six.moves.cStringIO"]
    # Check that aliases are preserved
    names = [
        (node.names[0].name, node.names[0].asname)
        for node in ast.walk(tree)
        if isinstance(node, typed_ast.ImportFrom)
    ]
    assert names == [("StringIO", "SI"), ("BytesIO", None)]
