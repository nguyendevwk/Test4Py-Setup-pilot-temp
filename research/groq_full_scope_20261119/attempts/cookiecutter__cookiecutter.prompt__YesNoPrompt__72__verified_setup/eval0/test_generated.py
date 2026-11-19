import pytest
from rich.prompt import InvalidResponse
from cookiecutter.prompt import YesNoPrompt

def test_process_response_yes_variants():
    """All accepted yes inputs return True."""
    prompt = YesNoPrompt()
    for input_value in ["1", "true", "t", "yes", "y", "on", "  YEs  "]:
        assert prompt.process_response(input_value) is True, f"Input {input_value!r} should be True"

def test_process_response_no_variants():
    """All accepted no inputs return False."""
    prompt = YesNoPrompt()
    for input_value in ["0", "false", "f", "no", "n", "off", "  NO  "]:
        assert prompt.process_response(input_value) is False, f"Input {input_value!r} should be False"

def test_process_response_invalid_raises():
    """Invalid inputs raise InvalidResponse."""
    prompt = YesNoPrompt()
    for input_value in ["maybe", "yesplease", "", "  "]:
        with pytest.raises(InvalidResponse):
            prompt.process_response(input_value)
