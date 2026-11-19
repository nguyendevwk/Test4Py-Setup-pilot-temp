import json
import pytest
from httpie.output.formatters.colors import ColorFormatter
from httpie.context import Environment

# Helper environment with colors enabled
class DummyEnv:
    def __init__(self, colors=256):
        self.colors = colors

def test_format_headers_returns_highlighted_output():
    env = DummyEnv(colors=256)
    formatter = ColorFormatter(env, color_scheme="autumn")
    headers = "GET / HTTP/1.1\r\nHost: example.com\r\n"
    highlighted = formatter.format_headers(headers)
    # The output should contain ANSI escape codes (e.g., \x1b[)
    assert "\x1b[" in highlighted
    # The original header lines should still be present
    assert "GET / HTTP/1.1" in highlighted
    assert "Host: example.com" in highlighted

def test_format_body_json_highlights_and_returns_string():
    env = DummyEnv(colors=256)
    formatter = ColorFormatter(env, explicit_json=True, color_scheme="autumn")
    body_dict = {"key": "value"}
    body = json.dumps(body_dict, indent=2)
    highlighted = formatter.format_body(body, mime="application/json")
    # The output should contain ANSI escape codes
    assert "\x1b[" in highlighted
    # The JSON keys and values should still be present
    assert '"key"' in highlighted
    assert '"value"' in highlighted
    # The output should be a string (not None)
    assert isinstance(highlighted, str)

def test_get_lexer_for_body_returns_none_for_unknown_mime():
    env = DummyEnv(colors=256)
    formatter = ColorFormatter(env, explicit_json=False, color_scheme="autumn")
    # Use a MIME type that is unlikely to have a lexer
    lexer = formatter.get_lexer_for_body("application/unknown", body="some content")
    assert lexer is None
