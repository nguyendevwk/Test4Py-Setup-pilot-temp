import pytest
from pycg.machinery.imports import ImportManager, ImportManagerError


def test_import_manager_create_node_and_edge_behavior():
    mgr = ImportManager()

    # create_node should raise for invalid names
    with pytest.raises(ImportManagerError):
        mgr.create_node(None)
    with pytest.raises(ImportManagerError):
        mgr.create_node(123)

    # create_node should succeed for a valid name
    node = mgr.create_node("pkg.module")
    assert node == {"filename": "", "imports": set()}
    assert mgr.get_node("pkg.module") is node

    # duplicate node creation should raise
    with pytest.raises(ImportManagerError):
        mgr.create_node("pkg.module")

    # create_edge should raise if current module not set
    with pytest.raises(ImportManagerError):
        mgr.create_edge("other.module")

    # set current module to an existing node
    mgr.set_current_mod("pkg.module", "dummy.py")

    # create_edge should raise for invalid dest
    with pytest.raises(ImportManagerError):
        mgr.create_edge(None)
    with pytest.raises(ImportManagerError):
        mgr.create_edge(456)

    # create_edge should add dest to imports set
    mgr.create_edge("other.module")
    assert "other.module" in mgr.get_node("pkg.module")["imports"]

    # get_node should return None for non-existent node
    assert mgr.get_node("nonexistent") is None
