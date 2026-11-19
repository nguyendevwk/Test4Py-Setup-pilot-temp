import os
import pytest
from pycg.machinery.imports import ImportManager, ImportManagerError


def test_handle_import_level_behavior():
    mgr = ImportManager()
    # Normal module path, not an __init__ file
    mgr.set_current_mod("pkg.subpkg.module", "module.py")
    # level 1: relative import one level up
    mod_name, package = mgr._handle_import_level("foo", 1)
    assert mod_name == ".foo"
    assert package == "pkg.subpkg"

    # level 0: absolute import
    mod_name, package = mgr._handle_import_level("bar", 0)
    assert mod_name == "bar"
    assert package == "pkg.subpkg.module"

    # __init__ file case: current module is a package
    mgr.set_current_mod("pkg.subpkg", os.path.join("pkg", "subpkg", "__init__.py"))
    mgr.input_file = os.path.abspath(os.path.join("pkg", "subpkg", "__init__.py"))
    mod_name, package = mgr._handle_import_level("baz", 1)
    assert mod_name == ".baz"
    assert package == "pkg"

    # level beyond top level raises ImportError
    mgr.set_current_mod("pkg", os.path.join("pkg", "__init__.py"))
    mgr.input_file = os.path.abspath(os.path.join("pkg", "__init__.py"))
    with pytest.raises(ImportError):
        mgr._handle_import_level("qux", 2)
