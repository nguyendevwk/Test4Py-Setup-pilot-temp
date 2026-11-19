import pytest
from typesystem.composites import NeverMatch


def test_validate_always_raises_validation_error():
    """NeverMatch.validate should always raise a ValidationError with the correct message."""
    field = NeverMatch()
    with pytest.raises(Exception) as excinfo:
        field.validate("any value")
    # The exception should be a ValidationError from typesystem, but we only check the message.
    assert "never" in str(excinfo.value)
    assert "This never validates." in str(excinfo.value)


def test_init_disallows_allow_null():
    """NeverMatch.__init__ should raise an AssertionError if allow_null is provided."""
    with pytest.raises(AssertionError):
        NeverMatch(allow_null=True)


def test_init_without_allow_null_succeeds():
    """NeverMatch.__init__ should accept any kwargs except allow_null."""
    # Passing a normal keyword argument should succeed.
    field = NeverMatch(custom="value")
    assert isinstance(field, NeverMatch)
    # The custom attribute should be stored on the instance.
    assert getattr(field, "custom") == "value"
