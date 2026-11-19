import pytest
from pycg.machinery.definitions import DefinitionManager
import pycg.machinery.utils as utils

def test_transitive_closure_basic():
    manager = DefinitionManager()

    # Create three definitions with simple name pointers
    manager.create('A', utils.constants.NAME_DEF)
    manager.create('B', utils.constants.NAME_DEF)
    manager.create('C', utils.constants.NAME_DEF)

    # A points to B, B points to C
    manager.get('A').get_name_pointer().add('B')
    manager.get('B').get_name_pointer().add('C')

    closure = manager.transitive_closure()

    # The closure should contain all namespaces
    assert set(closure.keys()) == {'A', 'B', 'C'}

    # According to the implementation, only the reachable names are returned
    # (self is added only when there are no outgoing pointers)
    assert closure['A'] == {'C'}
    assert closure['B'] == {'C'}
    assert closure['C'] == {'C'}
