import pytest
import typesystem
from typesystem.fields import Field

# Create a simple Field subclass for testing
class PositiveIntField(Field):
    def validate(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Value must be a positive integer")
        return value

def test_allof_valid_value_passes(tmp_path):
    """AllOf should accept a value that satisfies all child fields."""
    all_of_field = typesystem.composites.AllOf(
        all_of=[PositiveIntField(), PositiveIntField()]
    )
    # The value 5 satisfies both PositiveIntField instances
    result = all_of_field.validate(5)
    assert result == 5

def test_allof_invalid_value_raises(tmp_path):
    """AllOf should raise an exception if any child field fails validation."""
    all_of_field = typesystem.composites.AllOf(
        all_of=[PositiveIntField(), PositiveIntField()]
    )
    with pytest.raises(ValueError, match="Value must be a positive integer"):
        all_of_field.validate(-3)

def test_allof_disallows_allow_null_kw(tmp_path):
    """AllOf should not accept the allow_null keyword argument."""
    with pytest.raises(AssertionError):
        typesystem.composites.AllOf(all_of=[PositiveIntField()], allow_null=True)
