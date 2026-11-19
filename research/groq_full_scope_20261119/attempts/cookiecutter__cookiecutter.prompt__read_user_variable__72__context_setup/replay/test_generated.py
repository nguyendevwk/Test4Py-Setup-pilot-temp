import builtins
import inspect
import types
import pytest
from cookiecutter.prompt import read_user_variable, Prompt

def test_read_user_variable_uses_prompt_with_custom_prompt(monkeypatch):
    """Verify that the function uses the custom prompt text when provided."""
    captured = {}
    def fake_ask(question, default=None):
        captured['question'] = question
        captured['default'] = default
        return default  # simulate user pressing Enter

    monkeypatch.setattr(Prompt, "ask", staticmethod(fake_ask))
    result = read_user_variable("project_name", "default_proj", prompts={"project_name": "Enter project name:"})
    assert result == "default_proj"
    assert captured['question'] == "Enter project name:"
    assert captured['default'] == "default_proj"

def test_read_user_variable_uses_var_name_as_question_when_no_prompt(monkeypatch):
    """Verify that the function falls back to the variable name when no custom prompt is given."""
    captured = {}
    def fake_ask(question, default=None):
        captured['question'] = question
        captured['default'] = default
        return default

    monkeypatch.setattr(Prompt, "ask", staticmethod(fake_ask))
    result = read_user_variable("author", "John Doe")
    assert result == "John Doe"
    assert captured['question'] == "author"
    assert captured['default'] == "John Doe"

def test_read_user_variable_applies_prefix_to_question(monkeypatch):
    """Verify that the prefix is correctly prepended to the question string."""
    captured = {}
    def fake_ask(question, default=None):
        captured['question'] = question
        captured['default'] = default
        return default

    monkeypatch.setattr(Prompt, "ask", staticmethod(fake_ask))
    result = read_user_variable("license", "MIT", prefix="[Setup] ")
    assert result == "MIT"
    assert captured['question'] == "[Setup] license"
    assert captured['default'] == "MIT"
