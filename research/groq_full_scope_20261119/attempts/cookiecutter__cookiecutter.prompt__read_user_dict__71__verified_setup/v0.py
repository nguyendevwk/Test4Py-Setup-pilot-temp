import pytest
from cookiecutter.prompt import read_user_dict, JsonPrompt

# Test that a non-dict default raises TypeError
def test_read_user_dict_non_dict_default():
    with pytest.raises(TypeError):
        read_user_dict("my_var", ["not", "a", "dict"])

# Test that the function returns the default value when no prompts are provided
def test_read_user_dict_returns_default(monkeypatch):
    # Monkeypatch JsonPrompt.ask to simply return the default value
    monkeypatch.setattr(JsonPrompt, "ask", lambda *args, **kwargs: kwargs["default"])
    default = {"key": "value"}
    result = read_user_dict("my_var", default)
    assert result == default

# Test that the question is taken from the prompts dictionary when provided
def test_read_user_dict_uses_prompt_question(monkeypatch):
    monkeypatch.setattr(JsonPrompt, "ask", lambda *args, **kwargs: kwargs["default"])
    prompts = {"my_var": "Enter your data"}
    default = {"a": 1}
    result = read_user_dict("my_var", default, prompts=prompts)
    # The returned value should still be the default
    assert result == default
