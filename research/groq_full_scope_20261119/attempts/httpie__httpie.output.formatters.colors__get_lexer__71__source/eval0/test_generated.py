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
    # The returned lexer should be the enhanced JSON lexer
    assert isinstance(lexer, type(pygments.lexers.get_lexer_by_name("json")))
    # Ensure it is not the base JsonLexer
    assert not isinstance(lexer, JsonLexer)

def test_get_lexer_with_plus_and_fallback():
    # MIME type with '+' should try both parts and fallback to subtype
    lexer = get_lexer("application/vnd.api+json")
    # The lexer should be the enhanced JSON lexer because 'json' is in subtype
    assert isinstance(lexer, type(pygments.lexers.get_lexer_by_name("json")))
    # Ensure that the lexer is not the base JsonLexer
    assert not isinstance(lexer, JsonLexer)

def test_get_lexer_explicit_json_body():
    # Provide a body that is valid JSON but with an incorrect MIME type
    body = '{"key": "value"}'
    lexer = get_lexer("text/plain", explicit_json=True, body=body)
    # Explicit JSON should override and return the enhanced JSON lexer
    assert isinstance(lexer, type(pygments.lexers.get_lexer_by_name("json")))
    # The lexer should not be a TextLexer
    assert not isinstance(lexer, TextLexer)
