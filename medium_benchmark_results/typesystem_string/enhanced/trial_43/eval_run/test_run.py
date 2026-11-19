import pytest
from typesystem.fields import String

def test_string_validate_none_with_allow_blank_returns_empty_string():
    # When allow_blank is True, validate(None) should return an empty string.
    f = String(allow_blank=True)
    result = f.validate(None)
    assert result == ""
    assert isinstance(result, str)
