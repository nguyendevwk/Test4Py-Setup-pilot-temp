import pytest
from pycg.machinery.classes import ClassManager, ClassNode

def test_class_manager_create_and_get():
    cm = ClassManager()
    name = "my_module.MyClass"
    module = "test_module"

    # Create a new class node
    node = cm.create(name, module)
    assert isinstance(node, ClassNode)
    assert node.ns == name
    assert node.get_module() == module
    assert node.get_mro() == [name]

    # Subsequent get should return the same instance
    same_node = cm.get(name)
    assert same_node is node

    # get_classes should expose the created node
    classes = cm.get_classes()
    assert name in classes
    assert classes[name] is node

    # Creating again with the same name returns the existing node
    node_again = cm.create(name, module)
    assert node_again is node

    # get on a non-existent name returns None
    assert cm.get("non.existent.Class") is None

    # Verify that adding a parent updates the MRO
    node.add_parent("ParentClass")
    assert "ParentClass" in node.get_mro()
