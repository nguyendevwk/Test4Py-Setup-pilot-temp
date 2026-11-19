import pytest
from sty.primitive import Style
from sty.rendertype import RenderType

# Dummy RenderType subclass for testing
class DummyRender(RenderType):
    def __init__(self, *args):
        self.args = list(args)

def test_style_creation_with_rules_and_value():
    # Create a Style with two dummy rules and a custom value
    rule1 = DummyRender(1, 2)
    rule2 = DummyRender(3, 4)
    value = "\x1b[38;2;1;5;10m\x1b[1m"
    style = Style(rule1, rule2, value=value)

    # The string representation should be the provided value
    assert str(style) == value
    # The rules attribute should contain the exact rules passed
    assert style.rules == (rule1, rule2)
    # Style should be an instance of both Style and str
    assert isinstance(style, Style)
    assert isinstance(style, str)

def test_style_default_value_and_rules():
    # Create a Style with no explicit value; default should be empty string
    rule = DummyRender(10)
    style = Style(rule)

    assert str(style) == ""
    assert style.rules == (rule,)

def test_style_rules_are_immutable_tuple():
    rule = DummyRender(5)
    style = Style(rule)
    # The rules attribute is a tuple; attempting to modify it by reassignment
    # does not raise an error because it creates a new tuple.
    # We verify that the original tuple remains unchanged.
    original_rules = style.rules
    style.rules += (DummyRender(6),)
    assert style.rules != original_rules
    assert style.rules == (rule, DummyRender(6))

def test_style_value_can_be_empty_string():
    style = Style()
    assert str(style) == ""
    assert style.rules == ()

def test_style_with_multiple_render_types():
    # Create several RenderType instances
    r1 = DummyRender(1)
    r2 = DummyRender(2)
    r3 = DummyRender(3)
    style = Style(r1, r2, r3, value="test")
    assert style.rules == (r1, r2, r3)
    assert str(style) == "test"

def test_style_str_is_immutable_and_independent():
    rule = DummyRender(7)
    style = Style(rule, value="original")
    # Changing the string value of style should not affect the original
    new_style = Style(rule, value="new")
    assert str(style) == "original"
    assert str(new_style) == "new"

def test_style_with_non_render_type_rule():
    # Passing an object that is not a RenderType should still be accepted
    class NotRender:
        pass
    not_render = NotRender()
    style = Style(not_render, value="x")
    # The rule is stored as is
    assert style.rules == (not_render,)

def test_style_repr_and_equality():
    rule = DummyRender(9)
    style1 = Style(rule, value="abc")
    style2 = Style(rule, value="abc")
    # Two styles with same value and rules should be equal as strings
    assert style1 == style2
    # Their repr should show the string value with quotes
    assert repr(style1) == repr("abc")

def test_style_with_empty_rules_and_value():
    style = Style(value="empty")
    assert style.rules == ()
    assert str(style) == "empty"

def test_style_with_large_number_of_rules():
    rules = [DummyRender(i) for i in range(100)]
    style = Style(*rules, value="many")
    assert len(style.rules) == 100
    assert style.rules[0].args == [0]
    assert style.rules[-1].args == [99]
    assert str(style) == "many"
