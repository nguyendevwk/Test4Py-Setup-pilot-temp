import pytest
from sanic.utils import str_to_bool

def test_str_to_bool_true_values():
    """Verify that all accepted true strings return True."""
    true_values = [
        "Y", "yes", "Yep", "YUP", "t", "TRUE", "On", "enable", "Enabled", "1"
    ]
    for val in true_values:
        assert str_to_bool(val) is True, f"Expected True for {val!r}"

def test_str_to_bool_false_values():
    """Verify that all accepted false strings return False."""
    false_values = [
        "n", "No", "f", "NOPE", "false", "OFF", "disable", "Disabled", "0"
    ]
    for val in false_values:
        assert str_to_bool(val) is False, f"Expected False for {val!r}"

def test_str_to_bool_invalid_input():
    """Verify that invalid strings raise ValueError."""
    invalid_values = ["", "maybe", "2", "truthy", "0.0", "yesno"]
    for val in invalid_values:
        with pytest.raises(ValueError, match=f"Invalid truth value {val.lower()}"):
            str_to_bool(val)
