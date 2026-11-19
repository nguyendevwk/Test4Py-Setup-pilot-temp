import json
import pytest
from httpie.output.formatters.colors import ColorFormatter, AUTO_STYLE, PIE_STYLES
from httpie.context import Environment
from httpie.plugins import FormatterPlugin

# Helper to create a minimal Environment with colors enabled
def make_env(colors=256):
    env = Environment()
    env.colors = colors
    return env

def test_format_headers_basic():
    """Headers are highlighted with ANSI escape codes when colors are enabled."""
    env = make_env(colors=256)
    formatter = ColorFormatter(env, color_scheme=AUTO_STYLE)
    # Simple HTTP request headers
    headers = "GET / HTTP/1.1\r\nHost: example.com\r\n\r\n"
    highlighted = formatter.format_headers(headers)
    # ANSI escape codes start with \x1b[ and end with m
    assert "\x1b[" in highlighted
    assert highlighted.endswith("\x1b[0m")  # reset code at end
    # The original text should still be present
    assert "GET / HTTP/1.1" in highlighted
    assert "Host: example.com" in highlighted

def test_format_body_json_explicit():
    """Explicit JSON flag forces JSON lexer regardless of MIME type."""
    env = make_env(colors=256)
    formatter = ColorFormatter(env, explicit_json=True)
    body = '{"key": "value"}'
    # MIME type that is not JSON
    highlighted = formatter.format_body(body, mime="text/plain")
    # Should contain JSON lexer tokens (e.g., color for string)
    assert "\x1b[" in highlighted
    assert "value" in highlighted
    # Ensure the body is not returned unchanged
    assert highlighted != body

def test_invalid_style_fallback():
    """Providing an unknown style falls back to Solarized256Style without error."""
    env = make_env(colors=256)
    # Use a nonsense style name
    formatter = ColorFormatter(env, color_scheme="nonexistent_style")
    # Format headers; should not raise and should use fallback style
    headers = "GET / HTTP/1.1\r\nHost: example.com\r\n\r\n"
    highlighted = formatter.format_headers(headers)
    assert "\x1b[" in highlighted
    # The fallback style still produces ANSI codes
    assert highlighted.endswith("\x1b[0m")
