import pytest
from genty.genty_args import GentyArgs

def test_genty_args_iteration_and_properties():
    g = GentyArgs(1, 'two', key='val', another=3)
    assert g.args == (1, 'two')
    assert g.kwargs == {'key': 'val', 'another': 3}
    assert list(g) == ['1', "'two'", 'another=3', "key='val'"]
    g_empty = GentyArgs()
    assert list(g_empty) == []
