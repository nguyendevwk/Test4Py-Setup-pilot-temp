import pytest
from typesystem.tokenize.tokens import ScalarToken
from typesystem.base import Position

# Helper to create a dummy Position (line 1, column 1)
def dummy_position():
    return Position(1, 1)

def test_scalar_token_hash_consistency():
    """Hash of a ScalarToken should be stable across multiple calls."""
    token = ScalarToken("example", dummy_position())
    first_hash = hash(token)
    second_hash = hash(token)
    assert first_hash == second_hash, "Hash should be deterministic"

def test_scalar_token_value_access():
    """_get_value should return the original value passed to the token."""
    value = 42
    token = ScalarToken(value, dummy_position())
    assert token._get_value() == value, "Value retrieved should match the original"

def test_scalar_token_hash_difference():
    """Tokens with different values should produce different hash values."""
    token_a = ScalarToken("foo", dummy_position())
    token_b = ScalarToken("bar", dummy_position())
    assert hash(token_a) != hash(token_b), "Different values should yield different hashes"
