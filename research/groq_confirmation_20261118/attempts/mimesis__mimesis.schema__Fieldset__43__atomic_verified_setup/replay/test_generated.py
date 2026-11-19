import pytest
from mimesis.schema import Fieldset
from mimesis.exceptions import FieldsetError


def test_default_iterations_returns_correct_length_and_values():
    """Fieldset without explicit i should return 10 items."""
    fieldset = Fieldset()
    result = fieldset("username")
    assert isinstance(result, list)
    assert len(result) == 10
    # All items should be strings (typical provider output)
    assert all(isinstance(item, str) for item in result)


def test_custom_iterations_via_kwarg_and_attribute():
    """Fieldset should respect custom i passed at call time and via constructor."""
    # Constructor level
    fieldset_ctor = Fieldset(i=3)
    result_ctor = fieldset_ctor("email")
    assert len(result_ctor) == 3

    # Call level overrides constructor
    result_call = fieldset_ctor("email", i=5)
    assert len(result_call) == 5

    # Ensure values are different across iterations
    assert len(set(result_call)) == 5


def test_error_on_invalid_iterations():
    """Fieldset should raise FieldsetError when i < 1."""
    fieldset = Fieldset()
    with pytest.raises(FieldsetError):
        fieldset("username", i=0)
    with pytest.raises(FieldsetError):
        fieldset("username", i=-5)
