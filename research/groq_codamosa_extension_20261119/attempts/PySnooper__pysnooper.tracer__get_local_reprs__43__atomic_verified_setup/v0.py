import inspect
import collections
import pytest
from pysnooper.tracer import get_local_reprs
from pysnooper import utils

# Helper variable class for the `watch` argument
class DummyWatch:
    def items(self, frame, normalize):
        # Return a dict with a single item derived from a local variable
        return {"watched": frame.f_locals.get("x", None)}

def test_get_local_reprs_order_and_repr():
    # Define a function with several local variables
    def sample():
        a = 1
        b = "hello"
        c = [1, 2, 3]
        d = {"key": "value"}
        return locals()

    # Capture the frame of the function call
    frame = inspect.currentframe()
    try:
        # Call the function to populate locals
        sample()
        # Get the frame of the function itself
        func_frame = frame.f_back
        # Call get_local_reprs on that frame
        result = get_local_reprs(func_frame)
        # The result should be an OrderedDict preserving the order of co_varnames
        expected_keys = list(func_frame.f_code.co_varnames)
        assert list(result.keys()) == expected_keys
        # Check that the reprs are shortish and match utils.get_shortish_repr
        for key, value in func_frame.f_locals.items():
            expected_repr = utils.get_shortish_repr(value, (), None, False)
            assert result[key] == expected_repr
    finally:
        del frame

def test_get_local_reprs_with_watch_and_normalize():
    # Define a function that uses a local variable and a watch
    def sample():
        x = 42
        return locals()

    frame = inspect.currentframe()
    try:
        sample()
        func_frame = frame.f_back
        # Use DummyWatch to add a watched item
        watch = [DummyWatch()]
        result = get_local_reprs(func_frame, watch=watch, normalize=True)
        # The watched item should be present
        assert "watched" in result
        # The watched value should be the same as the local variable x
        assert result["watched"] == func_frame.f_locals["x"]
        # The order should still start with the original locals
        assert list(result.keys())[0] == "x"
    finally:
        del frame

def test_get_local_reprs_max_length_truncation():
    # Define a function with a very long string
    def sample():
        long_str = "a" * 200
        return locals()

    frame = inspect.currentframe()
    try:
        sample()
        func_frame = frame.f_back
        # Set max_length to 50 to force truncation
        result = get_local_reprs(func_frame, max_length=50)
        # The representation of long_str should be truncated
        repr_value = result["long_str"]
        assert repr_value.endswith("...")  # utils.get_shortish_repr appends ellipsis
        assert len(repr_value) <= 53  # 50 chars + '...'
    finally:
        del frame
