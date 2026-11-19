import pytest
from pysnooper.variables import Keys
from pysnooper import utils

def test_keys_basic_dict():
    """Keys should return all keys and values for a normal dictionary."""
    kv = Keys("d")
    d = {"a": 1, "b": 2}
    frame = type("Frame", (), {"f_globals": {}, "f_locals": {"d": d}})
    items = kv.items(frame)
    # Expect one entry for the dict itself and one per key
    assert len(items) == 3
    # First item is the dict representation
    assert items[0][0] == "d"
    assert items[0][1] == utils.get_shortish_repr(d)
    # Subsequent items contain formatted keys
    keys = {item[0] for item in items[1:]}
    assert keys == {"[a]", "[b]"}
    values = {item[1] for item in items[1:]}
    assert values == {utils.get_shortish_repr(1), utils.get_shortish_repr(2)}

def test_keys_exclude_parameter():
    """Keys should skip keys listed in the exclude tuple."""
    kv = Keys("d", exclude=("b",))
    d = {"a": 1, "b": 2, "c": 3}
    frame = type("Frame", (), {"f_globals": {}, "f_locals": {"d": d}})
    items = kv.items(frame)
    # Should contain entries for 'a' and 'c' only
    keys = {item[0] for item in items[1:]}
    assert keys == {"[a]", "[c]"}
    # Ensure 'b' is not present
    assert "[b]" not in keys

def test_keys_error_handling_on_value_access():
    """Keys should skip keys whose value access raises an exception."""
    class BadDict(dict):
        def __getitem__(self, key):
            if key == "bad":
                raise KeyError("bad key")
            return super().__getitem__(key)

    kv = Keys("d")
    d = BadDict({"good": 42, "bad": None})
    frame = type("Frame", (), {"f_globals": {}, "f_locals": {"d": d}})
    items = kv.items(frame)
    # Should contain only the good key
    keys = {item[0] for item in items[1:]}
    assert keys == {"[good]"}
    # Ensure the bad key is omitted
    assert "[bad]" not in keys
