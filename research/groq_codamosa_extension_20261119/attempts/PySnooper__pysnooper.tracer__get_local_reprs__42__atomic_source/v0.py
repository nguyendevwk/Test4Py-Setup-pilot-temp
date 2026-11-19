import inspect
import collections
import pytest
from pysnooper.tracer import get_local_reprs

# Dummy watch variable that provides items(frame, normalize)
class DummyWatch:
    def items(self, frame, normalize):
        # Return a dict with a key that is not in the frame locals
        return {"watch_var": "watched_value"}

def test_get_local_reprs_order_and_repr(tmp_path):
    # Define a function with locals to capture
    def sample_func():
        a = 1
        b = "long string that should be truncated"
        c = [1, 2, 3]
        # Capture the frame
        frame = inspect.currentframe()
        return get_local_reprs(frame, max_length=10, normalize=True)

    result = sample_func()
    # The order should follow the code object's co_varnames
    assert list(result.keys()) == ["a", "b", "c"]
    # Representation of 'a' should be simple
    assert result["a"] == "1"
    # Representation of 'b' should be truncated to max_length
    assert len(result["b"]) <= 10
    # Representation of 'c' should be a shortish repr
    assert result["c"].startswith("[1, 2")

def test_get_local_reprs_with_watch_variable(tmp_path):
    def sample_func():
        x = 42
        frame = inspect.currentframe()
        return get_local_reprs(frame, watch=[DummyWatch()])

    result = sample_func()
    # Original locals
    assert result["x"] == "42"
    # Watch variable should be added
    assert "watch_var" in result
    assert result["watch_var"] == "watched_value"

def test_get_local_reprs_invalid_custom_repr():
    def sample_func():
        y = 10
        frame = inspect.currentframe()
        # Pass a non-iterable custom_repr to trigger TypeError
        return get_local_reprs(frame, custom_repr=42)

    with pytest.raises(TypeError):
        sample_func()
