import sys
import io
import os
import pytest
from httpie.uploads import is_stdin


def test_is_stdin_with_regular_file(tmp_path):
    """`is_stdin` should return False for a normal file."""
    file_path = tmp_path / "test.txt"
    file_path.write_text("content")
    with open(file_path, "rb") as f:
        assert is_stdin(f) is False


def test_is_stdin_with_stdin_object():
    """`is_stdin` should return True when the file's fileno matches sys.stdin's."""
    class DummyStdin:
        def fileno(self):
            return sys.stdin.fileno()

    dummy = DummyStdin()
    assert is_stdin(dummy) is True


def test_is_stdin_with_no_fileno():
    """`is_stdin` should return False when the object has no fileno method."""
    class NoFileno:
        pass

    obj = NoFileno()
    assert is_stdin(obj) is False
