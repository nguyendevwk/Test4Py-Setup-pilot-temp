import pytest
from sanic.utils import str_to_bool

def test_str_to_bool_true_values():
    """Verify that all accepted true strings return True."""
    true_inputs = [
        "Y", "yes", "Yep", "YUP", "t", "TRUE", "On", "enable", "Enabled", "1"
    ]
    for inp in true_inputs:
        assert str_to_bool(inp) is True, f"Expected True for input {inp!r}"

def test_str_to_bool_false_values():
    """Verify that all accepted false strings return False."""
    false_inputs = [
        "n", "No", "f", "NOPE", "false", "OFF", "disable", "Disabled", "0"
    ]
    for inp in false_inputs:
        assert str_to_bool(inp) is False, f"Expected False for input {inp!r}"

def test_str_to_bool_invalid_input():
    """Verify that an invalid string raises ValueError."""
    invalid_inputs = ["", "maybe", "2", "truthy", "nopeyes", "  true  "]
    for inp in invalid_inputs:
        with pytest.raises(ValueError, match="Invalid truth value"):
            str_to_bool(inp)
