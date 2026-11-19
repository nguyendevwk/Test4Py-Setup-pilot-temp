import pytest
from typesystem.schemas import Schema
from typesystem.fields import String, Integer
from typesystem.base import ValidationError


def test_schema_validate_applies_default_for_missing_optional_field():
    """
    Schema should apply default values for fields that are not required
    (i.e., have a default) when those fields are missing from the input.
    """
    # Arrange: create a schema where `age` has a default, making it optional
    schema = Schema(
        fields={
            "username": String(max_length=50),
            "age": Integer(default=18),
        }
    )

    # Act: validate input missing the optional `age` field
    result = schema.validate({"username": "alice"})

    # Assert: the returned dict contains the provided username and the default age
    assert result == {"username": "alice", "age": 18}

    # Act: validate input that explicitly provides a value for `age`
    result_with_age = schema.validate({"username": "bob", "age": 25})

    # Assert: the provided age is preserved
    assert result_with_age == {"username": "bob", "age": 25}
