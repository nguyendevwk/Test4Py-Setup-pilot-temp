import os
import pytest
from pycg.machinery.imports import ImportManager, ImportManagerError

def test_import_manager_node_and_edge_creation_and_errors():
    mgr = ImportManager()

    # Valid node creation
    node_name = "pkg.module"
    node = mgr.create_node(node_name)
    assert isinstance(node, dict)
    assert node["filename"] == ""
    assert node["imports"] == set()

    # Duplicate node creation should raise
    with pytest.raises(ImportManagerError, match="Can't create a node a second time"):
        mgr.create_node(node_name)

    # Invalid node names should raise
    for bad_name in (None, 123, ""):
        with pytest.raises(ImportManagerError, match="Invalid node name"):
            mgr.create_node(bad_name)

    # Set current module to the node we just created
    mgr.set_current_mod(node_name, __file__)

    # Valid edge creation
    dest_name = "pkg.other"
    mgr.create_edge(dest_name)
    assert dest_name in mgr.get_imports(node_name)

    # Edge creation with invalid dest should raise
    for bad_dest in (None, 456, ""):
        with pytest.raises(ImportManagerError, match="Invalid node name"):
            mgr.create_edge(bad_dest)

    # Edge creation when current module node does not exist should raise
    mgr.set_current_mod("nonexistent.module", __file__)
    with pytest.raises(ImportManagerError, match="Can't add edge to a non existing node"):
        mgr.create_edge("some.dest")
