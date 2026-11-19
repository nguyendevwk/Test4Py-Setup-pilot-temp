import pytest
from pycg.machinery.imports import ImportManager, ImportManagerError


def test_create_node_invalid_and_duplicate():
    manager = ImportManager()

    # Invalid name: None
    with pytest.raises(ImportManagerError, match="Invalid node name"):
        manager.create_node(None)

    # Invalid name: non-string
    with pytest.raises(ImportManagerError, match="Invalid node name"):
        manager.create_node(123)

    # Valid creation
    node = manager.create_node("foo")
    assert isinstance(node, dict)
    assert node == {"filename": "", "imports": set()}

    # Duplicate creation should raise
    with pytest.raises(ImportManagerError, match="Can't create a node a second time"):
        manager.create_node("foo")
