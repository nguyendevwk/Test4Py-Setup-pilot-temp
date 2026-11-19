import pytest
from typesystem.tokenize.tokens import ScalarToken

def test_scalar_token_hash_and_value():
    token = ScalarToken(value=42, start_index=0, end_index=0, content="42")
    # Hash should be based on the underlying value
    assert hash(token) == hash(42)
    # The value property should return the original value
    assert token.value == 42

def test_scalar_token_equality_and_repr():
    token_a = ScalarToken(value="foo", start_index=1, end_index=3, content="foo")
    token_b = ScalarToken(value="foo", start_index=1, end_index=3, content="foo")
    token_c = ScalarToken(value="bar", start_index=1, end_index=3, content="bar")
    # Tokens with same value and indices are equal
    assert token_a == token_b
    # Tokens with different values are not equal
    assert token_a != token_c
    # Representation should include class name and string slice
    assert repr(token_a) == "ScalarToken(foo)"

def test_scalar_token_string_and_position():
    content = "abcde"
    token = ScalarToken(value="c", start_index=2, end_index=2, content=content)
    # The string property should return the slice from content
    assert token.string == "c"
    # The start and end positions should correspond to the same index
    assert token.start.index == 2
    assert token.end.index == 2
    # The line and column numbers should be 1 and 3 respectively (zero-based index +1)
    assert token.start.line_no == 1
    assert token.start.column_no == 3
    assert token.end.line_no == 1
    assert token.end.column_no == 3
