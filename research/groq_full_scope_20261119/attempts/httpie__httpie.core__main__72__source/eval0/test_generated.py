import inspect
import pytest
from httpie.core import main
from httpie.status import ExitStatus

def test_main_signature():
    """Verify that main accepts the expected parameters and returns ExitStatus."""
    sig = inspect.signature(main)
    assert sig.parameters["args"].default == pytest.importorskip("sys").argv
    assert sig.parameters["env"].default is not None
    assert sig.return_annotation is ExitStatus

def test_main_returns_exit_status_type():
    """Calling main with minimal arguments should return an ExitStatus instance."""
    # Use a minimal argument list that is unlikely to trigger complex logic
    # but still allows main to run without raising unexpected exceptions.
    # We catch any exception to ensure the function returns ExitStatus when possible.
    try:
        result = main(args=["httpie", "--version"])
    except Exception as exc:
        # If an exception occurs, ensure it's not a TypeError from wrong signature
        assert not isinstance(exc, TypeError)
        raise
    assert isinstance(result, ExitStatus)

def test_main_invalid_args_type():
    """Passing a non-list to args should raise a TypeError."""
    with pytest.raises(TypeError):
        main(args="not a list")
