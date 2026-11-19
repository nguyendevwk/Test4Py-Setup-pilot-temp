import pytest
from sanic.helpers import Default

def test_default_repr_and_str():
    """Default should have a consistent string representation."""
    d = Default()
    assert repr(d) == "<Default>"
    assert str(d) == "<Default>"
    # repr and str should be identical
    assert repr(d) == str(d)

def test_default_identity_and_hash(tmp_path):
    """Two Default instances are distinct objects and can be used as dict keys."""
    d1 = Default()
    d2 = Default()
    # Identity: different objects
    assert d1 is not d2
    # Hashability: can be used as keys
    mapping = {d1: "first", d2: "second"}
    assert mapping[d1] == "first"
    assert mapping[d2] == "second"
    # Ensure hash values are consistent across runs
    assert hash(d1) == hash(d1)

def test_default_behavior_in_collections(tmp_path):
    """Default should behave correctly in sets and as a default dict value."""
    d = Default()
    # As a set element
    s = {d}
    assert d in s
    # As a default value in a dict
    from collections import defaultdict
    dd = defaultdict(lambda: d)
    assert dd["missing"] is d
    # Ensure that modifying the dict does not affect the Default instance
    dd["missing"] = "changed"
    assert dd["missing"] == "changed"
    assert dd["another_missing"] is d
