import json
import pygments.lexers
import pytest
from httpie.output.formatters.colors import get_lexer
from pygments.lexers.data import JsonLexer
from pygments.lexers.special import TextLexer
from ..lexers.json import EnhancedJsonLexer  # type: ignore


def test_get_lexer_json_mime_returns_enhanced_json_lexer():
    """When the MIME type is application/json, the function should return
    the custom EnhancedJsonLexer."""
    lexer = get_lexer("application/json")
    assert lexer is EnhancedJsonLexer, (
        f"Expected EnhancedJsonLexer, got {lexer!r}"
    )
    # The returned lexer should be a subclass of JsonLexer
    assert issubclass(lexer, JsonLexer), (
        f"Returned lexer {lexer!r} is not a subclass of JsonLexer"
    )


def test_get_lexer_with_plus_in_subtype_returns_json_lexer():
    """MIME types with a '+' in the subtype should still resolve to a JSON lexer."""
    # The MIME type contains '+json', so the lexer should be the standard JSON lexer
    lexer = get_lexer("application/vnd.api+json")
    # The function should return the standard JsonLexer (not the enhanced one)
    assert lexer is pygments.lexers.get_lexer_by_name("json"), (
        f"Expected standard JsonLexer, got {lexer!r}"
    )
    # Ensure that the returned lexer is not the custom EnhancedJsonLexer
    assert lexer is not EnhancedJsonLexer, (
        "Returned lexer should not be EnhancedJsonLexer for '+json' subtype"
    )


def test_get_lexer_explicit_json_with_non_json_body_returns_none():
    """When explicit_json is True but the body is not valid JSON, the lexer should remain None."""
    # Use a MIME type that normally resolves to TextLexer
    lexer = get_lexer("text/plain", explicit_json=True, body="not a json string")
    # Since the body is not JSON, the function should not override the lexer
    assert lexer is None or isinstance(lexer, TextLexer), (
        f"Expected None or TextLexer, got {lexer!r}"
    )
    # Ensure that no JSON lexer is returned
    assert not isinstance(lexer, JsonLexer), (
        "Lexer should not be a JsonLexer when body is not JSON"
    )
