import pytest
from pycg.machinery.imports import ImportManager, ImportManagerError

def test_import_manager_node_and_edge_creation_and_errors():
    mod = ImportManager()

    # Create a node and verify its initial state
    node = mod.create_node('pkg.main')
    assert node == {'filename': '', 'imports': set()}

    # Set the current module and create an edge to a new module
    mod.set_current_mod('pkg.main', 'main.py')
    mod.create_edge('pkg.sub')
    assert 'pkg.sub' in mod.get_imports('pkg.main')

    # Duplicate node creation should raise an error
    with pytest.raises(ImportManagerError):
        mod.create_node('pkg.main')

    # Invalid node name should raise an error
    with pytest.raises(ImportManagerError):
        mod.create_node('')

    # Creating an edge without a current module should raise an error
    mod2 = ImportManager()
    with pytest.raises(ImportManagerError):
        mod2.create_edge('pkg.sub')
