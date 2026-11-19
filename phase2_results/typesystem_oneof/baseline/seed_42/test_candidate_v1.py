import pytest
from typesystem.composites import OneOf
from typesystem import fields
from typesystem.exceptions import ValidationError

def test_oneof_validate_behavior():
    int_field = fields.Integer()
    str_field = fields.String()
    oneof = OneOf([int_field, str_field])

    # Exactly one match: integer
    assert oneof.validate(5) == 5

    # Exactly one match: string
    assert oneof.validate("hello") == "hello"

    # Multiple matches: two integer fields
    int_field2 = fields.Integer()
    oneof_multi = OneOf([int_field, int_field2])
    with pytest.raises(ValidationError) as excinfo:
        oneof_multi.validate(5)
    assert "multiple_matches" in str(excinfo.value)

    # No match: boolean
    with pytest.raises(ValidationError) as excinfo:
        oneof.validate(True)
    assert "no_match" in str(excinfo.value)
