import pytest
from sanic.helpers import Default
import os

def test_default_repr_and_str():
    """Default should have a consistent string representation."""
    d = Default()
    assert repr(d) == "<Default>"
    assert str(d) == "<Default>"
    # repr and str should be identical
    assert repr(d) == str(d)

def test_default_identity_and_equality():
    """Each Default instance is unique and not equal to None or object()."""
    d1 = Default()
    d2 = Default()
    # Different instances are not the same object
    assert d1 is not d2
    # They are not equal to None or a generic sentinel
    assert d1 != None
    assert d1 != object()
    # Equality is based on identity
    assert d1 == d1

def test_default_as_dict_key(tmp_path):
    """Default can be used as a dictionary key and behaves like any object."""
    d = Default()
    # Create a temporary file to use its path as another key
    temp_file = tmp_path / "temp.txt"
    temp_file.write_text("test")
    key_path = str(temp_file)

    mapping = {d: "default_value", key_path: "file_value"}
    # Ensure both keys are present
    assert mapping[d] == "default_value"
    assert mapping[key_path] == "file_value"
    # The Default key should not collide with the file path key
    assert d != key_path
