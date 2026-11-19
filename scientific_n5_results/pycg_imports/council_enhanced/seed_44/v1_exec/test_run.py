import os
import pytest
from pycg.machinery.imports import ImportManager, ImportManagerError
from pycg.machinery import utils

def test_import_manager_handle_import_and_graph(tmp_path):
    # Create a minimal package structure
    pkg_dir = tmp_path / "pkg"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("")
    (pkg_dir / "main.py").write_text("")
    sub_file = pkg_dir / "sub.py"
    sub_file.write_text("x = 1")

    mod = ImportManager()
    mod.set_pkg(str(pkg_dir))
    mod.install_hooks()

    # Edge creation before current module is set should fail
    with pytest.raises(ImportManagerError):
        mod.create_edge("pkg.sub")

    mod.set_current_mod("pkg.main", str(pkg_dir / "main.py"))

    # Import the submodule and verify graph updates
    result = mod.handle_import("pkg.sub", 0)
    expected = utils.to_mod_name(os.path.relpath(sub_file, str(pkg_dir)))
    assert result == expected
    graph = mod.get_import_graph()
    assert "pkg.sub" in graph
    assert graph["pkg.sub"]["filename"] == os.path.abspath(sub_file)
    assert "pkg.sub" in graph["pkg.main"]["imports"]

    # Importing a non‑existent module returns None
    assert mod.handle_import("pkg.nonexistent", 0) is None
