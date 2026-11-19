import pytest
from mimesis.schema import Fieldset
from mimesis.exceptions import FieldsetError

def test_default_iterations_returns_correct_length_and_values():
    """Fieldset with no explicit i should return 10 items."""
    fs = Fieldset()
    result = fs("username")
    assert isinstance(result, list)
    assert len(result) == 10
    # All items should be strings (username provider returns str)
    assert all(isinstance(v, str) for v in result)

def test_custom_iterations_overrides_default_and_applies_key_function():
    """Providing i=3 should return 3 items and key function should transform them."""
    fs = Fieldset()
    # key function that uppercases each value
    result = fs("username", i=3, key=lambda x: x.upper())
    assert len(result) == 3
    assert all(isinstance(v, str) for v in result)
    # Ensure key function applied: all values are uppercase
    assert all(v.isupper() for v in result)

def test_iterations_less_than_one_raises_FieldsetError():
    """Providing i=0 should raise FieldsetError."""
    fs = Fieldset()
    with pytest.raises(FieldsetError):
        fs("username", i=0)
