import pytest
from typesystem.tokenize.tokens import DictToken
from typesystem.base import Position

def test_dict_token_value_and_lookup():
    # Create a simple dictionary token with two key/value pairs
    content = '{"a": 1, "b": 2}'
    # Construct the underlying Token objects manually
    # For simplicity, use DictToken directly with a dict of Token-like objects
    class SimpleToken(DictToken):
        def _get_value(self):
            return self._value

    # Build child tokens
    a_token = SimpleToken(1, 0, 0, content)
    b_token = SimpleToken(2, 0, 0, content)
    dict_token = DictToken({"a": a_token, "b": b_token}, 0, len(content)-1, content)

    # The value property should return a plain dict
    assert dict_token.value == {"a": 1, "b": 2}

    # lookup should return the child token for a given key
    assert dict_token.lookup(["a"]) is a_token
    assert dict_token.lookup(["b"]) is b_token

    # lookup_key should return the key token (here same as child token)
    assert dict_token.lookup_key(["a"]) is a_token
    assert dict_token.lookup_key(["b"]) is b_token

def test_empty_dict_token():
    content = '{}'
    empty_token = DictToken({}, 0, len(content)-1, content)
    # Value should be an empty dict
    assert empty_token.value == {}
    # lookup on empty dict should raise KeyError
    with pytest.raises(KeyError):
        empty_token.lookup(["missing"])
    # lookup_key on empty dict should raise KeyError
    with pytest.raises(KeyError):
        empty_token.lookup_key(["missing"])

def test_dict_token_position_and_repr():
    content = '{"x": 10}'
    x_token = DictToken(10, 0, 0, content)
    dict_token = DictToken({"x": x_token}, 0, len(content)-1, content)

    # start and end positions should be correct
    start_pos = dict_token.start
    end_pos = dict_token.end
    assert isinstance(start_pos, Position)
    assert isinstance(end_pos, Position)
    assert start_pos.index == 0
    assert end_pos.index == len(content)-1

    # string property should return the full content slice
    assert dict_token.string == content

    # __repr__ should include class name and string
    repr_str = repr(dict_token)
    assert repr_str.startswith("DictToken(")
    assert content in repr_str
