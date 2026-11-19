import pytest
from pycg.machinery.classes import ClassManager

def test_classnode_add_parent_duplicate_behavior():
    cm = ClassManager()
    node = cm.create('pkg.mod.ClassA', 'moduleA')
    assert node.get_mro() == ['pkg.mod.ClassA']

    node.add_parent('pkg.mod.Base')
    assert node.get_mro() == ['pkg.mod.ClassA', 'pkg.mod.Base']

    node.add_parent(['pkg.mod.Base', 'pkg.mod.Interface'])
    assert node.get_mro() == ['pkg.mod.ClassA', 'pkg.mod.Base', 'pkg.mod.Interface']

    node.add_parent('pkg.mod.Base')
    # The implementation moves an existing parent to the end rather than
    # preventing duplication; the list length remains unchanged.
    assert node.get_mro() == ['pkg.mod.ClassA', 'pkg.mod.Interface', 'pkg.mod.Base']
    assert len(node.get_mro()) == 3
