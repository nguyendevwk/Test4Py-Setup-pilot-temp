import pytest
from pysnooper.variables import CommonVariable
from pysnooper import utils

class DummyVariable(CommonVariable):
    """Concrete implementation for testing."""
    def __init__(self, source, unambiguous_source, exclude=None):
        super().__init__(source, unambiguous_source, exclude or set())

    def _keys(self, main_value):
        return main_value.keys()

    def _format_key(self, key):
        return f"[{key}]"

    def _get_value(self, main_value, key):
        return main_value[key]

def test_items_normal_dict(tmp_path):
    """Test normal behavior with a simple dictionary."""
    data = {"a": 1, "b": 2}
    var = DummyVariable("data", "data", exclude=set())
    items = var._items(data)
    # First item is the source representation
    assert items[0] == ("data", utils.get_shortish_repr(data))
    # Subsequent items correspond to keys in order
    expected = [
        ("data[a]", utils.get_shortish_repr(1)),
        ("data[b]", utils.get_shortish_repr(2)),
    ]
    assert items[1:] == expected

def test_items_exclude_key(tmp_path):
    """Test that excluded keys are omitted."""
    data = {"a": 1, "b": 2}
    var = DummyVariable("data", "data", exclude={"b"})
    items = var._items(data)
    # Only key 'a' should appear
    assert len(items) == 2
    assert items[1] == ("data[a]", utils.get_shortish_repr(1))
    assert all("b" not in key for key, _ in items)

def test_items_get_value_exception(tmp_path):
    """Test that keys raising exceptions in _get_value are skipped."""
    class FaultyVariable(DummyVariable):
        def _get_value(self, main_value, key):
            if key == "bad":
                raise ValueError("bad key")
            return super()._get_value(main_value, key)

    data = {"good": 42, "bad": "oops"}
    var = FaultyVariable("data", "data")
    items = var._items(data)
    # 'bad' key should be omitted due to exception
    assert len(items) == 2
    assert ("data[good]", utils.get_shortish_repr(42)) in items
    assert all("bad" not in key for key, _ in items)
