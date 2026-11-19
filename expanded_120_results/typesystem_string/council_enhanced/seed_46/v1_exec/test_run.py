import pytest
from typesystem.fields import String
from typesystem.exceptions import ValidationError

def test_string_allow_blank_and_default_and_validation():
    s = String(allow_blank=True)
    assert s.has_default()
    assert s.default == ""
    assert s.validate(None) == ""
    assert s.validate("") == ""
    assert s.validate("  abc  ") == "abc"
    assert s.validate("a\0b") == "ab"

    s_no_blank = String(allow_blank=False)
    with pytest.raises(ValidationError) as excinfo:
        s_no_blank.validate("")
    assert excinfo.value.code == "blank"
