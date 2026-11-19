import os
import pytest
from pycg.machinery.imports import ImportManager, ImportManagerError


def test_create_node_and_edge_behavior():
    mgr = ImportManager()
    mgr.set_pkg("/tmp")  # dummy package directory

    # Valid node creation
    node = mgr.create_node("module1")
    assert isinstance(node, dict)
    assert node["filename"] == ""
    assert node["imports"] == set()

    # Duplicate node creation raises error
    with pytest.raises(ImportManagerError, match="Can't create a node a second time"):
        mgr.create_node("module1")

    # Invalid node name raises error
    with pytest.raises(ImportManagerError, match="Invalid node name"):
        mgr.create_node(None)

    # Edge creation requires a current module
    mgr.set_current_mod("module1", "dummy.py")
    # Valid edge creation
    mgr.create_edge("module2")
    assert "module2" in mgr.get_node("module1")["imports"]

    # Edge creation with invalid destination raises error
    with pytest.raises(ImportManagerError, match="Invalid node name"):
        mgr.create_edge(None)

    # Edge creation when current module node does not exist raises error
    mgr.set_current_mod("nonexistent", "dummy.py")
    with pytest.raises(ImportManagerError, match="Can't add edge to a non existing node"):
        mgr.create_edge("module3")

    # get_imports returns set of imports or empty list for unknown module
    imports = mgr.get_imports("module1")
    assert isinstance(imports, set)
    assert imports == {"module2"}
    assert mgr.get_imports("unknown") == []
