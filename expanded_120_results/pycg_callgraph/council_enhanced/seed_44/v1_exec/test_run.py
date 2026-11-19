import pytest
from pycg.machinery.callgraph import CallGraph, CallGraphError

def test_callgraph_add_node_behavior():
    cg = CallGraph()

    # Adding a non‑string node name raises an error
    with pytest.raises(CallGraphError, match="Only string node names allowed"):
        cg.add_node(123)

    # Adding an empty string node name raises an error
    with pytest.raises(CallGraphError, match="Empty node name"):
        cg.add_node("")

    # Valid node addition creates an entry with an empty set and stores the modname
    cg.add_node("module.func", modname="module")
    assert "module.func" in cg.get()
    assert cg.get()["module.func"] == set()
    assert cg.get_modules()["module.func"] == "module"

    # Adding the same node again with an empty modname does not overwrite the existing modname
    cg.add_node("module.func", modname="")
    assert cg.get_modules()["module.func"] == "module"

    # Adding the same node again with a new modname when the previous modname is empty updates it
    cg.add_node("new.module", modname="old")
    cg.add_node("new.module", modname="new")
    assert cg.get_modules()["new.module"] == "new"

    # Adding a node that already exists but with a different modname when the existing modname is empty
    cg.add_node("empty.mod", modname="")
    cg.add_node("empty.mod", modname="filled")
    assert cg.get_modules()["empty.mod"] == "filled"
