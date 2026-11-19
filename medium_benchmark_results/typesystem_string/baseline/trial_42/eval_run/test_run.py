import pytest
from typesystem.fields import String
from typesystem.base import ValidationError

def test_string_allow_blank_coerces_none_to_empty_string():
    # When allow_blank is True and no default is set, default becomes an empty string.
    field = String(allow_blank=True)
    assert field.default == ""

    # validate(None) should return an empty string because allow_blank is True.
    assert field.validate(None) == ""

    # validate("") should also return an empty string (no trimming needed).
    assert field.validate("") == ""

    # If coerce_types is disabled, validate(None) should raise a ValidationError.
    field_no_coerce = String(allow_blank=True, coerce_types=False)
    with pytest.raises(ValidationError) as excinfo:
        field_no_coerce.validate(None)
    assert excinfo.value.code == "null"
