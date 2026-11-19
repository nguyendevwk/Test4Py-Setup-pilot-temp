import os
import io
import pytest
from httpie.cli.requestitems import RequestItems, SEPARATOR_HEADER, SEPARATOR_QUERY_PARAM, SEPARATOR_DATA_STRING, SEPARATOR_FILE_UPLOAD, SEPARATOR_DATA_RAW_JSON, SEPARATOR_GROUP_NESTED_JSON_ITEMS
from httpie.cli.argtypes import KeyValueArg
from httpie.cli.constants import RequestType

def make_arg(key, value, sep):
    return KeyValueArg(key=key, value=value, sep=sep, orig=f"{key}{sep}{value}")

def test_basic_header_query_and_data(tmp_path):
    # Create a temporary text file for header embedding
    header_file = tmp_path / "header.txt"
    header_file.write_text("X-Custom: Value\n")

    # Create a temporary file for data embedding
    data_file = tmp_path / "data.txt"
    data_file.write_text("embedded data")

    args = [
        make_arg("User-Agent", "curl/7.68.0", SEPARATOR_HEADER),
        make_arg("Accept", "", SEPARATOR_HEADER_EMPTY),
        make_arg("q", "search", SEPARATOR_QUERY_PARAM),
        make_arg("file", str(header_file), SEPARATOR_HEADER_EMBED),
        make_arg("payload", str(data_file), SEPARATOR_DATA_EMBED_FILE_CONTENTS),
        make_arg("raw", '{"key":"value"}', SEPARATOR_DATA_RAW_JSON),
    ]

    items = RequestItems.from_args(args, request_type=RequestType.JSON)

    # Header assertions
    assert items.headers["User-Agent"] == "curl/7.68.0"
    assert items.headers["Accept"] == ""
    assert items.headers["file"] == "X-Custom: Value"

    # Query param assertion
    assert items.params["q"] == "search"

    # Data assertions
    assert items.data["payload"] == "embedded data"
    assert items.data["raw"] == {"key": "value"}

def test_empty_header_error():
    args = [make_arg("Empty-Header", "value", SEPARATOR_HEADER_EMPTY)]
    with pytest.raises(Exception) as excinfo:
        RequestItems.from_args(args, request_type=RequestType.JSON)
    assert "Invalid item" in str(excinfo.value)

def test_multipart_and_json_conversion(tmp_path):
    # Create a file to upload
    upload_file = tmp_path / "upload.bin"
    upload_file.write_bytes(b"\x00\x01\x02")

    # JSON nested items
    nested_json_file = tmp_path / "nested.json"
    nested_json_file.write_text('{"a":1,"b":2}')

    args = [
        make_arg("file", f"{upload_file}{SEPARATOR_FILE_UPLOAD_TYPE}application/octet-stream", SEPARATOR_FILE_UPLOAD),
        make_arg("json", f"{nested_json_file}", SEPARATOR_GROUP_NESTED_JSON_ITEMS),
        make_arg("simple", "123", SEPARATOR_DATA_STRING),
    ]

    items = RequestItems.from_args(args, request_type=RequestType.JSON)

    # Multipart data should contain the file
    assert "file" in items.multipart_data
    filename, fileobj, mime = items.multipart_data["file"]
    assert filename == "upload.bin"
    assert mime == "application/octet-stream"
    assert isinstance(fileobj, io.BufferedReader)

    # Nested JSON should be parsed into data dict
    assert items.data["json"] == {"a": 1, "b": 2}

    # Simple string data
    assert items.data["simple"] == "123"
