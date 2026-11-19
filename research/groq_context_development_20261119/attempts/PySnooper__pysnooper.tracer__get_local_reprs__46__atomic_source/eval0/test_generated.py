import inspect
import collections
import pytest
from pysnooper.tracer import get_local_reprs

def test_get_local_reprs_order_and_repr(tmp_path):
    # Define a function with several local variables
    def sample():
        a = 1
        b = "hello world"
        c = [1, 2, 3]
        d = {"key": "value"}
        return locals()

    # Capture the frame of the sample function
    frame = inspect.currentframe()
    # Call get_local_reprs on the frame of sample
    result = get_local_reprs(frame.f_back)

    # The result should be an OrderedDict preserving the order of co_varnames
    expected_keys = list(sample.__code__.co_varnames) + list(sample.__code__.co_cellvars) + list(sample.__code__.co_freevars)
    # Include any other locals that might appear
    for key in result.keys():
        assert key in expected_keys

    # Check that the reprs are shortish and match the expected values
    assert result["a"] == "1"
    assert result["b"] == "\"hello world\""
    assert result["c"] == "[1, 2, 3]"
    assert result["d"] == "{'key': 'value'}"

def test_get_local_reprs_max_length_truncation(tmp_path):
    # Define a function with a long string
    def long_string():
        long = "x" * 100
        return locals()

    frame = inspect.currentframe()
    # Use max_length to truncate the representation
    result = get_local_reprs(frame.f_back, max_length=10)

    # The long string should be truncated to 10 characters plus ellipsis
    assert result["long"].startswith("'xxxxxxxxxx")
    assert result["long"].endswith("...'")

def test_get_local_reprs_watch_updates(tmp_path):
    # Define a simple watch object that returns additional items
    class SimpleWatch:
        def items(self, frame, normalize):
            return [("watch1", "value1"), ("watch2", "value2")]

    def with_watch():
        x = 42
        return locals()

    frame = inspect.currentframe()
    # Pass the watch object to get_local_reprs
    result = get_local_reprs(frame.f_back, watch=[SimpleWatch()])

    # The watch items should be present and sorted alphabetically
    assert list(result.keys())[-2:] == ["watch1", "watch2"]
    assert result["watch1"] == "value1"
    assert result["watch2"] == "value2"
