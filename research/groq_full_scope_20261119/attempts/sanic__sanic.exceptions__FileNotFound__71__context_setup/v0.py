import pytest
from sanic.exceptions import FileNotFound
from sanic.helpers import STATUS_CODES
from pathlib import Path


def test_file_not_found_default_attributes(tmp_path):
    """FileNotFound should inherit status_code and default quiet from NotFound."""
    exc = FileNotFound()
    # Status code should be 404 as defined in NotFound
    assert exc.status_code == 404
    # Quiet should default to True as set in NotFound
    assert exc.quiet is True
    # Message should be None, leading to default status message
    assert exc.message is None
    # Path and relative_url should be None by default
    assert exc.path is None
    assert exc.relative_url is None
    # The default response message should match the status code description
    assert exc.message is None
    assert STATUS_CODES[exc.status_code] == "Not Found"


def test_file_not_found_with_path_and_headers(tmp_path):
    """Providing a path and custom headers should store them correctly."""
    test_file = tmp_path / "missing.txt"
    headers = {"X-Custom-Header": "value"}
    exc = FileNotFound(
        message="File not found",
        path=test_file,
        relative_url="/missing.txt",
        headers=headers,
    )
    # Message should be preserved
    assert exc.message == "File not found"
    # Path should be stored as a PathLike object
    assert isinstance(exc.path, Path)
    assert exc.path == test_file
    # Relative URL should be stored
    assert exc.relative_url == "/missing.txt"
    # Headers should be stored
    assert exc.headers == headers
    # Quiet should be None because we didn't override it
    assert exc.quiet is None


def test_file_not_found_invalid_message_type():
    """Passing a non-string/non-bytes message should raise a TypeError."""
    with pytest.raises(TypeError):
        FileNotFound(message=123)  # type: ignore[arg-type]
