import pytest
from rich.prompt import InvalidResponse
from cookiecutter.prompt import YesNoPrompt


def test_yes_no_prompt_accepts_yes_variants():
    """Verify that all defined yes choices return True."""
    prompt = YesNoPrompt()
    for choice in prompt.yes_choices:
        assert prompt.process_response(choice) is True, f"Choice '{choice}' should be True"


def test_yes_no_prompt_accepts_no_variants():
    """Verify that all defined no choices return False."""
    prompt = YesNoPrompt()
    for choice in prompt.no_choices:
        assert prompt.process_response(choice) is False, f"Choice '{choice}' should be False"


def test_yes_no_prompt_invalid_response_raises():
    """Verify that an invalid choice raises InvalidResponse."""
    prompt = YesNoPrompt()
    with pytest.raises(InvalidResponse):
        prompt.process_response("maybe")
