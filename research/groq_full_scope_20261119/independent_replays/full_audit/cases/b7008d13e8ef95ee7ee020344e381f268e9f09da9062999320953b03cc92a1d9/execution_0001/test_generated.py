import pytest
from mimesis.schema import Fieldset
from mimesis.exceptions import FieldsetError


def test_fieldset_default_iterations(tmp_path):
    """Fieldset returns the default number of values when no `i` is supplied."""
    fset = Fieldset()
    result = fset("username")
    # default iterations is 10
    assert isinstance(result, list)
    assert len(result) == 10
    # all items should be strings (mimesis username provider returns str)
    assert all(isinstance(v, str) for v in result)


def test_fieldset_custom_iterations(tmp_path):
    """Fieldset respects a custom iteration count passed via keyword."""
    fset = Fieldset()
    result = fset("email", i=3)
    assert isinstance(result, list)
    assert len(result) == 3
    # each item should be a valid email string
    assert all("@" in v for v in result)


def test_fieldset_invalid_iterations_raises():
    """Fieldset raises FieldsetError when iteration count is less than 1."""
    fset = Fieldset()
    with pytest.raises(FieldsetError):
        fset("username", i=0)
