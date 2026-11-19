import inspect
import collections
import pytest
from pysnooper.tracer import get_local_reprs
from pysnooper.variables import CommonVariable, Exploding, BaseVariable
from pysnooper import utils

def test_get_local_reprs_order_and_repr(tmp_path):
    # Define a function with several local variables
    def sample():
        a = 1
        b = "hello"
        c = [1, 2, 3]
        d = {"key": "value"}
        e = 3.14159
        return locals()

    # Capture the frame of the function call
    frame = inspect.currentframe()
    # Call get_local_reprs on the frame of sample()
    result = get_local_reprs(frame, max_length=10, normalize=True)

    # The result should be an OrderedDict preserving the order of co_varnames
    # plus any additional locals (here all are defined in the function)
    expected_keys = ["a", "b", "c", "d", "e"]
    assert list(result.keys()) == expected_keys

    # Check that the reprs are shortish and normalized
    assert result["a"] == "1"
    assert result["b"] == "'hello'"
    assert result["c"] == "[1, 2, 3]"
    assert result["d"] == "{'key': 'value'}"
    assert result["e"] == "3.14159"

def test_get_local_reprs_with_watch_variable(tmp_path):
    # Create a dummy watch variable that returns a dict of items
    class DummyWatch:
        def items(self, frame, normalize):
            return {"watch1": "value1", "watch2": "value2"}

    # Define a function with locals
    def sample():
        x = 42
        y = "test"
        return locals()

    frame = inspect.currentframe()
    watch = DummyWatch()
    result = get_local_reprs(frame, watch=(watch,), normalize=False)

    # The watch items should be merged into the result
    assert "watch1" in result
    assert "watch2" in result
    assert result["watch1"] == "value1"
    assert result["watch2"] == "value2"

    # The original locals should still be present
    assert "x" in result and result["x"] == "42"
    assert "y" in result and result["y"] == "'test'"

def test_get_local_reprs_invalid_watch_raises(tmp_path):
    # Passing a non-iterable watch should raise a TypeError
    def sample():
        a = 1
        return locals()

    frame = inspect.currentframe()
    with pytest.raises(TypeError):
        get_local_reprs(frame, watch=42, normalize=False)
