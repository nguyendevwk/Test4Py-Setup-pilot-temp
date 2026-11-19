import pytest
from typesystem.tokenize.tokens import ListToken, Token
from typesystem.base import Position

# Helper to create a simple Token that returns a known value
class SimpleToken(Token):
    def _get_value(self) -> int:
        return self._value

    def _get_child_token(self, key):
        raise NotImplementedError


def test_list_token_value_extraction():
    """ListToken should return a list of child token values."""
    # Create child tokens with integer values
    child_tokens = [SimpleToken(value=i, start_index=i, end_index=i) for i in range(3)]
    # Construct ListToken with the child tokens
    list_token = ListToken(value=child_tokens, start_index=0, end_index=2)
    # The _get_value method should return the list of child values
    assert list_token._get_value() == [0, 1, 2]


def test_list_token_child_access():
    """ListToken._get_child_token should return the correct child token."""
    child_tokens = [SimpleToken(value="a", start_index=0, end_index=0),
                    SimpleToken(value="b", start_index=1, end_index=1)]
    list_token = ListToken(value=child_tokens, start_index=0, end_index=1)
    # Access the second child token
    child = list_token._get_child_token(1)
    assert isinstance(child, SimpleToken)
    assert child._get_value() == "b"


def test_list_token_index_out_of_bounds():
    """Accessing an out-of-range index should raise IndexError."""
    child_tokens = [SimpleToken(value=42, start_index=0, end_index=0)]
    list_token = ListToken(value=child_tokens, start_index=0, end_index=0)
    with pytest.raises(IndexError):
        list_token._get_child_token(5)
