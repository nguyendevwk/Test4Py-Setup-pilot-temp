import builtins
import pytest
from cookiecutter.prompt import read_user_yes_no, YesNoPrompt
from rich.prompt import InvalidResponse

def test_read_user_yes_no_accepts_yes(monkeypatch):
    # Simulate user typing "yes" when prompted
    monkeypatch.setattr(builtins, "input", lambda _: "yes")
    result = read_user_yes_no("test_var", default_value=False, prompts={"test_var": "Do you agree?"})
    assert result is True, "Expected True when user inputs 'yes'"

def test_read_user_yes_no_accepts_no(monkeypatch):
    # Simulate user typing "no" when prompted
    monkeypatch.setattr(builtins, "input", lambda _: "no")
    result = read_user_yes_no("test_var", default_value=True, prompts={"test_var": "Do you agree?"})
    assert result is False, "Expected False when user inputs 'no'"

def test_read_user_yes_no_invalid_input(monkeypatch):
    # Simulate user typing an invalid response
    monkeypatch.setattr(builtins, "input", lambda _: "maybe")
    with pytest.raises(InvalidResponse):
        read_user_yes_no("test_var", default_value=True, prompts={"test_var": "Do you agree?"})
