# Module: genty.genty_args
import pytest
from genty.genty_args import genty_args, GentyArgs

def test_genty_args_with_positional_args_only():
    result = genty_args('a1', 'b1', 1, 'd1')
    assert isinstance(result, GentyArgs)
    assert result.args == ('a1', 'b1', 1, 'd1')
    assert result.kwargs == {}

def test_genty_args_with_keyword_args_only():
    result = genty_args(d='d2', c='c2')
    assert isinstance(result, GentyArgs)
    assert result.args == ()
    assert result.kwargs == {'d': 'd2', 'c': 'c2'}

def test_genty_args_with_mixed_args():
    result = genty_args('a3', 'b3', c='c3', d='d3')
    assert isinstance(result, GentyArgs)
    assert result.args == ('a3', 'b3')
    assert result.kwargs == {'c': 'c3', 'd': 'd3'}

def test_genty_args_with_default_positional_args():
    result = genty_args('a4', 'b4')
    assert isinstance(result, GentyArgs)
    assert result.args == ('a4', 'b4')
    assert result.kwargs == {}

def test_genty_args_with_default_args():
    result = genty_args()
    assert isinstance(result, GentyArgs)
    assert result.args == ()
    assert result.kwargs == {}

def test_genty_args_with_complex_combination():
    result = genty_args('a5', 'b5', 5, c='c5', d='d5', e='e5')
    assert isinstance(result, GentyArgs)
    assert result.args == ('a5', 'b5', 5)
    assert result.kwargs == {'c': 'c5', 'd': 'd5', 'e': 'e5'}

def test_genty_args_with_mixed_data_types():
    result = genty_args(10, 'string', True, [1, 2, 3], {'key': 'value'}, None)
    assert isinstance(result, GentyArgs)
    assert result.args == (10, 'string', True, [1, 2, 3], {'key': 'value'}, None)
    assert result.kwargs == {}
