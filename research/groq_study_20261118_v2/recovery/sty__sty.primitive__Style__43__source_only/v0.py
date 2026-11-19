import pytest
from sty.primitive import Style


def test_style_is_str_subclass_and_instance():
    """Style should be an instance of str and subclass of str."""
    s = Style("hello")
    assert isinstance(s, str)
    assert isinstance(s, Style)
    assert Style.__mro__[0] is Style
    assert Style.__mro__[1] is str


def test_style_value_and_repr():
    """The string value passed to Style should be preserved."""
    value = "\x1b[31m"
    s = Style(value=value)
    assert str(s) == value
    assert repr(s) == f"Style('{value}')"


def test_style_rules_storage():
    """Rules passed to Style should be stored in the `rules` attribute."""
    rule1 = object()
    rule2 = object()
    s = Style(rule1, rule2)
    assert hasattr(s, "rules")
    assert isinstance(s.rules, tuple)
    assert s.rules == (rule1, rule2)


def test_style_no_rules():
    """Creating a Style without rules should result in an empty tuple."""
    s = Style()
    assert s.rules == ()
    assert isinstance(s.rules, tuple)


def test_style_rules_can_be_any_iterable():
    """Style should accept any iterable of rules, not just tuples."""
    rule_list = [1, 2, 3]
    s = Style(*rule_list)
    assert s.rules == tuple(rule_list)


def test_style_immutability_of_rules():
    """The `rules` attribute should be immutable (tuple)."""
    rule = object()
    s = Style(rule)
    with pytest.raises(AttributeError):
        s.rules = (rule,)


def test_style_str_operations():
    """Style should support string operations like concatenation."""
    s1 = Style("\x1b[31m")
    s2 = Style("\x1b[0m")
    combined = s1 + s2
    assert isinstance(combined, str)
    assert combined == "\x1b[31m\x1b[0m"
    # The combined string should not be a Style instance
    assert not isinstance(combined, Style)


def test_style_equality_and_hash():
    """Style instances should compare equal to their string value."""
    s1 = Style("\x1b[32m")
    s2 = Style("\x1b[32m")
    assert s1 == s2
    assert hash(s1) == hash(s2)


def test_style_with_non_string_value_raises_type_error():
    """Style should only accept string values; passing non-string should raise."""
    with pytest.raises(TypeError):
        # The underlying str.__new__ will raise a TypeError if value is not str
        Style(123)  # type: ignore[arg-type]


def test_style_rules_are_not_shared_between_instances():
    """Each Style instance should have its own rules tuple."""
    rule = object()
    s1 = Style(rule)
    s2 = Style(rule)
    assert s1.rules is not s2.rules
    assert s1.rules == s2.rules == (rule,)


def test_style_str_conversion_is_identity():
    """Converting a Style to str should return the same string."""
    value = "\x1b[34m"
    s = Style(value=value)
    assert str(s) == value
    assert s == value
