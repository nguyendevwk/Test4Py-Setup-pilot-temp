import inspect
import collections
import pytest
from pysnooper.tracer import get_local_reprs
from pysnooper import utils

# Helper variable class for the `watch` argument
class DummyWatch:
    def items(self, frame, normalize):
        # Return a dict with a single item derived from a local variable
        return {"watch_value": frame.f_locals.get("x", None)}

def test_get_local_reprs_order_and_repr():
    # Define a function with several local variables
    def sample():
        a = 1
        b = "hello"
        c = [1, 2, 3]
        return a, b, c

    # Capture the frame of the function call
    frame = inspect.currentframe()
    try:
        # Call the function to populate locals
        sample()
        # Get the local representations from the caller's frame
        local_reprs = get_local_reprs(frame)
    finally:
        del frame

    # The result should be an OrderedDict preserving the order of local variables
    expected_keys = ["sample", "frame", "local_reprs", "a", "b", "c"]
    # The function's local variables are a, b, c; other locals are from the test scope
    # We only assert that the function's locals appear in the correct order
    assert list(local_reprs.keys())[-3:] == ["a", "b", "c"]
    # The representations should be shortish strings
    assert local_reprs["a"] == "1"
    assert local_reprs["b"] == "'hello'"
    assert local_reprs["c"] == "[1, 2, 3]"

def test_get_local_reprs_with_watch_and_normalize():
    # Define a function that creates a local variable
    def sample():
        x = 42
        return x

    frame = inspect.currentframe()
    try:
        sample()
        # Use DummyWatch to add a derived value to the result
        local_reprs = get_local_reprs(frame, watch=[DummyWatch()], normalize=True)
    finally:
        del frame

    # The watch value should be added to the result
    assert "watch_value" in local_reprs
    # The watch_value should equal the local variable x
    assert local_reprs["watch_value"] == 42
    # Normalization should not affect simple integers
    assert local_reprs["x"] == "42"

def test_get_local_reprs_max_length_truncation():
    # Define a function with a long string local variable
    def sample():
        long_str = "a" * 1000  # 1000 characters
        return long_str

    frame = inspect.currentframe()
    try:
        sample()
        # Set max_length to 10 to force truncation
        local_reprs = get_local_reprs(frame, max_length=10)
    finally:
        del frame

    # The representation of the long string should be truncated
    repr_value = local_reprs["long_str"]
    # It should start with the first 10 characters and end with '...'
    assert repr_value.startswith("'aaaaaaaaaa")
    assert repr_value.endswith("...'")
    # The total length should be 13 (10 chars + '...' + quotes)
    assert len(repr_value) == 13
