import pytest
from pycg.machinery.classes import ClassManager, ClassNode

def test_class_manager_and_node_behavior():
    cm = ClassManager()

    # Create a new ClassNode and verify its attributes
    node = cm.create('pkg.mod.Class', 'module1')
    assert isinstance(node, ClassNode)
    assert node.ns == 'pkg.mod.Class'
    assert node.module == 'module1'

    # Re‑creating the same name returns the same instance
    node2 = cm.create('pkg.mod.Class', 'module1')
    assert node2 is node

    # get returns the stored node
    same_node = cm.get('pkg.mod.Class')
    assert same_node is node

    # get returns None for a missing name
    assert cm.get('non.existent') is None

    # get_classes returns the internal mapping
    classes = cm.get_classes()
    assert isinstance(classes, dict)
    assert classes['pkg.mod.Class'] is node

    # Test ClassNode MRO manipulation
    node.add_parent('pkg.mod.Parent')
    assert node.get_mro() == ['pkg.mod.Class', 'pkg.mod.Parent']

    # Adding the same parent again should not duplicate it
    node.add_parent('pkg.mod.Parent')
    assert node.get_mro() == ['pkg.mod.Class', 'pkg.mod.Parent']

    # Adding a list of parents updates the MRO accordingly
    node.add_parent(['pkg.mod.A', 'pkg.mod.B'])
    assert node.get_mro() == ['pkg.mod.Class', 'pkg.mod.Parent', 'pkg.mod.A', 'pkg.mod.B']
