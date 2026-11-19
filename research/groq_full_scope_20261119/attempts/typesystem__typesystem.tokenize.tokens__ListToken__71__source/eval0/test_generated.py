import pytest
from typesystem.tokenize.tokens import ListToken

# Helper dummy token that mimics the interface of Token
class DummyToken:
    def __init__(self, value):
        self._value = value

    def _get_value(self):
        return self._value

def test_list_token_value():
    """ListToken should return a list of child token values."""
    tokens = [DummyToken(1), DummyToken("a"), DummyToken(3.14)]
    lt = ListToken(tokens)
    assert lt._get_value() == [1, "a", 3.14]

def test_child_token_access():
    """_get_child_token should return the correct child token."""
    tokens = [DummyToken("x"), DummyToken("y")]
    lt = ListToken(tokens)
    child = lt._get_child_token(1)
    assert isinstance(child, DummyToken)
    assert child._get_value() == "y"

def test_child_token_out_of_range():
    """Accessing an out-of-range index should raise IndexError."""
    tokens = [DummyToken(42)]
    lt = ListToken(tokens)
    with pytest.raises(IndexError):
        lt._get_child_token(5)
