import os
import pytest
from pycg.machinery.imports import ImportManager, ImportManagerError


def test_handle_import_level_behavior():
    mgr = ImportManager()

    # Normal case: non-init file, level 1
    mgr.set_current_mod("pkg.subpkg.module", "/tmp/pkg/subpkg/module.py")
    mod_name, package = mgr._handle_import_level("submodule", 1)
    assert mod_name == ".submodule"
    assert package == "pkg.subpkg"

    # Edge case: level 0 (no relative dots)
    mod_name, package = mgr._handle_import_level("submodule", 0)
    assert mod_name == "submodule"
    assert package == "pkg.subpkg.module"

    # Init file special handling: level > 1
    mgr.set_current_mod("pkg.subpkg", "/tmp/pkg/subpkg/__init__.py")
    mod_name, package = mgr._handle_import_level("module", 2)
    # For an __init__ file, level 2 becomes level 1 after adjustment
    assert mod_name == "..module"
    assert package == "pkg"

    # Init file special handling: level == 1
    mod_name, package = mgr._handle_import_level("module", 1)
    assert mod_name == ".module"
    assert package == "pkg.subpkg"

    # Error case: level beyond package depth
    mgr.set_current_mod("pkg.subpkg", "/tmp/pkg/subpkg/__init__.py")
    with pytest.raises(ImportError):
        mgr._handle_import_level("module", 3)
