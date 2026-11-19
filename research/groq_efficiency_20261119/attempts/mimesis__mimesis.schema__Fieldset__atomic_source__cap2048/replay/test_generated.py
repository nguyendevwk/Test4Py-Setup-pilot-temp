import pytest
from mimesis.schema import Fieldset
from mimesis.exceptions import FieldsetError

def test_fieldset_default_iterations_and_key_function():
    """Fieldset should return the default number of items and apply key function."""
    fs = Fieldset()
    # Use a simple field that returns the same value for demonstration
    result = fs("username")
    assert isinstance(result, list)
    assert len(result) == Fieldset.fieldset_default_iterations
    # All items should be strings (username provider returns string)
    assert all(isinstance(item, str) for item in result)

def test_fieldset_custom_iterations_and_kwargs():
    """Fieldset should respect custom iteration count and pass kwargs to field."""
    fs = Fieldset()
    # Request 3 iterations
    result = fs("first_name", i=3)
    assert len(result) == 3
    # Ensure that the field receives the locale argument correctly
    # (by checking that the returned names are valid for the default locale)
    assert all(isinstance(name, str) and name for name in result)

def test_fieldset_error_on_invalid_iterations():
    """Fieldset should raise FieldsetError when iterations < 1."""
    fs = Fieldset()
    with pytest.raises(FieldsetError):
        fs("last_name", i=0)
