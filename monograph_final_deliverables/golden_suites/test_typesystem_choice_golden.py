import pytest
from typesystem.fields import Choice, ValidationError


def test_choice_validation_behavior():
    # Basic valid choice
    c = Choice(choices=["active", "inactive"], allow_null=True, coerce_types=True)
    val, err = c.validate_or_error("active")
    assert err is None and val == "active"

    # Invalid choice
    val, err = c.validate_or_error("unknown")
    assert isinstance(err, ValidationError)
    if hasattr(err, "code"):
        assert err.code == "choice"

    # Empty string with allow_null=True and coerce_types=True -> None
    val, err = c.validate_or_error("")
    assert err is None and val is None

    # Empty string with allow_null=False -> required error
    c2 = Choice(choices=["a"], allow_null=False, coerce_types=True)
    val, err = c2.validate_or_error("")
    assert isinstance(err, ValidationError)
    if hasattr(err, "code"):
        assert err.code == "required"

    # None with allow_null=True
    val, err = c.validate_or_error(None)
    assert err is None and val is None

    # None with allow_null=False -> null error
    c3 = Choice(choices=["a"], allow_null=False)
    val, err = c3.validate_or_error(None)
    assert isinstance(err, ValidationError)
    if hasattr(err, "code"):
        assert err.code == "null"

    # coerce_types=False: empty string not coerced
    c4 = Choice(choices=["a"], allow_null=True, coerce_types=False)
    val, err = c4.validate_or_error("")
    assert isinstance(err, ValidationError)
    if hasattr(err, "code"):
        assert err.code == "required"

    # Tuple choices: only first element is valid key
    c5 = Choice(choices=[("a", "A"), ("b", "B")])
    val, err = c5.validate_or_error("a")
    assert err is None and val == "a"
    val, err = c5.validate_or_error("A")
    assert isinstance(err, ValidationError)
    if hasattr(err, "code"):
        assert err.code == "choice"
