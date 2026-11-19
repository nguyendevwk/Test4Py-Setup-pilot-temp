import ast
import typed_ast.ast3 as typed_ast
import pytest

from py_backwards.transformers.python2_future import Python2FutureTransformer
from py_backwards.utils.snippet import snippet


def test_target_attribute():
    """The transformer should expose the correct target tuple."""
    assert Python2FutureTransformer.target == (2, 7)


def test_visit_module_adds_future_imports(tmp_path):
    """visit_Module should prepend the required __future__ imports."""
    # Create a simple module with a single function definition
    source = "def foo():\n    return 42\n"
    module_node = snippet(source)

    transformer = Python2FutureTransformer()
    transformed = transformer.visit(module_node)

    # The first four statements should be the future imports
    import_names = [
        (stmt.value.args[0].s, stmt.value.args[1].s)
        for stmt in transformed.body[:4]
        if isinstance(stmt, typed_ast.ImportFrom)
    ]

    expected = [
        ("__future__", "absolute_import"),
        ("__future__", "division"),
        ("__future__", "print_function"),
        ("__future__", "unicode_literals"),
    ]
    assert import_names == expected

    # The remaining body should contain the original function definition
    remaining_body = transformed.body[4:]
    assert len(remaining_body) == 1
    assert isinstance(remaining_body[0], typed_ast.FunctionDef)
    assert remaining_body[0].name == "foo"


def test_visit_module_with_existing_imports(tmp_path):
    """If the module already contains future imports, they are duplicated."""
    # Module with an existing future import
    source = (
        "from __future__ import division\n"
        "def bar():\n    return 1\n"
    )
    module_node = snippet(source)

    transformer = Python2FutureTransformer()
    transformed = transformer.visit(module_node)

    # Count how many division imports exist
    division_imports = [
        stmt
        for stmt in transformed.body
        if isinstance(stmt, typed_ast.ImportFrom)
        and stmt.module == "__future__"
        and any(arg.s == "division" for arg in stmt.value.args)
    ]
    # Should be two: one added by transformer, one original
    assert len(division_imports) == 2
