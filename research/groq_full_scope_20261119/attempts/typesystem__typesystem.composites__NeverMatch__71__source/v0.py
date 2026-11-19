import pytest
from typesystem.composites import NeverMatch
from typesystem.fields import ValidationError


def test_nevermatch_init_disallows_allow_null():
    """Initializing NeverMatch with allow_null should raise an AssertionError."""
    with pytest.raises(AssertionError):
        NeverMatch(allow_null=True)


def test_nevermatch_validate_raises_validation_error():
    """Calling validate on NeverMatch should raise a ValidationError with the correct message."""
    field = NeverMatch()
    with pytest.raises(ValidationError) as excinfo:
        field.validate("any value")
    # The ValidationError should contain the key 'never' and the corresponding message.
    assert "never" in excinfo.value.args[0]
    assert "This never validates." in excinfo.value.args[0]


def test_nevermatch_validate_consistently_raises():
    """Repeated calls to validate should consistently raise ValidationError."""
    field = NeverMatch()
    for _ in range(3):
        with pytest.raises(ValidationError):
            field.validate(123)
