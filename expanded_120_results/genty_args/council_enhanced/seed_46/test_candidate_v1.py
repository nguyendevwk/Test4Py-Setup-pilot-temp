import pytest
from genty.genty_args import GentyArgs

def test_genty_args_properties_and_iteration():
    g = GentyArgs(1, 'two', 3.0, flag=True, name='Alice')
    # Check stored positional and keyword arguments
    assert isinstance(g.args, tuple)
    assert g.args == (1, 'two', 3.0)
    assert isinstance(g.kwargs, dict)
    assert g.kwargs == {'flag': True, 'name': 'Alice'}

    # Iteration yields formatted args followed by sorted kwargs
    iterated = list(g)
    assert iterated == ['1', "'two'", '3.0', 'flag=True', "name='Alice'"]
    assert iterated[:3] == ['1', "'two'", '3.0']
    assert iterated[3:] == ['flag=True', "name='Alice'"]

    # Empty GentyArgs behaves correctly
    empty = GentyArgs()
    assert empty.args == ()
    assert empty.kwargs == {}
    assert list(empty) == []
