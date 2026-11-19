import os
import pytest
from pycg.machinery.imports import ImportManager, ImportManagerError
from pycg.machinery.utils import to_mod_name

def test_import_manager_handle_import_and_graph(tmp_path):
    pkg_dir = tmp_path / "pkg"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("")
    (pkg_dir / "main.py").write_text("")
    sub_file = pkg_dir / "sub.py"
    sub_file.write_text("x = 1")

    mod = ImportManager()
    mod.set_pkg(str(pkg_dir))
    mod.install_hooks()

    edge_method = getattr(mod, "create_edge", None) or getattr(mod, "add_edge", None)
    assert edge_method is not None, "ImportManager missing edge creation method"
    with pytest.raises(ImportManagerError):
        edge_method("pkg.sub")

    mod.set_current_mod("pkg.main", str(pkg_dir / "main.py"))

    result = mod.handle_import("pkg.sub", 0)
    expected = to_mod_name(os.path.relpath(sub_file, str(pkg_dir)))
    assert result == expected

    graph = mod.get_import_graph()
    assert "pkg.sub" in graph
    assert graph["pkg.sub"]["filename"] == os.path.abspath(sub_file)
    assert "pkg.sub" in graph["pkg.main"]["imports"]

    assert mod.handle_import("pkg.nonexistent", 0) is None
