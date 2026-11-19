import os
import pytest
from httpie.cli.requestitems import load_text_file
from httpie.cli.argtypes import KeyValueArg
from httpie.cli.exceptions import ParseError

def test_load_text_file_success(tmp_path):
    # Create a temporary UTF‑8 text file
    txt = tmp_path / "sample.txt"
    txt.write_text("Hello, world!\nLine 2", encoding="utf-8")
    kv = KeyValueArg(orig="--data @sample.txt", value=str(txt), key=None, is_file=True)
    result = load_text_file(kv)
    assert result == "Hello, world!\nLine 2"

def test_load_text_file_not_found(tmp_path):
    # Path that does not exist
    missing = tmp_path / "missing.txt"
    kv = KeyValueArg(orig="--data @missing.txt", value=str(missing), key=None, is_file=True)
    with pytest.raises(ParseError) as excinfo:
        load_text_file(kv)
    assert "missing.txt" in str(excinfo.value)
    assert "No such file or directory" in str(excinfo.value)

def test_load_text_file_invalid_encoding(tmp_path):
    # Create a binary file that is not valid UTF‑8
    bin_file = tmp_path / "binary.bin"
    bin_file.write_bytes(b"\xff\xfe\xfd")
    kv = KeyValueArg(orig="--data @binary.bin", value=str(bin_file), key=None, is_file=True)
    with pytest.raises(ParseError) as excinfo:
        load_text_file(kv)
    assert "cannot embed the content of" in str(excinfo.value)
    assert "binary.bin" in str(excinfo.value)
