import os
import tempfile
import pytest
from httpie.cli.requestitems import RequestItems
from httpie.cli.argtypes import KeyValueArg
from httpie.cli.constants import (
    SEPARATOR_HEADER,
    SEPARATOR_HEADER_EMPTY,
    SEPARATOR_QUERY_PARAM,
    SEPARATOR_DATA_STRING,
    SEPARATOR_FILE_UPLOAD,
    SEPARATOR_GROUP_NESTED_JSON_ITEMS,
    SEPARATOR_DATA_RAW_JSON,
    RequestType,
)
from httpie.cli.exceptions import ParseError


def test_requestitems_from_args_basic():
    """Verify that headers, query params, data and files are parsed correctly."""
    # Create a temporary file to upload
    tmp_file = tempfile.NamedTemporaryFile(delete=False)
    tmp_file.write(b"hello world")
    tmp_file.close()

    args = [
        KeyValueArg(key="X-Test", value="value", sep=SEPARATOR_HEADER),
        KeyValueArg(key="q", value="search", sep=SEPARATOR_QUERY_PARAM),
        KeyValueArg(key="name", value="Alice", sep=SEPARATOR_DATA_STRING),
        KeyValueArg(key="file", value=tmp_file.name, sep=SEPARATOR_FILE_UPLOAD),
    ]

    items = RequestItems.from_args(args, request_type=RequestType.JSON)

    # Header
    assert items.headers["X-Test"] == ["value"]
    # Query param
    assert items.params["q"] == ["search"]
    # Data (JSON)
    assert items.data["name"] == "Alice"
    # File upload
    assert "file" in items.files
    assert items.files["file"].filename == os.path.basename(tmp_file.name)

    os.unlink(tmp_file.name)


def test_requestitems_from_args_empty_header_and_nested_json():
    """Test handling of empty header and nested JSON group."""
    args = [
        KeyValueArg(key="Empty", value="", sep=SEPARATOR_HEADER_EMPTY),
        KeyValueArg(key="json", value="{'a':1}", sep=SEPARATOR_GROUP_NESTED_JSON_ITEMS),
    ]

    items = RequestItems.from_args(args, request_type=RequestType.JSON)

    # Empty header should be present with empty string value
    assert items.headers["Empty"] == [""]
    # Nested JSON should be parsed into data dict
    assert items.data["json"] == {"a": 1}


def test_requestitems_from_args_invalid_separator_raises():
    """Passing an unknown separator should raise a KeyError."""
    args = [
        KeyValueArg(key="foo", value="bar", sep=":")  # not a defined separator
    ]

    with pytest.raises(KeyError):
        RequestItems.from_args(args, request_type=RequestType.JSON)
