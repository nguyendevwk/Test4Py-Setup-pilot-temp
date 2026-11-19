import pytest
from string_utils.manipulation import booleanize
from string_utils.errors import InvalidInputError

def test_booleanize_positive_cases():
    """Verify that known truthy strings return True."""
    truthy = ["true", "TRUE", "1", "yes", "YES", "y", "Y"]
    for s in truthy:
        assert booleanize(s) is True, f"Expected True for input {s!r}"

def test_booleanize_negative_cases():
    """Verify that non-truthy strings return False."""
    falsy = ["false", "0", "no", "maybe", "", "  ", "Trueish", "yess"]
    for s in falsy:
        assert booleanize(s) is False, f"Expected False for input {s!r}"

def test_booleanize_invalid_input():
    """Verify that non-string inputs raise InvalidInputError."""
    invalid_inputs = [None, 123, 1.5, [], {}, set(), b"bytes"]
    for inp in invalid_inputs:
        with pytest.raises(InvalidInputError):
            booleanize(inp)
