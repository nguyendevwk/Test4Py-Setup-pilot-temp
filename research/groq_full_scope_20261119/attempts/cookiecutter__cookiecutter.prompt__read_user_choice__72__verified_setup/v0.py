import pytest
from cookiecutter.prompt import read_user_choice
from rich.prompt import Prompt

# Test 1: Normal selection with default (no user input)
def test_read_user_choice_default(monkeypatch):
    # Monkeypatch Prompt.ask to simulate no input (default chosen)
    def fake_ask(prompt, choices, default):
        # Return the default value passed in
        return default
    monkeypatch.setattr(Prompt, "ask", fake_ask)

    options = ["apple", "banana", "cherry"]
    result = read_user_choice("fruit", options)
    assert result == "apple"  # first item is default

# Test 2: Custom prompts with __prompt__ and custom labels
def test_read_user_choice_custom_prompts(monkeypatch):
    def fake_ask(prompt, choices, default):
        # Simulate user selecting option 2
        return "2"
    monkeypatch.setattr(Prompt, "ask", fake_ask)

    options = ["red", "green", "blue"]
    prompts = {
        "color": {
            "__prompt__": "Choose a color",
            "red": "Crimson",
            "green": "Emerald",
            # blue not overridden
        }
    }
    result = read_user_choice("color", options, prompts=prompts)
    assert result == "green"  # option 2 corresponds to "green"

# Test 3: Error when options list is empty
def test_read_user_choice_empty_options():
    with pytest.raises(ValueError):
        read_user_choice("empty", [])
