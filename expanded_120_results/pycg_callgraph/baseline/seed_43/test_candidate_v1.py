import pytest
from pycg.machinery.callgraph import CallGraph

def test_callgraph_node_edge_and_module_tracking():
    cg = CallGraph()
    cg.add_node("A", "module_a")
    cg.add_node("B", "module_b")
    cg.add_edge("A", "B")
    cg.add_edge("B", "C")
    cg.add_node("C", "module_c")
    cg.add_node("A", "module_a2")  # should not override existing modname

    expected_adj = {"A": {"B"}, "B": {"C"}, "C": set()}
    assert cg.get() == expected_adj
    assert cg.get_modules() == {"A": "module_a", "B": "module_b", "C": "module_c"}
    assert sorted(cg.get_edges()) == [["A", "B"], ["B", "C"]]
