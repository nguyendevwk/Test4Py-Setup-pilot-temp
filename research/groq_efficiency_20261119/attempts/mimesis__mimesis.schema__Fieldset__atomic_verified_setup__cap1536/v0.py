import pytest
from mimesis.schema import Fieldset
from mimesis.exceptions import FieldsetError
from mimesis.providers.generic import Generic

# Helper provider to generate deterministic values
class DummyProvider(Generic):
    def __init__(self, seed=None):
        super().__init__(seed=seed)

    def username(self):
        return "user"

def test_fieldset_default_iterations_returns_correct_length():
    """Fieldset without explicit i should return the default number of items."""
    fieldset = Fieldset()
    # Use a dummy provider that always returns the same value
    result = fieldset("username")
    assert isinstance(result, list)
    assert len(result) == Fieldset.fieldset_default_iterations
    assert all(item == "user" for item in result)

def test_fieldset_single_iteration_returns_single_item():
    """Specifying i=1 should return a list with a single element."""
    fieldset = Fieldset()
    result = fieldset("username", i=1)
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0] == "user"

def test_fieldset_invalid_iterations_raises_error():
    """Providing i less than 1 should raise FieldsetError."""
    fieldset = Fieldset()
    with pytest.raises(FieldsetError):
        fieldset("username", i=0)
