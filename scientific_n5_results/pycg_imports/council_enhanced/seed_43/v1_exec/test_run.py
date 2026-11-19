import os
import pytest
from pycg.machinery.imports import ImportManager, ImportManagerError

def test_import_manager_node_and_edge_creation():
    mgr = ImportManager()
    mgr.create_node('pkg.main')
    mgr.set_current_mod('pkg.main', 'main.py')
    mgr.set_filepath('pkg.main', 'src/pkg/main.py')
    assert mgr.get_filepath('pkg.main') == os.path.abspath('src/pkg/main.py')
    mgr.create_node('pkg.sub')
    mgr.create_edge('pkg.sub')
    assert 'pkg.sub' in mgr.get_imports('pkg.main')
    with pytest.raises(ImportManagerError):
        mgr.create_node('')
    with pytest.raises(ImportManagerError):
        mgr.create_node('pkg.main')
    with pytest.raises(ImportManagerError):
        mgr.set_filepath('pkg.nonexistent', 'file.py')
    with pytest.raises(ImportManagerError):
        mgr.set_filepath('pkg.main', '')
