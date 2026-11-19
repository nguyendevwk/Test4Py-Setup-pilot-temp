import inspect
import collections
import pytest
from pysnooper.tracer import get_local_reprs

def test_get_local_reprs_order_and_repr(tmp_path):
    # Define a function with local variables and a nested function to capture a frame
    def inner():
        a = 1
        b = "hello world"
        c = [1, 2, 3]
        # Capture the current frame
        return inspect.currentframe()

    frame = inner()
    # Call get_local_reprs without any special options
    result = get_local_reprs(frame)

    # The result should be an OrderedDict preserving the order of local variables
    assert isinstance(result, collections.OrderedDict)
    # The keys should match the local variable names in the order they were defined
    assert list(result.keys()) == ["a", "b", "c"]
    # The representations should be the shortish reprs of the values
    assert result["a"] == "1"
    assert result["b"] == "'hello world'"
    assert result["c"] == "[1, 2, 3]"

def test_get_local_reprs_custom_repr_and_max_length(tmp_path):
    # Define a function with a local variable that will be represented specially
    def inner():
        data = {"key": "value", "long": "x" * 50}
        return inspect.currentframe()

    frame = inner()
    # Custom repr: replace representation of dicts with a fixed string
    def custom_repr(obj):
        if isinstance(obj, dict):
            return "<dict>"
        return None

    result = get_local_reprs(frame, custom_repr=custom_repr, max_length=10)
    # The dict should use the custom representation
    assert result["data"] == "<dict>"
    # The max_length should truncate the representation of the long string if it were shown
    # Since custom_repr overrides, we test that a non-dict value respects max_length
    def custom_repr_none(obj):
        return None
    frame2 = inner()
    result2 = get_local_reprs(frame2, custom_repr=custom_repr_none, max_length=10)
    # The long string should be truncated to 10 characters
    assert result2["data"] == "{'key': 'value', 'long': 'xxxxxxxxxx'}"

def test_get_local_reprs_watch_and_error(tmp_path):
    # Define a function to capture a frame
    def inner():
        x = 42
        return inspect.currentframe()

    frame = inner()

    # Define a watch object that provides items
    class DummyWatch:
        def items(self, frame, normalize):
            # Return a dict with a key that is not in the frame locals
            return {"watch_key": "watch_value"}

    watch_obj = DummyWatch()
    result = get_local_reprs(frame, watch=[watch_obj])
    # The watch key should be added to the result
    assert "watch_key" in result
    assert result["watch_key"] == "watch_value"

    # Define a watch object that lacks the required items method to trigger an error
    class BadWatch:
        pass

    bad_watch = BadWatch()
    with pytest.raises(AttributeError):
        get_local_reprs(frame, watch=[bad_watch])
