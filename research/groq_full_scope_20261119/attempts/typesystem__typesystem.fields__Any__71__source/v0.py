import pytest
import typesystem
from typesystem.fields import Any

def test_any_accepts_various_types(tmp_path):
    """Any.validate should return the value unchanged for different types."""
    any_field = Any()
    # Primitive types
    assert any_field.validate(42) == 42
    assert any_field.validate("hello") == "hello"
    assert any_field.validate(3.14) == 3.14
    # Complex types
    assert any_field.validate([1, 2, 3]) == [1, 2, 3]
    assert any_field.validate({"a": 1}) == {"a": 1}
    # Temporary file path
    file_path = tmp_path / "test.txt"
    file_path.write_text("content")
    assert any_field.validate(str(file_path)) == str(file_path)

def test_any_returns_same_object_identity():
    """Any.validate should return the exact same object instance."""
    any_field = Any()
    obj = {"key": "value"}
    result = any_field.validate(obj)
    assert result is obj

def test_any_does_not_raise_validation_error():
    """Any.validate should never raise ValidationError for any input."""
    any_field = Any()
    for value in [None, 0, "", [], {}, set(), lambda x: x]:
        try:
            any_field.validate(value)
        except Exception as exc:
            pytest.fail(f"Any.validate raised an exception {exc!r} for value {value!r}")
