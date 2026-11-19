import pytest
from pycg.machinery.callgraph import CallGraph, CallGraphError

def test_add_edge_creates_nodes_and_edge_and_modnames():
    cg = CallGraph()
    # Adding an edge should create both nodes and the edge
    cg.add_edge('foo', 'bar')
    assert set(cg.get().keys()) == {'foo', 'bar'}
    assert cg.get()['foo'] == {'bar'}

    # Adding the same edge again should not duplicate it
    cg.add_edge('foo', 'bar')
    assert cg.get()['foo'] == {'bar'}

    # get_edges should reflect the single edge
    assert cg.get_edges() == [['foo', 'bar']]

    # Modnames for auto-added nodes default to empty strings
    assert cg.get_modules() == {'foo': '', 'bar': ''}

    # Adding a node with a module name
    cg.add_node('baz', 'module.baz')
    assert cg.get_modules()['baz'] == 'module.baz'

    # Adding the same node without a module name should preserve the existing name
    cg.add_node('baz')
    assert cg.get_modules()['baz'] == 'module.baz'

    # Adding the same node with an empty module name should not overwrite the existing name
    cg.add_node('baz', '')
    assert cg.get_modules()['baz'] == 'module.baz'
