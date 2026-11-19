import pytest
from cookiecutter.prompt import read_user_variable
from rich.prompt import Prompt

@pytest.fixture
def fake_ask(monkeypatch):
    """Replace Prompt.ask with a function that records its arguments and returns a fixed value."""
    calls = []

    def fake_ask(message, default=None):
        calls.append((message, default))
        return "fixed_value"

    monkeypatch.setattr(Prompt, "ask", fake_ask)
    return calls

def test_default_value_used_when_no_prompt_provided(fake_ask):
    # No prompts dict provided, default should be used in the message
    result = read_user_variable("name", default_value="John")
    assert result == "fixed_value"
    # The message should contain the variable name
    assert fake_ask[0][0] == "name"
    # The default passed to Prompt.ask should be the default_value
    assert fake_ask[0][1] == "John"

def test_custom_prompt_overrides_variable_name(fake_ask):
    # Provide a custom prompt for the variable
    prompts = {"name": "What is your full name?"}
    result = read_user_variable("name", default_value="John", prompts=prompts)
    assert result == "fixed_value"
    # The message should use the custom prompt
    assert fake_ask[0][0] == "What is your full name?"
    # The default passed to Prompt.ask should still be the default_value
    assert fake_ask[0][1] == "John"

def test_prefix_is_prepended_to_prompt(fake_ask):
    # Provide a prefix that should appear before the question
    prompts = {"name": "What is your full name?"}
    result = read_user_variable("name", default_value="John", prompts=prompts, prefix=">>> ")
    assert result == "fixed_value"
    # The message should start with the prefix
    assert fake_ask[0][0].startswith(">>> ")
    # The rest of the message should be the custom prompt
    assert fake_ask[0][0] == ">>> What is your full name?"
