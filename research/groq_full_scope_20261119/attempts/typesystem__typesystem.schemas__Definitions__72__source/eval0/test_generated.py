import pytest
from typesystem.schemas import Definitions

def test_definitions_basic_operations():
    defs = Definitions()
    # set new items
    defs["a"] = 1
    defs["b"] = "two"
    # get items
    assert defs["a"] == 1
    assert defs["b"] == "two"
    # length and iteration
    assert len(defs) == 2
    assert set(iter(defs)) == {"a", "b"}

def test_definitions_duplicate_key_error():
    defs = Definitions()
    defs["x"] = 42
    with pytest.raises(AssertionError) as excinfo:
        defs["x"] = 99
    assert "Definition for 'x' has already been set." in str(excinfo.value)

def test_definitions_deletion_and_reassignment():
    defs = Definitions()
    defs["foo"] = "bar"
    assert "foo" in defs
    del defs["foo"]
    assert "foo" not in defs
    # after deletion, can reassign
    defs["foo"] = "baz"
    assert defs["foo"] == "baz"
