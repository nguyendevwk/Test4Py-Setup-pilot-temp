import pytest
from sty.primitive import Style
from sty.rendertype import RenderType

def test_style_is_str_and_has_rules_attribute():
    # Create a Style with two dummy rules
    rule1 = RenderType()
    rule2 = RenderType()
    s = Style(rule1, rule2, value="custom")
    # Style should be a subclass of str
    assert isinstance(s, str)
    # The string value should be exactly the provided value
    assert str(s) == "custom"
    # The rules attribute should contain the passed rules in order
    assert hasattr(s, "rules")
    assert tuple(s.rules) == (rule1, rule2)

def test_style_without_rules_and_default_value():
    # Creating a Style with no rules and no explicit value
    s = Style()
    # Should default to empty string
    assert str(s) == ""
    # Rules should be an empty tuple
    assert tuple(s.rules) == ()

def test_style_rules_are_immutable_and_ordered():
    rule1 = RenderType()
    rule2 = RenderType()
    s = Style(rule1, rule2)
    # The rules attribute should be a tuple (immutable)
    assert isinstance(s.rules, tuple)
    # Changing the original rule objects should not affect the stored rules
    rule1.args.append(1)
    rule2.args.append(2)
    # The stored rules still reference the same objects, so changes reflect
    # but the tuple itself remains unchanged
    assert len(s.rules) == 2
    assert s.rules[0].args == [1]
    assert s.rules[1].args == [2]

def test_style_value_overrides_rules_string_representation():
    rule = RenderType()
    # Provide a non-empty value; rules should still be stored
    s = Style(rule, value="hello")
    assert str(s) == "hello"
    assert tuple(s.rules) == (rule,)

def test_style_rules_can_include_render_type_and_style_instances():
    # Create a nested Style
    inner = Style(RenderType(), value="inner")
    outer = Style(inner, RenderType(), value="outer")
    # Outer should contain the inner Style as a rule
    assert inner in outer.rules
    # The string representation is based on the outer value
    assert str(outer) == "outer"

def test_style_rules_are_iterable_and_can_be_converted_to_list():
    rule1 = RenderType()
    rule2 = RenderType()
    s = Style(rule1, rule2)
    # Convert rules to list
    rules_list = list(s.rules)
    assert rules_list == [rule1, rule2]
    # Ensure that iterating over rules yields the same objects
    for i, rule in enumerate(s.rules):
        assert rule is rules_list[i]

def test_style_value_can_be_empty_string_and_rules_present():
    rule = RenderType()
    s = Style(rule, value="")
    assert str(s) == ""
    assert tuple(s.rules) == (rule,)

def test_style_rules_are_not_modified_by_external_assignment():
    rule = RenderType()
    s = Style(rule)
    # Attempt to modify the rules attribute externally
    with pytest.raises(AttributeError):
        s.rules = (RenderType(),)
    # The original rules remain unchanged
    assert tuple(s.rules) == (rule,)

def test_style_str_conversion_is_consistent():
    rule = RenderType()
    s1 = Style(rule, value="test")
    s2 = Style(rule, value="test")
    # Two separate instances with same value should be equal as strings
    assert str(s1) == str(s2)
    assert s1 == s2
    # But they are distinct objects
    assert s1 is not s2

def test_style_repr_and_hash_behavior():
    rule = RenderType()
    s = Style(rule, value="repr")
    # The repr should include the class name and the string value
    assert repr(s).startswith("Style('repr'")
    # Hash should be based on the string value
    assert hash(s) == hash("repr")
