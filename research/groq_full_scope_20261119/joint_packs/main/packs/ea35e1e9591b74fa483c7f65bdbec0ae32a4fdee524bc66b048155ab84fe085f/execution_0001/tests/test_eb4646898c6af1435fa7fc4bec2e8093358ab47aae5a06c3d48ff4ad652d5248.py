import pytest
from cookiecutter.prompt import read_repo_password, Prompt, InvalidResponse

def test_read_repo_password_returns_value(monkeypatch):
    # Arrange: monkeypatch Prompt.ask to return a known password
    def fake_ask(question, password=False):
        assert question == "Enter password"
        assert password is True
        return "secret123"
    monkeypatch.setattr(Prompt, "ask", fake_ask)

    # Act
    result = read_repo_password("Enter password")

    # Assert
    assert result == "secret123"

def test_read_repo_password_empty_string(monkeypatch):
    # Arrange: monkeypatch Prompt.ask to return an empty string
    def fake_ask(question, password=False):
        return ""
    monkeypatch.setattr(Prompt, "ask", fake_ask)

    # Act
    result = read_repo_password("Enter password")

    # Assert
    assert result == ""

def test_read_repo_password_invalid_response(monkeypatch):
    # Arrange: monkeypatch Prompt.ask to raise InvalidResponse
    def fake_ask(question, password=False):
        raise InvalidResponse("User aborted")
    monkeypatch.setattr(Prompt, "ask", fake_ask)

    # Act & Assert
    with pytest.raises(InvalidResponse, match="User aborted"):
        read_repo_password("Enter password")
