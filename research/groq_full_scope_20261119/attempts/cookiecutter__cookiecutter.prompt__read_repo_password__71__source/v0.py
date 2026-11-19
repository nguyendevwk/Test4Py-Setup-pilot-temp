import inspect
import typing
import pytest
from cookiecutter.prompt import read_repo_password

def test_read_repo_password_signature_and_return_annotation():
    """Verify that read_repo_password is a callable with the expected signature and return type."""
    assert inspect.isfunction(read_repo_password), "read_repo_password should be a function"
    sig = inspect.signature(read_repo_password)
    params = sig.parameters
    assert len(params) == 1, "read_repo_password should accept exactly one positional argument"
    assert "question" in params, "Parameter name should be 'question'"
    assert params["question"].annotation is inspect._empty or params["question"].annotation is str, \
        "Parameter 'question' should be annotated as str or unannotated"
    assert sig.return_annotation is inspect._empty or sig.return_annotation is str, \
        "Return annotation should be str or unannotated"

def test_read_repo_password_raises_on_non_string_argument():
    """Passing a non-string argument should raise a TypeError because Prompt.ask expects a string."""
    with pytest.raises(TypeError):
        read_repo_password(123)  # type: ignore[arg-type]

def test_read_repo_password_type_hints():
    """Ensure that the function's type hints are consistent with its implementation."""
    hints = typing.get_type_hints(read_repo_password)
    assert hints.get("question") is str, "Type hint for 'question' should be str"
    assert hints.get("return") is str, "Return type hint should be str"
