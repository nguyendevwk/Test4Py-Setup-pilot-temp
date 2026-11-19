import pytest
from sty.primitive import Style
from sty.rendertype import RenderType

def test_style_is_str_and_has_rules_attribute():
    # Create a Style with no rules and default empty string
    s = Style()
    assert isinstance(s, str)
    assert isinstance(s, Style)
    assert s == ""  # default value
    # rules attribute should be an empty tuple
    assert isinstance(s.rules, tuple)
    assert s.rules == ()

def test_style_with_rules_and_value():
    # Define a dummy RenderType instance
    rt = RenderType()
    rt.args = [1, 2, 3]
    # Create a Style with rules and a custom value
    custom_value = "\x1b[31m"
    s = Style(rt, value=custom_value)
    assert isinstance(s, str)
    assert s == custom_value
    # rules should contain the RenderType instance
    assert s.rules == (rt,)

def test_style_rules_are_immutable_tuple():
    rt1 = RenderType()
    rt2 = RenderType()
    s = Style(rt1, rt2)
    # The rules attribute should be a tuple, not a list
    assert isinstance(s.rules, tuple)
    with pytest.raises(AttributeError):
        # Trying to modify the tuple should raise an error
        s.rules += (RenderType(),)

def test_style_with_multiple_rules_and_order():
    rt1 = RenderType()
    rt2 = RenderType()
    rt3 = RenderType()
    s = Style(rt1, rt2, rt3)
    # The order of rules should be preserved
    assert s.rules == (rt1, rt2, rt3)

def test_style_value_overrides_default():
    # Passing a non-empty value should override the default empty string
    s = Style(value="hello")
    assert s == "hello"

def test_style_rules_can_be_any_objects():
    # Rules can be any objects, not just RenderType
    class DummyRule:
        pass
    dummy = DummyRule()
    s = Style(dummy, value="test")
    assert s.rules == (dummy,)
    assert s == "test"

def test_style_str_representation_and_equality():
    # Two Style objects with same value should be equal
    s1 = Style(value="abc")
    s2 = Style(value="abc")
    assert s1 == s2
    # But they are distinct objects
    assert s1 is not s2
    # The string representation is the value itself
    assert str(s1) == "abc"

def test_style_with_empty_value_and_rules():
    # Even with empty value, rules can be present
    rt = RenderType()
    s = Style(rt, value="")
    assert s == ""
    assert s.rules == (rt,)

def test_style_rules_attribute_is_readonly_after_creation():
    # After creation, attempting to reassign the rules attribute should work,
    # but the original tuple remains unchanged
    rt = RenderType()
    s = Style(rt)
    original_rules = s.rules
    s.rules = (RenderType(),)
    assert s.rules != original_rules
    assert original_rules == (rt,)

def test_style_with_non_string_value_raises_type_error():
    # Style expects a string value; passing a non-string should raise a TypeError
    with pytest.raises(TypeError):
        Style(value=123)  # type: ignore[arg-type]
