import ast
import typed_ast.ast3 as typed_ast
import pytest
from py_backwards.transformers.python2_future import Python2FutureTransformer
from py_backwards.utils.snippet import snippet

def parse_source(src: str) -> typed_ast.Module:
    """Parse source code into a typed_ast Module node."""
    return typed_ast.parse(src)

def test_imports_added_to_empty_module(tmp_path):
    """The transformer should prepend the required __future__ imports to an empty module."""
    src = ""
    tree = parse_source(src)
    transformer = Python2FutureTransformer()
    transformer.visit(tree)
    # The first four statements should be the future imports
    import_names = [stmt.names[0].name for stmt in tree.body[:4]]
    expected = [
        "__future__.absolute_import",
        "__future__.division",
        "__future__.print_function",
        "__future__.unicode_literals",
    ]
    assert import_names == expected
    # No other statements should be present
    assert len(tree.body) == 4

def test_existing_content_preserved(tmp_path):
    """Existing module content should remain after the imports are added."""
    src = "def foo():\n    return 42\n"
    tree = parse_source(src)
    transformer = Python2FutureTransformer()
    transformer.visit(tree)
    # The function definition should be the fifth statement
    assert isinstance(tree.body[4], typed_ast.FunctionDef)
    assert tree.body[4].name == "foo"
    # The function body should be unchanged
    assert isinstance(tree.body[4].body[0], typed_ast.Return)
    assert tree.body[4].body[0].value.n == 42

def test_snippet_output_includes_imports(tmp_path):
    """The snippet helper should produce source code that includes the future imports."""
    src = "x = 1\n"
    tree = parse_source(src)
    transformer = Python2FutureTransformer()
    transformer.visit(tree)
    code = snippet(tree)
    # The snippet should start with the future imports
    assert code.startswith(
        "from __future__ import absolute_import\n"
        "from __future__ import division\n"
        "from __future__ import print_function\n"
        "from __future__ import unicode_literals\n"
    )
    # The original code should still be present
    assert "x = 1" in code
