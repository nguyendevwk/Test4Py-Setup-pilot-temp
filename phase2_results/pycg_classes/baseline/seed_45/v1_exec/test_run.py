import pytest
from pycg.machinery.classes import ClassManager, ClassNode


def test_class_manager_create_and_get():
    manager = ClassManager()
    dummy_module = type("DummyModule", (), {})()

    # get should return None for unknown names
    assert manager.get("unknown") is None

    # create should instantiate a ClassNode and store it
    first = manager.create("TestClass", dummy_module)
    assert isinstance(first, ClassNode)
    assert first.name == "TestClass"
    assert first.module is dummy_module

    # subsequent get should return the same instance
    second = manager.get("TestClass")
    assert second is first

    # creating again with a different module should not overwrite the existing node
    new_module = type("NewModule", (), {})()
    third = manager.create("TestClass", new_module)
    assert third is first
    assert third.module is dummy_module  # original module preserved

    # get_classes should expose the internal mapping
    classes = manager.get_classes()
    assert isinstance(classes, dict)
    assert "TestClass" in classes
    assert classes["TestClass"] is first
