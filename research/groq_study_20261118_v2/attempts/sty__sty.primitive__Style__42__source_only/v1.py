import pytest
from sty.primitive import Style
from typing import Iterable


def test_style_creation_with_rules_and_value():
    """Creating a Style with explicit rules and a value stores both correctly."""
    rule1 = object()
    rule2 = object()
    value = "\x1b[31m"
    style = Style(rule1, rule2, value=value)
    # The string representation should be the provided value
    assert str(style) == value
    # The rules attribute should be a tuple containing the rules in order
    assert isinstance(style.rules, tuple)
    assert style.rules == (rule1, rule2)


def test_style_creation_without_rules():
    """Creating a Style without rules should still produce a string and empty rules."""
    value = "\x1b[32m"
    style = Style(value=value)
    assert str(style) == value
    assert style.rules == ()
    # The type of rules should be a tuple (empty)
    assert isinstance(style.rules, tuple)


def test_style_is_subclass_of_str_and_immutable():
    """Style instances should behave like strings and be immutable."""
    style = Style("\x1b[33m")
    # isinstance checks
    assert isinstance(style, Style)
    assert isinstance(style, str)
    # Immutability: attempting to modify should not raise an error but create a new string
    new_style = style + "extra"
    assert isinstance(new_style, Style)
    assert new_style != style
    # Direct item assignment is not allowed on strings
    with pytest.raises(TypeError):
        style[0] = "x"


def test_style_rules_are_not_shared_between_instances():
    """Rules should be stored per instance, not shared."""
    rule = object()
    style1 = Style(rule, value="a")
    style2 = Style(rule, value="b")
    assert style1.rules is not style2.rules
    assert style1.rules == style2.rules == (rule,)


def test_style_str_conversion_and_repr():
    """String conversion and representation should reflect the underlying string."""
    value = "\x1b[34m"
    style = Style(value=value)
    # str() should return the value
    assert str(style) == value
    # repr() should show the string representation with escape sequences
    assert repr(style) == repr(value)


def test_style_rules_can_be_any_iterable():
    """Rules can be any iterable; they are stored as a tuple."""
    rules_list: Iterable[int] = [1, 2, 3]
    style = Style(*rules_list, value="x")
    assert style.rules == (1, 2, 3)


def test_style_rules_are_readonly():
    """Attempting to modify the rules attribute should raise AttributeError."""
    style = Style(1, 2, value="x")
    with pytest.raises(AttributeError):
        style.rules = (3, 4)


def test_style_equality_and_hash():
    """Style instances compare equal to their string value and are hashable."""
    value = "\x1b[35m"
    style1 = Style(value=value)
    style2 = Style(value=value)
    assert style1 == style2
    assert hash(style1) == hash(value)
    # They are equal to a plain string because Style is a subclass of str
    assert style1 == value


def test_style_with_empty_value_and_rules():
    """Creating a Style with no value and no rules should produce an empty string."""
    style = Style()
    assert str(style) == ""
    assert style.rules == ()
