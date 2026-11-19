import pytest
from flutes.structure import no_map_instance, _NO_MAP_INSTANCE_ATTR, _no_map_type


def test_no_map_instance_sets_attribute_on_mutable_object(tmp_path):
    """When the instance allows attribute setting, the attribute is set and the same object is returned."""
    class Dummy:
        pass

    obj = Dummy()
    result = no_map_instance(obj)
    assert result is obj
    assert hasattr(result, _NO_MAP_INSTANCE_ATTR)
    assert getattr(result, _NO_MAP_INSTANCE_ATTR) is True


def test_no_map_instance_returns_subclass_for_immutable_type():
    """For immutable built‑in types (e.g., int) the function returns a new instance of a subclass that has the marker attribute."""
    original = 42
    result = no_map_instance(original)
    # The result should be an instance of the same type (int) but not the original object
    assert isinstance(result, int)
    assert result is not original
    # The returned instance should have the marker attribute
    assert hasattr(result, _NO_MAP_INSTANCE_ATTR)
    assert getattr(result, _NO_MAP_INSTANCE_ATTR) is True
    # The value should be preserved
    assert result == original


def test_no_map_instance_handles_none_and_other_non_settable_objects():
    """Passing None or other objects that cannot have attributes set should still return an instance with the marker attribute."""
    # None is a singleton; attempting to set an attribute raises AttributeError
    result = no_map_instance(None)
    # The result should still be None (since NoneType constructor returns None)
    assert result is None
    # NoneType cannot have attributes, so the marker attribute should not exist on the result
    assert not hasattr(result, _NO_MAP_INSTANCE_ATTR)

    # Test with a tuple, which is immutable and cannot have attributes set
    original = (1, 2, 3)
    result = no_map_instance(original)
    assert isinstance(result, tuple)
    assert result is not original
    assert hasattr(result, _NO_MAP_INSTANCE_ATTR)
    assert getattr(result, _NO_MAP_INSTANCE_ATTR) is True
    assert result == original
