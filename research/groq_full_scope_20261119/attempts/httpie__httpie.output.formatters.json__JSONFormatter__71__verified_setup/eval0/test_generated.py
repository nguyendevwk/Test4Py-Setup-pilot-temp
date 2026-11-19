import json
import pytest
from httpie.output.formatters.json import JSONFormatter


def test_format_body_formats_valid_json_with_default_options():
    # Default formatter options: indent=4, sort_keys=True
    formatter = JSONFormatter()
    body = '{"b":2,"a":1}'
    mime = 'application/json'
    formatted = formatter.format_body(body, mime)
    # The output should be pretty‑printed and sorted by key
    expected = json.dumps(
        {"a": 1, "b": 2},
        sort_keys=True,
        ensure_ascii=False,
        indent=4
    )
    assert formatted == expected


def test_format_body_parses_explicit_json_when_mime_not_json():
    # Set explicit_json to True so that the formatter attempts to parse
    formatter = JSONFormatter(explicit_json=True)
    body = '{"z": 26, "y": 25}'
    mime = 'text/plain'  # not a JSON mime type
    formatted = formatter.format_body(body, mime)
    expected = json.dumps(
        {"y": 25, "z": 26},
        sort_keys=True,
        ensure_ascii=False,
        indent=4
    )
    assert formatted == expected


def test_format_body_ignores_invalid_json_and_returns_original_body():
    formatter = JSONFormatter()
    body = 'not a json string'
    mime = 'application/json'
    # The formatter should catch ValueError and return the original body unchanged
    formatted = formatter.format_body(body, mime)
    assert formatted == body
