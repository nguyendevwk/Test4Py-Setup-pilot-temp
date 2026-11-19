import json
import pygments.lexers
import pytest
from httpie.output.formatters.colors import get_lexer
from pygments.lexers.data import JsonLexer
from pygments.lexers.special import TextLexer
from pygments.lexers.text import HttpLexer as PygmentsHttpLexer

def test_get_lexer_basic_mime():
    # MIME type without '+' should map to the subtype lexer
    lexer = get_lexer("application/json")
    assert isinstance(lexer, JsonLexer) or isinstance(lexer, type(EnhancedJsonLexer))
    # MIME type with '+' should try both parts
    lexer_plus = get_lexer("application/vnd.api+json")
    # The lexer should be the JSON lexer because of the 'json' suffix
    assert isinstance(lexer_plus, JsonLexer) or isinstance(lexer_plus, type(EnhancedJsonLexer))

def test_get_lexer_fallback_to_name_and_json():
    # MIME type that is not registered should fall back to name lookup
    lexer = get_lexer("application/x-custom+json")
    # Since 'x-custom' is not a known lexer, it should fall back to 'json'
    assert isinstance(lexer, JsonLexer) or isinstance(lexer, type(EnhancedJsonLexer))
    # Explicit JSON with wrong Content-Type should still return JSON lexer
    body = '{"key":"value"}'
    lexer_explicit = get_lexer("text/plain", explicit_json=True, body=body)
    assert isinstance(lexer_explicit, JsonLexer) or isinstance(lexer_explicit, type(EnhancedJsonLexer))

def test_get_lexer_invalid_json_body():
    # Explicit JSON flag with invalid JSON body should not change lexer
    lexer = get_lexer("text/plain", explicit_json=True, body="not a json")
    # Should return None because no lexer found and body invalid
    assert lexer is None
