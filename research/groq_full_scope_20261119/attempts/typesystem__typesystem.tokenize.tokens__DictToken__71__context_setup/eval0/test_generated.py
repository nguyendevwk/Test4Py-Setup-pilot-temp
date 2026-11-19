import pytest
from typesystem.tokenize.tokens import DictToken, Token
from typesystem.base import Position

# Helper to create simple leaf tokens
def leaf(value, start, end, content=""):
    return Token(value, start, end, content)

def test_dict_token_value_and_lookup():
    # Construct a DictToken with two key/value pairs
    key1 = leaf("a", 0, 0, "a")
    val1 = leaf(1, 1, 1, "1")
    key2 = leaf("b", 2, 2, "b")
    val2 = leaf(2, 3, 3, "2")
    dtoken = DictToken({key1: val1, key2: val2}, 0, 3, "a1b2")

    # value property should return a plain dict
    assert dtoken.value == {"a": 1, "b": 2}

    # lookup should retrieve the value token by key
    assert dtoken.lookup(["a"]) is val1
    assert dtoken.lookup(["b"]) is val2

    # lookup_key should retrieve the key token
    assert dtoken.lookup_key(["a"]) is key1
    assert dtoken.lookup_key(["b"]) is key2

def test_dict_token_equality_and_repr():
    key = leaf("x", 0, 0, "x")
    val = leaf(42, 1, 1, "42")
    t1 = DictToken({key: val}, 0, 1, "x42")
    t2 = DictToken({key: val}, 0, 1, "x42")
    t3 = DictToken({key: val}, 0, 1, "x42")

    # Tokens with identical structure and indices are equal
    assert t1 == t2
    assert t2 == t3
    assert t1 == t3

    # Representation should include class name and string slice
    assert repr(t1).startswith("DictToken(")
    assert t1.string == "x42"

def test_dict_token_position_and_error():
    key = leaf("k", 0, 0, "k")
    val = leaf("v", 1, 1, "v")
    dtoken = DictToken({key: val}, 0, 1, "kv")

    # start and end positions should be correct
    assert dtoken.start == Position(1, 1, 0)
    assert dtoken.end == Position(1, 2, 1)

    # Accessing a non-existent key should raise KeyError
    with pytest.raises(KeyError):
        dtoken._get_child_token("missing")
    with pytest.raises(KeyError):
        dtoken._get_key_token("missing")
