import pytest
from genty.genty_args import GentyArgs


def test_genty_args_iteration_and_properties():
    # Instantiate with a mix of positional and keyword arguments
    g = GentyArgs(1, "foo", key="bar", num=42, other="baz")

    # Verify that the stored args and kwargs match the constructor inputs
    assert g.args == (1, "foo")
    assert g.kwargs == {"key": "bar", "num": 42, "other": "baz"}

    # Expected formatted strings: positional args first, then sorted kwargs
    expected = [
        "1",          # format_arg(1) -> '1'
        "'foo'",      # format_arg('foo') -> "'foo'"
        "key='bar'",  # format_kwarg('key', 'bar')
        "num=42",     # format_kwarg('num', 42)
        "other='baz'",# format_kwarg('other', 'baz')
    ]

    # Iteration should yield the expected sequence
    assert list(g) == expected

    # Iteration should produce an iterator object
    it = iter(g)
    assert hasattr(it, "__next__")

    # Iterating over an empty GentyArgs yields no items
    empty = GentyArgs()
    assert empty.args == ()
    assert empty.kwargs == {}
    assert list(empty) == []

    # Ensure that the iterator yields the correct number of items
    assert len(list(g)) == len(expected)
