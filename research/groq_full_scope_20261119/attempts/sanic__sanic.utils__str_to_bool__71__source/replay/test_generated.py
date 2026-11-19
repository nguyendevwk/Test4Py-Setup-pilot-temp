import pytest
from sanic.utils import str_to_bool

def test_str_to_bool_true_values():
    """Verify that all accepted true strings return True."""
    true_inputs = [
        "Y", "yes", "Yep", "Yup", "T", "TRUE", "On", "enable", "ENABLED", "1"
    ]
    for inp in true_inputs:
        assert str_to_bool(inp) is True, f"Expected True for input {inp!r}"

def test_str_to_bool_false_values():
    """Verify that all accepted false strings return False."""
    false_inputs = [
        "n", "NO", "f", "Nope", "FALSE", "off", "disable", "DISABLED", "0"
    ]
    for inp in false_inputs:
        assert str_to_bool(inp) is False, f"Expected False for input {inp!r}"

def test_str_to_bool_invalid_input_raises():
    """Verify that an invalid string raises ValueError."""
    invalid_inputs = ["", "maybe", "2", "truth", "falsey", "onoff"]
    for inp in invalid_inputs:
        with pytest.raises(ValueError, match=f"Invalid truth value {inp.lower()}"):
            str_to_bool(inp)
