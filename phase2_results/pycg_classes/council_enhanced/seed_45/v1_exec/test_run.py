import pytest
from pycg.machinery.classes import ClassManager, ClassNode

def test_class_manager_create_and_get():
    cm = ClassManager()
    name = "my_module.MyClass"
    module = "dummy_module"

    # create a new ClassNode
    node = cm.create(name, module)
    assert isinstance(node, ClassNode)
    assert node.get_module() == module
    assert node.get_mro() == [name]

    # get should return the same instance
    same_node = cm.get(name)
    assert same_node is node

    # get_classes should expose the mapping
    classes = cm.get_classes()
    assert isinstance(classes, dict)
    assert classes[name] is node

    # repeated create returns the existing node
    node2 = cm.create(name, "other_module")
    assert node2 is node
    assert node2.get_module() == module  # module should not change

    # get on a non-existent name returns None
    assert cm.get("unknown.Class") is None
