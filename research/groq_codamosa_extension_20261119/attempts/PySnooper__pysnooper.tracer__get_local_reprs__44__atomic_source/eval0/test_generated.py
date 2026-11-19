import inspect
import collections
import datetime as datetime_module
import pytest

from pysnooper.tracer import get_local_reprs
from pysnooper import utils


def test_get_local_reprs_order_and_repr(tmp_path):
    """Test that local variables are ordered correctly and their reprs are produced."""
    def inner():
        a = 1
        b = 2
        c = "hello"
        frame = inspect.currentframe()
        result = get_local_reprs(frame, max_length=None, normalize=False)
        # Order should follow co_varnames + f_locals keys
        assert list(result.keys()) == ["a", "b", "c"]
        # Reprs should be shortish
        assert result["a"] == "1"
        assert result["b"] == "2"
        assert result["c"] == "'hello'"

    inner()


def test_get_local_reprs_max_length_truncation(tmp_path):
    """Test that long string values are truncated when max_length is set."""
    long_str = "x" * 100
    def inner():
        s = long_str
        frame = inspect.currentframe()
        result = get_local_reprs(frame, max_length=10, normalize=False)
        # The repr should be truncated to 10 characters (including quotes)
        assert result["s"].startswith("'x" * 9)  # 9 x's plus opening quote
        assert result["s"].endswith("'")  # closing quote

    inner()


def test_get_local_reprs_with_watch(tmp_path):
    """Test that watch variables are merged and sorted correctly."""
    class DummyWatch:
        def items(self, frame, normalize):
            # Return a dict with a key that should appear after locals
            return {"z": 99}

    def inner():
        a = 1
        b = 2
        frame = inspect.currentframe()
        result = get_local_reprs(frame, watch=[DummyWatch()], max_length=None, normalize=False)
        # Order should be a, b, z
        assert list(result.keys()) == ["a", "b", "z"]
        assert result["z"] == "99"

    inner()
