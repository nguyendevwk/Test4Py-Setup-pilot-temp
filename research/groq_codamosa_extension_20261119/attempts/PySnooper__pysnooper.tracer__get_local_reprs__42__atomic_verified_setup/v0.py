import inspect
import collections
import pytest
from pysnooper.tracer import get_local_reprs
from pysnooper.variables import CommonVariable, Exploding, BaseVariable

def _frame_with_locals():
    a = 1
    b = "hello world"
    c = [1, 2, 3]
    d = {"key": "value"}
    return inspect.currentframe()

def test_order_and_repr_basic():
    frame = _frame_with_locals()
    result = get_local_reprs(frame)
    # The order should follow the code object's co_varnames + locals
    expected_keys = ("a", "b", "c", "d")
    assert list(result.keys()) == list(expected_keys)
    # Repr should be shortish (no truncation)
    assert result["a"] == "1"
    assert result["b"] == "'hello world'"
    assert result["c"] == "[1, 2, 3]"
    assert result["d"] == "{'key': 'value'}"

def test_custom_repr_and_max_length():
    frame = _frame_with_locals()
    # Custom repr for list type
    custom_repr = (list, lambda x: f"<list len={len(x)}>") 
    result = get_local_reprs(frame, custom_repr=custom_repr, max_length=10)
    assert result["c"] == "<list len=3>"
    # Max length truncates long string
    long_str = "x" * 20
    frame.f_locals["long"] = long_str
    result = get_local_reprs(frame, max_length=10)
    assert result["long"] == "'xxxxxxxxxx…'"

def test_watch_and_normalize():
    frame = _frame_with_locals()
    # Define a watch variable that adds a derived value
    class WatchVar(BaseVariable):
        def items(self, frame, normalize):
            return {"derived": frame.f_locals["a"] * 10}
    watch = [WatchVar()]
    result = get_local_reprs(frame, watch=watch, normalize=True)
    assert "derived" in result
    assert result["derived"] == "10"
    # Normalize should convert int to str
    frame.f_locals["a"] = 5
    result = get_local_reprs(frame, watch=watch, normalize=True)
    assert result["derived"] == "50"
