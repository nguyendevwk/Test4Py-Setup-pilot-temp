import pytest
from pytutils.props import lazyclassproperty, roclassproperty


class Dummy:
    """Simple class to test lazyclassproperty."""

    counter = 0

    @lazyclassproperty
    def value(cls):
        """Return a value that increments a counter each time it's computed."""
        cls.counter += 1
        return f"computed_{cls.counter}"

    # Prevent accidental setting of the property
    def __setattr__(self, name, value):
        if name == "value":
            raise AttributeError("cannot set read‑only property 'value'")
        super().__setattr__(name, value)


def test_lazyclassproperty_computes_once():
    # The property should compute only once per class.
    assert Dummy.value == "computed_1"
    # Subsequent accesses should return the cached value.
    assert Dummy.value == "computed_1"
    # The counter should not have increased after the first access.
    assert Dummy.counter == 1


def test_lazyclassproperty_is_readonly():
    # Attempting to set the property should raise AttributeError.
    with pytest.raises(AttributeError):
        Dummy.value = "new_value"


def test_lazyclassproperty_inheritance():
    class SubDummy(Dummy):
        pass

    # Subclass should have its own cached value separate from the base class.
    assert SubDummy.value == "computed_2"
    assert SubDummy.value == "computed_2"
    # Base class counter should remain unchanged after subclass access.
    assert Dummy.counter == 1
    # Subclass counter should reflect its own computation.
    assert SubDummy.counter == 2


def test_lazyclassproperty_error_propagation():
    class ErrorDummy:
        @lazyclassproperty
        def bad(cls):
            raise RuntimeError("intentional failure")

    # The exception should propagate on first access.
    with pytest.raises(RuntimeError, match="intentional failure"):
        _ = ErrorDummy.bad

    # Subsequent accesses should still raise the same exception.
    with pytest.raises(RuntimeError, match="intentional failure"):
        _ = ErrorDummy.bad


def test_lazyclassproperty_attribute_name():
    # Ensure that the internal attribute name is correctly set.
    attr_name = "_lazy_value"
    assert hasattr(Dummy, attr_name)
    assert getattr(Dummy, attr_name) == "computed_1"
    # The attribute should not be present on the class before first access.
    class NewDummy:
        @lazyclassproperty
        def new_prop(cls):
            return 42

    assert not hasattr(NewDummy, "_lazy_new_prop")
    _ = NewDummy.new_prop
    assert hasattr(NewDummy, "_lazy_new_prop")
    assert getattr(NewDummy, "_lazy_new_prop") == 42
