import pytest
from pycg.machinery.imports import ImportManager, ImportManagerError

def test_create_node_valid_and_errors():
    mgr = ImportManager()

    # Invalid names should raise ImportManagerError
    with pytest.raises(ImportManagerError):
        mgr.create_node(None)
    with pytest.raises(ImportManagerError):
        mgr.create_node(123)

    # Valid node creation
    node = mgr.create_node("module1")
    assert node == {"filename": "", "imports": set()}
    assert mgr.get_node("module1") is node

    # Duplicate node creation should raise ImportManagerError
    with pytest.raises(ImportManagerError):
        mgr.create_node("module1")
