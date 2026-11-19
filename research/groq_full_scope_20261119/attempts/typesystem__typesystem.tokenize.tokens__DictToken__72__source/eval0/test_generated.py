import pytest
from typesystem.tokenize.tokens import DictToken, Token
from typesystem.base import Position


class DummyToken(Token):
    """Simple Token implementation for testing purposes."""

    def __init__(self, value):
        # Position is not used in these tests; provide a dummy one.
        super().__init__(Position(0, 0), value)

    def _get_value(self):
        return self._value


def test_dict_token_normal_behavior(tmp_path):
    """Verify that DictToken correctly stores and retrieves key/value tokens."""
    # Create key and value tokens
    key1 = DummyToken("first")
    key2 = DummyToken("second")
    val1 = DummyToken(1)
    val2 = DummyToken(2)

    # Construct the underlying dict mapping key tokens to value tokens
    underlying = {key1: val1, key2: val2}

    # Instantiate DictToken
    dict_token = DictToken(underlying)

    # _get_value should return a plain dict with resolved values
    expected = {"first": 1, "second": 2}
    assert dict_token._get_value() == expected

    # _get_child_token should return the original value token
    assert dict_token._get_child_token("first") is val1
    assert dict_token._get_child_token("second") is val2

    # _get_key_token should return the original key token
    assert dict_token._get_key_token("first") is key1
    assert dict_token._get_key_token("second") is key2


def test_dict_token_empty(tmp_path):
    """An empty DictToken should return an empty dict and have no child tokens."""
    empty_dict_token = DictToken({})
    assert empty_dict_token._get_value() == {}
    # No keys to retrieve; accessing any key should raise KeyError
    with pytest.raises(KeyError):
        empty_dict_token._get_child_token("any")
    with pytest.raises(KeyError):
        empty_dict_token._get_key_token("any")


def test_dict_token_missing_key_error(tmp_path):
    """Accessing a non‑existent key should raise KeyError."""
    key = DummyToken("existing")
    val = DummyToken(42)
    dict_token = DictToken({key: val})

    # Existing key works
    assert dict_token._get_child_token("existing") is val

    # Missing key raises KeyError
    with pytest.raises(KeyError):
        dict_token._get_child_token("missing")
    with pytest.raises(KeyError):
        dict_token._get_key_token("missing")
