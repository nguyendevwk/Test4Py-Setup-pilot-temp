import pytest
from sanic.helpers import Default


def test_repr_and_str_are_consistent_and_correct():
    """`__repr__` and `__str__` should return the same string "<Default>"."""
    d = Default()
    rep = repr(d)
    str_rep = str(d)
    assert rep == "<Default>", f"repr returned {rep!r}"
    assert str_rep == "<Default>", f"str returned {str_rep!r}"
    assert rep is str_rep, "repr and str should return the same string object"


def test_default_instances_are_distinct_and_not_equal_to_none_or_object():
    """Each `Default` instance should be a distinct object and not equal to None or a generic sentinel."""
    d1 = Default()
    d2 = Default()
    assert d1 is not d2, "Two Default instances should not be the same object"
    assert d1 != d2, "Two Default instances should not compare equal"
    assert d1 != None, "Default should not equal None"
    assert d1 != object(), "Default should not equal a generic sentinel object"


def test_default_can_be_used_as_dict_key_and_is_hashable():
    """`Default` instances should be hashable and usable as dictionary keys."""
    d = Default()
    mapping = {d: "value"}
    assert mapping[d] == "value", "Default instance should be usable as a dict key"
    # Ensure that the hash is consistent across lookups
    assert hash(d) == hash(d), "Hash of Default instance should be stable"
