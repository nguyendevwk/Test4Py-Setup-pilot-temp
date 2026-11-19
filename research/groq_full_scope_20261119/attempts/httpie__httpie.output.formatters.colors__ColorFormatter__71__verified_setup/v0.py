import json
import re
import pygments
import pytest
from httpie.output.formatters.colors import ColorFormatter
from httpie.context import Environment
from httpie.plugins import FormatterPlugin

# Helper to create a minimal Environment with colors enabled
def make_env(colors=256):
    env = Environment()
    env.colors = colors
    return env

def test_format_headers_includes_ansi_codes():
    """Headers should be syntax highlighted with ANSI escape codes."""
    env = make_env(colors=256)
    formatter = ColorFormatter(env, color_scheme="monokai")
    headers = "GET / HTTP/1.1\r\nHost: example.com\r\n\r\n"
    highlighted = formatter.format_headers(headers)
    # ANSI escape codes start with \x1b[ and end with m
    assert re.search(r"\x1b\[[0-9;]*m", highlighted), "No ANSI codes found in highlighted headers"
    # The output should not contain the raw header string
    assert headers.strip() not in highlighted, "Raw headers should be escaped"

def test_get_lexer_for_body_returns_json_lexer_for_json_mime():
    """Explicit JSON flag or application/json mime should return a JSON lexer."""
    env = make_env(colors=256)
    formatter = ColorFormatter(env, explicit_json=True)
    body = '{"key": "value"}'
    lexer = formatter.get_lexer_for_body("application/json", body)
    assert lexer is not None, "Lexer should not be None for JSON"
    # The lexer should be a subclass of pygments.lexer.Lexer
    assert issubclass(lexer, pygments.lexer.Lexer), "Returned lexer is not a Pygments lexer"

def test_get_lexer_for_body_returns_none_for_unknown_mime():
    """Unknown MIME types should result in no lexer and no highlighting."""
    env = make_env(colors=256)
    formatter = ColorFormatter(env)
    body = "Some plain text"
    lexer = formatter.get_lexer_for_body("application/unknown", body)
    assert lexer is None, "Lexer should be None for unsupported MIME type"
    # When lexer is None, format_body should return the original body unchanged
    formatted = formatter.format_body(body, "application/unknown")
    assert formatted == body, "Body should be unchanged when no lexer is found"
