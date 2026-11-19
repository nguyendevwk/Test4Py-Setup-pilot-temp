import builtins
import types
import pytest
from pysnooper.variables import CommonVariable, BaseVariable, utils, pycompat

# Helper subclass that exposes the abstract methods for testing
class DummyVariable(CommonVariable):
    def __init__(self, source, exclude=()):
        super().__init__(source, exclude)

    def _keys(self, main_value):
        # For a dict, return its keys; for other types, return empty
        if isinstance(main_value, dict):
            return main_value.keys()
        return ()

    def _format_key(self, key):
        return f"[{repr(key)}]"

    def _get_value(self, main_value, key):
        return main_value[key]


def test_common_variable_normal(tmp_path):
    """Test normal extraction of items from a dictionary."""
    # Create a simple dictionary
    data = {"a": 1, "b": 2}
    # Prepare a frame with locals containing the dictionary
    frame = types.FrameType(
        None, None, None, None, {"data": data}, None, None, None, None
    )
    var = DummyVariable("data")
    items = var.items(frame)
    # Expected items: source repr and each key/value pair
    expected = [
        ("data", utils.get_shortish_repr(data)),
        ("data[a]", utils.get_shortish_repr(1)),
        ("data[b]", utils.get_shortish_repr(2)),
    ]
    assert items == expected


def test_common_variable_exclude(tmp_path):
    """Test that excluded keys are omitted from the result."""
    data = {"x": 10, "y": 20}
    frame = types.FrameType(
        None, None, None, None, {"data": data}, None, None, None, None
    )
    var = DummyVariable("data", exclude=("y",))
    items = var.items(frame)
    # Only key 'x' should appear
    expected = [
        ("data", utils.get_shortish_repr(data)),
        ("data[x]", utils.get_shortish_repr(10)),
    ]
    assert items == expected
    # Ensure 'y' is not present
    assert all("y" not in key for key, _ in items)


def test_common_variable_error_handling(tmp_path):
    """Test that errors during key access are gracefully skipped."""
    class FaultyDict(dict):
        def __getitem__(self, key):
            if key == "bad":
                raise ValueError("bad key")
            return super().__getitem__(key)

    data = FaultyDict({"good": 1, "bad": 2})
    frame = types.FrameType(
        None, None, None, None, {"data": data}, None, None, None, None
    )
    var = DummyVariable("data")
    items = var.items(frame)
    # 'bad' key should be skipped, only 'good' appears
    expected = [
        ("data", utils.get_shortish_repr(data)),
        ("data[good]", utils.get_shortish_repr(1)),
    ]
    assert items == expected
    # Ensure no entry for 'bad'
    assert all("bad" not in key for key, _ in items)
