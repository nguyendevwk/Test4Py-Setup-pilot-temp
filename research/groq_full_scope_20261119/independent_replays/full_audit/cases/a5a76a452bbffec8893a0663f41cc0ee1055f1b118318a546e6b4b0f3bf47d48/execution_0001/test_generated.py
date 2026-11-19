import pytest
from cookiecutter.prompt import read_user_variable
from rich.prompt import Prompt

@pytest.fixture
def fake_prompt(monkeypatch):
    """Replace Prompt.ask with a stub that records its arguments and returns a fixed value."""
    calls = []

    def stub_ask(message, default=None):
        calls.append((message, default))
        return "stub_value"

    monkeypatch.setattr(Prompt, "ask", staticmethod(stub_ask))
    return calls

def test_default_value_used_when_no_prompt_provided(fake_prompt):
    """When no prompts dict is supplied, the variable name is used as the question."""
    result = read_user_variable("project_name", default_value="default_proj")
    assert result == "stub_value"
    # The question should be the variable name itself
    assert fake_prompt[0][0] == "project_name"
    # The default passed to Prompt.ask should be the default_value
    assert fake_prompt[0][1] == "default_proj"

def test_custom_prompt_overrides_variable_name(fake_prompt):
    """When a prompts dict contains a non-empty entry, it overrides the question."""
    prompts = {"project_name": "What is the project name?"}
    result = read_user_variable("project_name", default_value="default_proj", prompts=prompts)
    assert result == "stub_value"
    # The question should be taken from the prompts dict
    assert fake_prompt[0][0] == "What is the project name?"
    # The default passed to Prompt.ask should still be the default_value
    assert fake_prompt[0][1] == "default_proj"

def test_prefix_is_prepended_to_question(fake_prompt):
    """The prefix argument is prepended to the question string."""
    prompts = {"project_name": "Project name?"}
    result = read_user_variable("project_name", default_value="default_proj", prompts=prompts, prefix=">>> ")
    assert result == "stub_value"
    # The question should include the prefix
    assert fake_prompt[0][0] == ">>> Project name?"
    # The default passed to Prompt.ask should still be the default_value
    assert fake_prompt[0][1] == "default_proj"
