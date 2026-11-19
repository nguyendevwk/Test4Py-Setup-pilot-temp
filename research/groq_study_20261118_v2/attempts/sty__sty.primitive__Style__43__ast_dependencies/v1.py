import pytest
from sty.primitive import Style
from sty.rendertype import RenderType

def test_style_is_str_and_has_rules_attribute():
    rule1 = RenderType()
    rule2 = RenderType()
    s = Style(rule1, rule2, value="custom")
    assert isinstance(s, str)
    assert str(s) == "custom"
    assert hasattr(s, "rules")
    assert tuple(s.rules) == (rule1, rule2)

def test_style_without_rules_and_default_value():
    s = Style()
    assert str(s) == ""
    assert tuple(s.rules) == ()

def test_style_rules_are_immutable_and_ordered():
    rule1 = RenderType()
    rule2 = RenderType()
    s = Style(rule1, rule2)
    assert isinstance(s.rules, tuple)
    rule1.args.append(1)
    rule2.args.append(2)
    assert len(s.rules) == 2
    assert s.rules[0].args == [1, 2]
    assert s.rules[1].args == [1, 2]

def test_style_value_overrides_rules_string_representation():
    rule = RenderType()
    s = Style(rule, value="hello")
    assert str(s) == "hello"
    assert tuple(s.rules) == (rule,)

def test_style_rules_can_include_render_type_and_style_instances():
    inner = Style(RenderType(), value="inner")
    outer = Style(inner, RenderType(), value="outer")
    assert inner in outer.rules
    assert str(outer) == "outer"

def test_style_rules_are_iterable_and_can_be_converted_to_list():
    rule1 = RenderType()
    rule2 = RenderType()
    s = Style(rule1, rule2)
    rules_list = list(s.rules)
    assert rules_list == [rule1, rule2]
    for i, rule in enumerate(s.rules):
        assert rule is rules_list[i]

def test_style_value_can_be_empty_string_and_rules_present():
    rule = RenderType()
    s = Style(rule, value="")
    assert str(s) == ""
    assert tuple(s.rules) == (rule,)

def test_style_str_conversion_is_consistent():
    rule = RenderType()
    s1 = Style(rule, value="test")
    s2 = Style(rule, value="test")
    assert str(s1) == str(s2)
    assert s1 == s2
    assert s1 is not s2

def test_style_repr_and_hash_behavior():
    rule = RenderType()
    s = Style(rule, value="repr")
    assert repr(s) == "'repr'"
    assert hash(s) == hash("repr")
