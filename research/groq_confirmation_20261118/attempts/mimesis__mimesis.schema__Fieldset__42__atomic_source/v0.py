import pytest
from mimesis.schema import Fieldset
from mimesis.exceptions import FieldsetError

def test_fieldset_default_iterations_returns_list_of_length_10():
    """Fieldset with no explicit iterations should return 10 values."""
    fieldset = Fieldset(seed=42)
    result = fieldset("username")
    assert isinstance(result, list)
    assert len(result) == 10
    # All elements should be strings (generic username provider returns str)
    assert all(isinstance(v, str) for v in result)

def test_fieldset_single_iteration_returns_single_value_list():
    """Specifying i=1 should return a list with one element."""
    fieldset = Fieldset(seed=42)
    result = fieldset("first_name", i=1)
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], str)

def test_fieldset_invalid_iterations_raises_error():
    """Providing i less than 1 should raise FieldsetError."""
    fieldset = Fieldset(seed=42)
    with pytest.raises(FieldsetError):
        fieldset("last_name", i=0)
