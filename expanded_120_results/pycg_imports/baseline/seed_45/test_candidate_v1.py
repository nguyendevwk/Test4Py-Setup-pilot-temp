import os
import pytest
from pycg.machinery.imports import ImportManager, ImportManagerError

def test_import_manager_node_and_edge_creation_and_errors():
    mgr = ImportManager()

    # create_node with invalid name should raise ImportManagerError
    with pytest.raises(ImportManagerError):
        mgr.create_node(None)
    with pytest.raises(ImportManagerError):
        mgr.create_node("")

    # create_node with valid name
    node = mgr.create_node("module1")
    assert node == {"filename": "", "imports": set()}
    # duplicate node creation should raise ImportManagerError
    with pytest.raises(ImportManagerError):
        mgr.create_node("module1")

    # create_edge before setting current module should raise ImportManagerError
    with pytest.raises(ImportManagerError):
        mgr.create_edge("module2")

    # set current module and create edge
    mgr.set_current_mod("module1", __file__)
    mgr.create_edge("module2")
    imports = mgr.get_imports("module1")
    assert "module2" in imports

    # create_edge with invalid dest should raise ImportManagerError
    with pytest.raises(ImportManagerError):
        mgr.create_edge("")
