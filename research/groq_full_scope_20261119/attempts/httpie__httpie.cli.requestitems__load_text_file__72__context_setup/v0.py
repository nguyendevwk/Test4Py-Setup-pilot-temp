import os
import pytest
from httpie.cli.requestitems import load_text_file
from httpie.cli.argtypes import KeyValueArg
from httpie.cli.exceptions import ParseError

def test_load_text_file_success(tmp_path):
    # Create a temporary UTF‑8 text file
    file_path = tmp_path / "sample.txt"
    file_path.write_text("Hello, world!\nLine 2", encoding="utf-8")

    # Build a KeyValueArg with the file path
    kv = KeyValueArg(orig="--data @sample.txt", value=str(file_path), key=None)

    # load_text_file should return the file contents as a string
    content = load_text_file(kv)
    assert content == "Hello, world!\nLine 2"

def test_load_text_file_missing_file(tmp_path):
    # Path that does not exist
    missing_path = tmp_path / "does_not_exist.txt"
    kv = KeyValueArg(orig="--data @does_not_exist.txt", value=str(missing_path), key=None)

    # load_text_file should raise ParseError with a message containing the original argument
    with pytest.raises(ParseError) as excinfo:
        load_text_file(kv)
    assert "does_not_exist.txt" in str(excinfo.value)
    assert "does_not_exist.txt" in kv.orig

def test_load_text_file_invalid_encoding(tmp_path):
    # Create a binary file that is not valid UTF‑8
    binary_path = tmp_path / "binary.bin"
    binary_path.write_bytes(b'\xff\xfe\xfa\xfb')

    kv = KeyValueArg(orig="--data @binary.bin", value=str(binary_path), key=None)

    # load_text_file should raise ParseError indicating encoding issue
    with pytest.raises(ParseError) as excinfo:
        load_text_file(kv)
    assert "cannot embed the content of" in str(excinfo.value)
    assert "binary.bin" in str(excinfo.value)
