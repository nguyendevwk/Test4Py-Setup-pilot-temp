import pytest
from typesystem.composites import AllOf
from typesystem.fields import Any, Integer, String

def test_allof_success():
    """AllOf should validate when all child fields accept the value."""
    field = AllOf(all_of=[String(min_length=1), Integer(minimum=0)])
    # String(min_length=1) accepts "hello", Integer(minimum=0) accepts 5
    assert field.validate("hello") == "hello"
    assert field.validate(5) == 5

def test_allof_empty():
    """AllOf with no child fields should accept any value."""
    field = AllOf(all_of=[])
    # No child validation, so any value passes
    assert field.validate(None) is None
    assert field.validate(123) == 123
    assert field.validate("test") == "test"

def test_allof_failure():
    """AllOf should raise ValidationError if any child field fails."""
    field = AllOf(all_of=[String(min_length=5), Integer(minimum=10)])
    with pytest.raises(Exception):
        # "hi" fails String(min_length=5)
        field.validate("hi")
    with pytest.raises(Exception):
        # 5 fails Integer(minimum=10)
        field.validate(5)
