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
    # Construct a KeyValueArg with a MIME type
    arg = KeyValueArg(orig="file", value=f"{file_path}::text/plain")
    name, fobj, mime = process_file_upload_arg(arg)
    # Assertions
    assert name == "test.txt"
    assert isinstance(fobj, io.BufferedReader)
    assert mime == "text/plain"
    # Verify file content
    assert fobj.read() == b"hello world"
    fobj.close()

def test_process_file_upload_arg_without_mime(tmp_path):
    # Create a temporary file with a .txt extension
    file_path = tmp_path / "data.txt"
    file_path.write_text("sample")
    # Construct a KeyValueArg without specifying MIME type
    arg = KeyValueArg(orig="file", value=str(file_path))
    name, fobj, mime = process_file_upload_arg(arg)
    # Assertions
    assert name == "data.txt"
    assert isinstance(fobj, io.BufferedReader)
    # MIME type should be guessed from extension
    assert mime == "text/plain"
    assert fobj.read() == b"sample"
    fobj.close()

def test_process_file_upload_arg_missing_file(tmp_path):
    # Path to a non-existent file
    missing_path = tmp_path / "missing.txt"
    arg = KeyValueArg(orig="file", value=str(missing_path))
    with pytest.raises(ParseError) as excinfo:
        process_file_upload_arg(arg)
    # The exception message should contain the original argument and the OS error
    assert str(missing_path) in str(excinfo.value)
    assert "No such file or directory" in str(excinfo.value)
