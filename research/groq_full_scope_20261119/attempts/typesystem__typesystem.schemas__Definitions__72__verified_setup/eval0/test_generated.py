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
    defs["alpha"] = 1
    # attempting to set the same key again should trigger the assertion
    with pytest.raises(AssertionError) as excinfo:
        defs["alpha"] = 2
    assert "Definition for 'alpha' has already been set." in str(excinfo.value)

def test_definitions_deletion_and_existence():
    defs = Definitions({"x": 10, "y": 20})
    # ensure both keys exist
    assert "x" in defs and "y" in defs
    # delete one key
    del defs["x"]
    # length updated
    assert len(defs) == 1
    # accessing deleted key raises KeyError
    with pytest.raises(KeyError):
        _ = defs["x"]
    # remaining key still accessible
    assert defs["y"] == 20
