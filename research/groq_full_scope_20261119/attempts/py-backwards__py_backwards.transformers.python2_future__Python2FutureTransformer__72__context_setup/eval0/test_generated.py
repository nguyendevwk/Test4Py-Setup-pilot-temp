import ast
import pytest
from typed_ast import ast3 as typed_ast
from py_backwards.transformers.python2_future import Python2FutureTransformer

def test_target_attribute():
    """The transformer should target Python 2.7."""
    assert Python2FutureTransformer.target == (2, 7)

def test_visit_module_sets_tree_changed_flag(tmp_path):
    """visit_Module should set the _tree_changed flag to True."""
    transformer = Python2FutureTransformer()
    # Create a minimal module node
    module = typed_ast.Module(body=[], type_ignores=[])
    # Ensure flag is False before visiting
    assert not getattr(transformer, "_tree_changed", False)
    transformer.visit_Module(module)
    # After visiting, flag should be True
    assert transformer._tree_changed is True

def test_visit_module_inserts_future_imports(tmp_path):
    """visit_Module should prepend the module body with future imports."""
    transformer = Python2FutureTransformer()
    # Create a module with a single pass statement
    pass_stmt = typed_ast.Pass()
    module = typed_ast.Module(body=[pass_stmt], type_ignores=[])
    # Visit the module
    transformer.visit_Module(module)
    # The first four nodes should be ImportFrom nodes for __future__ imports
    import_nodes = module.body[:4]
    import_names = [node.names[0].name for node in import_nodes]
    expected = [
        "absolute_import",
        "division",
        "print_function",
        "unicode_literals",
    ]
    assert import_names == expected
    # The last node should be the original pass statement
    assert module.body[-1] is pass_stmt
