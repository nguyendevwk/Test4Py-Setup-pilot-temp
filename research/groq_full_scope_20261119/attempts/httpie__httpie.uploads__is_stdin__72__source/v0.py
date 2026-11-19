import sys
import io
import types
import pytest
from httpie.uploads import is_stdin


def test_is_stdin_with_regular_file(tmp_path):
    """A real file object should not be considered stdin."""
    file_path = tmp_path / "test.txt"
    file_path.write_text("content")
    with file_path.open("rb") as f:
        assert is_stdin(f) is False


def test_is_stdin_with_sys_stdin():
    """sys.stdin itself should be identified as stdin."""
    assert is_stdin(sys.stdin) is True


def test_is_stdin_with_non_fileno_and_exception():
    """Objects lacking fileno or raising on fileno should return False."""
    class NoFileno:
        pass

    class RaisesFileno:
        def fileno(self):
            raise OSError("no fileno")

    assert is_stdin(NoFileno()) is False
    assert is_stdin(RaisesFileno()) is False
