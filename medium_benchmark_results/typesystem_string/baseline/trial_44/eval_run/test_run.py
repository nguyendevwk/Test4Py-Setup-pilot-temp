import pytest
from typesystem.fields import String, ValidationError

def test_string_trim_and_allow_blank():
    # allow_blank=True: whitespace-only strings are coerced to empty string
    field = String(allow_blank=True, trim_whitespace=True)
    assert field.validate("   ") == ""
    assert field.validate("  abc  ") == "abc"
    # None is also coerced to empty string when allow_blank is True
    assert field.validate(None) == ""

    # allow_blank=False: whitespace-only strings raise a ValidationError
    field_no_blank = String(allow_blank=False, trim_whitespace=True)
    with pytest.raises(ValidationError) as excinfo:
        field_no_blank.validate("   ")
    assert excinfo.value.code == "blank"
