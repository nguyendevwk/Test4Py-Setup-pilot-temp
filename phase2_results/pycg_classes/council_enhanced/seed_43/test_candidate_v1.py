import pytest
from pycg.machinery.classes import ClassManager, ClassNode

def test_class_manager_create_and_get():
    cm = ClassManager()
    name = "my_module.MyClass"
    module = "dummy_module"

    # Create a new ClassNode via ClassManager
    node = cm.create(name, module)
    assert isinstance(node, ClassNode)
    assert node.get_module() == module
    assert node.get_mro() == [name]

    # Retrieve the same node
    assert cm.get(name) is node

    # get_classes should expose the mapping
    classes = cm.get_classes()
    assert name in classes
    assert classes[name] is node

    # Re‑creating the same name returns the existing node
    node2 = cm.create(name, "other_module")
    assert node2 is node
    assert node2.get_module() == module  # module remains unchanged

    # Getting a non‑existent name returns None
    assert cm.get("nonexistent") is None
