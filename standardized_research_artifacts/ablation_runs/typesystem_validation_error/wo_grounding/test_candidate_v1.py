import pytest
from typesystem.base import ValidationError, BaseError


def test_validation_error_inheritance_and_docstring():
    # ValidationError should inherit from BaseError
    assert issubclass(ValidationError, BaseError)

    # The docstring should match the source definition
    expected_doc = "Raised by `.validate()` or returned by `.validate_or_error()`."
    assert ValidationError.__doc__.strip() == expected_doc
