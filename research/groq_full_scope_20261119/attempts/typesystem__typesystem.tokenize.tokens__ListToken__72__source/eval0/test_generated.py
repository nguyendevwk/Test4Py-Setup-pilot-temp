import pytest
from typesystem.tokenize.tokens import Token, ListToken


class DummyToken(Token):
    """Simple Token implementation for testing purposes."""

    def __init__(self, value):
        self._value = value

    def _get_value(self):
        return self._value


def test_list_token_value_and_child_access():
    """Verify that ListToken correctly aggregates child values and returns child tokens."""
    child_tokens = [DummyToken(i) for i in range(3)]
    list_token = ListToken(child_tokens)

    # _get_value should return a list of the child values
    assert list_token._get_value() == [0, 1, 2]

    # _get_child_token should return the exact child token instance
    for idx, child in enumerate(child_tokens):
        assert list_token._get_child_token(idx) is child


def test_list_token_empty_and_boundary():
    """Test ListToken behavior with an empty list and boundary indices."""
    empty_token = ListToken([])
    # Empty list should yield an empty list of values
    assert empty_token._get_value() == []

    # Accessing any index should raise IndexError
    with pytest.raises(IndexError):
        empty_token._get_child_token(0)

    # Boundary test: single element list
    single = ListToken([DummyToken('only')])
    assert single._get_value() == ['only']
    assert single._get_child_token(0)._get_value() == 'only'


def test_list_token_invalid_key_type():
    """Ensure that providing a non-integer key raises a TypeError."""
    tokens = [DummyToken('a'), DummyToken('b')]
    list_token = ListToken(tokens)

    # Using a string key should raise a TypeError when accessing child token
    with pytest.raises(TypeError):
        list_token._get_child_token('invalid')
