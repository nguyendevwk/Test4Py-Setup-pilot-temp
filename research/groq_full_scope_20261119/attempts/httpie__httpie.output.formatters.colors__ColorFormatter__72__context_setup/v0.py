import json
import pygments
import pytest
from httpie.output.formatters.colors import ColorFormatter, get_lexer
from httpie.context import Environment
from httpie.plugins import FormatterPlugin


class DummyEnvironment(Environment):
    """Minimal Environment stub for testing ColorFormatter."""
    def __init__(self, colors):
        self.colors = colors
        self._config = {}


def test_color_formatter_formats_headers_and_body(tmp_path):
    """ColorFormatter should apply syntax highlighting to headers and body."""
    env = DummyEnvironment(colors=256)
    formatter = ColorFormatter(env, explicit_json=False, color_scheme="solarized256")
    headers = "GET / HTTP/1.1\r\nHost: example.com\r\n"
    body = '{"key":"value"}'

    # Format headers
    formatted_headers = formatter.format_headers(headers)
    # The output should contain ANSI escape sequences (start with \x1b)
    assert "\x1b[" in formatted_headers
    # The original header lines should still be present
    assert "GET / HTTP/1.1" in formatted_headers
    assert "Host: example.com" in formatted_headers

    # Format body with JSON mime
    formatted_body = formatter.format_body(body, "application/json")
    assert "\x1b[" in formatted_body
    assert json.loads(formatted_body.splitlines()[-1]) == {"key": "value"}


def test_color_formatter_no_colors_disables_plugin(tmp_path):
    """When Environment.colors is falsy, the plugin should be disabled."""
    env = DummyEnvironment(colors=0)
    formatter = ColorFormatter(env, explicit_json=False, color_scheme="solarized256")
    # The plugin should be disabled and return None for formatters
    assert not formatter.enabled
    # format_headers should return the original string unchanged
    headers = "GET / HTTP/1.1\r\nHost: example.com\r\n"
    assert formatter.format_headers(headers) == headers
    # format_body should return the original body unchanged
    body = '{"key":"value"}'
    assert formatter.format_body(body, "application/json") == body


def test_color_formatter_explicit_json_uses_json_lexer(tmp_path):
    """When explicit_json is True, a JSON body with wrong MIME should still be highlighted."""
    env = DummyEnvironment(colors=256)
    formatter = ColorFormatter(env, explicit_json=True, color_scheme="solarized256")
    # Wrong MIME but JSON body
    body = '{"foo":"bar"}'
    formatted_body = formatter.format_body(body, "text/plain")
    # Should contain ANSI codes indicating JSON highlighting
    assert "\x1b[" in formatted_body
    # The JSON content should still be valid
    assert json.loads(formatted_body.splitlines()[-1]) == {"foo": "bar"}
