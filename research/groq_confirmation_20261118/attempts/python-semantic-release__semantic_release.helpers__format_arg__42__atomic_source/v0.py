import pytest
from semantic_release.helpers import format_arg

def test_format_arg_with_regular_string():
    """String values should be quoted and stripped of surrounding whitespace."""
    result = format_arg("  hello world  ")
    assert result == "'hello world'", f"Expected quoted stripped string, got {result}"

def test_format_arg_with_empty_string_and_non_string():
    """Empty string should be quoted as '' and non-string types should be converted to str."""
    empty_result = format_arg("")
    assert empty_result == "''", f"Expected '' for empty string, got {empty_result}"
    int_result = format_arg(42)
    assert int_result == "42", f"Expected '42' for integer, got {int_result}"
    float_result = format_arg(3.14)
    assert float_result == "3.14", f"Expected '3.14' for float, got {float_result}"
    bool_result = format_arg(True)
    assert bool_result == "True", f"Expected 'True' for bool, got {bool_result}"

def test_format_arg_with_special_characters_and_unicode():
    """Strings containing special characters or unicode should be handled correctly."""
    special = format_arg("  \t\n'\"\\\n")
    assert special == "'''\"\\'''", f"Unexpected formatting for special characters: {special}"
    unicode_str = format_arg("  café  ")
    assert unicode_str == "'café'", f"Unexpected formatting for unicode string: {unicode_str}"
