import pytest
from dataclasses_json.cfg import Exclude


def test_always_excludes_everything():
    """Exclude.ALWAYS should return True for any input."""
    assert Exclude.ALWAYS(1) is True
    assert Exclude.ALWAYS("foo") is True
    assert Exclude.ALWAYS(None) is True
    assert Exclude.ALWAYS({"key": "value"}) is True


def test_never_excludes_nothing():
    """Exclude.NEVER should return False for any input."""
    assert Exclude.NEVER(1) is False
    assert Exclude.NEVER("foo") is False
    assert Exclude.NEVER(None) is False
    assert Exclude.NEVER({"key": "value"}) is False


def test_exclude_constants_are_distinct_and_callable():
    """Ensure the two constants are distinct callables and behave as expected."""
    assert callable(Exclude.ALWAYS)
    assert callable(Exclude.NEVER)
    assert Exclude.ALWAYS is not Exclude.NEVER
    # Verify that calling them with the same argument yields different results
    sample = object()
    assert Exclude.ALWAYS(sample) is True
    assert Exclude.NEVER(sample) is False
