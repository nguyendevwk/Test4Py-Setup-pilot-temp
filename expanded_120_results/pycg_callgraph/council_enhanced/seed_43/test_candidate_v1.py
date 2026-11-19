import pytest
from pycg.machinery.callgraph import CallGraph, CallGraphError

def test_callgraph_node_and_edge_behavior():
    cg = CallGraph()

    # Add a valid node with a module name
    cg.add_node('a', 'module_a')
    assert cg.get()['a'] == set()
    assert cg.get_modules()['a'] == 'module_a'

    # Adding the same node again with a different module name should not overwrite
    cg.add_node('a', 'module_b')
    assert cg.get_modules()['a'] == 'module_a'

    # Adding an edge creates the destination node automatically
    cg.add_edge('a', 'b')
    assert 'b' in cg.get()
    assert cg.get()['a'] == {'b'}

    # Adding the same edge again should not duplicate
    cg.add_edge('a', 'b')
    assert cg.get()['a'] == {'b'}

    # get_edges returns a list of [src, dst] pairs
    edges = cg.get_edges()
    assert ['a', 'b'] in edges
    assert len(edges) == 1

    # Invalid node names raise CallGraphError
    with pytest.raises(CallGraphError):
        cg.add_node(123)
    with pytest.raises(CallGraphError):
        cg.add_node('')
