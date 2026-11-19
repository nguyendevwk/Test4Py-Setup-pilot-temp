import os
import io
import pytest
from httpie.cli.requestitems import process_file_upload_arg
from httpie.cli.argtypes import KeyValueArg
from httpie.exceptions import ParseError

def test_process_file_upload_arg_reads_file_and_infers_mime(tmp_path):
    # Create a temporary file with known content and extension
    tmp_file = tmp_path / "test.txt"
    tmp_file.write_text("hello world")
    # Construct KeyValueArg with file path only (no MIME type)
    arg = KeyValueArg(orig="file", key="file", value=str(tmp_file))
    # Call the function
    name, fobj, mime = process_file_upload_arg(arg)
    # Assertions
    assert name == "test.txt"
    assert isinstance(fobj, io.BufferedReader)
    assert mime == "text/plain"
    # Verify file content
    assert fobj.read() == b"hello world"
    fobj.close()

def test_process_file_upload_arg_includes_explicit_mime(tmp_path):
    # Create a temporary file with .bin extension
    tmp_file = tmp_path / "data.bin"
    tmp_file.write_bytes(b"\x00\x01\x02")
    # Construct KeyValueArg with explicit MIME type
    arg = KeyValueArg(orig="file", key="file", value=f"{tmp_file}{KeyValueArg.SEPARATOR_FILE_UPLOAD_TYPE}application/octet-stream")
    name, fobj, mime = process_file_upload_arg(arg)
    assert name == "data.bin"
    assert mime == "application/octet-stream"
    assert fobj.read() == b"\x00\x01\x02"
    fobj.close()

def test_process_file_upload_arg_raises_parse_error_on_missing_file(tmp_path):
    # Path that does not exist
    missing_path = tmp_path / "nonexistent.txt"
    arg = KeyValueArg(orig="file", key="file", value=str(missing_path))
    with pytest.raises(ParseError) as excinfo:
        process_file_upload_arg(arg)
    # The exception message should contain the original argument string
    assert str(missing_path) in str(excinfo.value)
