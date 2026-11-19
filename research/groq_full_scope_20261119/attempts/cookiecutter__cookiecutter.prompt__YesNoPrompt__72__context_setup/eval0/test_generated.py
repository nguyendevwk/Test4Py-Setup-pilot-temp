import pytest
from cookiecutter.prompt import YesNoPrompt
from rich.prompt import InvalidResponse


def test_process_response_accepts_yes_variants():
    prompt = YesNoPrompt()
    for choice in YesNoPrompt.yes_choices:
        assert prompt.process_response(choice) is True, f"Expected True for choice '{choice}'"


def test_process_response_accepts_no_variants():
    prompt = YesNoPrompt()
    for choice in YesNoPrompt.no_choices:
        assert prompt.process_response(choice) is False, f"Expected False for choice '{choice}'"


def test_process_response_invalid_raises():
    prompt = YesNoPrompt()
    with pytest.raises(InvalidResponse):
        prompt.process_response("maybe")
