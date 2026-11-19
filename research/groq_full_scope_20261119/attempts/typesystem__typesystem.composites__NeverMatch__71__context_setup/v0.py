import pytest
from typesystem.composites import NeverMatch
from typesystem.fields import Field


def test_never_match_validation_error():
    """NeverMatch.validate always raises a ValidationError with the correct message."""
    field = NeverMatch()
    with pytest.raises(field.ValidationError) as excinfo:
        field.validate("anything")
    # The error message should come from the `errors` mapping
    assert str(excinfo.value) == "This never validates."


def test_never_match_constructor_disallows_allow_null():
    """Passing allow_null to the constructor should raise an AssertionError."""
    with pytest.raises(AssertionError):
        NeverMatch(allow_null=True)


def test_never_match_errors_dict_contains_never_key():
    """The errors dictionary should contain the key 'never'."""
    assert "never" in NeverMatch.errors
    assert NeverMatch.errors["never"] == "This never validates."
