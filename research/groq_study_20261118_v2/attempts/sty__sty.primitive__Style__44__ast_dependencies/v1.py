import pytest
from sty.primitive import Style
from sty.rendertype import RenderType

def test_style_is_str_and_has_rules_attribute():
    s = Style()
    assert isinstance(s, str)
    assert isinstance(s, Style)
    assert s == ""
    assert isinstance(s.rules, tuple)
    assert s.rules == ()

def test_style_with_rules_and_value():
    rt = RenderType()
    rt.args = [1, 2, 3]
    custom_value = "\x1b[31m"
    s = Style(rt, value=custom_value)
    assert isinstance(s, str)
    assert s == custom_value
    assert s.rules == (rt,)

def test_style_rules_are_immutable_tuple():
    rt1 = RenderType()
    rt2 = RenderType()
    s = Style(rt1, rt2)
    assert isinstance(s.rules, tuple)
    # The tuple itself is immutable; attempting to modify it creates a new tuple
    new_rules = s.rules + (RenderType(),)
    assert new_rules != s.rules
    assert s.rules == (rt1, rt2)

def test_style_with_multiple_rules_and_order():
    rt1 = RenderType()
    rt2 = RenderType()
    rt3 = RenderType()
    s = Style(rt1, rt2, rt3)
    assert s.rules == (rt1, rt2, rt3)

def test_style_value_overrides_default():
    s = Style(value="hello")
    assert s == "hello"

def test_style_rules_can_be_any_objects():
    class DummyRule:
        pass
    dummy = DummyRule()
    s = Style(dummy, value="test")
    assert s.rules == (dummy,)
    assert s == "test"

def test_style_str_representation_and_equality():
    s1 = Style(value="abc")
    s2 = Style(value="abc")
    assert s1 == s2
    assert s1 is not s2
    assert str(s1) == "abc"

def test_style_with_empty_value_and_rules():
    rt = RenderType()
    s = Style(rt, value="")
    assert s == ""
    assert s.rules == (rt,)

def test_style_rules_attribute_is_readonly_after_creation():
    rt = RenderType()
    s = Style(rt)
    original_rules = s.rules
    s.rules = (RenderType(),)
    assert s.rules != original_rules
    assert original_rules == (rt,)

def test_style_with_non_string_value_does_not_raise():
    # Style accepts any value that can be converted to a string
    s = Style(value=123)  # type: ignore[arg-type]
    assert s == "123"
