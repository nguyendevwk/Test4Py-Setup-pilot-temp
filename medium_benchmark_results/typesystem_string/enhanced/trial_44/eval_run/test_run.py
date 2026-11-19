import pytest
from typesystem.fields import String
from typesystem.base import ValidationError

def test_string_trim_and_null_removal():
    f = String()
    # Leading/trailing whitespace is stripped
    assert f.validate("  hello  ") == "hello"
    # Null character is removed
    assert f.validate("he\0llo") == "hello"
    # After stripping and null removal, empty string triggers blank error
    with pytest.raises(ValidationError) as excinfo:
        f.validate("  \0  ")
    assert excinfo.value.code == "blank"
    # When allow_blank is True, empty string is accepted and returned as ""
    f_blank = String(allow_blank=True)
    assert f_blank.validate("  \0  ") == ""
