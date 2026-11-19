import pytest
from typesystem.composites import OneOf
from typesystem.fields import String
from typesystem.base import ValidationError

def test_oneof_multiple_matches_raises_error():
    """
    OneOf should raise a ValidationError with code 'multiple_matches'
    when more than one child field validates the same value.
    """
    schema = OneOf([String(), String()])  # two identical string validators
    with pytest.raises(ValidationError) as excinfo:
        schema.validate_or_error("duplicate")
    # The ValidationError should carry the correct error message
    assert excinfo.value.text == "Matched more than one type."
    # If the ValidationError exposes a code attribute, it should match the key
    if hasattr(excinfo.value, "code"):
        assert excinfo.value.code == "multiple_matches"
