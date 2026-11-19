import json
import pytest
from httpie.output.formatters.json import JSONFormatter


def test_format_body_with_valid_json_and_default_options():
    """When body contains valid JSON and mime indicates JSON, the formatter
    should pretty‑print it with default indentation and sorted keys."""
    formatter = JSONFormatter()
    body = '{"b":2,"a":1}'
    mime = 'application/json'
    formatted = formatter.format_body(body, mime)
    # The output should be pretty‑printed with 4‑space indent and sorted keys
    expected = json.dumps(
        {"a": 1, "b": 2},
        sort_keys=True,
        ensure_ascii=False,
        indent=4
    )
    assert formatted == expected


def test_format_body_with_explicit_json_flag_and_non_json_mime():
    """When explicit_json is True, the formatter should attempt to parse
    the body regardless of the mime type."""
    formatter = JSONFormatter(explicit_json=True)
    body = '{"z": 26, "y": 25}'
    mime = 'text/plain'
    formatted = formatter.format_body(body, mime)
    expected = json.dumps(
        {"y": 25, "z": 26},
        sort_keys=True,
        ensure_ascii=False,
        indent=4
    )
    assert formatted == expected


def test_format_body_with_invalid_json_returns_original_body():
    """If the body cannot be parsed as JSON, the formatter should return the
    original body unchanged."""
    formatter = JSONFormatter()
    body = 'this is not json'
    mime = 'application/json'
    formatted = formatter.format_body(body, mime)
    assert formatted == body
