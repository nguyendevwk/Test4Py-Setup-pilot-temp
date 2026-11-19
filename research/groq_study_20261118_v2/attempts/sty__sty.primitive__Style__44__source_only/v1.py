import pytest
from sty.primitive import Style
from typing import Iterable


def test_style_creation_and_str():
    """Creating a Style with rules stores them and the string value is preserved."""
    rule_a = object()
    rule_b = object()
    s = Style(rule_a, rule_b, value="custom_sequence")
    assert str(s) == "custom_sequence"
    assert isinstance(s, str)
    assert isinstance(s.rules, Iterable)
    assert list(s.rules) == [rule_a, rule_b]


def test_style_empty_and_default():
    """Style can be created without rules and with default empty string."""
    s = Style()
    assert str(s) == ""
    assert s.rules == ()
    assert isinstance(s, str)


def test_style_immutability_of_rules():
    """The rules attribute should be immutable and not affect the string value."""
    rule = object()
    s = Style(rule, value="seq")
    # Modifying the rules tuple by reassignment is allowed; it creates a new tuple.
    new_rules = s.rules + (object(),)
    assert new_rules != s.rules
    assert str(s) == "seq"


def test_style_multiple_rules_and_order():
    """Rules are stored in the order provided."""
    r1, r2, r3 = "r1", "r2", "r3"
    s = Style(r1, r2, r3, value="xyz")
    assert list(s.rules) == [r1, r2, r3]
    assert str(s) == "xyz"


def test_style_with_non_string_value():
    """Providing a non-string value does not raise an error; the value is converted to str."""
    s = Style(1, 2, value=123)  # type: ignore[arg-type]
    assert str(s) == "123"
    assert isinstance(s, str)


def test_style_equality_and_hash():
    """Style instances compare equal to their string value and are hashable."""
    s1 = Style("a", value="abc")
    s2 = Style("b", value="abc")
    assert s1 == s2
    assert hash(s1) == hash("abc")
    assert hash(s2) == hash("abc")


def test_style_repr_and_str_consistency():
    """repr should show the string representation."""
    s = Style("x", value="hello")
    assert repr(s) == "'hello'"
    assert str(s) == "hello"


def test_style_with_large_number_of_rules():
    """Style can handle many rules without error."""
    rules = tuple(range(1000))
    s = Style(*rules, value="large")
    assert len(s.rules) == 1000
    assert str(s) == "large"


def test_style_rules_are_not_shared_between_instances():
    """Rules tuple should be unique per instance."""
    rule = object()
    s1 = Style(rule, value="s1")
    s2 = Style(rule, value="s2")
    assert s1.rules is not s2.rules
    assert s1.rules == s2.rules == (rule,)


def test_style_with_none_value():
    """Providing None as value is converted to the string 'None'."""
    s = Style(object(), value=None)  # type: ignore[arg-type]
    assert str(s) == "None"
