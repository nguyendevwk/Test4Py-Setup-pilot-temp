import os
import io
import pytest
from httpie.cli.requestitems import process_file_upload_arg
from httpie.argtypes import KeyValueArg
from httpie.exceptions import ParseError

def test_process_file_upload_arg_with_mime(tmp_path):
    # Create a temporary file with known content
    file_path = tmp_path / "test.txt"
    file_path.write_text("hello world")
    # Construct a KeyValueArg with explicit MIME type
    arg = KeyValueArg(orig="file=./test.txt:text/plain", key="file", value=str(file_path) + ":text/plain")
    name, fobj, mime = process_file_upload_arg(arg)
    # Assertions
    assert name == "test.txt"
    assert isinstance(fobj, io.BufferedReader)
    assert mime == "text/plain"
    # Verify file content
    assert fobj.read() == b"hello world"
    fobj.close()

def test_process_file_upload_arg_without_mime(tmp_path):
    # Create a temporary file with a .json extension
    file_path = tmp_path / "data.json"
    file_path.write_text('{"key":"value"}')
    # Construct a KeyValueArg without MIME type
    arg = KeyValueArg(orig="file=./data.json", key="file", value=str(file_path))
    name, fobj, mime = process_file_upload_arg(arg)
    # Assertions
    assert name == "data.json"
    assert isinstance(fobj, io.BufferedReader)
    # MIME type should be inferred from extension
    assert mime == "application/json"
    # Verify file content
    assert fobj.read() == b'{"key":"value"}'
    fobj.close()

def test_process_file_upload_arg_missing_file(tmp_path):
    # Path that does not exist
    missing_path = tmp_path / "does_not_exist.txt"
    arg = KeyValueArg(orig="file=./does_not_exist.txt", key="file", value=str(missing_path))
    with pytest.raises(ParseError) as excinfo:
        process_file_upload_arg(arg)
    # The exception message should contain the original argument string
    assert "does_not_exist.txt" in str(excinfo.value)
    # And should mention the OSError message
    assert "No such file or directory" in str(excinfo.value)
