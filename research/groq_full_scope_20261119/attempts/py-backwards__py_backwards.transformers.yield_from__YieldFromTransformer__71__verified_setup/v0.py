import pytest
import typed_ast.ast3 as ast
from py_backwards.transformers.yield_from import YieldFromTransformer


def create_module_with_assign_yield_from():
    """Return an ast.Module whose body contains a single Assign with a YieldFrom."""
    assign = ast.Assign(
        targets=[ast.Name(id="x", ctx=ast.Store())],
        value=ast.YieldFrom(value=ast.Name(id="gen", ctx=ast.Load())),
    )
    return ast.Module(body=[assign], type_ignores=[])


def create_module_with_expr_yield_from():
    """Return an ast.Module whose body contains a single Expr with a YieldFrom."""
    expr = ast.Expr(
        value=ast.YieldFrom(value=ast.Name(id="gen", ctx=ast.Load())),
    )
    return ast.Module(body=[expr], type_ignores=[])


def test_get_yield_from_index_returns_correct_index():
    """_get_yield_from_index should return the index of the first Assign with a YieldFrom."""
    module = create_module_with_assign_yield_from()
    transformer = YieldFromTransformer()
    index = transformer._get_yield_from_index(module, ast.Assign)
    assert index == 0, "Expected the Assign with YieldFrom to be at index 0"


def test_handle_assignments_replaces_assign_with_yield_from_body():
    """_handle_assignments should replace an Assign containing YieldFrom with the body returned by _emulate_yield_from."""
    module = create_module_with_assign_yield_from()
    transformer = YieldFromTransformer()
    transformed = transformer._handle_assignments(module)
    # After handling, the body should no longer contain an Assign node
    assert all(not isinstance(node, ast.Assign) for node in transformed.body), \
        "Assign node with YieldFrom should have been replaced"
    # The tree_changed flag should be set to True
    assert transformer._tree_changed is True, "Tree change flag should be True after replacement"


def test_handle_expressions_replaces_expr_with_yield_from_body():
    """_handle_expressions should replace an Expr containing YieldFrom with the body returned by _emulate_yield_from."""
    module = create_module_with_expr_yield_from()
    transformer = YieldFromTransformer()
    transformed = transformer._handle_expressions(module)
    # After handling, the body should no longer contain an Expr node
    assert all(not isinstance(node, ast.Expr) for node in transformed.body), \
        "Expr node with YieldFrom should have been replaced"
    # The tree_changed flag should be set to True
    assert transformer._tree_changed is True, "Tree change flag should be True after replacement"
