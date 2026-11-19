import pytest
from typesystem.tokenize.tokens import DictToken, Token
from typesystem.base import Position


class DummyToken(Token):
    """A minimal Token implementation for testing purposes."""

    def __init__(self, value: str, position: Position | None = None):
        super().__init__(value=value, position=position)
        self._value = value

    def _get_value(self) -> str:
        return self._value


def test_dict_token_value_extraction():
    """Verify that DictToken correctly extracts values from child tokens."""
    key1 = DummyToken("k1")
    val1 = DummyToken("v1")
    key2 = DummyToken("k2")
    val2 = DummyToken("v2")

    d = {"k1": key1, "k2": key2}
    # The DictToken expects a mapping of key tokens to value tokens
    dict_token = DictToken(d)

    # _get_value should return a dict mapping key values to value values
    expected = {"k1": "v1", "k2": "v2"}
    assert dict_token._get_value() == expected


def test_dict_token_empty_and_child_access():
    """Test behavior with an empty dict and child token/key retrieval."""
    empty_dict_token = DictToken({})

    # Empty dict should yield an empty mapping
    assert empty_dict_token._get_value() == {}

    # Accessing a non-existent child should raise KeyError
    with pytest.raises(KeyError):
        empty_dict_token._get_child_token("missing")

    with pytest.raises(KeyError):
        empty_dict_token._get_key_token("missing")


def test_dict_token_child_token_retrieval():
    """Ensure that child tokens are correctly stored and retrievable."""
    key_token = DummyToken("key")
    value_token = DummyToken("value")
    mapping = {"key": key_token}
    dict_token = DictToken(mapping)

    # _get_child_token should return the value token associated with the key value
    assert dict_token._get_child_token("key") is value_token

    # _get_key_token should return the key token associated with the key value
    assert dict_token._get_key_token("key") is key_token
