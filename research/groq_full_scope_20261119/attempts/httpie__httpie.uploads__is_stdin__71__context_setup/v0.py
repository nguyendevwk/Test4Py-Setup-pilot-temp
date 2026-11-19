import sys
import io
import pytest
from httpie.uploads import is_stdin


def test_is_stdin_with_actual_stdin():
    """When the file is sys.stdin, is_stdin should return True."""
    assert is_stdin(sys.stdin) is True


def test_is_stdin_with_regular_file(tmp_path):
    """When the file is a regular file, is_stdin should return False."""
    file_path = tmp_path / "test.txt"
    file_path.write_text("content")
    with open(file_path, "rb") as f:
        assert is_stdin(f) is False


def test_is_stdin_with_object_without_fileno():
    """When the object has no fileno method, is_stdin should return False."""
    class Dummy:
        pass

    dummy = Dummy()
    assert is_stdin(dummy) is False
