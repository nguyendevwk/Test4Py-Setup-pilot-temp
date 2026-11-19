import pytest
from pycg.machinery.callgraph import CallGraph, CallGraphError

def test_callgraph_behavior():
    cg = CallGraph()
    # add_node valid
    cg.add_node('node1', 'module1')
    assert 'node1' in cg.get()
    assert cg.get()['node1'] == set()
    assert cg.get_modules()['node1'] == 'module1'
    # adding same node with different modname should not overwrite
    cg.add_node('node1', 'module2')
    assert cg.get_modules()['node1'] == 'module1'
    # error on empty name
    with pytest.raises(CallGraphError):
        cg.add_node('')
    # error on non-string
    with pytest.raises(CallGraphError):
        cg.add_node(123)
    # add_edge auto-adds nodes
    cg.add_edge('node1', 'node2')
    assert 'node2' in cg.get()
    assert 'node2' in cg.get_modules()
    assert cg.get()['node1'] == {'node2'}
    # get_edges
    edges = cg.get_edges()
    assert ['node1', 'node2'] in edges
    # get_modules returns mapping
    modules = cg.get_modules()
    assert modules['node1'] == 'module1'
    assert modules['node2'] == ''
