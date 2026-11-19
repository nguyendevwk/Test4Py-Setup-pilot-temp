import pytest
from cookiecutter.prompt import read_user_choice
from rich.prompt import Prompt

# Test 1: Normal selection with default (no user input)
def test_read_user_choice_default(monkeypatch):
    # Monkeypatch Prompt.ask to simulate no input (returns default)
    def fake_ask(prompt, choices, default):
        # Ensure the default is the first option
        assert default == "1"
        return default
    monkeypatch.setattr(Prompt, "ask", fake_ask)

    options = ["apple", "banana", "cherry"]
    result = read_user_choice("fruit", options)
    assert result == "apple", "Default should return the first option"

# Test 2: Custom prompts with __prompt__ and custom labels
def test_read_user_choice_custom_prompts(monkeypatch):
    # Simulate user selecting option 2
    def fake_ask(prompt, choices, default):
        # The prompt should contain the custom __prompt__
        assert "Pick a color" in prompt
        # The choices should be strings of numbers
        assert choices == ["1", "2", "3"]
        return "2"
    monkeypatch.setattr(Prompt, "ask", fake_ask)

    options = ["red", "green", "blue"]
    prompts = {
        "color": {
            "__prompt__": "Pick a color",
            "red": "Bright Red",
            "green": "Lush Green",
            # No custom label for blue, should fallback to key
        }
    }
    result = read_user_choice("color", options, prompts=prompts)
    assert result == "green", "Should return the second option"

# Test 3: Error when options list is empty
def test_read_user_choice_empty_options():
    with pytest.raises(ValueError):
        read_user_choice("empty", [])
