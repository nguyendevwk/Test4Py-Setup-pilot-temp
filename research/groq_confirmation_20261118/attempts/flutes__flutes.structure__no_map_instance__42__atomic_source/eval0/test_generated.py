import pytest
from flutes.structure import no_map_instance

# The attribute name used internally by no_map_instance
_NO_MAP_INSTANCE_ATTR = "_NO_MAP_INSTANCE_ATTR"

def test_no_map_instance_sets_attribute_on_mutable_object():
    class Mutable:
        pass

    obj = Mutable()
    result = no_map_instance(obj)
    # The function should return the same instance
    assert result is obj
    # The attribute should be set to True
    assert getattr(result, _NO_MAP_INSTANCE_ATTR) is True

def test_no_map_instance_returns_wrapper_for_immutable_object():
    # Tuples are immutable and cannot have attributes set
    original = (1, 2, 3)
    result = no_map_instance(original)
    # The result should not be the original tuple
    assert result is not original
    # The wrapper should expose the original tuple via __iter__ or similar
    assert list(result) == list(original)
    # The wrapper should have the marker attribute set to True
    assert getattr(result, _NO_MAP_INSTANCE_ATTR) is True

def test_no_map_instance_does_not_modify_original_immutable_object():
    original = (4, 5, 6)
    result = no_map_instance(original)
    # Ensure the original tuple remains unchanged
    assert original == (4, 5, 6)
    # Ensure the result is a distinct object
    assert result is not original
    # The result should still be iterable and equal to the original
    assert tuple(result) == original
