import os
import json
import tempfile
import pytest
from httpie.cli.requestitems import RequestItems, SEPARATOR_HEADER, SEPARATOR_DATA_STRING, SEPARATOR_FILE_UPLOAD, SEPARATOR_DATA_RAW_JSON
from httpie.cli.argtypes import KeyValueArg
from httpie.cli.constants import RequestType

def test_header_and_query_params(tmp_path):
    # Create a header and a query param
    header_arg = KeyValueArg(key="X-Test", value="value", sep=SEPARATOR_HEADER)
    query_arg = KeyValueArg(key="q", value="search", sep=SEPARATOR_HEADER)  # using header separator for simplicity
    items = RequestItems.from_args([header_arg, query_arg])
    # Header should be stored in headers dict
    assert items.headers["X-Test"] == "value"
    # Query param should be stored in params dict
    assert items.params["q"] == "search"

def test_data_string_and_json_mode(tmp_path):
    # Data string argument in JSON mode
    data_arg = KeyValueArg(key="name", value="Alice", sep=SEPARATOR_DATA_STRING)
    items = RequestItems.from_args([data_arg], request_type=RequestType.JSON)
    # In JSON mode, data should be a JSON dict
    assert items.is_json is True
    assert items.data["name"] == "Alice"
    # Raw JSON argument should be parsed into dict
    raw_json_arg = KeyValueArg(key="config", value='{"enabled":true}', sep=SEPARATOR_DATA_RAW_JSON)
    items = RequestItems.from_args([raw_json_arg], request_type=RequestType.JSON)
    assert items.data["config"] == {"enabled": True}

def test_file_upload_and_multipart(tmp_path):
    # Create a temporary file to upload
    file_path = tmp_path / "test.txt"
    file_path.write_text("content")
    file_arg = KeyValueArg(key="file", value=str(file_path), sep=SEPARATOR_FILE_UPLOAD)
    # Add a multipart data field
    multipart_arg = KeyValueArg(key="field", value="value", sep=SEPARATOR_HEADER)
    items = RequestItems.from_args([file_arg, multipart_arg])
    # File should be present in files dict
    assert "file" in items.files
    # Multipart data should be stored separately
    assert items.multipart_data["field"] == "value"
    # The file content should be readable
    with items.files["file"] as f:
        assert f.read() == b"content"
