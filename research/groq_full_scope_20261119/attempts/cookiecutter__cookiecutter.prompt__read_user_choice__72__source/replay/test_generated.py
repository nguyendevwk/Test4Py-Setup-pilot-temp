import builtins
import pytest
from cookiecutter.prompt import read_user_choice

def test_default_choice_when_no_input(monkeypatch):
    # Simulate no user input by patching Prompt.ask to return the default
    monkeypatch.setattr(
        "cookiecutter.prompt.Prompt.ask",
        lambda prompt, choices, default: default,
    )
    options = ["apple", "banana", "cherry"]
    result = read_user_choice("fruit", options)
    assert result == "apple", "Default should be the first option when no input is given"

def test_custom_prompt_and_choice(monkeypatch):
    # Simulate user selecting the second option
    monkeypatch.setattr(
        "cookiecutter.prompt.Prompt.ask",
        lambda prompt, choices, default: "2",
    )
    options = ["red", "green", "blue"]
    prompts = {"color": {"__prompt__": "Pick a color", "red": "Bright Red", "green": "Lush Green"}}
    result = read_user_choice("color", options, prompts=prompts)
    assert result == "green", "Should return the option corresponding to the user's numeric choice"

def test_empty_options_raises_value_error():
    with pytest.raises(ValueError):
        read_user_choice("empty", [])
