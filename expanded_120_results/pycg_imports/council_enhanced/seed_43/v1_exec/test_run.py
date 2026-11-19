import os
import pytest
from pycg.machinery.imports import ImportManager, ImportManagerError

def test_import_manager_node_and_edge_and_filepath():
    mod = ImportManager()
    # create a valid node
    node = mod.create_node("pkg.main")
    assert node == {"filename": "", "imports": set()}
    # set current module and file
    mod.set_current_mod("pkg.main", "main.py")
    # set and get filepath
    mod.set_filepath("pkg.main", "path/to/file.py")
    abs_path = os.path.abspath("path/to/file.py")
    assert mod.get_filepath("pkg.main") == abs_path
    # imports initially empty
    assert mod.get_imports("pkg.main") == []
    # add an edge
    mod.create_edge("pkg.sub")
    assert mod.get_imports("pkg.main") == ["pkg.sub"]
    # create the target node
    mod.create_node("pkg.sub")
    # duplicate edge does not duplicate imports
    mod.create_edge("pkg.sub")
    assert mod.get_imports("pkg.main") == ["pkg.sub"]
    # error cases
    with pytest.raises(ImportManagerError):
        mod.create_node("")
    with pytest.raises(ImportManagerError):
        mod.create_node(123)
    with pytest.raises(ImportManagerError):
        mod.create_node("pkg.main")  # duplicate
    with pytest.raises(ImportManagerError):
        mod.create_edge("")
    with pytest.raises(ImportManagerError):
        mod.create_edge(123)
    with pytest.raises(ImportManagerError):
        mod.create_edge("nonexistent")  # node not exist
    with pytest.raises(ImportManagerError):
        mod.set_filepath("nonexistent", "file.py")
    with pytest.raises(ImportManagerError):
        mod.set_filepath("pkg.main", "")
    # get_imports for missing node returns empty list
    assert mod.get_imports("missing") == []
