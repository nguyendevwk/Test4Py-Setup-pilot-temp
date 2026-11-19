import pytest
from dataclasses_json.cfg import Exclude

def test_always_exclude_returns_true_for_any_object():
    """Exclude.ALWAYS should return True for any input."""
    assert Exclude.ALWAYS(1) is True
    assert Exclude.ALWAYS("foo") is True
    assert Exclude.ALWAYS(None) is True
    assert Exclude.ALWAYS({"key": "value"}) is True

def test_never_exclude_returns_false_for_any_object():
    """Exclude.NEVER should return False for any input."""
    assert Exclude.NEVER(1) is False
    assert Exclude.NEVER("foo") is False
    assert Exclude.NEVER(None) is False
    assert Exclude.NEVER({"key": "value"}) is False

def test_exclude_callable_can_be_used_in_conditional_logic():
    """Using Exclude constants in a conditional should behave as expected."""
    def should_exclude(field_value, exclude_func):
        return exclude_func(field_value)

    # When using ALWAYS, the field should be excluded
    assert should_exclude("some value", Exclude.ALWAYS) is True

    # When using NEVER, the field should not be excluded
    assert should_exclude("some value", Exclude.NEVER) is False
