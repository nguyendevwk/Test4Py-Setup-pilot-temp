import json
import pygments.lexers
import pytest
from httpie.output.formatters.colors import get_lexer
from pygments.lexers.data import JsonLexer
from pygments.lexers.special import TextLexer
from pygments.lexers.text import HttpLexer as PygmentsHttpLexer

def test_get_lexer_basic_mime():
    # MIME type with no '+' should map to the subtype lexer
    lexer = get_lexer("application/json")
    assert isinstance(lexer, type)
    # The returned lexer should be the enhanced JSON lexer
    assert issubclass(lexer, JsonLexer) or lexer.__name__ == "EnhancedJsonLexer"

def test_get_lexer_with_plus_and_fallback():
    # MIME type with '+' should try both parts and fallback to subtype
    lexer = get_lexer("application/vnd.api+json")
    # Should resolve to the JSON lexer (enhanced)
    assert isinstance(lexer, type)
    assert issubclass(lexer, JsonLexer) or lexer.__name__ == "EnhancedJsonLexer"

def test_get_lexer_explicit_json_body():
    # Provide a body that is valid JSON but MIME type is plain text
    body = '{"key": "value"}'
    lexer = get_lexer("text/plain", explicit_json=True, body=body)
    # Should return the JSON lexer because body is valid JSON
    assert isinstance(lexer, type)
    assert issubclass(lexer, JsonLexer) or lexer.__name__ == "EnhancedJsonLexer"
