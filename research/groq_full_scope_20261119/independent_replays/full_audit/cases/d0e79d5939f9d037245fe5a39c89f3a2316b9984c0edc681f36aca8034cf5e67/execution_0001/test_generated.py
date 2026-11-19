import pytest
from sanic.utils import str_to_bool

def test_str_to_bool_true_values():
    """Verify that all accepted true strings return True."""
    true_values = [
        "Y", "yes", "Yep", "YUP", "t", "True", "ON", "enable", "Enabled", "1"
    ]
    for val in true_values:
        assert str_to_bool(val) is True, f"Expected True for {val!r}"

def test_str_to_bool_false_values():
    """Verify that all accepted false strings return False."""
    false_values = [
        "n", "No", "f", "NOPE", "false", "Off", "disable", "Disabled", "0"
    ]
    for val in false_values:
        assert str_to_bool(val) is False, f"Expected False for {val!r}"

def test_str_to_bool_invalid_value():
    """Verify that an invalid string raises ValueError."""
    with pytest.raises(ValueError, match="Invalid truth value"):
        str_to_bool("maybe")
