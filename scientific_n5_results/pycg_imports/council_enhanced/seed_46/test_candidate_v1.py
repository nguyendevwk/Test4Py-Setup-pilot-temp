import os
import pytest
from pycg.machinery.imports import ImportManager, ImportManagerError

def test_import_manager_node_edge_and_filepath():
    mgr = ImportManager()
    # create node
    node = mgr.create_node('pkg.main')
    assert node == {"filename": "", "imports": set()}
    # duplicate node raises error
    with pytest.raises(ImportManagerError):
        mgr.create_node('pkg.main')
    # set current module
    mgr.set_current_mod('pkg.main', 'main.py')
    # set filepath
    mgr.set_filepath('pkg.main', 'main.py')
    assert os.path.isabs(mgr.get_filepath('pkg.main'))
    # create edge
    mgr.create_edge('pkg.sub')
    assert 'pkg.sub' in mgr.get_imports('pkg.main')
    # get import graph
    graph = mgr.get_import_graph()
    assert 'pkg.main' in graph
    assert graph['pkg.main']['imports'] == {'pkg.sub'}
    # error when adding edge to non-existing node
    mgr2 = ImportManager()
    mgr2.set_current_mod('pkg.nonexistent', 'dummy.py')
    with pytest.raises(ImportManagerError):
        mgr2.create_edge('pkg.sub')
    # get_node returns None for missing
    assert mgr.get_node('missing') is None
    # get_imports returns empty list for missing
    assert mgr.get_imports('missing') == []
