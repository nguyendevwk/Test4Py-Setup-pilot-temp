import builtins
import inspect
import types
import pytest
from cookiecutter.prompt import read_repo_password

def test_read_repo_password_docstring():
    """The function should have a docstring describing its purpose."""
    assert inspect.isfunction(read_repo_password)
    assert "Prompt the user" in read_repo_password.__doc__

def test_read_repo_password_signature():
    """The function should accept exactly one positional argument."""
    sig = inspect.signature(read_repo_password)
    params = list(sig.parameters.values())
    assert len(params) == 1
    assert params[0].name == "question"
    assert params[0].kind == inspect.Parameter.POSITIONAL_OR_KEYWORD

def test_read_repo_password_returns_input(monkeypatch):
    """When the user provides input, the function returns that string."""
    # Simulate user entering 's3cr3t' as the password
    monkeypatch.setattr(builtins, "input", lambda *args, **kwargs: "s3cr3t")
    result = read_repo_password("Enter password:")
    assert isinstance(result, str)
    assert result == "s3cr3t"
