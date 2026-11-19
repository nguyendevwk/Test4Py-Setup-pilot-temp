import pytest
from typesystem.composites import NeverMatch
from typesystem.fields import Field

def test_never_match_validation_error():
    field = NeverMatch()
    with pytest.raises(field.ValidationError) as excinfo:
        field.validate("anything")
    assert excinfo.value.code == "never"
    assert str(excinfo.value) == "This never validates."

def test_never_match_constructor_disallows_allow_null():
    with pytest.raises(AssertionError):
        NeverMatch(allow_null=True)

def test_never_match_errors_dict_present():
    field = NeverMatch()
    assert isinstance(field.errors, dict)
    assert "never" in field.errors
    assert field.errors["never"] == "This never validates."
