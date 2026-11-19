import pytest
from pycg.machinery.classes import ClassManager, ClassNode

def test_class_manager_create_and_get():
    cm = ClassManager()

    # get on nonexistent name returns None
    assert cm.get("missing") is None

    # create a new class node
    node1 = cm.create("pkg.Class", module="module1")
    assert isinstance(node1, ClassNode)
    assert node1.ns == "pkg.Class"
    assert node1.get_module() == "module1"
    assert node1.get_mro() == ["pkg.Class"]

    # get returns the same instance
    assert cm.get("pkg.Class") is node1
    assert cm.get_classes() is cm.names
    assert len(cm.get_classes()) == 1

    # creating the same name again returns the existing instance
    node2 = cm.create("pkg.Class", module="module2")
    assert node2 is node1
    assert node1.get_module() == "module1"  # original module preserved

    # create a different class node
    node3 = cm.create("pkg.Other", module="module3")
    assert node3 is not node1
    assert len(cm.get_classes()) == 2
    assert "pkg.Other" in cm.get_classes()
    assert cm.get("pkg.Other") is node3

    # create with module=None
    node4 = cm.create("pkg.NoneModule", module=None)
    assert node4.get_module() is None
    assert cm.get("pkg.NoneModule") is node4
    assert len(cm.get_classes()) == 3
