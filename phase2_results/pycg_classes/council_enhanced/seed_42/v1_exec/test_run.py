import pytest
from pycg.machinery.classes import ClassManager, ClassNode

def test_class_manager_create_and_retrieve():
    cm = ClassManager()

    # Create a new class node
    node = cm.create('pkg.mod.Class', module='mod')
    assert isinstance(node, ClassNode)
    assert node.ns == 'pkg.mod.Class'
    assert node.get_module() == 'mod'
    assert node.get_mro() == ['pkg.mod.Class']

    # Retrieving the same node
    same = cm.get('pkg.mod.Class')
    assert same is node

    # Unknown name returns None
    assert cm.get('unknown') is None

    # get_classes returns the internal mapping
    classes = cm.get_classes()
    assert isinstance(classes, dict)
    assert 'pkg.mod.Class' in classes
    assert classes['pkg.mod.Class'] is node

    # Creating again with the same name does not overwrite
    node2 = cm.create('pkg.mod.Class', module='other')
    assert node2 is node
    assert node.get_module() == 'mod'  # original module preserved

    # Creating a different name adds a new node
    node3 = cm.create('pkg.mod.Other', module='other')
    assert node3 is not node
    assert node3.ns == 'pkg.mod.Other'
    assert node3.get_module() == 'other'
