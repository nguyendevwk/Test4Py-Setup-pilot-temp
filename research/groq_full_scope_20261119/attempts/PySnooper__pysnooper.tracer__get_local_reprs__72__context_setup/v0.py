import inspect
import collections
import pytest
from pysnooper.tracer import get_local_reprs

# Helper class to act as a watch variable
class DummyWatch:
    def __init__(self, mapping):
        self._mapping = mapping

    def items(self, frame, normalize):
        # Return items sorted by key
        return sorted(self._mapping.items())

def test_get_local_reprs_order_and_repr(tmp_path):
    # Define a function with local variables
    def inner():
        a = 1
        b = "text"
        c = [1, 2, 3]
        return locals()

    # Capture the frame of the inner function
    frame = inspect.currentframe()
    try:
        # Call inner to populate its locals
        inner()
        # Get the frame of the inner function
        inner_frame = frame.f_back
        # Call get_local_reprs on that frame
        result = get_local_reprs(inner_frame, max_length=10, normalize=True)
        # Ensure the result is an OrderedDict
        assert isinstance(result, collections.OrderedDict)
        # Check that keys are in the order of co_varnames
        expected_keys = ("a", "b", "c")
        assert list(result.keys()) == list(expected_keys)
        # Verify that reprs are shortish and normalized
        assert result["a"] == "1"
        assert result["b"] == "'text'"
        assert result["c"] == "[1, 2, 3]"
    finally:
        del frame

def test_get_local_reprs_with_watch(tmp_path):
    # Define a function with local variables
    def inner():
        x = 42
        y = "hello"
        return locals()

    frame = inspect.currentframe()
    try:
        inner()
        inner_frame = frame.f_back
        # Create a watch variable that adds a new key
        watch = DummyWatch({"z": "watched"})
        result = get_local_reprs(inner_frame, watch=[watch])
        # Ensure watch key is present
        assert "z" in result
        assert result["z"] == "watched"
        # Ensure original locals are still present
        assert result["x"] == "42"
        assert result["y"] == "'hello'"
    finally:
        del frame

def test_get_local_reprs_invalid_frame_raises():
    # Passing None should raise AttributeError due to missing f_code
    with pytest.raises(AttributeError):
        get_local_reprs(None)
