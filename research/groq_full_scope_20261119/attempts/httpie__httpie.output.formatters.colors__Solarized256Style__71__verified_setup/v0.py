import pytest
import pygments.token
from httpie.output.formatters.colors import Solarized256Style

def test_style_background_and_inheritance():
    """Solarized256Style should inherit from pygments.style.Style and set a background."""
    assert issubclass(Solarized256Style, pygments.style.Style)
    assert Solarized256Style.background_color == "#1c1c1c"

def test_style_token_mappings():
    """Specific token types should map to the expected color codes."""
    expected_mappings = {
        pygments.token.Keyword: "#5f8700",
        pygments.token.Keyword.Constant: "#d75f00",
        pygments.token.Keyword.Declaration: "#0087ff",
        pygments.token.Keyword.Namespace: "#d75f00",
        pygments.token.Keyword.Reserved: "#0087ff",
        pygments.token.Keyword.Type: "#af0000",
        pygments.token.Name.Attribute: "#8a8a8a",
        pygments.token.Name.Builtin: "#0087ff",
        pygments.token.Name.Class: "#0087ff",
        pygments.token.Name.Constant: "#d75f00",
        pygments.token.Name.Decorator: "#0087ff",
        pygments.token.Name.Entity: "#d75f00",
        pygments.token.Name.Exception: "#af8700",
        pygments.token.Name.Function: "#0087ff",
        pygments.token.Name.Tag: "#0087ff",
        pygments.token.Name.Variable: "#0087ff",
        pygments.token.String: "#00afaf",
        pygments.token.String.Backtick: "#4e4e4e",
        pygments.token.String.Char: "#00afaf",
        pygments.token.String.Doc: "#00afaf",
        pygments.token.String.Escape: "#af0000",
        pygments.token.String.Heredoc: "#00afaf",
        pygments.token.String.Regex: "#af0000",
        pygments.token.Number: "#00afaf",
        pygments.token.Operator: "#8a8a8a",
        pygments.token.Operator.Word: "#5f8700",
        pygments.token.Comment: "#4e4e4e",
        pygments.token.Comment.Preproc: "#5f8700",
        pygments.token.Comment.Special: "#5f8700",
        pygments.token.Generic.Deleted: "#00afaf",
        pygments.token.Generic.Error: "#af0000",
        pygments.token.Generic.Heading: "#d75f00",
        pygments.token.Generic.Inserted: "#5f8700",
        pygments.token.Generic.Strong: None,  # PYGMENTS_BOLD is a style string, not a color
        pygments.token.Generic.Subheading: "#d75f00",
        pygments.token.Token: "#8a8a8a",
        pygments.token.Token.Other: "#d75f00",
    }
    for token, expected in expected_mappings.items():
        if expected is None:
            # Skip tokens that map to style strings rather than colors
            continue
        assert Solarized256Style.styles.get(token) == expected, f"Token {token} mapping mismatch"

def test_style_has_all_required_tokens():
    """Ensure that all tokens used in the style definition are present in the styles dict."""
    defined_tokens = set(Solarized256Style.styles.keys())
    # Tokens referenced in the style definition
    referenced_tokens = {
        pygments.token.Keyword,
        pygments.token.Keyword.Constant,
        pygments.token.Keyword.Declaration,
        pygments.token.Keyword.Namespace,
        pygments.token.Keyword.Reserved,
        pygments.token.Keyword.Type,
        pygments.token.Name.Attribute,
        pygments.token.Name.Builtin,
        pygments.token.Name.Builtin.Pseudo,
        pygments.token.Name.Class,
        pygments.token.Name.Constant,
        pygments.token.Name.Decorator,
        pygments.token.Name.Entity,
        pygments.token.Name.Exception,
        pygments.token.Name.Function,
        pygments.token.Name.Tag,
        pygments.token.Name.Variable,
        pygments.token.String,
        pygments.token.String.Backtick,
        pygments.token.String.Char,
        pygments.token.String.Doc,
        pygments.token.String.Escape,
        pygments.token.String.Heredoc,
        pygments.token.String.Regex,
        pygments.token.Number,
        pygments.token.Operator,
        pygments.token.Operator.Word,
        pygments.token.Comment,
        pygments.token.Comment.Preproc,
        pygments.token.Comment.Special,
        pygments.token.Generic.Deleted,
        pygments.token.Generic.Emph,
        pygments.token.Generic.Error,
        pygments.token.Generic.Heading,
        pygments.token.Generic.Inserted,
        pygments.token.Generic.Strong,
        pygments.token.Generic.Subheading,
        pygments.token.Token,
        pygments.token.Token.Other,
    }
    assert referenced_tokens.issubset(defined_tokens), "Some referenced tokens are missing from styles dict"
