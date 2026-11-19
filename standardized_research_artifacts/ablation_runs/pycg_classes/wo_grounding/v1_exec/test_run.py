import pytest
from pycg.machinery.classes import ClassManager, ClassNode


def test_class_manager_create_and_get_behavior():
    cm = ClassManager()
    dummy_module = object()

    # First creation should instantiate a ClassNode and store it
    cls1 = cm.create("TestClass", dummy_module)
    assert isinstance(cls1, ClassNode)
    assert cm.get("TestClass") is cls1
    assert list(cm.get_classes().keys()) == ["TestClass"]

    # Subsequent creation with the same name returns the existing instance
    cls2 = cm.create("TestClass", dummy_module)
    assert cls2 is cls1

    # get should return None for a name that hasn't been created
    assert cm.get("NonExistent") is None
