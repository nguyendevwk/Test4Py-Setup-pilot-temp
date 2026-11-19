import pytest
from mimesis.schema import Fieldset
from mimesis.exceptions import FieldsetError


def test_default_iterations_returns_list_of_length_10():
    """Fieldset without explicit i should return 10 items."""
    fs = Fieldset()
    result = fs("username")
    assert isinstance(result, list)
    assert len(result) == 10
    # All items should be strings (username provider returns str)
    assert all(isinstance(item, str) for item in result)


def test_custom_iterations_returns_correct_number_and_values():
    """Fieldset with i=3 should return exactly 3 items."""
    fs = Fieldset()
    result = fs("first_name", i=3)
    assert isinstance(result, list)
    assert len(result) == 3
    # Ensure values are different (greedy fieldset should produce distinct values)
    assert len(set(result)) == 3
    assert all(isinstance(item, str) for item in result)


def test_negative_iterations_raises_fieldset_error():
    """Providing i less than 1 should raise FieldsetError."""
    fs = Fieldset()
    with pytest.raises(FieldsetError):
        fs("last_name", i=0)
