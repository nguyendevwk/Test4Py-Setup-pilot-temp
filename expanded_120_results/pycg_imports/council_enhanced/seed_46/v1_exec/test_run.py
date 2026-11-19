import os
import pytest
from pycg.machinery.imports import ImportManager, ImportManagerError

def test_import_manager_node_and_edge_and_filepath():
    mod = ImportManager()

    # Create a node and verify its initial state
    node = mod.create_node('pkg.main')
    assert node == {"filename": "", "imports": set()}

    # Set the file path for the node and verify absolute path resolution
    mod.set_filepath('pkg.main', 'some/path/main.py')
    assert mod.get_filepath('pkg.main').endswith('main.py')

    # Add an import edge and verify it appears in the imports set
    mod.create_edge('pkg.sub')
    assert 'pkg.sub' in mod.get_imports('pkg.main')

    # Verify that creating a node with an invalid name raises an error
    with pytest.raises(ImportManagerError):
        mod.create_node('')

    # Verify that creating a duplicate node raises an error
    with pytest.raises(ImportManagerError):
        mod.create_node('pkg.main')

    # Verify that creating an edge with an invalid destination raises an error
    with pytest.raises(ImportManagerError):
        mod.create_edge('')

    # Verify that creating an edge to a non‑existent node raises an error
    with pytest.raises(ImportManagerError):
        mod.create_edge('pkg.other')

    # Verify that setting a file path for a non‑existent node raises an error
    with pytest.raises(ImportManagerError):
        mod.set_filepath('pkg.other', 'file.py')

    # Verify that setting an invalid file path raises an error
    with pytest.raises(ImportManagerError):
        mod.set_filepath('pkg.main', '')
