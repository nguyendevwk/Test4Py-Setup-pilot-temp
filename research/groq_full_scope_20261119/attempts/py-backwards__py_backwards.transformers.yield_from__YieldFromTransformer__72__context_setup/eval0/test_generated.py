import pytest
import typed_ast.ast3 as ast
from py_backwards.transformers.yield_from import YieldFromTransformer
from py_backwards.utils.tree import insert_at

# Helper to create a simple module with a yield from inside an assignment
def make_module_with_yield_from():
    # a = (yield from iterable)
    assign = ast.Assign(
        targets=[ast.Name(id='a', ctx=ast.Store())],
        value=ast.YieldFrom(value=ast.Name(id='iterable', ctx=ast.Load()))
    )
    return ast.Module(body=[assign], type_ignores=[])

# Helper to create a simple module with a yield from inside an expression
def make_module_with_yield_from_expr():
    # yield from iterable
    expr = ast.Expr(value=ast.YieldFrom(value=ast.Name(id='iterable', ctx=ast.Load())))
    return ast.Module(body=[expr], type_ignores=[])

def test_get_yield_from_index_finds_assignment():
    module = make_module_with_yield_from()
    transformer = YieldFromTransformer()
    # _get_yield_from_index should return 0 for the assignment
    index = transformer._get_yield_from_index(module, ast.Assign)
    assert index == 0, "Expected to find YieldFrom in the first body element"

def test_visit_removes_yield_from_nodes():
    module = make_module_with_yield_from()
    transformer = YieldFromTransformer()
    transformed = transformer.visit(module)
    # After transformation, there should be no YieldFrom nodes in the tree
    yield_from_nodes = [node for node in ast.walk(transformed) if isinstance(node, ast.YieldFrom)]
    assert not yield_from_nodes, "YieldFrom nodes should be removed after transformation"

def test_handle_assignments_replaces_assignment_with_yield_from_body():
    module = make_module_with_yield_from()
    transformer = YieldFromTransformer()
    # Capture original body length
    original_len = len(module.body)
    # Apply assignment handling
    transformed = transformer._handle_assignments(module)
    # After handling, the original assignment should be removed
    assert len(transformed.body) == original_len, "Body length should remain the same after replacement"
    # The first element should no longer be an Assign node
    assert not isinstance(transformed.body[0], ast.Assign), "Assign node should be replaced"
    # There should be no YieldFrom nodes in the transformed body
    yield_from_nodes = [node for node in ast.walk(transformed) if isinstance(node, ast.YieldFrom)]
    assert not yield_from_nodes, "YieldFrom nodes should be replaced by other statements"
