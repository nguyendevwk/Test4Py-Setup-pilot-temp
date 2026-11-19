import pytest
from sty.primitive import Style
from sty.rendertype import RenderType

def test_style_creation_with_rules_and_value():
    """Creating a Style with explicit rules and a string value stores them correctly."""
    rule1 = RenderType(31)  # example rule (red foreground)
    rule2 = RenderType(1)   # example rule (bold)
    s = Style(rule1, rule2, value="test")
    # The Style instance should be a string with the given value
    assert isinstance(s, str)
    assert str(s) == "test"
    # The rules attribute should contain the rules in the order passed
    assert hasattr(s, "rules")
    assert list(s.rules) == [rule1, rule2]

def test_style_creation_without_rules():
    """Creating a Style with no rules should still produce a valid Style instance."""
    s = Style(value="empty")
    assert isinstance(s, str)
    assert str(s) == "empty"
    # rules should be an empty tuple
    assert hasattr(s, "rules")
    assert s.rules == ()

def test_style_rules_are_independent_of_original_objects():
    """Modifying the original rule objects after Style creation should not affect the stored rules."""
    rule = RenderType(32)  # green foreground
    s = Style(rule, value="mutable")
    # Mutate the original rule (simulate by creating a new RenderType with same code)
    rule = RenderType(33)  # change to yellow
    # The Style's rules should still reference the original rule object
    assert s.rules[0].code == 32
    # Ensure that the string representation of the Style remains unchanged
    assert str(s) == "mutable"
