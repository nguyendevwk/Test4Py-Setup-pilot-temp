import pytest
from sty.primitive import Style

class DummyRule:
    """Simple stand‑in for a styling rule."""
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"DummyRule({self.name!r})"

def test_style_default_value_and_rules(tmp_path):
    """Style created with no explicit value should be an empty string."""
    rule_a = DummyRule("a")
    rule_b = DummyRule("b")
    s = Style(rule_a, rule_b)
    # Style is a subclass of str
    assert isinstance(s, str)
    # The string value is empty by default
    assert s == ""
    # The rules attribute contains the passed rules in order
    assert s.rules == (rule_a, rule_b)

def test_style_value_override(tmp_path):
    """Providing a value overrides the default empty string."""
    rule_x = DummyRule("x")
    custom_value = "\x1b[31m"
    s = Style(rule_x, value=custom_value)
    assert isinstance(s, str)
    assert s == custom_value
    assert s.rules == (rule_x,)

def test_style_rules_order_and_identity(tmp_path):
    """Rules are stored exactly as passed and are distinct objects."""
    rule1 = DummyRule("first")
    rule2 = DummyRule("second")
    rule3 = DummyRule("third")
    s = Style(rule1, rule2, rule3)
    # Order preserved
    assert s.rules[0] is rule1
    assert s.rules[1] is rule2
    assert s.rules[2] is rule3
    # Changing a rule object after creation does not affect the stored reference
    rule2.name = "changed"
    assert s.rules[1].name == "changed"
