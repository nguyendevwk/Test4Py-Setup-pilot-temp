import pytest
from mimesis.schema import Fieldset
from mimesis.exceptions import FieldsetError


def test_fieldset_default_iterations(tmp_path):
    """Fieldset should return a list of the default number of values."""
    fset = Fieldset()
    # Use a simple provider field that returns a deterministic value
    result = fset("uuid")
    assert isinstance(result, list)
    assert len(result) == fset.fieldset_default_iterations
    # All elements should be strings (uuid provider returns string)
    assert all(isinstance(v, str) for v in result)


def test_fieldset_custom_iterations(tmp_path):
    """Fieldset should respect a custom iteration count passed via the kwarg."""
    fset = Fieldset()
    custom_i = 3
    result = fset("username", i=custom_i)
    assert isinstance(result, list)
    assert len(result) == custom_i
    # Ensure that the values are different (username provider generates random names)
    assert len(set(result)) == custom_i


def test_fieldset_invalid_iterations_raises():
    """Fieldset should raise FieldsetError when iterations < 1."""
    fset = Fieldset()
    with pytest.raises(FieldsetError):
        fset("email", i=0)
