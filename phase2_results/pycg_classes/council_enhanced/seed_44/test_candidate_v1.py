import pytest
from pycg.machinery.classes import ClassManager, ClassNode

def test_class_manager_create_and_get():
    cm = ClassManager()
    name = "my_module.MyClass"
    module = "dummy_module"

    # Create a new class node
    node = cm.create(name, module)
    assert isinstance(node, ClassNode)
    assert node.ns == name
    assert node.module == module
    assert node.get_mro() == [name]
    assert node.get_module() == module

    # Retrieve the same node
    same_node = cm.get(name)
    assert same_node is node

    # Non‑existent name returns None
    assert cm.get("unknown") is None

    # get_classes returns the internal mapping
    classes = cm.get_classes()
    assert isinstance(classes, dict)
    assert classes[name] is node

    # Re‑creating with the same name returns the existing node
    new_node = cm.create(name, "other_module")
    assert new_node is node
    # The module remains the original one
    assert new_node.module == module
