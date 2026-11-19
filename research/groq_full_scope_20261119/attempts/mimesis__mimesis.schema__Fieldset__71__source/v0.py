import pytest
from mimesis.schema import Fieldset
from mimesis.exceptions import FieldsetError

def test_fieldset_default_iterations_and_key_function():
    """Fieldset should return the default number of items and apply key function."""
    fs = Fieldset()
    # Use a simple field that returns a constant value
    result = fs("constant", key=lambda x: x.upper(), i=3)
    assert isinstance(result, list)
    assert len(result) == 3
    assert all(isinstance(v, str) for v in result)
    assert all(v == "CONSTANT" for v in result)

def test_fieldset_custom_iterations_kwarg_and_no_name():
    """Fieldset should respect custom iterations kwarg and work without a name."""
    fs = Fieldset()
    # When name is None, perform should still work (uses default provider)
    result = fs(i=5)
    assert isinstance(result, list)
    assert len(result) == 5
    # All items should be strings (default provider returns strings)
    assert all(isinstance(v, str) for v in result)

def test_fieldset_error_on_invalid_iterations():
    """Fieldset should raise FieldsetError when iterations < 1."""
    fs = Fieldset()
    with pytest.raises(FieldsetError):
        fs("username", i=0)
