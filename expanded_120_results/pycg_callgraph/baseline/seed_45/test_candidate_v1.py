from pycg.machinery.callgraph import CallGraph, CallGraphError
import pytest

def test_add_edge_auto_nodes_and_get_edges():
    cg = CallGraph()
    cg.add_edge('a', 'b')
    assert set(cg.get()) == {'a', 'b'}
    assert cg.get()['a'] == {'b'}
    assert cg.get()['b'] == set()
    assert cg.get_modules() == {'a': '', 'b': ''}

    cg.add_edge('a', 'c')
    assert cg.get()['a'] == {'b', 'c'}
    assert cg.get()['c'] == set()

    edges = cg.get_edges()
    assert sorted(edges) == [['a', 'b'], ['a', 'c']]

    cg.add_edge('a', 'b')
    assert cg.get()['a'] == {'b', 'c'}

    with pytest.raises(CallGraphError):
        cg.add_edge('a', 123)
