import pytest
from mimesis.schema import Fieldset
from mimesis.exceptions import FieldsetError


def test_fieldset_default_iterations(tmp_path):
    """Fieldset returns the default number of items when no `i` is supplied."""
    fieldset = Fieldset()
    result = fieldset("username")
    # Default iterations is 10
    assert isinstance(result, list)
    assert len(result) == 10
    # All items should be strings (mimesis username provider returns str)
    assert all(isinstance(item, str) for item in result)


def test_fieldset_custom_iterations(tmp_path):
    """Fieldset respects a custom iteration count passed via keyword argument."""
    fieldset = Fieldset()
    result = fieldset("email", i=3)
    assert isinstance(result, list)
    assert len(result) == 3
    # All items should be strings (mimesis email provider returns str)
    assert all(isinstance(item, str) for item in result)


def test_fieldset_invalid_iterations_raises():
    """Fieldset raises FieldsetError when iteration count is less than 1."""
    fieldset = Fieldset()
    with pytest.raises(FieldsetError):
        fieldset("username", i=0)
