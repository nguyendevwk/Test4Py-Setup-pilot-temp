import mimetypes
import os
import tempfile
import pytest
from httpie.utils import get_content_type

def test_known_extension(tmp_path):
    # Create a temporary file with a known extension
    file_path = tmp_path / "example.txt"
    file_path.write_text("Hello, world!")
    # The MIME type for .txt should be 'text/plain'
    assert get_content_type(str(file_path)) == "text/plain"
    # Ensure that mimetypes can guess the same type
    assert mimetypes.guess_type(str(file_path), strict=False)[0] == "text/plain"

def test_unknown_extension(tmp_path):
    # Create a temporary file with an unknown extension
    file_path = tmp_path / "file.unknownext"
    file_path.write_text("Some content")
    # The function should return None for an unknown extension
    assert get_content_type(str(file_path)) is None
    # Verify that mimetypes also returns None for this extension
    assert mimetypes.guess_type(str(file_path), strict=False)[0] is None

def test_empty_string():
    # Passing an empty string should result in None
    assert get_content_type("") is None
    # Mimic the underlying mimetypes behavior for an empty string
    assert mimetypes.guess_type("", strict=False)[0] is None
