import pytest
from sty.primitive import Style

class DummyRule:
    """Simple dummy rule for testing."""
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"DummyRule({self.name!r})"

def test_style_creation_with_rules():
    """Creating a Style with explicit rules stores them and the string value."""
    rule1 = DummyRule("first")
    rule2 = DummyRule("second")
    s = Style(rule1, rule2, value="hello")
    # Style should be a subclass of str and contain the provided value
    assert isinstance(s, Style)
    assert isinstance(s, str)
    assert str(s) == "hello"
    # The rules attribute should be a tuple containing the rules in order
    assert isinstance(s.rules, tuple)
    assert s.rules == (rule1, rule2)

def test_style_default_value_and_no_rules():
    """When no value is provided, the default empty string is used."""
    s = Style()
    assert isinstance(s, Style)
    assert str(s) == ""
    # No rules should result in an empty tuple
    assert s.rules == ()

def test_style_rules_are_immutable_and_shared():
    """The rules attribute should be immutable and shared across instances."""
    rule = DummyRule("shared")
    s1 = Style(rule, value="one")
    s2 = Style(rule, value="two")
    # The rules tuple should be the same object for both instances
    assert s1.rules is s2.rules
    # Modifying the rule object should reflect in both instances
    rule.name = "modified"
    assert s1.rules[0].name == "modified"
    assert s2.rules[0].name == "modified"
    # Attempting to modify the rules tuple should raise a TypeError
    with pytest.raises(TypeError):
        s1.rules += (DummyRule("new"),)
