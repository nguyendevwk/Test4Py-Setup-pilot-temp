import inspect
import collections
import pytest
from pysnooper.tracer import get_local_reprs

def test_get_local_reprs_order_and_repr():
    # Define a function with local variables, cellvars, freevars, and a local dict key
    def inner():
        a = 1
        b = "hello world"
        c = [1, 2, 3]
        d = {"x": 10}
        # create a closure variable
        def closure():
            return a
        return closure, a, b, c, d

    closure_func, a_val, b_val, c_val, d_val = inner()
    # Capture the frame of the closure function
    frame = closure_func.__closure__[0].cell_contents.__code__.co_freevars
    # Instead, use inspect to get a frame where locals are set
    def test_frame():
        x = 42
        y = "test string"
        z = [1, 2, 3]
        return locals()
    frame = inspect.currentframe()
    try:
        # Move to the frame where test_frame locals are defined
        while frame.f_code.co_name != "test_frame":
            frame = frame.f_back
        result = get_local_reprs(frame, max_length=5, normalize=True)
    finally:
        del frame

    # The result should be an OrderedDict preserving the order of local variables
    expected_keys = ["x", "y", "z"]
    assert list(result.keys()) == expected_keys

    # The reprs should be truncated to max_length and normalized
    assert result["x"] == "42"
    assert result["y"] == "'tes'"
    assert result["z"] == "[1, 2, 3]"

def test_get_local_reprs_custom_repr_and_watch():
    # Custom repr function that returns a fixed string
    def custom_repr(obj):
        return f"<{type(obj).__name__}>"

    # Dummy watch variable that provides items
    class DummyWatch:
        def items(self, frame, normalize):
            return {"watch_var": "watched"}

    frame = inspect.currentframe()
    try:
        while frame.f_code.co_name != "test_get_local_reprs_custom_repr_and_watch":
            frame = frame.f_back
        result = get_local_reprs(frame, watch=[DummyWatch()], custom_repr=[custom_repr])
    finally:
        del frame

    # All local variables should use the custom repr
    for key, val in result.items():
        if key == "watch_var":
            assert val == "watched"
        else:
            assert val == f"<{type(val).__name__}>"

def test_get_local_reprs_invalid_watch_raises():
    # Watch element that does not provide an items method
    class BadWatch:
        pass

    frame = inspect.currentframe()
    try:
        while frame.f_code.co_name != "test_get_local_reprs_invalid_watch_raises":
            frame = frame.f_back
        with pytest.raises(AttributeError):
            get_local_reprs(frame, watch=[BadWatch()])
    finally:
        del frame
