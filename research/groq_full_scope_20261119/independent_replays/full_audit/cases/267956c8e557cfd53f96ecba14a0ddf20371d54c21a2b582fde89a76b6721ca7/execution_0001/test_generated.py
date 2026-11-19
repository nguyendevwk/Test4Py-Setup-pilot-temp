import json
import pytest
from httpie.output.formatters.json import JSONFormatter


def test_json_formatter_indents_and_sorts_keys(tmp_path):
    # Prepare a formatter with sorting and indentation enabled
    formatter = JSONFormatter(
        format_options={
            'json': {'format': True, 'sort_keys': True, 'indent': 2}
        },
        explicit_json=False
    )
    # Body contains JSON with unsorted keys
    body = '{"b": 1, "a": 2}'
    mime = 'application/json'
    formatted = formatter.format_body(body, mime)

    # The output should be pretty‑printed with keys sorted alphabetically
    expected = json.dumps(
        {"a": 2, "b": 1},
        sort_keys=True,
        ensure_ascii=False,
        indent=2
    )
    assert formatted == expected


def test_json_formatter_with_explicit_json_flag(tmp_path):
    # When explicit_json is True, the formatter should attempt to parse the body
    formatter = JSONFormatter(
        format_options={
            'json': {'format': True, 'sort_keys': False, 'indent': None}
        },
        explicit_json=True
    )
    # Body contains JSON with a prefix
    body = 'prefix: {"c": 3, "b": 2}'
    mime = 'text/plain'
    formatted = formatter.format_body(body, mime)

    # The prefix should be preserved and the JSON part should be formatted
    expected_json = json.dumps(
        {"c": 3, "b": 2},
        sort_keys=False,
        ensure_ascii=False,
        indent=None
    )
    assert formatted == f'prefix: {expected_json}'


def test_json_formatter_invalid_json_returns_original(tmp_path):
    # Formatter should ignore invalid JSON and return the original body
    formatter = JSONFormatter(
        format_options={
            'json': {'format': True, 'sort_keys': True, 'indent': 4}
        },
        explicit_json=False
    )
    body = 'not a json string'
    mime = 'application/json'
    formatted = formatter.format_body(body, mime)

    # The body should be unchanged because parsing failed
    assert formatted == body
