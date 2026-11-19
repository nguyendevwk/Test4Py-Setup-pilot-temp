import pytest
from mimesis.schema import Fieldset
from mimesis.exceptions import FieldsetError


def test_fieldset_default_iterations_returns_correct_length():
    """Fieldset without explicit i should return the default number of items."""
    fieldset = Fieldset()
    result = fieldset("username")
    assert isinstance(result, list)
    assert len(result) == Fieldset.fieldset_default_iterations
    # All items should be strings (username provider returns str)
    assert all(isinstance(item, str) for item in result)


def test_fieldset_custom_iterations_and_key_function():
    """Fieldset should respect custom i and apply key function to each item."""
    # Use a simple key function that appends a suffix
    def key_func(value):
        return f"{value}_suffix"

    fieldset = Fieldset()
    result = fieldset("username", i=3, key=key_func)
    assert len(result) == 3
    assert all(item.endswith("_suffix") for item in result)
    # Ensure the key function was applied to each original value
    original_values = [item.replace("_suffix", "") for item in result]
    assert all(isinstance(v, str) for v in original_values)


def test_fieldset_invalid_iterations_raises_error():
    """Fieldset should raise FieldsetError when i is less than 1."""
    fieldset = Fieldset()
    with pytest.raises(FieldsetError):
        fieldset("username", i=0)
