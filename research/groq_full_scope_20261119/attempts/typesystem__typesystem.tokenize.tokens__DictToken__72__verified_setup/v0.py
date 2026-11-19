import pytest
from typesystem.tokenize.tokens import DictToken, StringToken, Token

# Helper to create a simple token that behaves like StringToken
# (StringToken is assumed to exist in the package and accepts a string value)
def make_string_token(value: str) -> Token:
    return StringToken(value=value)

def test_dict_token_value_extraction():
    # Create a dictionary of tokens: {"a": "1", "b": "2"}
    key_a = make_string_token("a")
    key_b = make_string_token("b")
    val_1 = make_string_token("1")
    val_2 = make_string_token("2")
    token_dict = {key_a: val_1, key_b: val_2}

    # Instantiate DictToken with the token dictionary
    dict_token = DictToken(value=token_dict)

    # The _get_value method should return a plain dict with underlying values
    expected = {"a": "1", "b": "2"}
    assert dict_token._get_value() == expected

def test_dict_token_child_and_key_tokens():
    # Create tokens for keys and values
    key_x = make_string_token("x")
    key_y = make_string_token("y")
    val_x = make_string_token("10")
    val_y = make_string_token("20")
    token_dict = {key_x: val_x, key_y: val_y}

    dict_token = DictToken(value=token_dict)

    # _get_child_token should return the value token for a given key value
    assert dict_token._get_child_token("x") is val_x
    assert dict_token._get_child_token("y") is val_y

    # _get_key_token should return the key token for a given key value
    assert dict_token._get_key_token("x") is key_x
    assert dict_token._get_key_token("y") is key_y

def test_dict_token_missing_key_raises():
    # Create a simple dictionary with one key-value pair
    key_k = make_string_token("k")
    val_k = make_string_token("100")
    token_dict = {key_k: val_k}

    dict_token = DictToken(value=token_dict)

    # Accessing a non-existent key should raise a KeyError
    with pytest.raises(KeyError):
        dict_token._get_child_token("missing")
    with pytest.raises(KeyError):
        dict_token._get_key_token("missing")
