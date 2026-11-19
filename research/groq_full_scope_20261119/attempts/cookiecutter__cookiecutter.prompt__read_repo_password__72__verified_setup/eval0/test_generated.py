import pytest
from cookiecutter.prompt import read_repo_password
from rich.prompt import Prompt, InvalidResponse

def test_read_repo_password_normal(monkeypatch):
    # Simulate a normal password entry
    def fake_ask(question, password=False):
        assert question == "Enter password:"
        assert password is True
        return "s3cr3t"
    monkeypatch.setattr(Prompt, "ask", fake_ask)
    result = read_repo_password("Enter password:")
    assert result == "s3cr3t"

def test_read_repo_password_empty(monkeypatch):
    # Simulate the user entering an empty password
    def fake_ask(question, password=False):
        assert question == "Password?"
        assert password is True
        return ""
    monkeypatch.setattr(Prompt, "ask", fake_ask)
    result = read_repo_password("Password?")
    assert result == ""

def test_read_repo_password_invalid_response(monkeypatch):
    # Simulate Prompt.ask raising an InvalidResponse exception
    def fake_ask(question, password=False):
        raise InvalidResponse("User aborted")
    monkeypatch.setattr(Prompt, "ask", fake_ask)
    with pytest.raises(InvalidResponse, match="User aborted"):
        read_repo_password("Any question")
