import pytest
from cookiecutter.prompt import YesNoPrompt
from rich.prompt import InvalidResponse

def test_yes_no_prompt_accepts_yes_variants():
    prompt = YesNoPrompt()
    for variant in ["1", "true", "t", "yes", "y", "on", "  Y  ", "TrUe"]:
        assert prompt.process_response(variant) is True, f"Variant {variant!r} should be True"

def test_yes_no_prompt_accepts_no_variants():
    prompt = YesNoPrompt()
    for variant in ["0", "false", "f", "no", "n", "off", "  n  ", "FaLsE"]:
        assert prompt.process_response(variant) is False, f"Variant {variant!r} should be False"

def test_yes_no_prompt_invalid_input_raises():
    prompt = YesNoPrompt()
    with pytest.raises(InvalidResponse):
        prompt.process_response("maybe")
    with pytest.raises(InvalidResponse):
        prompt.process_response("")
    with pytest.raises(InvalidResponse):
        prompt.process_response("  ")
