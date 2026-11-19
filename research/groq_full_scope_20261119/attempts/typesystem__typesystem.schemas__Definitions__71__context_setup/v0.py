import pytest
from typesystem.schemas import Definitions

def test_definitions_basic_operations():
    defs = Definitions()
    # Add a new definition
    defs["foo"] = {"type": "string"}
    assert defs["foo"] == {"type": "string"}
    # Length reflects added item
    assert len(defs) == 1
    # Iteration yields the key
    keys = list(defs)
    assert keys == ["foo"]
    # Delete the definition
    del defs["foo"]
    assert len(defs) == 0
    with pytest.raises(KeyError):
        _ = defs["foo"]

def test_definitions_duplicate_key_raises():
    defs = Definitions()
    defs["bar"] = {"type": "int"}
    # Attempting to set the same key again should raise an AssertionError
    with pytest.raises(AssertionError) as excinfo:
        defs["bar"] = {"type": "float"}
    assert "Definition for 'bar' has already been set." in str(excinfo.value)

def test_definitions_initialization_and_iteration():
    initial = {"a": 1, "b": 2}
    defs = Definitions(initial)
    # Verify initial contents
    assert defs["a"] == 1
    assert defs["b"] == 2
    # Adding a new key should work
    defs["c"] = 3
    assert defs["c"] == 3
    # Iteration order matches insertion order of the underlying dict
    assert list(defs) == ["a", "b", "c"]
    # Length reflects all items
    assert len(defs) == 3
