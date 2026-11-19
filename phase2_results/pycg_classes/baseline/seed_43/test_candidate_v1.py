import pytest
from pycg.machinery.classes import ClassManager, ClassNode

def test_create_idempotent_and_get_returns_same_instance():
    manager = ClassManager()
    dummy_module = object()

    # First creation should instantiate a ClassNode
    cls1 = manager.create("TestClass", dummy_module)
    assert isinstance(cls1, ClassNode)

    # Subsequent creation with the same name returns the same instance
    cls2 = manager.create("TestClass", dummy_module)
    assert cls1 is cls2

    # get should return the stored instance
    assert manager.get("TestClass") is cls1

    # get on a non‑existent name returns None
    assert manager.get("NonExistent") is None
