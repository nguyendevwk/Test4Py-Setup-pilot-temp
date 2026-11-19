import json
import pytest
from httpie.output.formatters.json import JSONFormatter


def test_format_body_formats_valid_json_with_sort_and_indent():
    """JSONFormatter should format a valid JSON body with sorting and indentation."""
    formatter = JSONFormatter(
        format_options={
            'json': {
                'format': True,
                'sort_keys': True,
                'indent': 2
            }
        },
        explicit_json=False
    )
    body = '{"b":1,"a":2}'
    mime = 'application/json'
    formatted = formatter.format_body(body, mime)
    # The output should be pretty‑printed with sorted keys
    expected = json.dumps(
        {"a": 2, "b": 1},
        sort_keys=True,
        ensure_ascii=False,
        indent=2
    )
    assert formatted == expected


def test_format_body_parses_explicit_json_when_mime_not_json():
    """When explicit_json is True, JSONFormatter should parse JSON even if MIME type is not JSON."""
    formatter = JSONFormatter(
        format_options={
            'json': {
                'format': True,
                'sort_keys': False,
                'indent': None
            }
        },
        explicit_json=True
    )
    body = '{"x":10,"y":20}'
    mime = 'text/plain'
    formatted = formatter.format_body(body, mime)
    # No indentation, no sorting
    expected = json.dumps(
        {"x": 10, "y": 20},
        sort_keys=False,
        ensure_ascii=False,
        indent=None
    )
    assert formatted == expected


def test_format_body_ignores_invalid_json_and_returns_original():
    """If the body is not valid JSON, JSONFormatter should return the original body unchanged."""
    formatter = JSONFormatter(
        format_options={
            'json': {
                'format': True,
                'sort_keys': True,
                'indent': 4
            }
        },
        explicit_json=False
    )
    body = 'not a json string'
    mime = 'application/json'
    formatted = formatter.format_body(body, mime)
    # Since parsing fails, the original body should be returned
    assert formatted == body
