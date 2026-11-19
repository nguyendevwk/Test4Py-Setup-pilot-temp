import pytest
from sty.primitive import Style
from sty.rendertype import RenderType

def test_style_creation_with_rules_and_value():
    """Creating a Style with explicit rules and a value stores both correctly."""
    rule1 = RenderType("fg", "red")
    rule2 = RenderType("bg", "blue")
    value = "\x1b[31m\x1b[44m"
    s = Style(rule1, rule2, value=value)
    # Style should be a subclass of str and contain the value
    assert isinstance(s, str)
    assert str(s) == value
    # The rules attribute should be a tuple of the passed rules
    assert isinstance(s.rules, tuple)
    assert s.rules == (rule1, rule2)

def test_style_creation_without_rules():
    """Creating a Style without rules results in an empty rules tuple."""
    value = "\x1b[0m"
    s = Style(value=value)
    assert isinstance(s, str)
    assert str(s) == value
    # No rules should be stored
    assert s.rules == ()

def test_style_equality_and_hash():
    """Two Style instances with the same value and rules are equal and hash identically."""
    rule = RenderType("fg", "green")
    value = "\x1b[32m"
    s1 = Style(rule, value=value)
    s2 = Style(rule, value=value)
    # Equality should be based on string value
    assert s1 == s2
    # Hash should match since strings are hashable
    assert hash(s1) == hash(s2)
    # Changing the value should break equality
    s3 = Style(rule, value="\x1b[31m")
    assert s1 != s3
