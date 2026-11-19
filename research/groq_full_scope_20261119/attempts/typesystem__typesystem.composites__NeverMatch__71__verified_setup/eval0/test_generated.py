import pytest
from typesystem.composites import NeverMatch
from typesystem.fields import Field

def test_nevermatch_constructor_forbids_allow_null():
    """Constructor should raise AssertionError if allow_null is passed."""
    with pytest.raises(AssertionError):
        NeverMatch(allow_null=True)

def test_nevermatch_validate_always_raises():
    """validate should always raise a ValidationError with the correct message."""
    field = NeverMatch()
    with pytest.raises(field.ValidationError) as excinfo:
        field.validate("anything")
    assert "never" in excinfo.value.args[0]
    assert "This never validates." in excinfo.value.args[0]

def test_nevermatch_errors_dict_contains_expected_key():
    """The errors dictionary should contain the 'never' key."""
    assert "never" in NeverMatch.errors
    assert NeverMatch.errors["never"] == "This never validates."
