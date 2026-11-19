import pytest
from typesystem.schemas import Definitions

def test_definitions_basic_operations():
    defs = Definitions()
    # set a new key
    defs["foo"] = "bar"
    # get the value
    assert defs["foo"] == "bar"
    # length reflects one item
    assert len(defs) == 1
    # iteration yields the key
    assert list(defs) == ["foo"]

def test_definitions_duplicate_key_raises():
    defs = Definitions()
    defs["key"] = 123
    # attempting to set the same key again should raise an AssertionError
    with pytest.raises(AssertionError) as excinfo:
        defs["key"] = 456
    assert "Definition for 'key' has already been set." in str(excinfo.value)

def test_definitions_deletion_and_length():
    defs = Definitions(a=1, b=2)
    assert len(defs) == 2
    # delete one key
    del defs["a"]
    assert len(defs) == 1
    assert "a" not in defs
    # remaining key still accessible
    assert defs["b"] == 2
