import pytest
from flutes.structure import no_map_instance

# Helper class that allows setting attributes
class Mutable:
    pass

# Helper class that does not allow setting attributes
class Immutable:
    __slots__ = ()

def test_no_map_instance_sets_attribute_on_mutable():
    obj = Mutable()
    result = no_map_instance(obj)
    # The function should return the same instance
    assert result is obj
    # The attribute should be set to True
    assert getattr(result, "_NO_MAP_INSTANCE_ATTR") is True

def test_no_map_instance_returns_new_instance_for_immutable():
    tup = (1, 2, 3)
    result = no_map_instance(tup)
    # For immutable types, a new instance is returned
    assert result is not tup
    # The returned instance should still be a tuple
    assert isinstance(result, tuple)
    # The attribute should be set on the new instance
    assert getattr(result, "_NO_MAP_INSTANCE_ATTR") is True

def test_no_map_instance_attribute_persistence():
    obj = Mutable()
    # Call twice to ensure idempotence
    first = no_map_instance(obj)
    second = no_map_instance(first)
    assert first is second
    assert getattr(second, "_NO_MAP_INSTANCE_ATTR") is True
