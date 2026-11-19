import builtins
import pytest
from cookiecutter.prompt import read_user_yes_no, YesNoPrompt


def test_read_user_yes_no_accepts_various_truthy_values(monkeypatch):
    """Verify that all truthy strings are interpreted as True."""
    truthy_inputs = ["1", "true", "t", "yes", "y", "on", "  YES  ", "TrUe"]
    for inp in truthy_inputs:
        # Monkeypatch builtins.input to return the test string
        monkeypatch.setattr(builtins, "input", lambda _: inp)
        result = read_user_yes_no("test_var", default_value=False)
        assert result is True, f"Input '{inp}' should be True"


def test_read_user_yes_no_default_and_falsy_values(monkeypatch):
    """Verify that default is used when no input is given and falsy strings are False."""
    # Simulate empty input (user just presses Enter)
    monkeypatch.setattr(builtins, "input", lambda _: "")
    # Default should be returned
    assert read_user_yes_no("test_var", default_value=True) is True

    falsy_inputs = ["0", "false", "f", "no", "n", "off", "  NO  ", "FaLsE"]
    for inp in falsy_inputs:
        monkeypatch.setattr(builtins, "input", lambda _: inp)
        result = read_user_yes_no("test_var", default_value=True)
        assert result is False, f"Input '{inp}' should be False"


def test_read_user_yes_no_invalid_input_raises(monkeypatch):
    """Verify that an invalid response raises InvalidResponse."""
    # Monkeypatch builtins.input to return an invalid string
    monkeypatch.setattr(builtins, "input", lambda _: "maybe")
    with pytest.raises(YesNoPrompt.InvalidResponse):
        read_user_yes_no("test_var", default_value=False)
