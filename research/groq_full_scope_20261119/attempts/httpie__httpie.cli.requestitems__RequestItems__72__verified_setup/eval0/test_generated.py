import os
import json
import tempfile
import pytest
from httpie.cli.requestitems import RequestItems
from httpie.cli.argtypes import KeyValueArg
from httpie.cli.constants import (
    SEPARATOR_HEADER,
    SEPARATOR_HEADER_EMPTY,
    SEPARATOR_DATA_STRING,
    SEPARATOR_DATA_RAW_JSON,
    SEPARATOR_FILE_UPLOAD,
    RequestType,
)
from httpie.cli.dicts import HTTPHeadersDict, RequestDataDict, RequestFilesDict


def test_header_and_empty_header_parsing(tmp_path):
    """Headers should be parsed correctly, including empty values."""
    # Create a temporary file for the file upload test
    header_file = tmp_path / "header.txt"
    header_file.write_text("value")

    args = [
        KeyValueArg(key="X-Custom", sep=SEPARATOR_HEADER, value="123"),
        KeyValueArg(key="X-Empty", sep=SEPARATOR_HEADER_EMPTY, value=""),
        KeyValueArg(key="X-File", sep=SEPARATOR_HEADER, value=str(header_file)),
    ]

    items = RequestItems.from_args(args, request_type=RequestType.JSON)

    # Headers are stored in an HTTPHeadersDict
    assert isinstance(items.headers, HTTPHeadersDict)
    assert items.headers["X-Custom"] == ["123"]
    assert items.headers["X-Empty"] == [""]
    # Header file content is read and stored as a string
    assert items.headers["X-File"] == [header_file.read_text()]


def test_data_string_and_raw_json_parsing(tmp_path):
    """Data string and raw JSON should be parsed into the data dict."""
    # Create a temporary JSON file for raw JSON embedding
    json_file = tmp_path / "data.json"
    json_file.write_text(json.dumps({"foo": "bar"}))

    args = [
        KeyValueArg(key="name", sep=SEPARATOR_DATA_STRING, value="Alice"),
        KeyValueArg(key="config", sep=SEPARATOR_DATA_RAW_JSON, value=json_file),
    ]

    items = RequestItems.from_args(args, request_type=RequestType.JSON)

    # Data is stored in a RequestJSONDataDict
    assert isinstance(items.data, RequestDataDict)
    assert items.data["name"] == ["Alice"]
    # Raw JSON file is parsed and stored as a dict
    assert items.data["config"] == [{"foo": "bar"}]


def test_file_upload_and_multipart_parsing(tmp_path):
    """File upload arguments should populate files and multipart_data correctly."""
    # Create a temporary file to upload
    upload_file = tmp_path / "upload.txt"
    upload_file.write_text("content")

    args = [
        KeyValueArg(key="file1", sep=SEPARATOR_FILE_UPLOAD, value=str(upload_file)),
        KeyValueArg(key="field1", sep=SEPARATOR_DATA_STRING, value="value1"),
    ]

    items = RequestItems.from_args(args, request_type=RequestType.JSON)

    # Files dict should contain the file path
    assert isinstance(items.files, RequestFilesDict)
    assert items.files["file1"] == [str(upload_file)]

    # Multipart data should contain the same key for file uploads
    assert isinstance(items.multipart_data, RequestDataDict)
    assert items.multipart_data["file1"] == [str(upload_file)]

    # Non-file data should be in the normal data dict
    assert items.data["field1"] == ["value1"]
