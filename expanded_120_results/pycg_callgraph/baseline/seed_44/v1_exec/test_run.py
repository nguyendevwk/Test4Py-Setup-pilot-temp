import pytest
from pycg.machinery.callgraph import CallGraph, CallGraphError

def test_callgraph_add_edge_and_nodes_and_errors():
    cg = CallGraph()
    # add edge creates nodes
    cg.add_edge('a', 'b')
    assert cg.get() == {'a': {'b'}, 'b': set()}
    assert cg.get_edges() == [['a', 'b']]
    assert cg.get_modules() == {'a': '', 'b': ''}

    # add node with module names
    cg.add_node('a', 'module1')
    cg.add_node('b', 'module2')
    cg.add_node('c', 'module3')
    assert cg.get_modules() == {'a': 'module1', 'b': 'module2', 'c': 'module3'}

    # add another edge
    cg.add_edge('c', 'a')
    assert ['c', 'a'] in cg.get_edges()
    assert cg.get()['c'] == {'a'}

    # errors
    with pytest.raises(CallGraphError):
        cg.add_node('', 'mod')
    with pytest.raises(CallGraphError):
        cg.add_node(123, 'mod')
    # ensure modname unchanged when adding node without modname
    cg.add_node('a')
    assert cg.get_modules()['a'] == 'module1'
