import pytest
from mimesis.schema import Fieldset
from mimesis.exceptions import FieldsetError

# Test 1: Normal behavior with default iterations (10)
def test_fieldset_default_iterations():
    fs = Fieldset(seed=123)
    result = fs("username")
    assert isinstance(result, list)
    assert len(result) == 10
    # All elements should be strings and non-empty
    assert all(isinstance(v, str) and v for v in result)

# Test 2: Boundary behavior with i=1 (single iteration)
def test_fieldset_single_iteration():
    fs = Fieldset(i=1, seed=456)
    result = fs("email")
    assert isinstance(result, list)
    assert len(result) == 1
    # The single element should be a valid email string
    assert isinstance(result[0], str)
    assert "@" in result[0]

# Test 3: Error behavior when i < 1
def test_fieldset_invalid_iterations():
    fs = Fieldset(seed=789)
    with pytest.raises(FieldsetError):
        fs("name", i=0)
