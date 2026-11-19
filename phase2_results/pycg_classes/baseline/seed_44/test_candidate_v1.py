import pytest
from pycg.machinery.classes import ClassManager, ClassNode

def test_create_and_get_returns_same_instance():
    manager = ClassManager()
    dummy_module = object()

    # Create a new class node
    cls1 = manager.create("TestClass", dummy_module)
    assert isinstance(cls1, ClassNode)

    # Subsequent get should return the same instance
    cls2 = manager.get("TestClass")
    assert cls2 is cls1

    # get_classes should contain the created instance
    classes_dict = manager.get_classes()
    assert "TestClass" in classes_dict
    assert classes_dict["TestClass"] is cls1

    # Creating again with the same name returns the existing instance
    cls3 = manager.create("TestClass", dummy_module)
    assert cls3 is cls1
