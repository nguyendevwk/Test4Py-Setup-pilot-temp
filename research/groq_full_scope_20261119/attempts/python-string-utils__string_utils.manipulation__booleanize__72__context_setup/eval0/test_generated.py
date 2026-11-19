import pytest
from string_utils.manipulation import booleanize
from string_utils.errors import InvalidInputError

def test_booleanize_positive_values():
    # Positive values should return True regardless of case
    assert booleanize("true") is True
    assert booleanize("TRUE") is True
    assert booleanize("1") is True
    assert booleanize("Yes") is True
    assert booleanize("y") is True

def test_booleanize_negative_values():
    # Any other string should return False
    assert booleanize("false") is False
    assert booleanize("0") is False
    assert booleanize("no") is False
    assert booleanize("maybe") is False
    assert booleanize("") is False

def test_booleanize_invalid_input():
    # Non-string input should raise InvalidInputError
    with pytest.raises(InvalidInputError):
        booleanize(123)
    with pytest.raises(InvalidInputError):
        booleanize(None)
    with pytest.raises(InvalidInputError):
        booleanize(["true"])
