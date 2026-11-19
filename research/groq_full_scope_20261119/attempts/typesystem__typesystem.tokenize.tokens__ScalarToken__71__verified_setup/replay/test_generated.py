import pytest
from typesystem.tokenize.tokens import ScalarToken
from typesystem.base import Position

def test_scalar_token_hash_consistency(tmp_path):
    # Create a temporary file to use as content
    tmp_file = tmp_path / "content.txt"
    tmp_file.write_text("example content")
    content = tmp_file.read_text()

    token = ScalarToken(value=42, start_index=0, end_index=2, content=content)
    # Hash should be deterministic and based on the value
    expected_hash = hash(42)
    assert hash(token) == expected_hash
    # Recompute hash to ensure consistency
    assert hash(token) == expected_hash

def test_scalar_token_value_retrieval(tmp_path):
    tmp_file = tmp_path / "content.txt"
    tmp_file.write_text("another example")
    content = tmp_file.read_text()

    token = ScalarToken(value="hello", start_index=5, end_index=10, content=content)
    # The protected method _get_value should return the original value
    assert token._get_value() == "hello"
    # Ensure the value is stored correctly in the token's internal state
    assert token._value == "hello"

def test_scalar_token_hash_difference(tmp_path):
    tmp_file = tmp_path / "content.txt"
    tmp_file.write_text("diff content")
    content = tmp_file.read_text()

    token_a = ScalarToken(value="foo", start_index=1, end_index=3, content=content)
    token_b = ScalarToken(value="bar", start_index=1, end_index=3, content=content)
    # Hashes for different values should differ
    assert hash(token_a) != hash(token_b)
    # Ensure that tokens with the same value have the same hash
    token_c = ScalarToken(value="foo", start_index=4, end_index=6, content=content)
    assert hash(token_a) == hash(token_c)
