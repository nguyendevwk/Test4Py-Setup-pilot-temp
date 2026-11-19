import pytest
from typesystem.tokenize.tokens import ScalarToken


def test_scalar_token_hash_and_value():
    """Hash should be based on the underlying value and value property returns it."""
    token = ScalarToken(value=42, start_index=0, end_index=0, content="42")
    assert token.value == 42
    assert hash(token) == hash(42)
    # Two tokens with same value but different positions should still hash the same
    token2 = ScalarToken(value=42, start_index=1, end_index=1, content="42")
    assert hash(token2) == hash(token)
    # But they are not equal because positions differ
    assert token != token2


def test_scalar_token_string_and_position():
    """The string property should slice the content correctly and positions should be accurate."""
    content = "abcde"
    token = ScalarToken(value="c", start_index=2, end_index=2, content=content)
    assert token.string == "c"
    # Position line and column for single line content
    assert token.start.line_no == 1
    assert token.start.column_no == 3
    assert token.end.line_no == 1
    assert token.end.column_no == 3
    # Multi-line content
    multi = "line1\nline2\nline3"
    token2 = ScalarToken(value="2", start_index=7, end_index=7, content=multi)
    assert token2.string == "2"
    assert token2.start.line_no == 2
    assert token2.start.column_no == 2
    assert token2.end.line_no == 2
    assert token2.end.column_no == 2


def test_scalar_token_equality_and_repr():
    """Equality should compare value and positions; repr should include class name and string."""
    token_a = ScalarToken(value="x", start_index=0, end_index=0, content="x")
    token_b = ScalarToken(value="x", start_index=0, end_index=0, content="x")
    token_c = ScalarToken(value="y", start_index=0, end_index=0, content="y")
    token_d = ScalarToken(value="x", start_index=1, end_index=1, content="x")
    # Equal tokens
    assert token_a == token_b
    # Different value
    assert token_a != token_c
    # Same value, different position
    assert token_a != token_d
    # Representation includes class name and string
    assert repr(token_a).startswith("ScalarToken('x')")
    assert "x" in repr(token_a)
