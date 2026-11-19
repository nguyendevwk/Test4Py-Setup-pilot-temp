import pytest
from pysnooper.variables import Exploding, Attrs, Keys, Indices
from collections import OrderedDict

# Test 1: Exploding with a mapping (dict) should delegate to Keys
def test_exploding_mapping():
    source = "data"
    data = {"a": 1, "b": 2}
    var = Exploding(source)
    # Use a dummy frame with locals containing data
    class DummyFrame:
        f_globals = {}
        f_locals = {"data": data}
    items = var.items(DummyFrame())
    # First item is the source itself
    assert items[0] == ("data", "{'a': 1, 'b': 2}")
    # Subsequent items correspond to keys
    expected_keys = {"data.a", "data.b"}
    actual_keys = {k for k, _ in items[1:]}
    assert actual_keys == expected_keys

# Test 2: Exploding with a sequence (list) should delegate to Indices
def test_exploding_sequence():
    source = "lst"
    lst = [10, 20, 30]
    var = Exploding(source)
    class DummyFrame:
        f_globals = {}
        f_locals = {"lst": lst}
    items = var.items(DummyFrame())
    # First item is the source itself
    assert items[0] == ("lst", "[10, 20, 30]")
    # Subsequent items correspond to indices
    expected_keys = {"lst[0]", "lst[1]", "lst[2]"}
    actual_keys = {k for k, _ in items[1:]}
    assert actual_keys == expected_keys

# Test 3: Attrs should correctly format attributes and handle __slots__
def test_attrs_with_slots_and_dict():
    class WithSlots:
        __slots__ = ("x", "y")
        def __init__(self):
            self.x = 5
            self.y = 6
    obj = WithSlots()
    obj.z = 7  # add a dict attribute
    attrs = Attrs("obj")
    class DummyFrame:
        f_globals = {}
        f_locals = {"obj": obj}
    items = attrs.items(DummyFrame())
    # First item is the source itself
    assert items[0] == ("obj", "<__main__.WithSlots object at 0x...>")
    # Check that attributes from __slots__ and __dict__ are present
    keys = {k for k, _ in items[1:]}
    assert ".x" in keys
    assert ".y" in keys
    assert ".z" in keys
    # Verify that values are correctly represented
    values = {k: v for k, v in items[1:]}
    assert values[".x"] == "5"
    assert values[".y"] == "6"
    assert values[".z"] == "7"
