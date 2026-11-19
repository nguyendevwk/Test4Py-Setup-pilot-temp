import pytest
from pycg.machinery.imports import ImportManager, ImportManagerError

def test_import_manager_node_and_edge_creation_and_errors():
    mgr = ImportManager()

    # Valid node creation
    node = mgr.create_node("moduleA")
    assert node == {"filename": "", "imports": set()}
    assert mgr.get_node("moduleA") is node

    # Duplicate node creation raises error
    with pytest.raises(ImportManagerError):
        mgr.create_node("moduleA")

    # Invalid node names raise error
    for bad_name in (None, "", 123):
        with pytest.raises(ImportManagerError):
            mgr.create_node(bad_name)

    # Set current module and create an edge
    mgr.set_current_mod("moduleA", "moduleA.py")
    mgr.create_edge("moduleB")
    assert "moduleB" in mgr.get_node("moduleA")["imports"]

    # Edge creation with invalid destination names raises error
    for bad_dest in (None, "", 456):
        with pytest.raises(ImportManagerError):
            mgr.create_edge(bad_dest)

    # Edge creation when current module node does not exist raises error
    mgr.set_current_mod("moduleC", "moduleC.py")
    with pytest.raises(ImportManagerError):
        mgr.create_edge("moduleD")
