import pytest
from pysnooper.variables import CommonVariable
from pysnooper import utils

class DummyVariable(CommonVariable):
    """Concrete implementation for testing."""
    def __init__(self, source, unambiguous_source, exclude=None):
        super().__init__(source, unambiguous_source, exclude or set())

    def _keys(self, main_value):
        # Return all keys of a dict; raise if main_value is not a dict
        if not isinstance(main_value, dict):
            raise TypeError("Expected dict")
        return main_value.keys()

    def _format_key(self, key):
        return f"[{key}]"

    def _get_value(self, main_value, key):
        # Simulate a value retrieval that may raise for a specific key
        if key == "bad":
            raise ValueError("bad key")
        return main_value[key]

def test_normal_behavior():
    """Test that _items returns correct representations for a normal dict."""
    var = DummyVariable("src", "unsrc")
    data = {"a": 1, "b": "text"}
    items = var._items(data)
    # First item is the source representation
    assert items[0] == ("src", utils.get_shortish_repr(data))
    # Subsequent items correspond to each key/value pair
    expected = [
        ("unsrc[a]", utils.get_shortish_repr(1)),
        ("unsrc[b]", utils.get_shortish_repr("text")),
    ]
    assert items[1:] == expected

def test_exclude_and_error_in_get_value():
    """Test that excluded keys are skipped and errors in _get_value are ignored."""
    var = DummyVariable("src", "unsrc", exclude={"b"})
    data = {"a": 1, "b": 2, "bad": 3}
    items = var._items(data)
    # 'b' should be excluded; 'bad' should be skipped due to ValueError
    assert ("unsrc[a]", utils.get_shortish_repr(1)) in items
    assert ("unsrc[b]", utils.get_shortish_repr(2)) not in items
    assert ("unsrc[bad]", utils.get_shortish_repr(3)) not in items
    # Ensure source representation is present
    assert items[0] == ("src", utils.get_shortish_repr(data))

def test_keys_raises_exception():
    """Test that if _keys raises an exception, _items returns only the source."""
    class FaultyVariable(DummyVariable):
        def _keys(self, main_value):
            raise RuntimeError("cannot get keys")

    var = FaultyVariable("src", "unsrc")
    data = {"a": 1}
    items = var._items(data)
    # Only the source representation should be present
    assert items == [("src", utils.get_shortish_repr(data))]
