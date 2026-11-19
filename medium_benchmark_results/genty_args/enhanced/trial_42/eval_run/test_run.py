import pytest
from genty.genty_args import genty_args, GentyArgs


def test_genty_args_iteration_and_properties():
    # Create GentyArgs with mixed positional and keyword arguments
    ga = genty_args('foo', 42, bar='baz', alpha=1)

    # Verify the returned object is an instance of GentyArgs
    assert isinstance(ga, GentyArgs)

    # Positional arguments should be stored as a tuple
    assert ga.args == ('foo', 42)

    # Keyword arguments should be stored as a dict
    assert ga.kwargs == {'bar': 'baz', 'alpha': 1}

    # Iteration should yield formatted positional args followed by sorted kwargs
    # format_arg('foo') -> "'foo'", format_arg(42) -> '42'
    # format_kwarg('alpha', 1) -> 'alpha=1', format_kwarg('bar', 'baz') -> "bar='baz'"
    expected = ["'foo'", '42', 'alpha=1', "bar='baz'"]
    assert list(ga) == expected
