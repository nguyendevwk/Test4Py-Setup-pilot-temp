import json
import pygments.lexers
import pytest
from httpie.output.formatters.colors import get_lexer
from httpie.lexers.json import EnhancedJsonLexer
from pygments.lexers.data import JsonLexer
from pygments.lexers.special import TextLexer


def test_get_lexer_json_mime_returns_enhanced_json_lexer():
    """When the MIME type is application/json, the function should return
    the custom EnhancedJsonLexer."""
    lexer = get_lexer("application/json")
    assert isinstance(lexer, type), "Expected a lexer class, got None"
    # The returned lexer should be the EnhancedJsonLexer class
    assert lexer is EnhancedJsonLexer, f"Expected EnhancedJsonLexer, got {lexer}"


def test_get_lexer_plus_mime_returns_json_lexer():
    """For a MIME type containing '+json', the function should resolve to
    the standard JSON lexer before falling back to the enhanced one."""
    lexer = get_lexer("application/vnd.api+json")
    # The standard JsonLexer is returned before the enhanced one is applied
    assert lexer is JsonLexer, f"Expected JsonLexer, got {lexer}"
    # Explicitly requesting the enhanced lexer still yields the same class
    enhanced = get_lexer("application/vnd.api+json", explicit_json=True)
    assert enhanced is EnhancedJsonLexer, f"Expected EnhancedJsonLexer, got {enhanced}"


def test_get_lexer_explicit_json_with_non_json_body_returns_none():
    """When explicit_json is True but the body is not valid JSON, the
    function should not override the lexer and should return None."""
    # MIME type that does not match any lexer
    lexer = get_lexer("application/unknown", explicit_json=True, body="not a json")
    assert lexer is None, f"Expected None, got {lexer}"
    # If a lexer is found but is TextLexer, it should still return None
    lexer = get_lexer("text/plain", explicit_json=True, body="not a json")
    assert lexer is None, f"Expected None, got {lexer}"
