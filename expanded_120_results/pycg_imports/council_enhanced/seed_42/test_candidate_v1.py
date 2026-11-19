import pytest
from pycg.machinery.imports import ImportManager, ImportManagerError

def test_create_node_and_edge_behavior():
    mgr = ImportManager()
    # valid node creation
    node = mgr.create_node("pkg.main")
    assert node == {"filename": "", "imports": set()}
    # duplicate node raises
    with pytest.raises(ImportManagerError):
        mgr.create_node("pkg.main")
    # invalid name raises
    with pytest.raises(ImportManagerError):
        mgr.create_node("")
    # set current module
    mgr.set_current_mod("pkg.main", "main.py")
    # valid edge creation
    mgr.create_edge("pkg.other")
    assert "pkg.other" in mgr.get_imports("pkg.main")
    # edge with invalid dest
    with pytest.raises(ImportManagerError):
        mgr.create_edge("")
    # edge when node missing
    mgr2 = ImportManager()
    mgr2.set_current_mod("pkg.missing", "missing.py")
    with pytest.raises(ImportManagerError):
        mgr2.create_edge("pkg.other")
