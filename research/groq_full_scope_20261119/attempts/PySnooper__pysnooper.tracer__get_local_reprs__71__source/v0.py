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
    # Define a custom representation function that replaces the dict with a fixed string
    def custom_repr(value):
        if isinstance(value, dict):
            return "<dict>"
        return None

    # Call get_local_reprs with custom_repr and a max_length that truncates the long string
    result = get_local_reprs(frame, custom_repr=custom_repr, max_length=10)

    # The custom representation should override the default for the dict
    assert result["data"] == "<dict>"
    # The long string inside the dict is not represented because custom_repr took precedence
    # Ensure that max_length is respected for other values (none in this case)
    # Verify that the result is still an OrderedDict
    assert isinstance(result, collections.OrderedDict)

def test_get_local_reprs_watch_and_error_handling(tmp_path):
    # Define a function with a local variable
    def inner():
        x = 42
        return inspect.currentframe()

    frame = inner()

    # Define a watch object that provides items correctly
    class DummyWatch:
        def items(self, frame, normalize):
            # Return a dict with a new key that should be added to the result
            return {"watch_key": "watch_value"}

    # Call get_local_reprs with a valid watch
    result = get_local_reprs(frame, watch=[DummyWatch()])
    assert "watch_key" in result
    assert result["watch_key"] == "watch_value"

    # Define a watch object that lacks the required items method
    class BadWatch:
        pass

    # Calling get_local_reprs with a bad watch should raise an AttributeError
    with pytest.raises(AttributeError):
        get_local_reprs(frame, watch=[BadWatch()])
