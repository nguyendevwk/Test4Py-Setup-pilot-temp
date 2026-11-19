import pytest
from typesystem.composites import OneOf
from typesystem.fields import Field


def test_oneof_multiple_matches_raises():
    class DummyField(Field):
        def __init__(self, validator):
            super().__init__()
            self.validator = validator

        def validate_or_error(self, value):
            try:
                return self.validator(value), None
            except Exception:
                return None, "error"

    int_field = DummyField(lambda v: v if isinstance(v, int) else (_ for _ in ()).throw(ValueError))
    any_field = DummyField(lambda v: v)  # always matches

    oneof = OneOf([int_field, any_field])

    with pytest.raises(Exception) as excinfo:
        oneof.validate(5)
    assert "multiple_matches" in str(excinfo.value)
