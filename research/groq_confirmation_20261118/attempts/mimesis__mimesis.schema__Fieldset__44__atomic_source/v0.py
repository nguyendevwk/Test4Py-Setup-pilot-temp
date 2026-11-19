import pytest
from mimesis.schema import Fieldset
from mimesis.exceptions import FieldsetError

def test_fieldset_default_iterations_and_key_function():
    """Fieldset should return the default number of values and apply key function."""
    fs = Fieldset()
    # default iterations is 10
    result = fs("username")
    assert isinstance(result, list)
    assert len(result) == 10
    # key function should transform each value
    transformed = fs("username", key=lambda x: x.upper())
    assert all(isinstance(v, str) and v.isupper() for v in transformed)
    assert transformed != result  # ensure key function applied

def test_fieldset_custom_iterations_and_kwargs():
    """Fieldset should respect custom iteration count and pass kwargs to provider."""
    fs = Fieldset()
    # request 3 iterations
    result = fs("username", i=3)
    assert len(result) == 3
    # ensure that provider receives kwargs (e.g., length)
    result_with_length = fs("username", i=2, length=5)
    assert len(result_with_length) == 2
    assert all(len(v) == 5 for v in result_with_length)

def test_fieldset_error_on_invalid_iterations():
    """Fieldset should raise FieldsetError when iterations < 1."""
    fs = Fieldset()
    with pytest.raises(FieldsetError):
        fs("username", i=0)
    with pytest.raises(FieldsetError):
        fs("username", i=-5)
