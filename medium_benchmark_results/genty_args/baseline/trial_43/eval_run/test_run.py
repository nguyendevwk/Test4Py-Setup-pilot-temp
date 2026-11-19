import pytest
from genty.genty_args import genty_args, GentyArgs

def test_genty_args_returns_correct_object_and_attributes():
    # No arguments
    ga = genty_args()
    assert isinstance(ga, GentyArgs)
    assert ga.args == ()
    assert ga.kwargs == {}

    # Positional arguments only
    ga2 = genty_args('a', 1, 2.5)
    assert isinstance(ga2, GentyArgs)
    assert ga2.args == ('a', 1, 2.5)
    assert ga2.kwargs == {}

    # Keyword arguments only
    ga3 = genty_args(x=10, y='test')
    assert isinstance(ga3, GentyArgs)
    assert ga3.args == ()
    assert ga3.kwargs == {'x': 10, 'y': 'test'}

    # Mixed positional and keyword arguments
    ga4 = genty_args('foo', bar='baz', num=42)
    assert isinstance(ga4, GentyArgs)
    assert ga4.args == ('foo',)
    assert ga4.kwargs == {'bar': 'baz', 'num': 42}

    # Ensure distinct instances
    assert ga2 is not ga3
