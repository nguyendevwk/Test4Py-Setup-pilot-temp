import json
import pytest
from httpie.output.formatters.json import JSONFormatter


def test_format_body_with_valid_json_and_sorting_and_indent():
    formatter = JSONFormatter(
        format_options={
            'json': {
                'format': True,
                'sort_keys': True,
                'indent': 2,
            }
        },
        explicit_json=False,
    )
    body = '{"b": 1, "a": 2}'
    mime = 'application/json'
    formatted = formatter.format_body(body, mime)
    # The output should be pretty‑printed with sorted keys
    expected = json.dumps(
        {"a": 2, "b": 1},
        sort_keys=True,
        ensure_ascii=False,
        indent=2,
    )
    assert formatted == expected


def test_format_body_with_explicit_json_flag_and_non_json_mime():
    formatter = JSONFormatter(
        format_options={
            'json': {
                'format': True,
                'sort_keys': False,
                'indent': None,
            }
        },
        explicit_json=True,
    )
    body = '{"z": 26, "y": 25}'
    mime = 'text/plain'
    formatted = formatter.format_body(body, mime)
    # Since explicit_json is True, it should format regardless of mime
    expected = json.dumps(
        {"z": 26, "y": 25},
        sort_keys=False,
        ensure_ascii=False,
        indent=None,
    )
    assert formatted == expected


def test_format_body_with_invalid_json_returns_original_body():
    formatter = JSONFormatter(
        format_options={
            'json': {
                'format': True,
                'sort_keys': True,
                'indent': 4,
            }
        },
        explicit_json=False,
    )
    body = 'not a json string'
    mime = 'application/json'
    formatted = formatter.format_body(body, mime)
    # Invalid JSON should leave the body unchanged
    assert formatted == body
