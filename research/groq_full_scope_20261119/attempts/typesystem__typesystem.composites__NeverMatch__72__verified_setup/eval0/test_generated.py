import pytest
from typesystem.composites import NeverMatch
from typesystem.fields import Field

def test_nevermatch_raises_validation_error():
    """NeverMatch.validate should always raise a ValidationError with the correct key."""
    field = NeverMatch()
    with pytest.raises(field.ValidationError) as excinfo:
        field.validate("anything")
    # The exception message should contain the key 'never'
    assert "never" in str(excinfo.value)
    # The exception should carry the error key in its data
    assert excinfo.value.args[0] == "never"

def test_nevermatch_constructor_disallows_allow_null():
    """Passing allow_null to the constructor should raise an AssertionError."""
    with pytest.raises(AssertionError):
        NeverMatch(allow_null=True)

def test_nevermatch_errors_dict_contains_never_key():
    """The errors dictionary should contain the 'never' key with the expected message."""
    field = NeverMatch()
    assert "never" in field.errors
    assert field.errors["never"] == "This never validates."
