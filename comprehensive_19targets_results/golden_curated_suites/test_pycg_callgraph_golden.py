import pytest
from pycg.machinery.callgraph import CallGraph, CallGraphError

def test_callgraph_behavior():
    cg = CallGraph()

    # Adding nodes with and without module names
    cg.add_node("a", "mod_a")
    cg.add_node("b")  # default empty modname
    assert cg.get() == {"a": set(), "b": set()}
    assert cg.get_modules() == {"a": "mod_a", "b": ""}

    # Adding duplicate node should not overwrite existing modname
    cg.add_node("a", "new_mod")
    assert cg.get_modules()["a"] == "mod_a"

    # Adding node with empty modname after existing node with empty modname
    cg.add_node("b", "mod_b")
    assert cg.get_modules()["b"] == "mod_b"

    # Adding edge creates nodes automatically
    cg.add_edge("a", "c")
    assert "c" in cg.get()
    assert cg.get()["a"] == {"c"}

    # Edge addition should not duplicate edges
    cg.add_edge("a", "c")
    assert cg.get()["a"] == {"c"}

    # get_edges returns list of [src, dst] pairs
    edges = cg.get_edges()
    assert ["a", "c"] in edges
    assert len(edges) == 1

    # Error conditions
    with pytest.raises(CallGraphError, match="Only string node names allowed"):
        cg.add_node(123)
    with pytest.raises(CallGraphError, match="Empty node name"):
        cg.add_node("")
