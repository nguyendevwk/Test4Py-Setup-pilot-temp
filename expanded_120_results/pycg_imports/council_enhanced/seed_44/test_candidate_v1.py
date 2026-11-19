import pytest
from pycg.machinery.imports import ImportManager


def test_create_edge_adds_import_to_current_module():
    """Verify that create_edge correctly records an import for the current module."""
    mgr = ImportManager()

    # Create a node and set it as the current module.
    mgr.create_node("pkg.main")
    mgr.set_current_mod("pkg.main", "main.py")

    # Add an import edge from the current module to another module.
    mgr.create_edge("pkg.submodule")

    # The imports set for the current module should now contain the new edge.
    imports = mgr.get_imports("pkg.main")
    assert isinstance(imports, set), "Imports should be a set"
    assert "pkg.submodule" in imports, "The new import should be recorded"
