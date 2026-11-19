import pytest
from httpie.output.formatters.colors import ColorFormatter
from httpie.context import Environment
from httpie.ui.palette import AUTO_STYLE

# Helper to create a minimal Environment with desired color setting
def make_env(colors):
    class DummyEnv:
        def __init__(self, colors):
            self.colors = colors
    return DummyEnv(colors)

def test_format_headers_returns_highlighted_string():
    env = make_env(colors=256)
    formatter = ColorFormatter(env, color_scheme=AUTO_STYLE)
    headers = "GET / HTTP/1.1\r\nHost: example.com\r\n"
    highlighted = formatter.format_headers(headers)
    # The output should contain ANSI escape sequences (e.g., \x1b[)
    assert "\x1b[" in highlighted
    # It should not be empty and should preserve the header lines
    assert "GET / HTTP/1.1" in highlighted
    assert "Host: example.com" in highlighted

def test_format_body_json_with_explicit_json():
    env = make_env(colors=256)
    formatter = ColorFormatter(env, explicit_json=True, color_scheme=AUTO_STYLE)
    body = '{"key":"value"}'
    highlighted = formatter.format_body(body, mime="application/json")
    # When explicit_json is True, the body should be highlighted
    assert "\x1b[" in highlighted
    # The original JSON should still be present
    assert '"key":"value"' in highlighted

def test_format_body_unknown_mime_returns_original():
    env = make_env(colors=256)
    formatter = ColorFormatter(env, explicit_json=False, color_scheme=AUTO_STYLE)
    body = "plain text body"
    highlighted = formatter.format_body(body, mime="text/plain")
    # No lexer should be found, so the body is returned unchanged
    assert highlighted == body
