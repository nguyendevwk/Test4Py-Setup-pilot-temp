import pytest
from pycg.machinery.imports import ImportManager, ImportManagerError

def test_import_manager_node_and_edge_creation():
    mgr = ImportManager()
    # create a node with a valid name
    node = mgr.create_node("pkg.main")
    assert node == {"filename": "", "imports": set()}
    # setting current module for edge creation
    mgr.set_current_mod("pkg.main", "main.py")
    # create a valid edge
    mgr.create_edge("pkg.sub")
    imports = mgr.get_imports("pkg.main")
    assert isinstance(imports, set) and "pkg.sub" in imports
    # attempting to create the same node again should raise
    with pytest.raises(ImportManagerError, match="Can't create a node a second time"):
        mgr.create_node("pkg.main")
    # creating a node with invalid name should raise
    with pytest.raises(ImportManagerError, match="Invalid node name"):
        mgr.create_node("")
    # creating an edge to a non-existent node should raise
    mgr.set_current_mod("pkg.nonexistent", "none.py")
    with pytest.raises(ImportManagerError, match="Can't add edge to a non existing node"):
        mgr.create_edge("pkg.other")
    # creating an edge with invalid destination should raise
    mgr.set_current_mod("pkg.main", "main.py")
    with pytest.raises(ImportManagerError, match="Invalid node name"):
        mgr.create_edge("")
