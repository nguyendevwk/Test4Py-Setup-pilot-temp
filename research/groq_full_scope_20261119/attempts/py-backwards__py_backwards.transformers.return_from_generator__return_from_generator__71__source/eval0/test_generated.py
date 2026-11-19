import pytest
from py_backwards.transformers.return_from_generator import return_from_generator

def test_return_from_generator_raises_stopiteration_with_value():
    """The function should raise StopIteration with the provided value."""
    with pytest.raises(StopIteration) as excinfo:
        return_from_generator(42)
    assert excinfo.value.value == 42
    assert isinstance(excinfo.value, StopIteration)

def test_return_from_generator_with_none_value():
    """Passing None should still raise StopIteration with value None."""
    with pytest.raises(StopIteration) as excinfo:
        return_from_generator(None)
    assert excinfo.value.value is None

def test_return_from_generator_does_not_modify_other_attributes():
    """Ensure that only the 'value' attribute is set and no other attributes are added."""
    with pytest.raises(StopIteration) as excinfo:
        return_from_generator("test")
    exc = excinfo.value
    # The StopIteration exception should not have any unexpected attributes
    # except 'value' and the standard ones.
    unexpected_attrs = set(dir(exc)) - {"value", "__class__", "__delattr__", "__dict__", "__dir__", "__doc__", "__eq__", "__format__", "__ge__", "__getattribute__", "__gt__", "__hash__", "__init__", "__init_subclass__", "__le__", "__lt__", "__module__", "__ne__", "__new__", "__reduce__", "__reduce_ex__", "__repr__", "__setattr__", "__sizeof__", "__str__", "__subclasshook__"}
    assert unexpected_attrs == set()
