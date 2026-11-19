import pytest
from pycg.machinery.callgraph import CallGraph, CallGraphError

def test_callgraph_basic():
    cg = CallGraph()

    # Add a node with a module name
    cg.add_node('a', 'mod1')
    assert 'a' in cg.get()
    assert cg.get()['a'] == set()
    assert cg.get_modules()['a'] == 'mod1'

    # Adding the same node again with a different module name should not overwrite
    cg.add_node('a', 'mod2')
    assert cg.get_modules()['a'] == 'mod1'

    # Add an edge; this should implicitly add the destination node
    cg.add_edge('a', 'b')
    assert 'b' in cg.get()
    assert cg.get()['a'] == {'b'}

    # Verify edges list
    edges = cg.get_edges()
    assert ['a', 'b'] in edges

    # Destination node should have an empty module name
    assert cg.get_modules()['b'] == ''

    # Error handling: non-string node name
    with pytest.raises(CallGraphError):
        cg.add_node(123)

    # Error handling: empty node name
    with pytest.raises(CallGraphError):
        cg.add_node('')

    # Ensure graph state unchanged after errors
    assert '123' not in cg.get()
    assert '' not in cg.get()
