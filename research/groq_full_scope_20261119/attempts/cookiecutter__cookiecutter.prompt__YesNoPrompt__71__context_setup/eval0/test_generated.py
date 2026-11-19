import pytest
from rich.prompt import InvalidResponse
from cookiecutter.prompt import YesNoPrompt


def test_process_response_accepts_yes_variants():
    """Verify that all defined yes choices return True."""
    prompt = YesNoPrompt()
    for choice in YesNoPrompt.yes_choices:
        assert prompt.process_response(choice) is True
        # also test with surrounding whitespace and mixed case
        assert prompt.process_response(f"  {choice.upper()}  ") is True


def test_process_response_accepts_no_variants():
    """Verify that all defined no choices return False."""
    prompt = YesNoPrompt()
    for choice in YesNoPrompt.no_choices:
        assert prompt.process_response(choice) is False
        # also test with surrounding whitespace and mixed case
        assert prompt.process_response(f"  {choice.upper()}  ") is False


def test_process_response_invalid_raises():
    """Verify that an invalid input raises InvalidResponse."""
    prompt = YesNoPrompt()
    with pytest.raises(InvalidResponse):
        prompt.process_response("maybe")
    with pytest.raises(InvalidResponse):
        prompt.process_response("")
    with pytest.raises(InvalidResponse):
        prompt.process_response("  ")
