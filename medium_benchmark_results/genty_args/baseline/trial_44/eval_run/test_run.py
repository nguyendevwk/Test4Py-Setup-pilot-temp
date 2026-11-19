import pytest

def test_genty_args_returns_correct_container():
    from genty.genty_args import genty_args, GentyArgs

    # Test with positional and keyword arguments
    ga = genty_args('x', y=10)
    assert isinstance(ga, GentyArgs)
    assert ga.args == ('x',)
    assert ga.kwargs == {'y': 10}
    rep = repr(ga)
    assert isinstance(rep, str)
    assert 'x' in rep
    assert 'y=10' in rep

    # Test with no arguments
    ga_empty = genty_args()
    assert ga_empty.args == ()
    assert ga_empty.kwargs == {}
