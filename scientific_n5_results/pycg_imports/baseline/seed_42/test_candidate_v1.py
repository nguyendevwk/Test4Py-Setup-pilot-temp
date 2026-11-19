import pytest
from pycg.machinery.imports import ImportManager, ImportManagerError
import os

def test_import_manager_node_and_edge_creation():
    mgr = ImportManager()

    # create_node should reject non-string names
    with pytest.raises(ImportManagerError):
        mgr.create_node(123)

    # create_node with a valid name
    node = mgr.create_node("pkg.module")
    assert node == {"filename": "", "imports": set()}

    # duplicate node creation should raise an error
    with pytest.raises(ImportManagerError):
        mgr.create_node("pkg.module")

    # get_node should return the same node
    assert mgr.get_node("pkg.module") is node

    # create_edge should reject non-string destinations
    mgr.set_current_mod("pkg.module", "dummy.py")
    with pytest.raises(ImportManagerError):
        mgr.create_edge(123)

    # create_edge when the current node exists should add the destination
    mgr.create_edge("other.module")
    assert "other.module" in node["imports"]

    # create_edge should raise an error if the current node does not exist
    mgr2 = ImportManager()
    mgr2.set_current_mod("missing.module", "missing.py")
    with pytest.raises(ImportManagerError):
        mgr2.create_edge("dest.module")
