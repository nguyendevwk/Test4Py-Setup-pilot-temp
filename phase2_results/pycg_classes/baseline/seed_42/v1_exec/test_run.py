import pytest
from pycg.machinery.classes import ClassManager, ClassNode

def test_class_manager_create_and_get():
    manager = ClassManager()
    module = object()
    name = "TestClass"

    # Create a new class node
    cls1 = manager.create(name, module)
    assert isinstance(cls1, ClassNode)

    # Retrieve the same instance
    assert manager.get(name) is cls1

    # Creating again returns the existing instance
    cls2 = manager.create(name, module)
    assert cls2 is cls1

    # get returns None for a missing name
    assert manager.get("Missing") is None

    # get_classes contains the created instance
    assert manager.get_classes()[name] is cls1
