import pytest
from mimesis.schema import Field
from mimesis.exceptions import FieldNameError

def test_field_call_returns_value():
    """Field instance should be callable and return a non‑empty value."""
    field = Field()
    result = field()
    assert result is not None, "Field() should not return None"
    assert isinstance(result, str) or isinstance(result, int), "Result should be a string or int"
    assert result != "", "Result should not be an empty string"

def test_field_call_with_name_returns_value():
    """Providing a valid name should return a value without raising."""
    field = Field()
    # 'username' is a common provider key; adjust if necessary
    result = field(name="username")
    assert result is not None, "Field(name='username') should not return None"
    assert isinstance(result, str), "Username should be a string"

def test_field_call_invalid_name_raises():
    """Using an invalid name should raise FieldNameError."""
    field = Field()
    with pytest.raises(FieldNameError):
        field(name="non_existent_provider")
