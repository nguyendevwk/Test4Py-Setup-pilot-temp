import sys
import types
import pytest

# Provide a minimal stub for the external `six` dependency required by genty.
six_stub = types.SimpleNamespace(
    iteritems=lambda d: d.items(),
    string_types=(str,),
    text_type=str,
    binary_type=bytes,
    PY3=True,
)
sys.modules["six"] = six_stub

from genty.genty_args import GentyArgs


def test_genty_args_iteration_and_properties():
    g = GentyArgs(1, "foo", key="bar", num=42, other="baz")

    # Stored args and kwargs
    assert g.args == (1, "foo")
    assert g.kwargs == {"key": "bar", "num": 42, "other": "baz"}

    # Expected formatted strings
    expected = [
        "1",
        "'foo'",
        "key='bar'",
        "num=42",
        "other='baz'",
    ]

    # Iteration yields the expected sequence
    assert list(g) == expected

    # `iter(g)` returns an iterator object
    it = iter(g)
    assert hasattr(it, "__next__")

    # Empty GentyArgs yields no items
    empty = GentyArgs()
    assert empty.args == ()
    assert empty.kwargs == {}
    assert list(empty) == []

    # Correct number of items
    assert len(list(g)) == len(expected)
