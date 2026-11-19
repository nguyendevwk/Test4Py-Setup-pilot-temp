import pytest
from typesystem.tokenize.tokens import ScalarToken

def test_scalar_token_hash_and_value():
    """ScalarToken should hash its underlying value and expose it via _get_value."""
    token_int = ScalarToken(42)
    token_str = ScalarToken("hello")
    token_none = ScalarToken(None)

    # Hash should match Python's hash of the value
    assert hash(token_int) == hash(42)
    assert hash(token_str) == hash("hello")
    assert hash(token_none) == hash(None)

    # _get_value should return the original value
    assert token_int._get_value() == 42
    assert token_str._get_value() == "hello"
    assert token_none._get_value() is None

def test_scalar_token_hash_equality_and_uniqueness():
    """Tokens with the same value should have equal hash; different values should differ."""
    token_a1 = ScalarToken("same")
    token_a2 = ScalarToken("same")
    token_b = ScalarToken("different")

    # Same value -> same hash
    assert hash(token_a1) == hash(token_a2)
    # Different value -> different hash
    assert hash(token_a1) != hash(token_b)

    # Ensure that equality of hash does not imply object equality
    assert token_a1 is not token_a2

def test_scalar_token_boundary_large_and_complex_values():
    """Test hashing and value retrieval for large integers and complex objects."""
    large_int = 10**100  # very large integer
    token_large = ScalarToken(large_int)
    assert hash(token_large) == hash(large_int)
    assert token_large._get_value() == large_int

    # Use a tuple as a complex value (hashable)
    complex_value = (1, 2, 3)
    token_complex = ScalarToken(complex_value)
    assert hash(token_complex) == hash(complex_value)
    assert token_complex._get_value() == complex_value
