import pytest
from typesystem.composites import OneOf
from typesystem.fields import String

def test_oneof_returns_first_match_when_multiple_match():
    """
    When multiple child validators match the same value, OneOf should
    return the value validated by the first matching child without raising.
    """
    schema = OneOf([String(), String()])  # two identical string validators
    result = schema.validate_or_error("duplicate")
    assert result == "duplicate"
    assert isinstance(result, str)
