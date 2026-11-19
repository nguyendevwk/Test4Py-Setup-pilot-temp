import pytest
from cookiecutter.prompt import read_user_dict, JsonPrompt

# Test that a non-dict default raises TypeError
def test_read_user_dict_non_dict_default():
    with pytest.raises(TypeError):
        read_user_dict("foo", ["not", "a", "dict"])

# Test that the function returns the default when JsonPrompt.ask is mocked
def test_read_user_dict_returns_default(monkeypatch):
    # Mock JsonPrompt.ask to simply return the default value
    def fake_ask(prompt, default, show_default):
        assert prompt.startswith("foo")
        assert show_default is False
        return default
    monkeypatch.setattr(JsonPrompt, "ask", staticmethod(fake_ask))
    default = {"key": "value"}
    result = read_user_dict("foo", default)
    assert result == default

# Test that the question string is derived from prompts when provided
def test_read_user_dict_uses_prompt_question(monkeypatch):
    def fake_ask(prompt, default, show_default):
        # The prompt should contain the custom question from prompts
        assert "Custom Question" in prompt
        return default
    monkeypatch.setattr(JsonPrompt, "ask", staticmethod(fake_ask))
    default = {"a": 1}
    prompts = {"foo": "Custom Question"}
    result = read_user_dict("foo", default, prompts=prompts)
    assert result == default
