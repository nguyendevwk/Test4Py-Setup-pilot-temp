import pytest
from typesystem.tokenize.tokens import ListToken, Token
from typesystem.base import Position

# Helper token that simply returns its stored value
class DummyToken(Token):
    def __init__(self, value, start_index=0, end_index=0, content=''):
        super().__init__(value, start_index, end_index, content)

    def _get_value(self):
        return self._value

    def _get_child_token(self, key):
        return self._value[key]

def test_list_token_normal_behavior(tmp_path):
    # Create a ListToken containing three DummyTokens
    tokens = [
        DummyToken(1, 0, 1, '1'),
        DummyToken(2, 1, 2, '2'),
        DummyToken(3, 2, 3, '3')
    ]
    list_token = ListToken(tokens, 0, 3, '123')
    # _get_value should return the list of underlying values
    assert list_token._get_value() == [1, 2, 3]
    # _get_child_token should return the corresponding DummyToken
    child = list_token._get_child_token(1)
    assert isinstance(child, DummyToken)
    assert child._get_value() == 2

def test_list_token_empty_list(tmp_path):
    # Empty ListToken should return an empty list
    empty_token = ListToken([], 0, 0, '')
    assert empty_token._get_value() == []
    # Accessing any child should raise IndexError
    with pytest.raises(IndexError):
        empty_token._get_child_token(0)

def test_list_token_invalid_child_access(tmp_path):
    # ListToken with a single element
    single_token = ListToken([DummyToken('a', 0, 1, 'a')], 0, 1, 'a')
    # Accessing out-of-range index should raise IndexError
    with pytest.raises(IndexError):
        single_token._get_child_token(5)
