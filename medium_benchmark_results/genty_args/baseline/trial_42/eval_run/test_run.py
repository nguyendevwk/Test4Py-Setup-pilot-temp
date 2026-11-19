import pytest
from genty.genty_args import genty_args, GentyArgs

def test_genty_args_returns_correct_object():
    # Test with positional and keyword arguments
    obj = genty_args('foo', 'bar', 42, key='value')
    assert isinstance(obj, GentyArgs)
    # The GentyArgs instance should expose the original args and kwargs
    assert hasattr(obj, 'args')
    assert hasattr(obj, 'kwargs')
    assert obj.args == ('foo', 'bar', 42)
    assert obj.kwargs == {'key': 'value'}

    # Test with only keyword arguments
    obj_kw = genty_args(x=1, y=2)
    assert isinstance(obj_kw, GentyArgs)
    assert obj_kw.args == ()
    assert obj_kw.kwargs == {'x': 1, 'y': 2}

    # Test with no arguments
    obj_none = genty_args()
    assert isinstance(obj_none, GentyArgs)
    assert obj_none.args == ()
    assert obj_none.kwargs == {}
