import json
import pytest
from httpie.output.formatters.colors import ColorFormatter, get_lexer
from httpie.context import Environment
from httpie.plugins import FormatterPlugin

# Helper environment with colors enabled
class DummyEnv(Environment):
    def __init__(self, colors):
        self.colors = colors

def test_format_headers_returns_highlighted_string():
    env = DummyEnv(colors=256)
    formatter = ColorFormatter(env, color_scheme="solarized256")
    headers = "GET / HTTP/1.1\r\nHost: example.com\r\n"
    highlighted = formatter.format_headers(headers)
    # The output should contain ANSI escape sequences for color
    assert "\x1b[" in highlighted
    # The original headers should still be present
    assert "GET / HTTP/1.1" in highlighted
    assert "Host: example.com" in highlighted

def test_format_body_json_highlights_and_parses():
    env = DummyEnv(colors=256)
    formatter = ColorFormatter(env, explicit_json=True, color_scheme="solarized256")
    body = json.dumps({"key": "value", "number": 123})
    highlighted = formatter.format_body(body, "application/json")
    # Should contain ANSI escape sequences
    assert "\x1b[" in highlighted
    # The JSON keys and values should be present
    assert '"key"' in highlighted
    assert '"value"' in highlighted
    # The body should not be truncated
    assert "123" in highlighted

def test_formatter_disabled_when_colors_off():
    env = DummyEnv(colors=0)
    formatter = ColorFormatter(env, color_scheme="solarized256")
    # When colors are disabled, the formatter should not be enabled
    assert not formatter.enabled
    # format_headers should return the raw headers without highlighting
    headers = "GET / HTTP/1.1\r\nHost: example.com\r\n"
    result = formatter.format_headers(headers)
    # No ANSI escape sequences should be present
    assert "\x1b[" not in result
    # The result should match the input exactly
    assert result == headers.strip()
