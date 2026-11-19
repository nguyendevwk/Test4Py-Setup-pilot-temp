import pytest
from typesystem.fields import String

def test_string_validate_none_with_allow_blank_and_coerce_types():
    # When allow_blank is True and coerce_types is True, None should be coerced to an empty string.
    field = String(allow_blank=True, coerce_types=True)
    assert field.validate(None) == ""

    # When coerce_types is False, None should raise a validation error.
    field_no_coerce = String(allow_blank=True, coerce_types=False)
    with pytest.raises(Exception) as excinfo:
        field_no_coerce.validate(None)
    assert "May not be null." in str(excinfo.value)
