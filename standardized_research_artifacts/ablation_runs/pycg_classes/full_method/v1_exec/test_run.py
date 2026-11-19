import pytest
from pycg.machinery.classes import ClassManager, ClassNode

def test_class_manager_and_node_behavior():
    cm = ClassManager()

    # Create a new ClassNode via ClassManager
    node = cm.create('pkg.mod.ClassA', 'moduleA')
    assert isinstance(node, ClassNode)
    assert node.ns == 'pkg.mod.ClassA'
    assert node.get_module() == 'moduleA'
    assert node.get_mro() == ['pkg.mod.ClassA']

    # Repeated create with same name returns the same instance
    same_node = cm.create('pkg.mod.ClassA', 'moduleB')
    assert same_node is node
    assert same_node.get_module() == 'moduleA'  # original module preserved

    # get returns the stored node
    assert cm.get('pkg.mod.ClassA') is node

    # get on unknown name returns None
    assert cm.get('unknown') is None

    # get_classes returns the internal mapping
    classes = cm.get_classes()
    assert isinstance(classes, dict)
    assert classes['pkg.mod.ClassA'] is node

    # Test ClassNode add_parent behavior
    node.add_parent('pkg.mod.Base')
    assert node.get_mro() == ['pkg.mod.ClassA', 'pkg.mod.Base']

    node.add_parent(['pkg.mod.Base', 'pkg.mod.Interface'])
    assert node.get_mro() == ['pkg.mod.ClassA', 'pkg.mod.Base', 'pkg.mod.Interface']

    # Adding an existing parent should not duplicate it
    node.add_parent('pkg.mod.Base')
    assert node.get_mro() == ['pkg.mod.ClassA', 'pkg.mod.Base', 'pkg.mod.Interface']
