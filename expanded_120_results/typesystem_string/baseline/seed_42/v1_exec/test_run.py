import pytest
from typesystem.fields import String

def test_string_validate_strips_null_and_whitespace():
    """Validate that null characters and surrounding whitespace are removed."""
    field = String(trim_whitespace=True, allow_blank=False)
    # Input contains null characters and leading/trailing whitespace
    raw = "\0  abc  \0"
    # Expected output after stripping nulls and trimming whitespace
    expected = "abc"
    result = field.validate(raw)
    assert result == expected, f"Expected '{expected}', got '{result}'"
