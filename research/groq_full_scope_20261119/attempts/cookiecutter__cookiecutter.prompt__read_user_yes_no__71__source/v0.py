import pytest
from cookiecutter.prompt import read_user_yes_no
from rich.prompt import YesNoPrompt, InvalidResponse

# Helper to patch YesNoPrompt.ask
@pytest.fixture
def patch_yesno(monkeypatch):
    def _patch(return_value=None, side_effect=None):
        if side_effect is not None:
            monkeypatch.setattr(YesNoPrompt, "ask", side_effect)
        else:
            monkeypatch.setattr(YesNoPrompt, "ask", lambda *_, **__: return_value)
    return _patch

def test_read_user_yes_no_default(monkeypatch):
    """When no prompts dict is provided, the function should use the var_name as question
    and return the default value without calling YesNoPrompt.ask."""
    # Patch to detect if called
    called = False
    def fake_ask(*_, **__):
        nonlocal called
        called = True
        return True
    monkeypatch.setattr(YesNoPrompt, "ask", fake_ask)

    result = read_user_yes_no("my_var", default_value=False)
    assert result is False
    assert not called, "YesNoPrompt.ask should not be called when prompts is None"

def test_read_user_yes_no_yes(monkeypatch, patch_yesno):
    """When the user answers 'yes', the function should return True."""
    patch_yesno(return_value=True)
    result = read_user_yes_no("confirm", default_value=False, prompts={"confirm": "Proceed?"})
    assert result is True

def test_read_user_yes_no_invalid(monkeypatch, patch_yesno):
    """If YesNoPrompt.ask raises InvalidResponse, read_user_yes_no should propagate the exception."""
    patch_yesno(side_effect=InvalidResponse("invalid"))
    with pytest.raises(InvalidResponse):
        read_user_yes_no("confirm", default_value=False, prompts={"confirm": "Proceed?"})
