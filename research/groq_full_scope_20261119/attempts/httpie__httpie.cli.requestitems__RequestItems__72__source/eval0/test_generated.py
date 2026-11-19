import os
import json
import tempfile
import pytest
from httpie.cli.requestitems import RequestItems
from httpie.cli.argtypes import KeyValueArg
from httpie.cli.constants import (
    SEPARATOR_HEADER,
    SEPARATOR_HEADER_EMPTY,
    SEPARATOR_HEADER_EMBED,
    SEPARATOR_QUERY_PARAM,
    SEPARATOR_QUERY_EMBED_FILE,
    SEPARATOR_FILE_UPLOAD,
    SEPARATOR_DATA_STRING,
    SEPARATOR_DATA_EMBED_FILE_CONTENTS,
    SEPARATOR_GROUP_NESTED_JSON_ITEMS,
    SEPARATOR_DATA_RAW_JSON,
    SEPARATOR_DATA_EMBED_RAW_JSON_FILE,
    RequestType,
)

# Helper to create a KeyValueArg
def kv(key: str, value: str, sep: str) -> KeyValueArg:
    return KeyValueArg(key=key, value=value, sep=sep)

def test_headers_and_query_params(tmp_path):
    # Header with value
    header_arg = kv("X-Test", "value", SEPARATOR_HEADER)
    # Empty header
    empty_header_arg = kv("X-Empty", "", SEPARATOR_HEADER_EMPTY)
    # Embedded header
    embed_header_arg = kv("X-Embed", "embed:value", SEPARATOR_HEADER_EMBED)
    # Query param
    query_arg = kv("q", "search", SEPARATOR_QUERY_PARAM)
    # Embedded query param from file
    file_path = tmp_path / "q.txt"
    file_path.write_text("filequery")
    embed_query_arg = kv("q", str(file_path), SEPARATOR_QUERY_EMBED_FILE)

    items = RequestItems.from_args(
        [header_arg, empty_header_arg, embed_header_arg, query_arg, embed_query_arg],
        request_type=RequestType.JSON,
    )

    # Headers
    assert items.headers["X-Test"] == ["value"]
    assert items.headers["X-Empty"] == [""]  # empty header preserved
    assert items.headers["X-Embed"] == ["embed:value"]
    # Query params
    assert items.params["q"] == ["search", "filequery"]
    # Data should be empty dict in JSON mode
    assert items.data == {}

def test_file_upload_and_data(tmp_path):
    # File upload
    file_path = tmp_path / "upload.txt"
    file_path.write_text("content")
    file_arg = kv("file", str(file_path), SEPARATOR_FILE_UPLOAD)
    # Data string
    data_arg = kv("name", "value", SEPARATOR_DATA_STRING)
    # Data embed file contents
    embed_file_arg = kv("desc", str(file_path), SEPARATOR_DATA_EMBED_FILE_CONTENTS)

    items = RequestItems.from_args(
        [file_arg, data_arg, embed_file_arg],
        request_type=RequestType.JSON,
    )

    # Files dict contains a file object
    assert "file" in items.files
    file_obj = items.files["file"]
    assert hasattr(file_obj, "read")
    file_obj.seek(0)
    assert file_obj.read() == b"content"
    # Data dict contains string and embedded file contents
    assert items.data["name"] == "value"
    assert items.data["desc"] == "content"

def test_json_mode_conversion_and_nested_json(tmp_path):
    # Raw JSON value that should be converted to form if not in JSON mode
    raw_json_arg = kv("config", '{"a":1}', SEPARATOR_DATA_RAW_JSON)
    # Raw JSON from file
    json_file = tmp_path / "config.json"
    json_file.write_text('{"b":2}')
    raw_json_file_arg = kv("config", str(json_file), SEPARATOR_DATA_EMBED_RAW_JSON_FILE)
    # Nested JSON items group
    nested_arg1 = kv("user.name", "Alice", SEPARATOR_GROUP_NESTED_JSON_ITEMS)
    nested_arg2 = kv("user.age", "30", SEPARATOR_GROUP_NESTED_JSON_ITEMS)

    items = RequestItems.from_args(
        [raw_json_arg, raw_json_file_arg, nested_arg1, nested_arg2],
        request_type=RequestType.JSON,
    )

    # In JSON mode, raw JSON should be parsed into dict
    assert items.data["config"] == {"a": 1}
    # File-based raw JSON parsed
    assert items.data["config"] == {"b": 2}
    # Nested JSON items merged into dict
    assert items.data["user"] == {"name": "Alice", "age": "30"}
