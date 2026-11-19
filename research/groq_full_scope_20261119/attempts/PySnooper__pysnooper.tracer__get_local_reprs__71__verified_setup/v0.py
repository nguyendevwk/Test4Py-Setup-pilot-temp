import inspect
import collections
import pytest
from pysnooper.tracer import get_local_reprs
from pysnooper import utils

# Helper variable class for watch functionality
class DummyWatch:
    def __init__(self, mapping):
        self._mapping = mapping

    def items(self, frame, normalize):
        # Return items sorted by key
        return sorted(self._mapping.items())

def _frame_with_locals():
    """Return a frame object with a known set of local variables."""
    def inner():
        a = 1
        b = "hello"
        c = [1, 2, 3]
        return inspect.currentframe()
    return inner()

def test_get_local_reprs_order_and_repr():
    frame = _frame_with_locals()
    # Capture local representations
    result = get_local_reprs(frame, max_length=None, normalize=False)
    # Ensure the order follows co_varnames + cellvars + freevars + f_locals keys
    expected_order = list(frame.f_code.co_varnames) + list(frame.f_code.co_cellvars) + list(frame.f_code.co_freevars) + list(frame.f_locals.keys())
    assert list(result.keys()) == sorted(set(expected_order), key=expected_order.index)
    # Check that each value is a string representation
    for key, val in result.items():
        assert isinstance(val, str)
    # Verify specific representations
    assert result["a"] == "1"
    assert result["b"] == "'hello'"
    assert result["c"] == "[1, 2, 3]"

def test_get_local_reprs_custom_repr_and_max_length():
    frame = _frame_with_locals()
    # Custom repr that returns a fixed string for any input
    def custom_repr(obj):
        return f"<custom:{type(obj).__name__}>"
    # Set max_length to truncate long representations
    result = get_local_reprs(frame, custom_repr=(custom_repr,), max_length=10, normalize=False)
    # Custom repr should be applied
    assert result["a"] == "<custom:int>"
    assert result["b"] == "<custom:str>"
    assert result["c"] == "<custom:list>"
    # Ensure max_length truncation is respected (though custom_repr ignores it)
    # Use default utils.get_shortish_repr to test truncation
    short_repr = utils.get_shortish_repr("a very long string", max_length=5)
    assert short_repr == "a ver..."

def test_get_local_reprs_watch_variable_integration():
    frame = _frame_with_locals()
    watch_var = DummyWatch({"watch1": "value1", "watch2": "value2"})
    result = get_local_reprs(frame, watch=(watch_var,), normalize=False)
    # Watch items should be present and sorted
    assert "watch1" in result
    assert "watch2" in result
    assert result["watch1"] == "value1"
    assert result["watch2"] == "value2"
    # Ensure watch items are appended after local variables
    local_keys = list(frame.f_locals.keys())
    watch_keys = ["watch1", "watch2"]
    # The order of watch keys in result should follow sorted order
    assert list(result.keys())[-2:] == sorted(watch_keys)
