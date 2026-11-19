import pytest
from cookiecutter.prompt import YesNoPrompt
from rich.prompt import InvalidResponse

def test_yes_no_prompt_accepts_valid_yes_choices():
    prompt = YesNoPrompt()
    for choice in ["1", "true", "t", "yes", "y", "on", "  Y  ", "TRUE"]:
        assert prompt.process_response(choice) is True, f"Expected True for choice '{choice}'"

def test_yes_no_prompt_accepts_valid_no_choices():
    prompt = YesNoPrompt()
    for choice in ["0", "false", "f", "no", "n", "off", "  n  ", "FALSE"]:
        assert prompt.process_response(choice) is False, f"Expected False for choice '{choice}'"

def test_yes_no_prompt_raises_invalid_response_for_unknown_input():
    prompt = YesNoPrompt()
    with pytest.raises(InvalidResponse):
        prompt.process_response("maybe")
    with pytest.raises(InvalidResponse):
        prompt.process_response("")
    with pytest.raises(InvalidResponse):
        prompt.process_response("  ")
