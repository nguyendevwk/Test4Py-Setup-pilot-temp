import pytest
from typesystem.tokenize.tokens import ScalarToken

def test_scalar_token_hash_consistency():
    """Hash of a ScalarToken should be deterministic and based on its value."""
    token_a = ScalarToken(value="foo", start_index=0, end_index=3)
    token_b = ScalarToken(value="foo", start_index=5, end_index=8)
    # Same value -> same hash
    assert hash(token_a) == hash(token_b)
    # Hash should be equal to hash of the underlying value
    assert hash(token_a) == hash("foo")

def test_scalar_token_hash_uniqueness():
    """Different values should produce different hash codes."""
    token_int = ScalarToken(value=42, start_index=0, end_index=2)
    token_str = ScalarToken(value="42", start_index=3, end_index=5)
    # Different types/values -> different hash
    assert hash(token_int) != hash(token_str)
    # Ensure hash matches the value's hash
    assert hash(token_int) == hash(42)
    assert hash(token_str) == hash("42")

def test_scalar_token_value_access():
    """The _get_value method should expose the stored value correctly."""
    token = ScalarToken(value=[1, 2, 3], start_index=0, end_index=5)
    # _get_value should return the exact value object
    assert token._get_value() is token._value
    # The returned value should be the same list instance
    assert token._get_value() == [1, 2, 3]
    # Changing the returned list should affect the token's value
    token._get_value().append(4)
    assert token._value == [1, 2, 3, 4]
