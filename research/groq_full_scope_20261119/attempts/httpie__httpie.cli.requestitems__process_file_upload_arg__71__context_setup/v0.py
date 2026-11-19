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
    # Construct KeyValueArg with filename only
    arg = KeyValueArg(orig="file", value=str(tmp_file))
    name, file_obj, mime = process_file_upload_arg(arg)
    # Assertions
    assert name == "test.txt"
    assert isinstance(file_obj, io.BufferedReader)
    assert file_obj.read() == b"hello world"
    # MIME type should be inferred from extension
    assert mime == "text/plain"

def test_process_file_upload_arg_with_explicit_mime(tmp_path):
    # Create a temporary file with .bin extension
    tmp_file = tmp_path / "data.bin"
    tmp_file.write_bytes(b"\x00\x01\x02")
    # Provide explicit MIME type after separator
    arg = KeyValueArg(orig="file", value=f"{tmp_file}{KeyValueArg.SEPARATOR_FILE_UPLOAD_TYPE}application/octet-stream")
    name, file_obj, mime = process_file_upload_arg(arg)
    assert name == "data.bin"
    assert file_obj.read() == b"\x00\x01\x02"
    # MIME type should be the explicit one
    assert mime == "application/octet-stream"

def test_process_file_upload_arg_missing_file_raises_parse_error(tmp_path):
    # Path that does not exist
    missing_path = tmp_path / "nonexistent.txt"
    arg = KeyValueArg(orig="file", value=str(missing_path))
    with pytest.raises(ParseError) as excinfo:
        process_file_upload_arg(arg)
    # The exception message should contain the original argument and the OS error
    assert str(missing_path) in str(excinfo.value)
    assert "No such file or directory" in str(excinfo.value)
