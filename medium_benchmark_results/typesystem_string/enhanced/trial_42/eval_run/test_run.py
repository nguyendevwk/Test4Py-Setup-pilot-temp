import pytest
from typesystem.fields import String

def test_string_default_set_when_allow_blank_and_no_default():
    # When allow_blank is True and no explicit default is provided,
    # the String field should automatically set its default to an empty string.
    field = String(allow_blank=True)
    # The field should now have a default attribute equal to "".
    assert hasattr(field, "default")
    assert field.default == ""
    # The has_default method should report that a default exists.
    assert field.has_default()
