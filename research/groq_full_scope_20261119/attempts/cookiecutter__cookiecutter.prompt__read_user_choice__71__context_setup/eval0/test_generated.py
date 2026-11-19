import builtins
import pytest
from cookiecutter.prompt import read_user_choice
from rich.prompt import Prompt

# Helper to patch Prompt.ask
def _patch_prompt_ask(monkeypatch, return_value):
    def fake_ask(prompt, choices=None, default=None):
        return return_value
    monkeypatch.setattr(Prompt, "ask", fake_ask)

def test_read_user_choice_default(monkeypatch):
    """When no user input, the first option is returned."""
    _patch_prompt_ask(monkeypatch, "1")  # simulate selecting first option
    result = read_user_choice("color", ["red", "green", "blue"])
    assert result == "red"

def test_read_user_choice_with_prompts(monkeypatch):
    """Custom prompts override the question and display labels."""
    _patch_prompt_ask(monkeypatch, "2")  # simulate selecting second option
    prompts = {
        "size": {
            "__prompt__": "Choose a size",
            "small": "Small",
            "large": "Large"
        }
    }
    result = read_user_choice("size", ["small", "large"], prompts=prompts)
    assert result == "large"

def test_read_user_choice_empty_options():
    """Providing an empty options list raises ValueError."""
    with pytest.raises(ValueError):
        read_user_choice("empty", [])
