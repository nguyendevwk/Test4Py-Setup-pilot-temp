import pytest
from typesystem.composites import OneOf
from typesystem.fields import String, Integer


class DummyField:
    def validate_or_error(self, value):
        return value, None


def test_oneof_behavior():
    schema = OneOf([String(), Integer()])

    # Exactly one match
    val, err = schema.validate_or_error('text')
    assert err is None
    assert val == 'text'

    # No match
    val, err = schema.validate_or_error(3.14)
    assert err is not None
    assert err.args[0] == OneOf.errors['no_match']

    # Multiple matches
    schema_multi = OneOf([String(), DummyField()])
    val, err = schema_multi.validate_or_error('text')
    assert err is not None
    assert err.args[0] == OneOf.errors['multiple_matches']

    # allow_null not allowed in constructor
    with pytest.raises(AssertionError):
        OneOf([String()], allow_null=True)
