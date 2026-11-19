import pytest
from typesystem.schemas import Definitions

def test_definitions_basic_operations():
    defs = Definitions()
    # Set a new key
    defs["foo"] = 123
    # Retrieve the value
    assert defs["foo"] == 123
    # Length reflects one item
    assert len(defs) == 1
    # Iteration yields the key
    assert list(defs) == ["foo"]

def test_definitions_duplicate_key_raises():
    defs = Definitions()
    defs["bar"] = "first"
    # Attempting to set the same key again should trigger the assertion
    with pytest.raises(AssertionError) as excinfo:
        defs["bar"] = "second"
    assert "Definition for 'bar' has already been set." in str(excinfo.value)

def test_definitions_deletion_of_missing_key_raises():
    defs = Definitions()
    defs["baz"] = True
    # Delete existing key
    del defs["baz"]
    assert len(defs) == 0
    # Deleting a non‑existent key should raise KeyError
    with pytest.raises(KeyError):
        del defs["missing"]
