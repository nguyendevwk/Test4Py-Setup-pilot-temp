import pytest
from pycg.machinery.callgraph import CallGraph, CallGraphError

def test_callgraph_basic_behavior():
    cg = CallGraph()

    # Adding invalid node names raises CallGraphError
    with pytest.raises(CallGraphError):
        cg.add_node(123)
    with pytest.raises(CallGraphError):
        cg.add_node("")

    # Add nodes with and without module names
    cg.add_node("a", "module_a")
    assert cg.get()["a"] == set()
    assert cg.get_modules()["a"] == "module_a"

    cg.add_node("b")
    assert cg.get()["b"] == set()
    assert cg.get_modules()["b"] == ""

    # Adding an edge auto‑adds missing nodes
    cg.add_edge("a", "b")
    assert "b" in cg.get()["a"]
    assert cg.get_edges() == [["a", "b"]]
    assert cg.get_modules() == {"a": "module_a", "b": ""}

    # Adding a new node via edge and updating module name
    cg.add_edge("a", "c")  # 'c' should be added automatically
    assert "c" in cg.get()
    assert cg.get_modules()["c"] == ""

    # Updating module name only if it was previously empty
    cg.add_node("b", "module_b")
    assert cg.get_modules()["b"] == "module_b"
    cg.add_node("a", "new_module")  # should not overwrite existing module name
    assert cg.get_modules()["a"] == "module_a"

    # Final edges list contains both edges
    assert sorted(cg.get_edges()) == sorted([["a", "b"], ["a", "c"]])
