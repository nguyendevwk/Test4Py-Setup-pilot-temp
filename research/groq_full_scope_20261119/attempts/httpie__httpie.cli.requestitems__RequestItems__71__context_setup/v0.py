import os
import io
import pytest
from httpie.cli.requestitems import RequestItems, SEPARATOR_HEADER, SEPARATOR_QUERY_PARAM, SEPARATOR_DATA_STRING, SEPARATOR_FILE_UPLOAD, SEPARATOR_HEADER_EMPTY
from httpie.cli.argtypes import KeyValueArg
from httpie.cli.constants import RequestType

def make_arg(key, value, sep, orig=None):
    """Helper to create a KeyValueArg with minimal required attributes."""
    if orig is None:
        orig = f"{key}{sep}{value}"
    return KeyValueArg(key=key, value=value, sep=sep, orig=orig)

def test_normal_header_and_query_and_data(tmp_path):
    # Create a temporary file for data embedding
    data_file = tmp_path / "data.txt"
    data_file.write_text("file content")
    # Build arguments
    args = [
        make_arg("X-Custom", "value", SEPARATOR_HEADER),
        make_arg("q", "search", SEPARATOR_QUERY_PARAM),
        make_arg("payload", "simple", SEPARATOR_DATA_STRING),
        make_arg("file", f"{data_file}::text/plain", SEPARATOR_FILE_UPLOAD),
    ]
    items = RequestItems.from_args(args, request_type=RequestType.JSON)
    # Header
    assert items.headers["X-Custom"] == "value"
    # Query param
    assert items.params["q"] == "search"
    # Data
    assert items.data["payload"] == "simple"
    # File upload
    filename, fileobj, mime = items.files["file"]
    assert filename == "data.txt"
    assert mime == "text/plain"
    assert fileobj.read() == b"file content"
    fileobj.close()

def test_empty_header_error():
    # Empty header should raise ParseError
    args = [make_arg("Empty", "", SEPARATOR_HEADER_EMPTY)]
    with pytest.raises(Exception) as excinfo:
        RequestItems.from_args(args)
    assert "Invalid item" in str(excinfo.value)

def test_multipart_order_preservation(tmp_path):
    # Create two files
    file1 = tmp_path / "a.txt"
    file1.write_text("a")
    file2 = tmp_path / "b.txt"
    file2.write_text("b")
    # Arguments with multipart separator
    args = [
        make_arg("part1", f"{file1}::text/plain", SEPARATOR_FILE_UPLOAD),
        make_arg("part2", f"{file2}::text/plain", SEPARATOR_FILE_UPLOAD),
    ]
    items = RequestItems.from_args(args)
    # multipart_data should preserve insertion order
    keys = list(items.multipart_data.keys())
    assert keys == ["part1", "part2"]
    # Verify file contents
    for key in keys:
        filename, fileobj, mime = items.files[key]
        content = fileobj.read()
        fileobj.close()
        assert content == (b"a" if key == "part1" else b"b")
        assert mime == "text/plain"
