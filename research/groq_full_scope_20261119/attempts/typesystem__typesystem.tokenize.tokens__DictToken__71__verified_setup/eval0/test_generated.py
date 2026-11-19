import pytest
from typesystem.tokenize.tokens import DictToken, Token

# Helper token that simply stores a value and returns it via _get_value
class SimpleToken(Token):
    def __init__(self, value):
        super().__init__(value=value)

    def _get_value(self):
        return self._value


def test_dict_token_normal_behavior():
    # Create simple key/value tokens
    key1 = SimpleToken("a")
    val1 = SimpleToken(1)
    key2 = SimpleToken("b")
    val2 = SimpleToken(2)

    # Construct a DictToken with a mapping of key tokens to value tokens
    dtoken = DictToken({key1: val1, key2: val2})

    # _get_value should return a plain dict with underlying values
    assert dtoken._get_value() == {"a": 1, "b": 2}

    # _get_child_token should retrieve the value token by key value
    assert dtoken._get_child_token("a") is val1
    assert dtoken._get_child_token("b") is val2

    # _get_key_token should retrieve the key token by key value
    assert dtoken._get_key_token("a") is key1
    assert dtoken._get_key_token("b") is key2


def test_dict_token_empty_dict():
    # Empty dictionary should produce empty mappings
    dtoken = DictToken({})

    # _get_value should be an empty dict
    assert dtoken._get_value() == {}

    # Accessing any key should raise KeyError
    with pytest.raises(KeyError):
        dtoken._get_child_token("missing")
    with pytest.raises(KeyError):
        dtoken._get_key_token("missing")


def test_dict_token_error_on_invalid_key():
    # Create a single key/value token
    key = SimpleToken("x")
    val = SimpleToken(42)
    dtoken = DictToken({key: val})

    # Accessing a non-existent key should raise KeyError
    with pytest.raises(KeyError):
        dtoken._get_child_token("y")
    with pytest.raises(KeyError):
        dtoken._get_key_token("y")
