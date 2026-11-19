import pytest
import typesystem
from typesystem.composites import OneOf
from typesystem.exceptions import ValidationError

def test_oneof_multiple_matches_raises_validation_error():
    field = OneOf([typesystem.Integer(), typesystem.Integer()])
    with pytest.raises(ValidationError) as excinfo:
        field.validate(5)
    assert "Matched more than one type." in str(excinfo.value)
