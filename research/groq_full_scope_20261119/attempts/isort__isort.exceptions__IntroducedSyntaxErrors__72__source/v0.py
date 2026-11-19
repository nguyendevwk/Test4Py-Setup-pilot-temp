import pytest
from isort.exceptions import IntroducedSyntaxErrors


def test_exception_initialization_and_message():
    """Verify that the exception stores the file path and constructs the correct message."""
    file_path = "example.py"
    exc = IntroducedSyntaxErrors(file_path)

    # The file_path attribute should be set correctly
    assert exc.file_path == file_path

    # The message should contain the file path and a descriptive prefix
    expected_start = "isort introduced syntax errors when attempting to sort the imports contained within"
    assert str(exc).startswith(expected_start)
    assert file_path in str(exc)


def test_exception_is_subclass_of_exception_and_str():
    """Ensure the exception behaves like a standard Exception."""
    file_path = "module.py"
    exc = IntroducedSyntaxErrors(file_path)

    # It should be an instance of Exception and the custom base class
    assert isinstance(exc, Exception)
    assert isinstance(exc, IntroducedSyntaxErrors)

    # The string representation should be the same as the message
    assert str(exc) == exc.args[0]


def test_exception_message_consistency_across_multiple_instances():
    """Check that multiple instances produce consistent messages with their respective file paths."""
    paths = ["a.py", "b.py", "c.py"]
    exceptions = [IntroducedSyntaxErrors(p) for p in paths]

    for exc, path in zip(exceptions, paths):
        # Each message should be unique to its file path
        assert path in str(exc)
        # The message should not accidentally contain other paths
        for other_path in paths:
            if other_path != path:
                assert other_path not in str(exc)
