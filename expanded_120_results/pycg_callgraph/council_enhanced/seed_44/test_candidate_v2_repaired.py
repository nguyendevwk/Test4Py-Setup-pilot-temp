import pytest
from pycg.machinery.callgraph import CallGraph, CallGraphError

def test_callgraph_node_modname_update_when_empty():
    cg = CallGraph()

    # Adding a node with an empty modname stores the empty string
    cg.add_node("empty.mod", modname="")
    assert cg.get_modules()["empty.mod"] == ""

    # Adding the same node with a non‑empty modname updates it
    cg.add_node("empty.mod", modname="filled")
    assert cg.get_modules()["empty.mod"] == "filled"

    # Adding the node again with an empty modname does not overwrite the existing modname
    cg.add_node("empty.mod", modname="")
    assert cg.get_modules()["empty.mod"] == "filled"

    # Adding a node with a non‑string name raises CallGraphError
    with pytest.raises(CallGraphError, match="Only string node names allowed"):
        cg.add_node(123)

    # Adding a node with an empty string name raises CallGraphError
    with pytest.raises(CallGraphError, match="Empty node name"):
        cg.add_node("")
