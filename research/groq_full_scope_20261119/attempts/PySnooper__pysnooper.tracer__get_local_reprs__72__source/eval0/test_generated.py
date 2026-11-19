import inspect
import collections
import pytest
from pysnooper.tracer import get_local_reprs
from pysnooper import utils

# Helper variable class for watch tests
class DummyWatch:
    def __init__(self, mapping):
        self._mapping = mapping

    def items(self, frame, normalize):
        # Return mapping as is; ignore frame and normalize for simplicity
        return self._mapping

def test_get_local_reprs_order_and_repr(tmp_path):
    # Define a function with local variables to capture a frame
    def inner():
        a = 1
        b = "hello"
        c = [1, 2, 3]
        return inspect.currentframe()

    frame = inner()
    result = get_local_reprs(frame)

    # Expected order: a, b, c (co_varnames order)
    expected_keys = ("a", "b", "c")
    assert list(result.keys()) == list(expected_keys)

    # Check that reprs are shortish and correct
    assert result["a"] == "1"
    assert result["b"] == "'hello'"
    # List repr should be truncated if longer than default max_length
    assert result["c"].startswith("[1, 2, 3]")  # full list fits default

def test_get_local_reprs_custom_repr_and_max_length(tmp_path):
    def inner():
        long_str = "x" * 50
        num = 123456789
        return inspect.currentframe()

    frame = inner()
    # Custom repr for int: show hex
    custom_repr = (int, lambda x: hex(x))
    # Max length 10 to truncate long_str
    result = get_local_reprs(frame, custom_repr=custom_repr, max_length=10)

    # long_str should be truncated
    assert result["long_str"].startswith("'xxxxxxxxxx")
    # int should use custom hex repr
    assert result["num"] == "0x75bcd15"

def test_get_local_reprs_watch_integration(tmp_path):
    def inner():
        x = 42
        y = "test"
        return inspect.currentframe()

    frame = inner()
    watch = DummyWatch({"watch_var": "watched_value"})
    result = get_local_reprs(frame, watch=watch)

    # Original locals should be present
    assert result["x"] == "42"
    assert result["y"] == "'test'"

    # Watch variable should be added and sorted appropriately
    # Since 'watch_var' is not in locals, it appears after existing keys
    assert list(result.keys())[-1] == "watch_var"
    assert result["watch_var"] == "watched_value"
