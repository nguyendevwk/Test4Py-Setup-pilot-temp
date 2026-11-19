import pytest
from typesystem.fields import String
from typesystem.base import ValidationError

def test_string_allow_blank_default_and_validation():
    # allow_blank without an explicit default should set default to empty string
    s = String(allow_blank=True)
    assert s.default == ""

    # validate(None) should coerce to empty string when allow_blank is True
    assert s.validate(None) == ""

    # validate("") should pass and return the empty string
    assert s.validate("") == ""

    # validate("  ") should be trimmed to empty string and pass
    assert s.validate("  ") == ""

    # When allow_blank is False, validate(None) should raise ValidationError
    s_no_blank = String(allow_blank=False)
    with pytest.raises(ValidationError) as excinfo:
        s_no_blank.validate(None)
    assert "null" in str(excinfo.value)
