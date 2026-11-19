import json
import pygments.lexers
import pytest
from httpie.output.formatters.colors import get_lexer
from pygments.lexers.data import JsonLexer
from pygments.lexers.special import TextLexer
from pygments.lexers.text import HttpLexer as PygmentsHttpLexer
from httpie.lexers.json import EnhancedJsonLexer

def test_get_lexer_plain_mime_returns_expected_lexer():
    # MIME type without '+' should map to the subtype lexer
    lexer = get_lexer("application/json")
    assert isinstance(lexer, type)  # returns a lexer class
    # The returned lexer should be the Pygments JSON lexer
    assert lexer is pygments.lexers.get_lexer_by_name("json")

def test_get_lexer_with_plus_in_subtype_fallbacks_to_subtype_and_suffix():
    # MIME type with '+' should try both parts and fallback to subtype
    lexer = get_lexer("application/vnd.api+json")
    # The lexer should be the JSON lexer because 'json' is in subtype
    assert lexer is pygments.lexers.get_lexer_by_name("json")

def test_get_lexer_explicit_json_parses_body_and_selects_json_lexer():
    # Provide a body that is valid JSON but MIME type is plain text
    body = json.dumps({"key": "value"})
    lexer = get_lexer("text/plain", explicit_json=True, body=body)
    # Should return the JSON lexer, not the plain text lexer
    assert lexer is pygments.lexers.get_lexer_by_name("json")
    # Ensure that the lexer is not the TextLexer
    assert not isinstance(lexer, TextLexer)
