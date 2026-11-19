import os
import pytest
from pycg.machinery.imports import ImportManager, ImportManagerError


def test_import_manager_node_and_edge_and_handle_import_level():
    mgr = ImportManager()

    # create_node should reject invalid names
    with pytest.raises(ImportManagerError):
        mgr.create_node(None)
    with pytest.raises(ImportManagerError):
        mgr.create_node("")

    # create_node with a valid name
    node = mgr.create_node("pkg.sub")
    assert node == {"filename": "", "imports": set()}
    # duplicate creation raises error
    with pytest.raises(ImportManagerError):
        mgr.create_node("pkg.sub")

    # create_edge before node exists should raise error
    with pytest.raises(ImportManagerError):
        mgr.create_edge("dest")

    # create edge after node exists
    mgr.set_current_mod("pkg.sub", "/tmp/pkg/sub/__init__.py")
    mgr.create_edge("dest")
    assert "dest" in mgr.get_imports("pkg.sub")

    # _handle_import_level with init file
    mgr.set_current_mod("pkg.sub", "/tmp/pkg/sub/__init__.py")
    mod_name, package = mgr._handle_import_level("module", 1)
    assert mod_name == ".module"
    assert package == "pkg"

    # level beyond package depth raises ImportError
    with pytest.raises(ImportError):
        mgr._handle_import_level("module", 3)

    # _handle_import_level with non-init file
    mgr.set_current_mod("pkg.sub", "/tmp/pkg/sub/file.py")
    mod_name, package = mgr._handle_import_level("module", 1)
    assert mod_name == ".module"
    assert package == "pkg"

    # level equal to package depth on non-init file
    mod_name, package = mgr._handle_import_level("module", 2)
    assert mod_name == "..module"
    assert package == ""

    # get_imports returns empty list for unknown module
    assert mgr.get_imports("unknown") == []

    # get_imports returns set of imports for known module
    assert mgr.get_imports("pkg.sub") == {"dest"}
